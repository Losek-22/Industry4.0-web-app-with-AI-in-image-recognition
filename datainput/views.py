from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .models import Measurements


def index(request):
    return render(request, "datainput/index.html", {'data': ['3213rpm', '321rpm', '12rps']})


def adddata(request):
    return render(request, "datainput")


def add_data_form_submission(request):
    print("Form submitted")
    motor_rotations = request.POST["Motor rotations"]
    temperature1 = request.POST["Temperature1"]
    temperature2 = request.POST["Temperature2"]
    comment = request.POST["Comment"]
    current = request.POST["Current"]
    measurement_time = str(datetime.now())[:-7]

    measurements = Measurements(
        date_of_measurement=measurement_time,
        motor_rotations=motor_rotations,
        temperature_1=temperature1,
        temperature_2=temperature2,
        current_draw=current,
        comment=comment
    )

    measurements.save()

    return render(request, "datainput/thank_you.html")