from .base import BaseView
from datetime import datetime


class DrinkingTime(BaseView):

    def post(self, request):
        now = datetime.now().time()



        mah_data = request.POST.get('some_data', None)
        return self.success_response(lol='lololol', moar_data=mah_data)
