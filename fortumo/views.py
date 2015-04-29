from django.conf import settings
from django.http import HttpResponse
from django.http.response import HttpResponseForbidden


def payment_processor(request):
    if (
            settings.FORTUMO_ENABLE_IP_VALIDATION and
            not request.META['REMOTE_ADDR'] in settings.FORTUMO_IPS
    ):
        return HttpResponseForbidden('403')

    return HttpResponse('dummy')
