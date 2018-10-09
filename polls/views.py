from django.http import HttpResponse
import urllib.request
import urllib.error
import json
import re
from django.template import loader


def get_data():
	with urllib.request.urlopen("http://localhost:85")as url:
		data = json.loads(url.read())
	return data


def get_worker():
	with urllib.request.urlopen("http://localhost:85/workers.json") as url:
		data = json.loads(url.read())
	return data


def get_balance():
	balance = 0
	with urllib.request.urlopen(
			"https://p5.minexmr.com/get_wid_stats?address"
			"=4BCeEPhodgPMbPWFN1dPwhWXdRX8q4mhhdZdA1dtSMLTLCEYvAj9QXjXAfF7CugEbmfBhgkqHbdgK9b2wKA6nqRZQCgvCDm"
			".a3f9726cd9865d8603162c0f88f8777a39ae849f28dc4e2b3860220609a7e512") as url:
		data = json.loads(url.read())
		for x in data:
			balance += float(x['balance'])
	return balance / 1000000000000



def get_price():
	with urllib.request.urlopen(
			"https://min-api.cryptocompare.com/data/price?fsym=XMR&tsyms=BTC,USD,EUR"
	) as url:
		data = json.loads(url.read())
		return float(data['USD'])


def get_usdprice():
	with urllib.request.urlopen(
			"http://call.tgju.org/ajax.json"
	) as url:
		data = json.loads(url.read())
		try:
			price = str(data['current']['price_dollar_rl']['p'])
		except KeyError:
			return int(0)
		price = price.replace(',', '')
		return int(price)



def api(request):

	try:
		usd_price = get_usdprice()
	except urllib.error.__all__:
		usd_price = 0
	try:
		price = get_price()
	except urllib.error.__all__:
		price = 0
	try:
		balance = get_balance()
	except urllib.error.__all__:
		balance = 0
	try:
		activeminer = str(get_data()['miners']['now'])
		accepted_shares = str(get_data()["results"]["accepted"])
	except urllib.error.__all__:
		activeminer = 0
		accepted_shares = 0
	response = ''
	response += '<p>Active Miners = '


	response += activeminer + "</p><p>Accepted Shares = " + accepted_shares + "</p>"
	response += "<p>Pending Payment = " + str(balance) + "</p>"
	response += "<p>XMRtoUSD : " + str(price) + " USD </p>"
	response += '<p>USDtoRIAL : ' + format(int(usd_price), ',d') + ' </p>'
	response += '<p>Charge : ' + format(price * balance, ".2f") + ' USD | ' + str(
		format(int(price * balance * usd_price), ',d')) + ' RIAL</p>'
	try:
		for workers in get_worker()['workers']:
			workerid = re.split(r'[.](?![^][]*\])', workers[0])
			response += "<p>" + workerid[2] + ' : [ Number Of Workers = ' + str(workers[2]) + " , Accepted Shares = " + str(
				workers[3]) + "]</p>"
	except urllib.error.__all__:
		print("Error")
	return HttpResponse(response)


def index(request):
	response = '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Info</title><style>body {font-size: ' \
			   '12px;font-family: Arial;}</style><script ' \
			   'src="https://code.jquery.com/jquery-1.10.2.js"></script></head><body><b>Info:</b><ol ' \
			   'id="new-projects"></ol><script>function loadlink(){$("#new-projects").load("/api",function () {$(' \
			   'this).unwrap();})};loadlink();setInterval(function(){loadlink()}, 10000);</script></body></html> '
	return HttpResponse(response)


def test(request):
	template = loader.get_template('dashboard.html')
	return HttpResponse(template.render())
