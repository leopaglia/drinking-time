from django.conf.urls import url
from app.views.drinkingtime import DrinkingTimeView

urlpatterns = [
    url(r'^$', DrinkingTimeView.as_view())
]
