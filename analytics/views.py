from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from .db import get_db, CUSTOMERS_COLLECTION, PREDICTIONS_COLLECTION
from .serializers import (
    CustomerSerializer,
    ChurnPredictionInputSerializer,
    ChurnPredictionOutputSerializer,
    BatchPredictionInputSerializer,
    AnalyticsFilterSerializer
)
from .services import prediction_service
from bson import ObjectId
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class CustomerListView(APIView):
    """
    GET: List customers with filtering and pagination
    POST: Bulk import customers
    """
    
    def get(self, request):
        """List customers with optional filtering"""
        try:
            db = get_db()
            customers = db[CUSTOMERS_COLLECTION]
            
            # Build query filter
            query = {}
            if 'contract' in request.query_params:
                query['Contract'] = request.query_params['contract']
            if 'internet_service' in request.query_params:
                query['InternetService'] = request.query_params['internet_service']
            if 'churn' in request.query_params:
                query['Churn'] = request.query_params['churn']
            
            # Pagination
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 100))
            skip = (page - 1) * page_size
            
            # Execute query with pagination
            cursor = customers.find(query).skip(skip).limit(page_size)
            total_count = customers.count_documents(query)
            
            # Convert ObjectId to string
            results = []
            for doc in cursor:
                doc['_id'] = str(doc['_id'])
                results.append(doc)
            
            return Response({
                'count': total_count,
                'page': page,
                'page_size': page_size,
                'results': results
            })
        except Exception as e:
            logger.error(f"Error listing customers: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        """Bulk import customers"""
        try:
            db = get_db()
            customers = db[CUSTOMERS_COLLECTION]
            
            # Validate data
            serializer = CustomerSerializer(data=request.data, many=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Insert in batches for performance
            documents = [doc for doc in serializer.validated_data]
            if documents:
                result = customers.insert_many(documents)
                return Response({
                    'message': f'Successfully imported {len(result.inserted_ids)} customers',
                    'count': len(result.inserted_ids)
                }, status=status.HTTP_201_CREATED)
            
            return Response({'message': 'No data to import'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error importing customers: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomerDetailView(APIView):
    """
    GET: Retrieve customer by ID
    """
    
    def get(self, request, customer_id):
        """Get customer details"""
        try:
            db = get_db()
            customers = db[CUSTOMERS_COLLECTION]
            
            customer = customers.find_one({'customer_id': customer_id})
            if customer:
                customer['_id'] = str(customer['_id'])
                return Response(customer)
            
            return Response(
                {'error': 'Customer not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving customer: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChurnPredictionView(APIView):
    """
    POST: Predict churn for a single customer
    """
    
    def post(self, request):
        """Predict churn probability"""
        try:
            # Validate input
            serializer = ChurnPredictionInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Make prediction
            prediction = prediction_service.predict_single(serializer.validated_data)
            
            # Save prediction to database
            db = get_db()
            predictions = db[PREDICTIONS_COLLECTION]
            prediction_doc = {
                **prediction,
                'input_data': serializer.validated_data,
                'created_at': datetime.now()
            }
            predictions.insert_one(prediction_doc)
            
            # Serialize output
            output_serializer = ChurnPredictionOutputSerializer(prediction)
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BatchChurnPredictionView(APIView):
    """
    POST: Batch churn prediction for multiple customers
    """
    
    def post(self, request):
        """Batch predict churn for multiple customers"""
        try:
            # Validate input
            serializer = BatchPredictionInputSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            customers_data = serializer.validated_data['customers']
            
            # Process in batches for performance
            batch_size = settings.BATCH_SIZE
            all_predictions = []
            
            for i in range(0, len(customers_data), batch_size):
                batch = customers_data[i:i + batch_size]
                predictions = prediction_service.predict_batch(batch)
                all_predictions.extend(predictions)
            
            return Response({
                'count': len(all_predictions),
                'predictions': all_predictions
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Batch prediction error: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChurnRateAnalyticsView(APIView):
    """
    GET: Get churn rate analytics with aggregation
    """
    
    def get(self, request):
        """Get aggregated churn statistics"""
        try:
            db = get_db()
            customers = db[CUSTOMERS_COLLECTION]
            
            # Aggregation pipeline for churn rate
            pipeline = [
                {
                    '$group': {
                        '_id': '$Churn',
                        'count': {'$sum': 1},
                        'avg_monthly_charges': {'$avg': '$MonthlyCharges'},
                        'avg_tenure': {'$avg': '$tenure'}
                    }
                }
            ]
            
            results = list(customers.aggregate(pipeline))
            
            # Calculate overall churn rate
            total = sum(r['count'] for r in results)
            churn_count = next((r['count'] for r in results if r['_id'] == 'Yes'), 0)
            churn_rate = (churn_count / total * 100) if total > 0 else 0
            
            return Response({
                'total_customers': total,
                'churned_customers': churn_count,
                'churn_rate': round(churn_rate, 2),
                'breakdown': results
            })
        except Exception as e:
            logger.error(f"Analytics error: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SegmentAnalysisView(APIView):
    """
    GET: Segment-based churn analysis
    """
    
    def get(self, request):
        """Get churn analysis by segments"""
        try:
            db = get_db()
            customers = db[CUSTOMERS_COLLECTION]
            
            segment_by = request.query_params.get('segment_by', 'Contract')
            
            # Aggregation pipeline for segment analysis
            pipeline = [
                {
                    '$group': {
                        '_id': f'${segment_by}',
                        'total': {'$sum': 1},
                        'churned': {
                            '$sum': {
                                '$cond': [{'$eq': ['$Churn', 'Yes']}, 1, 0]
                            }
                        },
                        'avg_monthly_charges': {'$avg': '$MonthlyCharges'},
                        'avg_tenure': {'$avg': '$tenure'}
                    }
                },
                {
                    '$project': {
                        'segment': '$_id',
                        'total': 1,
                        'churned': 1,
                        'churn_rate': {
                            '$multiply': [
                                {'$divide': ['$churned', '$total']},
                                100
                            ]
                        },
                        'avg_monthly_charges': {'$round': ['$avg_monthly_charges', 2]},
                        'avg_tenure': {'$round': ['$avg_tenure', 1]}
                    }
                },
                {
                    '$sort': {'churn_rate': -1}
                }
            ]
            
            results = list(customers.aggregate(pipeline))
            
            return Response({
                'segment_by': segment_by,
                'segments': results
            })
        except Exception as e:
            logger.error(f"Segment analysis error: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
