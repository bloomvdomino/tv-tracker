from django.http.response import JsonResponse
from django.views import View


class HealthCheckView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"data": "Ok"})
