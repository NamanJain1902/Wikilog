from django.urls import path

from countryStats.views import CountryTableClient

urlpatterns = [
    path('country_info/<slug:country>', CountryTableClient.as_view(), name='testapi'),
]