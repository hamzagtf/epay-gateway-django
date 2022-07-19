# epay-gateway-django
Chargily ePay Gateway (Django Package)

1. clone the app into your project
2. add it to your installed apps
3. add your api key in variable named "CHARGILY_API_KEY"
4. add your secret api key in "CHARGILY_SECRET_KEY"
5. make migrations
6. from payment import Chargily_Pay
7. make payemnt with Chargily_Pay._pay
8. return json response with Chargily_Pay.json
9.  Chargily_Pay.get_redirect_url
10.  check history Chargily_Pay.history
11.  get response Chargily_Pay.getResponseDetails
