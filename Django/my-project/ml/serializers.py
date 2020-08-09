from rest_framework import serializers

class AdmissionSerializer(serializers.Serializer):
    gre = serializers.IntegerField(required=True)
    toefl = serializers.IntegerField(required=True)
    rating = serializers.FloatField(required=True)
    sop = serializers.FloatField(required=True)
    lor = serializers.FloatField(required=True)
    cgpa = serializers.FloatField(required=True)
    research = serializers.IntegerField(required=True)
