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
	try:
		balance = 0
		with urllib.request.urlopen(
				"https://p5.minexmr.com/get_wid_stats?address"
				"=4BCeEPhodgPMbPWFN1dPwhWXdRX8q4mhhdZdA1dtSMLTLCEYvAj9QXjXAfF7CugEbmfBhgkqHbdgK9b2wKA6nqRZQCgvCDm"
				".a3f9726cd9865d8603162c0f88f8777a39ae849f28dc4e2b3860220609a7e512") as url:
			data = json.loads(url.read())
			for x in data:
				balance += float(x['balance'])
		return balance / 1000000000000
	except urllib.error.URLError:
		return 0


def get_price():
	try:
		with urllib.request.urlopen(
				"https://min-api.cryptocompare.com/data/price?fsym=XMR&tsyms=BTC,USD,EUR"
		) as url:
			data = json.loads(url.read())
			return float(data['USD'])
	except urllib.error.URLError:
		return float(0)


def get_usdprice():
	try:
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
	except urllib.error.URLError:
		return 0


def api(request):
	response = ''
	usd_price = get_usdprice()
	price = get_price()
	balance = get_balance()
	
	try:
		activeminer = str(get_data()['miners']['now'])
		accepted_shares = str(get_data()["results"]["accepted"])
		response += '<p>Active Miners = ' + activeminer + "</p><p>Accepted Shares = " + accepted_shares + "</p>"
	except urllib.error.URLError:
		response += '<H1>Proxy Server Unreachable</H1>'

	response += "<p>Pending Payment = " + str(balance) + "</p>"
	response += "<p>XMRtoUSD : " + str(price) + " USD </p>"
	response += '<p>USDtoRIAL : ' + format(int(usd_price), ',d') + ' </p>'
	response += '<p>Charge : ' + format(price * balance, ".2f") + ' USD | ' + str(
		format(int(price * balance * usd_price), ',d')) + ' RIAL</p>'
	try:
		for workers in get_worker()['workers']:
			workerid = re.split(r'[.](?![^][]*\])', workers[0])
			response += "<p>" + workerid[2] + ' : [ Number Of Workers = ' + str(workers[2]) + " , Accepted Shares = " + str(workers[3]) + "]</p>"
	except urllib.error.URLError:
		response += '<h2> No active Worker</h2>'
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
