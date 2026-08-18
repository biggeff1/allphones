from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("deposer/", views.deposit, name="deposit"),
    path("annonce/<int:pk>/", views.listing_detail, name="listing_detail"),
    path("annonce/<int:pk>/interesse/", views.interest, name="interest"),
]
