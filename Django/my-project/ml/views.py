from django.shortcuts import render
from .serializers import AdmissionSerializer, ImageSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
import numpy as np
import os
import pickle
from .utils import get_model, get_cnn, infer, get_le_clf
from PIL import Image

model = get_model()

cnn, decode_prediction = get_cnn()

le, clf = get_le_clf()

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
        admission_chance = prediction[0].round(4) * 100
        return Response({"chance": admission_chance})



class ImagePredict(GenericAPIView):

    serializer_class = ImageSerializer
    
    def post(self, request):
        """
        Returns prediction for image uploaded 
        """
        serialized = ImageSerializer(data=request.data)
        if not serialized.is_valid():
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        img = Image.open(request.FILES["image"])
        img = img.resize((299, 299))
        img = np.array(img)
        img = img / 255
        img = img.reshape(1,299,299,3)

        predictions = cnn.predict(img)
        predictions = decode_prediction(predictions)

        out = {"name": predictions[0][0][1], "probability": round(predictions[0][0][2] * 100, 2)}
        
        return Response(out)


class FacePredict(GenericAPIView):

    serializer_class = ImageSerializer
    
    def post(self, request):
        """
        Returns prediction for image uploaded 
        """
        serialized = ImageSerializer(data=request.data)
        if not serialized.is_valid():
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        img = Image.open(request.FILES["image"])
        pred = infer(le, clf, img)
        return Response(pred)


    
