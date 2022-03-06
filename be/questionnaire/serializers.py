from rest_framework import serializers
from questionnaire.models import Field


class MyFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ["id", "category","name","total_vote","image"]