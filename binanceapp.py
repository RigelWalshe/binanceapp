from flask import Flask,jsonify,request,render_template, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import threading
import time
import requests
from decimal import Decimal
import json
from flask import flash, render_template, request, redirect
import pymysql
app = Flask(__name__)
app.secret_key = "secret key"


host = "127.0.0.1"
user = "root"
password = "Ubuntu22#"
db = "test3"
con = pymysql.connect(host='127.0.0.1', user='root', password='Ubuntu22#', db='test3', cursorclass=pymysql.cursors.
													 DictCursor)
cur = con.cursor()

_10MIN=2
_15MIN=3
_30MIN=6
_1HR=12
_4HR=48
_12HR=144
_1DAY=288



def list_all():
		cur.execute("SELECT ADA,AGI,ARDR,ARK,AST,BAT,BCHABC,BCHSV,BNB,BLZ,BTT,BTS,CND,DCR,EOS,ETH,GVT,ICX,IOTA,KNC,KMD,LTC,MANA,NANO,NAV,NEO,POLY,QTUM,RLC,RVN,SC,SNT,STRAT,TRX,WAVES,XLM,XMR,XRP,XVG,ZRX,XZC,TIME FROM Binance LIMIT 300")
		result = cur.fetchall()
		return result


def list_one(ticker):
		# currency=
		print(ticker)
		# cur.execute("SELECT (%s),TIME FROM Binance LIMIT 1000",(ticker))
		cur.execute("SELECT ADA,AGI,ARDR,ARK,AST,BAT,BCHABC,BCHSV,BNB,BLZ,BTT,BTS,CND,DCR,EOS,ETH,GVT,ICX,IOTA,KNC,KMD,LTC,MANA,NANO,NAV,NEO,POLY,QTUM,RLC,RVN,SC,SNT,STRAT,TRX,WAVES,XLM,XMR,XRP,XVG,ZRX,XZC,TIME FROM Binance LIMIT 114,510")
		 # x = c.execute("SELECT * FROM users WHERE username = (%s)",
		#cur.execute("SELECT ADA, TIME FROM Binance LIMIT 114,514")
		result = cur.fetchall()
		times= [d['TIME'] for d in result]#[0::41]
		prices= [d[ticker] for d in result]
		data=times+prices
		return data

@app.route("/line/", methods=['GET','POST'])
def chart():
	# ticker="BTS"
	# interval=_1HR
	ticker=request.form.get("ticker")
	interval=request.form.get("time_period")
	print('form ticker=',ticker)
	print('form period=',interval)
	data=list_one(ticker)
	cut=(len(data)/2)
	times=data[:cut]
	prices=data[cut:]
	if interval==  "10MIN":
		interval=2
	elif interval=="15MIN":
		interval=3
	elif interval=="30MIN":
		interval=6
	elif interval=="1HR":
		interval=12
	elif interval=="4HR":
		interval=48
	elif interval=="12HR":
		interval=144
	elif interval=="1DAY":
		interval=288

	#print(data)
	labels= times[::interval]
	values= prices[::interval]
	time=str((interval*5))+"MIN"
	return render_template('binance-line-chart.html', values=values, labels=labels, ticker=ticker, interval=time)


class ReusableForm(Form):
	id = TextField('id:', validators=[validators.required(), validators.Length(min=6, max=35)])
	name = TextField('name:', validators=[validators.required(), validators.Length(min=6, max=35)])
	username = TextField('username:', validators=[validators.required(), validators.Length(min=3, max=35)])
	country = TextField('country:', validators=[validators.required(), validators.Length(min=6, max=35)])
	ip = TextField('ip:', validators=[validators.required(), validators.Length(min=3, max=35)])
	 
@app.route("/", methods=['GET','POST'])
def load_chart():
	form = ReusableForm(request.form)
	if request.method == 'POST':
		ticker = request.form['ticker']
		timeperiod= request.form['timeperiod']
		chart(ticker,timeperiod)
	if request.method == 'POST':
		if form.validate():

			flash('Added to database ' + name)
		else:
			flash('Error: validate failed. ')
	return render_template('load_chart.html', form=form)


@app.route("/update/", methods=['GET', 'POST'])
def edit():
	form = ReusableForm(request.form)
	if request.method == 'POST':
		ticker = request.form['ticker']
		price = request.form['price']
		timestamp = request.form['timestamp']
		try:
			cur = con.cursor()
			cur.execute("UPDATE test3 SET (%s)=%s  WHERE timestamp=%s",(ticker, price,timestamp))
			#cur.execute("UPDATE tryagain SET name=%s,username=%s, country=%s, ip=%s WHERE id=%s",(name,username,country,ip,id))
			con.commit()
		except Exception as e:
			print("Problem inserting into db: " + str(e))
			return False
		flash('Data added successfully!')
	if form.validate():

		flash('Added to database ' + name)
	else:
		flash('Error: validate failed. ')

	return render_template('update.html', form=form)
 


tickerapi= [  #IMPORTANT- ive used single quotes here and this worked, but JSON only works with double quotes so make the syntax shift
	{
	"price":"4321",
	"time":"2019-06-06 16:06:06"
	}
]

@app.route('/popupapi/')
def popupapi(): #added name arg
		return render_template('popupapi.html')



