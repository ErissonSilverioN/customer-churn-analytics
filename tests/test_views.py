import pytest
from rest_framework.test import APIClient
from analytics.db import get_db, CUSTOMERS_COLLECTION


class TestAPIEndpoints:
    """Integration tests for API endpoints"""
    
    @pytest.fixture
    def api_client(self):
        """Get API client"""
        return APIClient()
    
    @pytest.fixture
    def sample_prediction_data(self):
        """Sample data for prediction"""
        return {
            'tenure': 12,
            'Contract': 'Month-to-month',
            'InternetService': 'Fiber optic',
            'TechSupport': 'No',
            'PaymentMethod': 'Electronic check',
            'PaperlessBilling': 'Yes',
            'MonthlyCharges': 85.0,
            'SeniorCitizen': 0
        }
    
    def test_churn_rate_endpoint(self, api_client):
        """Test churn rate analytics endpoint"""
        response = api_client.get('/api/analytics/churn-rate/')
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'total_customers' in data
        assert 'churn_rate' in data
        assert 'breakdown' in data
    
    def test_segment_analysis_endpoint(self, api_client):
        """Test segment analysis endpoint"""
        response = api_client.get('/api/analytics/segment-analysis/?segment_by=Contract')
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'segment_by' in data
        assert 'segments' in data
        assert data['segment_by'] == 'Contract'
    
    def test_prediction_endpoint(self, api_client, sample_prediction_data):
        """Test single prediction endpoint"""
        response = api_client.post(
            '/api/predict/',
            data=sample_prediction_data,
            format='json'
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'churn_probability' in data
        assert 'churn_prediction' in data
        assert 'risk_level' in data
        assert 'confidence' in data
    
    def test_prediction_validation(self, api_client):
        """Test prediction endpoint with invalid data"""
        invalid_data = {
            'tenure': -5,  # Invalid: negative tenure
            'Contract': 'Invalid'  # Invalid contract type
        }
        
        response = api_client.post(
            '/api/predict/',
            data=invalid_data,
            format='json'
        )
        
        assert response.status_code == 400  # Bad request
    
    def test_batch_prediction_endpoint(self, api_client, sample_prediction_data):
        """Test batch prediction endpoint"""
        batch_data = {
            'customers': [sample_prediction_data for _ in range(5)]
        }
        
        response = api_client.post(
            '/api/predict/batch/',
            data=batch_data,
            format='json'
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'count' in data
        assert 'predictions' in data
        assert data['count'] == 5
        assert len(data['predictions']) == 5
    
    def test_customers_list_endpoint(self, api_client):
        """Test customer list endpoint"""
        response = api_client.get('/api/customers/')
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'count' in data
        assert 'results' in data
        assert 'page' in data
    
    def test_customers_list_pagination(self, api_client):
        """Test customer list pagination"""
        response = api_client.get('/api/customers/?page=1&page_size=10')
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['page'] == 1
        assert data['page_size'] == 10
        assert len(data['results']) <= 10
    
    def test_customers_list_filtering(self, api_client):
        """Test customer list filtering"""
        response = api_client.get('/api/customers/?contract=Month-to-month')
        
        assert response.status_code == 200
        data = response.json()
        
        # All results should have Month-to-month contract
        for customer in data['results']:
            if 'Contract' in customer:
                assert customer['Contract'] == 'Month-to-month'
