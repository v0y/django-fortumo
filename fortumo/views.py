from django.conf import settings
from django.http import HttpResponse
from django.http.response import HttpResponseForbidden

from fortumo import consts
from fortumo.models import (
    Message,
    Payment,
    Service,
)
from fortumo.utils import (
    generate_unique_pin,
    signature_is_valid,
)


def payment_processor(request):
    if (
            settings.FORTUMO_ENABLE_IP_VALIDATION and
            not request.META['REMOTE_ADDR'] in settings.FORTUMO_IPS
    ):
        return HttpResponseForbidden()

    if not signature_is_valid(request.GET):
        return HttpResponseForbidden()

    message = Message.objects.create(
        message=request.GET['message'],
        sender=request.GET['sender'],
        country=request.GET['country'],
        price=request.GET['price'],
        price_wo_vat=request.GET['price_wo_vat'],
        currency=request.GET['currency'],
        service_id=request.GET['service_id'],
        message_id=request.GET['message_id'],
        keyword=request.GET['keyword'],
        shortcode=request.GET['shortcode'],
        operator=request.GET['operator'],
        billing_type=request.GET['billing_type'],
        status=request.GET['status'],
        test=request.GET['test'],
        sig=request.GET['sig'],
    )

    pin = generate_unique_pin(request.GET['service_id'])

    Payment.objects.create(
        service=Service.objects.get(service_id=request.GET['service_id']),
        message=message,
        pin=pin,
    )

    return HttpResponse('dummy')


def check_pin(request):
    # TODO: add ip validation
    try:
        service = Service.objects.get(secret=request.POST.get('secret'))
    except Service.DoesNotExist:
        return HttpResponseForbidden()

    try:
        payment = Payment.objects.get(
            service=service,
            pin=request.POST.get('pin'),
        )
    except Payment.DoesNotExist:
        return HttpResponse(consts.PinResponse.INVALID)

    payment.used = True
    payment.save()

    return HttpResponse(consts.PinResponse.VALID)