@app.route('/tickerapi/<string:name>', methods=['GET']) #updated with methos and string:mname
def readapi(name): #added name arg
		def db_query():
				#db = Database()
				emps = list_all()
				return emps
		res = db_query()
		return jsonify({'tickerapi':tickerapi})

@app.route('/tickerdictapi/', methods=['GET']) #this is a demo with simple dict above
def readoneapi(): #added name arg
		def db_query():
				#db = Database()
				emps = list_all()
				return emps
		res = db_query()
		return jsonify({'tickerapi':tickerapi})


@app.route('/tickerapi/', methods=['GET']) #this is a demo with simple dict above
def readsqlapi(): #added name arg
		def db_query():
				#db = Database()
				emps = list_all()
				return emps
		res = db_query()
		return jsonify({'tickerapi':tickerapi})


@app.route('/tickerdictapi2', methods=['POST']) 
def addviaapi(): 
		request_data=request.get_json()
		new_tickdata={
		"price":request_data["price"],
		"time":request_data["time"]
		}
		tickerapi.append(new_tickdata)
		print(tickerapi)
		return jsonify(new_tickdata)

@app.route('/read/', methods=['GET']) #updated with methos and string:mname
def readall(name): #added name arg
		def db_query():
				#db = Database()
				emps = list_all()
				return emps
		res = db_query()
		return render_template('read_binance.html', result=res, content_type='application/json')



@app.route('/read/<string:name>', methods=['GET']) #updated with methos and string:mname
def readone(name): #added name arg
		def db_query():
				#db = Database()
				emps = list_one(name)
				return emps
		res = db_query()
		return render_template('read1_binance.html', result=res, content_type='application/json')
		

@app.route('/react/')
def react():
		def db_query():
				#db = Database()
				emps = list_all()
				return emps
		res = db_query()
		return render_template('react_binance.html', result=res, content_type='application/json')







@app.route("/add/", methods=['GET', 'POST'])
def add():
	price=[]
	urls=('https://api.binance.com/api/v1/ticker/price?symbol=ADABTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=AGIBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=ARDRBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=ARKBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=ASTBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=BATBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=BCHABCBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=BCHSVBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=BNBBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=BLZBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=BTTBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=BTSBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=CNDBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=DCRBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=EOSBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=ETHBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=GVTBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=ICXBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=IOTABTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=KNCBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=KMDBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=LTCBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=MANABTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=NANOBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=NAVBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=NEOBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=POLYBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=QTUMBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=RLCBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=RVNBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=SCBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=SNTBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=STRATBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=TRXBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=WAVESBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=XLMBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=XMRBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=XRPBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=XVGBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=ZRXBTC',
			'https://api.binance.com/api/v1/ticker/price?symbol=XZCBTC',
			)
	for item in urls:
			req = requests.request('GET',item)
			req_json=json.loads(req.text)
			price_data=(req_json.get('price'))
			price_dec=(Decimal(price_data))
			price_satoshis=int(price_dec*100000000)
			#print(price_satoshis)
			price.append(price_satoshis)
	ADA=price[0]
	AGI=price[1]
	ARDR=price[2]
	ARK=price[3]
	AST=price[4]
	BAT=price[5]
	BCHABC=price[6]
	BCHSV=price[7]
	BNB=price[8]
	BLZ=price[9]
	BTT=price[10]
	BTS=price[11]
	CND=price[12]
	DCR=price[13]
	EOS=price[14]
	ETH=price[15]
	GVT=price[16]
	ICX=price[17]
	IOTA=price[18]
	KNC=price[19]
	KMD=price[20]
	LTC=price[21]
	MANA=price[22]
	NANO=price[23]
	NAV=price[24]
	NEO=price[25]
	POLY=price[26]
	QTUM=price[27]
	RLC=price[28]
	RVN=price[29]
	SC=price[30]
	SNT=price[31]
	STRAT=price[32]
	TRX=price[33]
	WAVES=price[34]
	XLM=price[35]
	XMR=price[36]
	XRP=price[37]
	XVG=price[38]
	ZRX=price[39]
	XZC=price[40]
	TIME=time.strftime('%Y-%m-%d %H:%M:%S')
	print(ZRX)
	print(XZC)
	#print(json.dumps(r))

	#response = jsonify(r)
	#response.status_code = 200 # or 400 or whatever
	cur = con.cursor()
	cur.execute("INSERT INTO Binance (ADA,AGI,ARDR,ARK,AST,BAT,BCHABC,BCHSV,BNB,BLZ,BTT,BTS,CND,DCR,EOS,ETH,GVT,ICX,IOTA,KNC,KMD,LTC,MANA,NANO,NAV,NEO,POLY,QTUM,RLC,RVN,SC,SNT,STRAT,TRX,WAVES,XLM,XMR,XRP,XVG,ZRX,XZC,TIME) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (ADA,AGI,ARDR,ARK,AST,BAT,BCHABC,BCHSV,BNB,BLZ,BTT,BTS,CND,DCR,EOS,ETH,GVT,ICX,IOTA,KNC,KMD,LTC,MANA,NANO,NAV,NEO,POLY,QTUM,RLC,RVN,SC,SNT,STRAT,TRX,WAVES,XLM,XMR,XRP,XVG,ZRX,XZC, TIME))
	con.commit()
	print('result logged')
	time.sleep(300)

	return add()#rt#render_template('add.html', form=form)
 
 


	
if __name__ == "__main__":
		app.run()

