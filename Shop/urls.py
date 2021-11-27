from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name='aboutUs'),
    path("contact/", views.contact, name='contactUs'),
    path("tracker/", views.tracker, name="tracker"),
    path("search/", views.search, name="search"),
    path("productView/<int:id>", views.productView, name="productView"),
    path("checkout/", views.checkout, name="checkout"),
    path('handlerequest/', views.handlerequest, name='handlerequest')
]
