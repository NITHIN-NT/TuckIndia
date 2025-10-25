from django.urls import path
from . import views
urlpatterns = [
    path('',views.homepage,name='Home_page_user')
]
