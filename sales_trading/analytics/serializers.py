from rest_framework import serializers
from .models import TradeReport

class TradeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeReport
        fields = '__all__'
