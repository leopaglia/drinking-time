from django.conf.urls import url
from app.views.drinkingtime import DrinkingTimeView

urlpatterns = [
    url(r'^([1-5])$', DrinkingTimeView.as_view(), name='drinkingtime')
]
