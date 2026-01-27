from rest_framework import serializers


class CustomerSerializer(serializers.Serializer):
    """Serializer for customer data"""
    customer_id = serializers.CharField(max_length=50, required=False)
    gender = serializers.CharField(max_length=10, required=False)
    SeniorCitizen = serializers.IntegerField(required=False)
    Partner = serializers.CharField(max_length=10, required=False)
    Dependents = serializers.CharField(max_length=10, required=False)
    tenure = serializers.IntegerField(required=True)
    PhoneService = serializers.CharField(max_length=10, required=False)
    MultipleLines = serializers.CharField(max_length=50, required=False)
    InternetService = serializers.CharField(max_length=50, required=True)
    OnlineSecurity = serializers.CharField(max_length=50, required=False)
    OnlineBackup = serializers.CharField(max_length=50, required=False)
    DeviceProtection = serializers.CharField(max_length=50, required=False)
    TechSupport = serializers.CharField(max_length=50, required=True)
    StreamingTV = serializers.CharField(max_length=50, required=False)
    StreamingMovies = serializers.CharField(max_length=50, required=False)
    Contract = serializers.CharField(max_length=50, required=True)
    PaperlessBilling = serializers.CharField(max_length=10, required=True)
    PaymentMethod = serializers.CharField(max_length=100, required=True)
    MonthlyCharges = serializers.FloatField(required=True)
    TotalCharges = serializers.FloatField(required=False)
    Churn = serializers.CharField(max_length=10, required=False)

    def to_mongo(self):
        """Convert to MongoDB document format"""
        return dict(self.validated_data)


class ChurnPredictionInputSerializer(serializers.Serializer):
    """Serializer for churn prediction input"""
    tenure = serializers.IntegerField(min_value=0, max_value=100)
    Contract = serializers.ChoiceField(choices=['Month-to-month', 'One year', 'Two year'])
    InternetService = serializers.ChoiceField(choices=['DSL', 'Fiber optic', 'No'])
    TechSupport = serializers.ChoiceField(choices=['Yes', 'No', 'No internet service'])
    PaymentMethod = serializers.ChoiceField(
        choices=[
            'Electronic check',
            'Mailed check',
            'Bank transfer (automatic)',
            'Credit card (automatic)'
        ]
    )
    PaperlessBilling = serializers.ChoiceField(choices=['Yes', 'No'])
    MonthlyCharges = serializers.FloatField(min_value=0, max_value=200)
    SeniorCitizen = serializers.IntegerField(min_value=0, max_value=1, default=0)
    MultipleLines = serializers.ChoiceField(
        choices=['Yes', 'No', 'No phone service'],
        default='No'
    )
    
    # Optional fields with defaults
    gender = serializers.CharField(max_length=10, default='Male')
    Partner = serializers.CharField(max_length=10, default='No')
    Dependents = serializers.CharField(max_length=10, default='No')
    PhoneService = serializers.CharField(max_length=10, default='Yes')
    OnlineSecurity = serializers.CharField(max_length=50, default='No')
    OnlineBackup = serializers.CharField(max_length=50, default='No')
    DeviceProtection = serializers.CharField(max_length=50, default='No')
    StreamingTV = serializers.CharField(max_length=50, default='No')
    StreamingMovies = serializers.CharField(max_length=50, default='No')
    TotalCharges = serializers.FloatField(required=False, allow_null=True)


class ChurnPredictionOutputSerializer(serializers.Serializer):
    """Serializer for churn prediction output"""
    churn_probability = serializers.FloatField()
    churn_prediction = serializers.CharField()
    risk_level = serializers.CharField()
    confidence = serializers.FloatField()
    prediction_date = serializers.DateTimeField()


class BatchPredictionInputSerializer(serializers.Serializer):
    """Serializer for batch prediction input"""
    customers = ChurnPredictionInputSerializer(many=True)


class AnalyticsFilterSerializer(serializers.Serializer):
    """Serializer for analytics filtering"""
    contract_type = serializers.MultipleChoiceField(
        choices=['Month-to-month', 'One year', 'Two year'],
        required=False
    )
    internet_service = serializers.MultipleChoiceField(
        choices=['DSL', 'Fiber optic', 'No'],
        required=False
    )
    min_tenure = serializers.IntegerField(min_value=0, required=False)
    max_tenure = serializers.IntegerField(max_value=100, required=False)
    min_charges = serializers.FloatField(min_value=0, required=False)
    max_charges = serializers.FloatField(required=False)
