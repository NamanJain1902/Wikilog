from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from countryStats.fetch import fetchData

# Create your views here.


class CountryTableClient(APIView):

    def get(self, request, country=""):        
        print(country)

        data = fetchData(country=country)
        return Response(data)
