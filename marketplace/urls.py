from django.urls import path
from . import views, dashboard

urlpatterns = [
    path("", views.home, name="home"),
    path("inscription/", views.register, name="register"),
    path("deposer/", views.deposit, name="deposit"),
    path("creer-annonce/", views.create_listing, name="create_listing"),
    path("annonce/<int:pk>/photos/", views.add_listing_images, name="add_listing_images"),
    path("annonce/<int:pk>/", views.listing_detail, name="listing_detail"),
    path("annonce/<int:pk>/interesse/", views.interest, name="interest"),
    path("gestion/", dashboard.dashboard, name="agency_dashboard"),
]
