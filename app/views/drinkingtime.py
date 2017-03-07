from django.views.generic import TemplateView
from django.conf import settings
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.core.urlresolvers import reverse

from datetime import datetime
from datetime import timedelta
import json


@method_decorator(csrf_exempt, name='dispatch')
class DrinkingTimeView(TemplateView):

    def get(self, request, *args, **kwargs):

        gif_url = "{0}{1}.gif".format(settings.STATIC_ROOT, args[0])
        gif_data = open(gif_url, "rb").read()

        response = HttpResponse(gif_data, content_type="image/png")
        response["Cache-Control"] = "no-cache"

        return response

    def post(self, request):

        if request.POST.get('token') != settings.SLACK_TOKEN:
            return HttpResponse('Unauthorized', status=401)

        payload = self.get_payload_for_request(request)

        return HttpResponse(json.dumps(payload), content_type="application/json")

    def get_gif_name(self):

        now = datetime.now()
        gifs = settings.GIFS
        ivs = self.get_intervals()

        return next((gif for ((dfrom, dto), gif) in zip(ivs, gifs) if dfrom.time() <= now.time() <= dto.time()), '1')

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

        points = [datetime_from + distance_between_gifs * (x + 1) for x in range(0, 5)]
        return [(x, x + distance_between_gifs) for x in points]

    def get_next_change(self):

        now = datetime.now()
        intervals = self.get_intervals()

        return next((dfrom - timedelta(hours=3)).strftime('%H:%M') for (dfrom, dto) in intervals if dfrom.time() >= now.time())

    def get_every_change(self):

        intervals = self.get_intervals()

        return ' - '.join((dto - timedelta(hours=3)).strftime('%H:%M') for (dfrom, dto) in intervals)

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

        gifname = self.get_gif_name()

        payload = {
            'channel': channel,
            'username': 'Drinking Time'
        }

        if not text:
            payload['response_type'] = 'in_channel'
            payload['attachments'] = [{
                "text": "Drinking time",
                "image_url": request.build_absolute_uri(reverse('drinkingtime', args=[1]))
            }]

        elif text == 'next':
            payload['response_type'] = 'ephemeral'
            payload['text'] = self.get_next_change()

        elif text == 'hours':
            payload['response_type'] = 'ephemeral'
            payload['text'] = self.get_every_change()

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
