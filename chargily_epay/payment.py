import requests 
from django.shortcuts import redirect
from django.core.validators import URLValidator, EmailValidator
from django.conf import  settings
from .models import Chargily
from django.http import JsonResponse, HttpRequest 
import hmac 
import hashlib
import json

class Chargily_Pay:
	def __init__(self, **kwargs):
		if 'params' in kwargs.keys():
			self.params = kwargs['params']

		self.query_set = Chargily()

	def _checkParams(self):
		''' valid pramaters '''
		
		try:
			URLValidator(self.params['back_url'])
			URLValidator(self.params['webhook_url'])
		except Exception as e:
			raise e

		try:
			EmailValidator(self.params['client_email'])
		except Exception as e:
			raise e

		if int(self.params['amount']) < 70:
			raise ValueError('the amount should be greater than 70')

		if int(self.params['discount']) < 0  or int(self.params['discount']) > 99:
			raise ValueError('the discount should be between 0 and 99')


		if not self.params['mode'] == 'EDAHABIA' or self.params['mode'] == 'CIB':
			raise ValueError('the mode should be EDAHABIA or CIB')

		

		return self.params


	@property
	def _pay(self):
		headers = {
			'X-Authorization' : settings.CHARGILY_API_KEY,
			'Accept' : 'application/json'
		  }
		
		url = 'https://epay.chargily.com.dz/api/invoice'
		try:

			_response = requests.post(url, headers=headers ,
				params=self._checkParams())
			return _response
		except Exception as e:
			raise e 
		

	@property
	def status_code(self):
		return self._pay.status_code

	@property
	def json(self):
		return self._pay.json()

	@property
	def get_redirect_url(self):
		if self.status_code == 201:
			return self.json['checkout_url']
		return False


	def history(self, **kwargs):
		all_history = self.query_set.objects.all()
		filter_history = kwargs['filter']
		if filter_history:
			return filter_history

		return all_history

	def getResponseDetails(self, request):
		if request.method == 'POST':
			secret = settings.CHARGILY_SECRET_KEY
			body_content = HttpRequest.body
			headers = request.headers["Signature"]
			dig = hmac.new(secret ,msg=body_content, digestmod=hashlib.sha256).digest()
			validate = hmac.compare_digest(dig, headers)
			if validate:
				payment = json.dumps(body_content)
				if payment["invoice"]["status"] == 'paid':
					query = self.query_set(client=payment["invoice"]['client'],
						amount=payment["invoice"]['amount'],
						discount=payment["invoice"]['discount'],
						mode=payment["invoice"]['mod'],
						comment=payment["invoice"]['comment'])
					query.save()

				return payment
			return 'error'
	



	




