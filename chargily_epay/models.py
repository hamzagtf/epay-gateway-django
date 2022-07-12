from django.db import models

class Chargily(models.Model):
	EDAHABIA ='EDAHABIA'
	CIB = 'CIB'
	client = models.CharField(max_length=200)
	amount = models.CharField(max_length=200)
	discount = models.CharField(max_length=200)
	MODE_IN_CHOICES = [
		(EDAHABIA, 'EDAHABIA'),
		(CIB, 'CIB') 
	]
	mode = models.CharField(max_length=200, choices=MODE_IN_CHOICES, default=EDAHABIA)
	comment = models.CharField(max_length=200)
