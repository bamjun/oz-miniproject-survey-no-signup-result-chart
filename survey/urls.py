from django.urls import path
from .views import home_view, question_view, survey_complete_view, result_view

urlpatterns = [
    path('', home_view, name='home'),
    path('question/', question_view, name='question'),
    path('survey-complete/', survey_complete_view, name='survey_complete'),
    path('result/', result_view, name='result'),
]