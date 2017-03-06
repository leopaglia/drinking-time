from django.views.generic import View, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
import os
import ntpath
import json


class BaseView(TemplateView):

    csrf_exempt = True

    @classmethod
    def response(cls, response, no_cache=False, headers=None):
        response = HttpResponse(response)
        response = cls.__cache_headers(response, no_cache, headers)
        return response

    @classmethod
    def download(cls, filepath, content_type, delete=False, no_cache=False, headers=None):
        d_file = open(filepath, 'r')
        filename = ntpath.basename(filepath)
        response = HttpResponse(d_file, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
        response = cls.__cache_headers(response, no_cache, headers)
        if delete:
            os.remove(filepath)
        return response

    @staticmethod
    def server_error(response):
        response = HttpResponse(response)
        response.status_code = 500
        return response

    @staticmethod
    def redirect(url):
        return HttpResponseRedirect(url)

    @staticmethod
    def __cache_headers(response, no_cache, headers):
        if no_cache:
            response["Cache-Control"] = "max-age=0"
        if headers is not None:
            for key, value in headers.iteritems():
                response[key] = value
        return response


class AjaxView(View):

    @staticmethod
    def json_response(response):
        return HttpResponse(json.dumps(response))

    @staticmethod
    def json_loads(data):
        return json.loads(data)

    @staticmethod
    def json_dumps(data):
        return json.dumps(data)

    def success_response(self, **kwargs):
        response = {"status": "success"}
        response.update(kwargs)
        return self.json_response(response)

    def failure_response(self, error):
        return self.json_response({"status": "failure", "error": error})
