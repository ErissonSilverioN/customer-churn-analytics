import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class ChurnPredictionService:
    """Service for churn prediction using trained ML model"""
    
    _instance = None
    _model = None
    _scaler = None
    _feature_names = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChurnPredictionService, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance
    
    def _load_model(self):
        """Load trained model, scaler, and feature names"""
        try:
            base_dir = Path(settings.BASE_DIR)
            self._model = joblib.load(base_dir / 'churn_model_rf.joblib')
            self._scaler = joblib.load(base_dir / 'scaler.joblib')
            self._feature_names = joblib.load(base_dir / 'feature_names.joblib')
            logger.info("ML model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load ML model: {e}")
            raise
    
    def _tenure_bucket(self, tenure):
        """Convert tenure to bucket"""
        if tenure <= 12:
            return '0-12m'
        elif tenure <= 24:
            return '12-24m'
        elif tenure <= 48:
            return '24-48m'
        else:
            return '48m+'
    
    def _preprocess_input(self, customer_data):
        """Preprocess customer data for prediction"""
        # Create DataFrame
        df = pd.DataFrame([customer_data])
        
        # Add tenure bucket
        df['TenureBucket'] = df['tenure'].apply(self._tenure_bucket)
        
        # One-hot encode categorical variables
        df_encoded = pd.get_dummies(df)
        
        # Ensure all required features are present
        X_pred = pd.DataFrame(columns=self._feature_names)
        for col in self._feature_names:
            if col in df_encoded.columns:
                X_pred.at[0, col] = df_encoded.at[0, col]
            else:
                X_pred.at[0, col] = 0
        
        # Scale features
        X_scaled = self._scaler.transform(X_pred)
        
        return X_scaled
    
    def predict_single(self, customer_data):
        """
        Predict churn for a single customer
        
        Args:
            customer_data (dict): Customer features
            
        Returns:
            dict: Prediction results with probability and risk level
        """
        try:
            # Preprocess
            X_scaled = self._preprocess_input(customer_data)
            
            # Predict
            probability = self._model.predict_proba(X_scaled)[0][1]
            prediction = 'Yes' if probability > 0.5 else 'No'
            
            # Determine risk level
            if probability >= 0.7:
                risk_level = 'HIGH'
            elif probability >= 0.4:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'
            
            return {
                'churn_probability': float(probability),
                'churn_prediction': prediction,
                'risk_level': risk_level,
                'confidence': float(max(probability, 1 - probability)),
                'prediction_date': datetime.now()
            }
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise
    
    def predict_batch(self, customers_data):
        """
        Predict churn for multiple customers
        
        Args:
            customers_data (list): List of customer feature dictionaries
            
        Returns:
            list: List of prediction results
        """
        results = []
        for customer_data in customers_data:
            try:
                prediction = self.predict_single(customer_data)
                results.append(prediction)
            except Exception as e:
                logger.error(f"Batch prediction error for customer: {e}")
                results.append({
                    'error': str(e),
                    'churn_probability': None,
                    'churn_prediction': None,
                    'risk_level': None
                })
        return results


# Singleton instance
prediction_service = ChurnPredictionService()
