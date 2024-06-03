from django.urls import path
from . import views

urlpatterns = [
    path('create_payment/', views.create_payment, name='create_payment'),
    path("",views.index, name="index"),
]
