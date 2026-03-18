from django.http import HttpRequest

from quiz.models import Driver


def driver_info(request: HttpRequest):
    driver_id = request.session.get("driver_id")
    driver = None

    if driver_id:
        try:
            driver = Driver.objects.get(pk=driver_id)


        except Driver.DoesNotExist:
            pass

    return {"driver": driver}
