from django.views.generic import TemplateView
from django.conf import settings
from django.http import HttpResponse

from datetime import datetime
import requests


class DrinkingTimeView(TemplateView):

    def get(self, request, *args, **kwargs):

        gif_url = self.get_gif_path()
        gif_data = open(gif_url, "rb").read()

        return HttpResponse(gif_data, content_type="image/png")

    def post(self, request):

        # token = gIkuvaNzQIHg97ATvDxqgjtO
        # team_id = T0001
        # team_domain = example
        # channel_id = C2147483705
        # channel_name = test
        # user_id = U2147483697
        # user_name = Steve
        # command = / weather
        # text = 94070
        # response_url = https://hooks.slack.com/commands/1234/5678

        if request.POST.get('token') != settings.SLACK_TOKEN:
            return HttpResponse('Unauthorized', status=401)

        channel = request.POST.get('channel')
        response_url = request.POST.get('response_url')

        gif_url = self.get_gif_path()

        payload = {
            'unfurl_links': True,
            'text': '<{}>'.format(gif_url),
            'channel': channel,
            'username': 'Drinking Time'
        }

        requests.post(response_url, data=payload)

        return HttpResponse()

    @staticmethod
    def get_gif_path():

        gifs = settings.GIFS

        sfrom = settings.DATERANGE['initial']
        sto = settings.DATERANGE['final']

        fmt = '%H:%M:%S'

        datetime_from = datetime.strptime(sfrom, fmt)
        datetime_to = datetime.strptime(sto, fmt)
        now = datetime.now()

        delta = datetime_to - datetime_from
        distance_between_gifs = delta / len(gifs)

        points = [datetime_from + distance_between_gifs * x for x in range(0, 5)]
        intervals = [(x, x + distance_between_gifs) for x in points]

        gif_name = next((gif for ((dfrom, dto), gif) in zip(intervals, gifs) if dfrom <= now <= dto), gifs[0])
        return settings.STATIC_ROOT + gif_name
