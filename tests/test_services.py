import pytest
from analytics.services import ChurnPredictionService


class TestChurnPredictionService:
    """Test suite for churn prediction service"""
    
    @pytest.fixture
    def prediction_service(self):
        """Get prediction service instance"""
        return ChurnPredictionService()
    
    @pytest.fixture
    def sample_customer_data(self):
        """Sample customer data for testing"""
        return {
            'tenure': 12,
            'Contract': 'Month-to-month',
            'InternetService': 'Fiber optic',
            'TechSupport': 'No',
            'PaymentMethod': 'Electronic check',
            'PaperlessBilling': 'Yes',
            'MonthlyCharges': 85.0,
            'SeniorCitizen': 0,
            'MultipleLines': 'No'
        }
    
    def test_service_initialization(self, prediction_service):
        """Test that service initializes correctly"""
        assert prediction_service is not None
        assert prediction_service._model is not None
        assert prediction_service._scaler is not None
        assert prediction_service._feature_names is not None
    
    def test_tenure_bucket(self, prediction_service):
        """Test tenure bucketing logic"""
        assert prediction_service._tenure_bucket(6) == '0-12m'
        assert prediction_service._tenure_bucket(18) == '12-24m'
        assert prediction_service._tenure_bucket(36) == '24-48m'
        assert prediction_service._tenure_bucket(60) == '48m+'
    
    def test_predict_single(self, prediction_service, sample_customer_data):
        """Test single customer prediction"""
        result = prediction_service.predict_single(sample_customer_data)
        
        assert 'churn_probability' in result
        assert 'churn_prediction' in result
        assert 'risk_level' in result
        assert 'confidence' in result
        
        assert 0 <= result['churn_probability'] <= 1
        assert result['churn_prediction'] in ['Yes', 'No']
        assert result['risk_level'] in ['HIGH', 'MEDIUM', 'LOW']
    
    def test_predict_batch(self, prediction_service, sample_customer_data):
        """Test batch prediction"""
        customers = [sample_customer_data for _ in range(10)]
        results = prediction_service.predict_batch(customers)
        
        assert len(results) == 10
        for result in results:
            assert 'churn_probability' in result
            assert 'churn_prediction' in result
    
    def test_high_risk_customer(self, prediction_service):
        """Test prediction for high-risk customer profile"""
        high_risk_customer = {
            'tenure': 1,
            'Contract': 'Month-to-month',
            'InternetService': 'Fiber optic',
            'TechSupport': 'No',
            'PaymentMethod': 'Electronic check',
            'PaperlessBilling': 'Yes',
            'MonthlyCharges': 100.0,
            'SeniorCitizen': 1,
            'MultipleLines': 'Yes'
        }
        
        result = prediction_service.predict_single(high_risk_customer)
        # High-risk customers should have higher churn probability
        assert result['churn_probability'] > 0.3
    
    def test_low_risk_customer(self, prediction_service):
        """Test prediction for low-risk customer profile"""
        low_risk_customer = {
            'tenure': 60,
            'Contract': 'Two year',
            'InternetService': 'DSL',
            'TechSupport': 'Yes',
            'PaymentMethod': 'Credit card (automatic)',
            'PaperlessBilling': 'No',
            'MonthlyCharges': 50.0,
            'SeniorCitizen': 0,
            'MultipleLines': 'No'
        }
        
        result = prediction_service.predict_single(low_risk_customer)
        # Low-risk customers should have lower churn probability
        assert result['churn_probability'] < 0.7
