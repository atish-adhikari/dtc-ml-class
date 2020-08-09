from django.shortcuts import render
from .serializers import AdmissionSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
import os
import numpy

import pickle

this_dir = os.path.dirname(os.path.abspath(__file__)) 

pipeline_file = os.path.join(this_dir, "saved_models", "ml_pipeline.pkl")
f = open(pipeline_file, "rb")
model = pickle.load(f)
f.close()

class AdmissionPredict(GenericAPIView):

    serializer_class = AdmissionSerializer

    def post(self, request):
        """
        Returns chance of admission in University
        """
        serialized = AdmissionSerializer(data=request.data)
        if not serialized.is_valid():
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        sample = [list(serialized.data.values())]
        prediction = model.predict(sample)
        out = prediction[0].round(4) * 100
        return Response({"chance": out})
        