from django.http import HttpResponse
import urllib.request
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
	) as url :
		data = json.loads(url.read())
		return float(data['USD'])

def get_usdprice():
	with urllib.request.urlopen(
		"http://call.tgju.org/ajax.json"
	) as url:
		data=json.loads(url.read())
		price=str(data['current']['price_dollar_soleymani']['p'])
		price = price.replace(',', '')
		return int(price)

def api(request):
	response = ''
	response += '<p>Active Miners = '
	activeminer = str(get_data()['miners']['now'])
	accepted_shares = str(get_data()["results"]["accepted"])
	response += activeminer + "</p><p>Accepted Shares = " + accepted_shares + "</p>"
	response += "<p>Pending Payment = " + str(get_balance()) + "</p>"

	response += "<p> XMRtoUSD : " + str(get_price()) + " USD </p>"

	response += '<p> USDtoRIAL : ' + format(int(get_usdprice()), ',d') + ' </p>'

	response += '<p> Charge : ' + format(get_price() * get_balance(), ".2f") + ' USD | '+str(format(int(get_price()*get_balance()*get_usdprice()), ',d')) +' RIAL</p>'

	for workers in get_worker()['workers']:
		workerid = re.split(r'[.](?![^][]*\])', workers[0])
		response += "<p>" + workerid[2] + ' : [ Number Of Workers = ' + str(workers[2]) + " , Accepted Shares = "+str(workers[3]) +"]</p>"


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