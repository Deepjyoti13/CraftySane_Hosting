from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="Product"),
    path('addReview/<int:id>', views.addReview, name='addReview'),
    
]