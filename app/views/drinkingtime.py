from django.views.generic import TemplateView
from django.conf import settings
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.core.urlresolvers import reverse

from datetime import datetime
import json


@method_decorator(csrf_exempt, name='dispatch')
class DrinkingTimeView(TemplateView):

    def get(self, request, *args, **kwargs):

        gif_url = self.get_gif_path()
        gif_data = open(gif_url, "rb").read()

        return HttpResponse(gif_data, content_type="image/png")

    def post(self, request):

        if request.POST.get('token') != settings.SLACK_TOKEN:
            return HttpResponse('Unauthorized', status=401)

        payload = self.get_payload_for_request(request)

        return HttpResponse(json.dumps(payload), content_type="application/json")

    def get_gif_path(self):

        gifs = settings.GIFS
        now = datetime.now()

        intervals = self.get_intervals()

        gif_name = next((gif for ((dfrom, dto), gif) in zip(intervals, gifs) if dfrom <= now <= dto), gifs[0])
        return settings.STATIC_ROOT + gif_name

    @staticmethod
    def get_intervals():

        gifs = settings.GIFS

        sfrom = settings.DATERANGE['initial']
        sto = settings.DATERANGE['final']

        fmt = '%H:%M:%S'

        datetime_from = datetime.strptime(sfrom, fmt)
        datetime_to = datetime.strptime(sto, fmt)

        delta = datetime_to - datetime_from
        distance_between_gifs = delta / len(gifs)

        points = [datetime_from + distance_between_gifs * x for x in range(0, 5)]
        return [(x, x + distance_between_gifs) for x in points]

    def get_payload_for_request(self, request):

        # token = gIkuvaNzQIHg97ATvDxqgjtO
        # team_id = T0001
        # team_domain = example
        # channel_id = C2147483705
        # channel_name = test
        # user_id = U2147483697
        # user_name = Steve
        # command = /drinkingtime
        # text = one of {help, next, hours}
        # response_url = https://hooks.slack.com/commands/1234/5678

        text = request.POST.get('text')
        channel = request.POST.get('channel')

        now = datetime.now()

        payload = {
            'channel': channel,
            'username': 'Drinking Time'
        }

        if not text:
            payload['response_type'] = 'in_channel'
            payload['attachments'] = [{
                "text": "Drinking time",
                "image_url": request.build_absolute_uri(reverse('drinkingtime'))
            }]

        elif text == 'next':
            payload['response_type'] = 'ephemeral'
            payload['text'] = next(dfrom.strftime('%H:%M') for (dfrom, dto) in self.get_intervals() if dfrom >= now)

        elif text == 'hours':
            payload['response_type'] = 'ephemeral'
            payload['text'] = ' - '.join((dfrom.strftime('%H:%M') for (dfrom, dto) in self.get_intervals()))

        elif text == 'help':
            payload['response_type'] = 'ephemeral'
            payload['text'] = (
                "/drinkingtime - lenny tells everyone when sale shangai \n"
                "/drinkingtime next - get the next hour when light changes \n"
                "/drinkingtime hours - get the list of hours when the light changes \n"
            )

        else:
            payload['response_type'] = 'ephemeral'
            payload['text'] = 'Invalid argument specified. Try /drinkingtime help'

        return payload
