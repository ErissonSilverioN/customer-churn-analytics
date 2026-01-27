from django.urls import path
from .views import (
    CustomerListView,
    CustomerDetailView,
    ChurnPredictionView,
    BatchChurnPredictionView,
    ChurnRateAnalyticsView,
    SegmentAnalysisView
)

urlpatterns = [
    # Customer endpoints
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('customers/<str:customer_id>/', CustomerDetailView.as_view(), name='customer-detail'),
    
    # Prediction endpoints
    path('predict/', ChurnPredictionView.as_view(), name='churn-predict'),
    path('predict/batch/', BatchChurnPredictionView.as_view(), name='batch-predict'),
    
    # Analytics endpoints
    path('analytics/churn-rate/', ChurnRateAnalyticsView.as_view(), name='churn-rate'),
    path('analytics/segment-analysis/', SegmentAnalysisView.as_view(), name='segment-analysis'),
]
