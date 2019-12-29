from django.db import models

# Create your models here.


class UserInfo(models.Model):
	TEMP_TYPE = (
		('F', 'Fahrenheit'),
		('C', 'Celsius'),
		)
	zip_code = models.CharField(max_length=5)
	unit_of_temperature = models.CharField(max_length=1, choices=TEMP_TYPE)