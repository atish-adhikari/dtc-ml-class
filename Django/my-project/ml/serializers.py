from rest_framework import serializers

class AdmissionSerializer(serializers.Serializer):
    gre = serializers.IntegerField(required=True, min_value=240, max_value=340)
    toefl = serializers.IntegerField(required=True, min_value=50, max_value=120)
    rating = serializers.FloatField(required=True, min_value=0, max_value=5)
    sop = serializers.FloatField(required=True, min_value=0, max_value=5)
    lor = serializers.FloatField(required=True, min_value=0, max_value=5)
    cgpa = serializers.FloatField(required=True, min_value=0, max_value=10)
    research = serializers.IntegerField(required=True, min_value=0, max_value=1)


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
