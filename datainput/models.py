from django.db import models


class Measurements(models.Model):
    date_of_measurement = models.DateTimeField()
    motor_rotations = models.DecimalField(max_digits=7, decimal_places=2)
    temperature_1 = models.DecimalField(max_digits=5, decimal_places=2)
    temperature_2 = models.DecimalField(max_digits=5, decimal_places=2)
    current_draw = models.DecimalField(max_digits=7, decimal_places=4)
    user_name = models.TextField(blank=True,
                                 max_length=35)
    comment = models.TextField(blank=True,
                               max_length=200)

    def __str__(self):
        return str(self.date_of_measurement)[:-6] + " " + str(self.user_name)
