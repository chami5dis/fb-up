#king chami
from random import randint
from pymessenger import Bot
from flask import Flask, request
import os,time ,sys,json
from threading import Thread
import warnings , requests
from flask import send_file
import urllib
path=os.path.dirname(os.path.abspath(__file__))
oldmsg = "none"
oldsender = "12345"
warnings.filterwarnings("ignore")
app = Flask(__name__)
PAGE_ACCESS_TOKEN = os.getenv('FB_TOKEN')
bot = Bot(PAGE_ACCESS_TOKEN)

def randomn(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

@app.route('/', methods=['GET'])
def verify():
	global idb
	if request.args.get("link") and request.args.get("id"):
		#log(request.args.get("link"))
		global messaging_text
		global sender_id
		sender_id = request.args.get("id")
		messaging_text  = urllib.unquote_plus(request.args.get("link"))
		idb = sender_id+str(randomn(8))
		return str(idb)+" Prossessing! You can close the browser window.", 200
	if request.args.get("link") and not request.args.get("id"):
		global messaging_text
		global sender_id
		sender_id = os.getenv('ADMIN_ID')
		messaging_text  = urllib.unquote_plus(request.args.get("link"))
		idb = sender_id+str(randomn(8))
		return str(idb)+" Prossessing!....Sending to owner...You can close the browser window.", 200	
	return send_file(path+ "/index.html", attachment_filename='index.html')

@app.route('/ADM.txt', methods=['GET'])
def adm():
	if (request.args.get("id")):
		try:
			return send_file(path+ "/ADM"+str(request.args.get("id"))+".txt", attachment_filename='ADM.txt')
		except:
			return "ADM"+str(request.args.get("id"))+".txt not found!"		
	if (request.args.get("mid")):
		try:
			global idb
			mid = request.args.get("mid")
			idb = str(randomn(8))
			t = Thread(target=updateadmtext, args=(mid,idb, ))
			t.start()
			return str(idb)+" Prossessing!....You can close the browser window.", 200
		except Exception as e:
			return "Error occured!"+str(e)	
	try:
		return send_file(path+ "/ADM.txt", attachment_filename='ADM.txt')
	except:
		return "ADM"+str(request.args.get("id"))+".txt not found!"
	if (request.args.get("act") == "rm") and (request.args.get("id")):
		try:
			os.remove(path+ "/ADM"+str(request.args.get("id"))+".txt")
			return "Removed ADM"+str(request.args.get("id"))+".txt", 200
		except:
			return "ADM"+str(request.args.get("id"))+".txt not found!"
	if (request.args.get("act") == "rm"):
		try:
			os.remove(path+ "/ADM.txt")
			return "Removed ADM.txt", 200
		except:
			return "ADM.txt not found!"

@app.route('/tst.txt', methods=['GET'])
def tst():
	if (request.args.get("act") == "rm"):
		try:
			os.remove(path+ "/tst.txt")
			return "Removed tst.txt", 200
		except:
			return "tst.txt not found!"
	try:
		return send_file(path+ "/tst.txt", attachment_filename='tst.txt')
	except:
		return "tst.txt not found!"
	
@app.route('/msg.txt', methods=['GET'])
def msg():
	if (request.args.get("id")):
		try:
			return send_file(path+ "/msg"+str(request.args.get("id"))+".txt", attachment_filename='msg.txt')
		except:
			return "msg"+str(request.args.get("id"))+".txt not found!"		
	try:
		return send_file(path+ "/msg.txt", attachment_filename='msg.txt')
	except:
		return "msg"+str(request.args.get("id"))+".txt not found!"
	if (request.args.get("act") == "rm") and (request.args.get("id")):
		try:
			os.remove(path+ "/msg"+str(request.args.get("id"))+".txt")
			return "Removed msg"+str(request.args.get("id"))+".txt", 200
		except:
			return "msg"+str(request.args.get("id"))+".txt not found!"
	if (request.args.get("act") == "rm"):
		try:
			os.remove(path+ "/msg.txt")
			return "Removed msg.txt", 200
		except:
			return "msg.txt not found!"

		
@app.after_request
def after_request_func(response):
	#log(response)
	try:
		log(messaging_text)
		log(sender_id)
		try:
			if not (messaging_text == oldmsg):
				t = Thread(target=downup, args=(messaging_text,sender_id, ))
				t.start()
			if (messaging_text == oldmsg) and not (sender_id == oldsender):
				t = Thread(target=downup, args=(messaging_text,sender_id, ))
				t.start()				
		except Exception as e:
			log(e)
		global oldmsg
		global oldsender
		oldmsg = messaging_text
		oldsender = sender_id
	except Exception as e:
		log(e)
	return response
	
def downup(messaging_text,sender_id):
 id = idb
 log(id)
 lmsg  = ""
 if not ('http' in messaging_text):
		data = bot.send_text_message(sender_id,messaging_text )
		open("./tst.txt", "a+").write("################################################### "+str(id)+"\n")
		open("./tst.txt", "a+").write( str(data)+ "\n")
		mid = data['message_id']
		log(mid)
		#req = requests.get('https://graph.facebook.com/v6.0/'+str(mid)+'/attachments?access_token='+str(PAGE_ACCESS_TOKEN) )
		#data = req.json()
		#log(data)
 if 'http' in messaging_text and not (':::' in messaging_text) :
		bot.send_text_message(sender_id, "wait "+str(id))
		i = 0
		while i == 0:
			data = bot.send_file_url(sender_id, messaging_text)
			try:
				if (data['error']):
					i = 0
			except:
				i = 1
		log(data)
		open("./tst.txt", "a+").write("################################################### "+str(id)+"\n")
		open("./tst.txt", "a+").write( str(data)+ "\n")
		try:
			mid = data['message_id']
			log(mid)
			req = requests.get('https://graph.facebook.com/v6.0/'+str(mid)+'/attachments?access_token='+str(PAGE_ACCESS_TOKEN) )
			data = req.json()
			furl = data["data"][0]['file_url']
			open("./ADM.txt", "a+").write("################################################### "+str(id)+"\n")
			open("./ADM.txt", "a+").write( furl+ "\n")
			open("./ADM"+str(id)+".txt", "a+").write( furl+ "\n")
		except Exception as e:
			log(e)
		messaging_text = 'no text'
 if (':::' in messaging_text) and not (':-:' in messaging_text):
		open("./ADM.txt", "a+").write("################################################### "+str(id)+"\n")
		open("./tst.txt", "a+").write("################################################### "+str(id)+"\n")
		bot.send_text_message(sender_id, "wait "+str(id))
		for n in range(1,int(messaging_text.split(':::')[1])+1):
			i = 0
			while i == 0:
				data = bot.send_file_url(sender_id , str(messaging_text.split('001:::')[0])+str("{:03d}".format(n)))
				try:
					if (data['error']):
						i = 0
				except:
					i = 1
			log(data)
			open("./tst.txt", "a+").write( str(data)+ "\n")
			try:
				mid = data['message_id']
				log(mid)
				open("./msg"+str(id)+".txt", "a+").write( str(mid)+ ":")
				req = requests.get('https://graph.facebook.com/v6.0/'+str(mid)+'/attachments?access_token='+str(PAGE_ACCESS_TOKEN) )
				data = req.json()
				log(data)
				furl = data["data"][0]['file_url']
				open("./ADM.txt", "a+").write( furl+ "\n")
				open("./ADM"+str(id)+".txt", "a+").write( furl+ "\n")
			except Exception as e:
				log(e)
		#bot.send_attachment(sender_id, "file", "./ADM.txt")
		#os.remove("./ADM.txt")
		#log(lmsg)
		#bot.send_message(sender_id,lmsg)
		bot.send_file_url(sender_id, 'https://fb-up.herokuapp.com/ADM.txt?id='+str(id))
		bot.send_file_url(sender_id, 'https://fb-up.herokuapp.com/msg.txt?id='+str(id))
		#bot.send_file_url(sender_id, 'https://fb-up.herokuapp.com/tst.txt')
		messaging_text = 'no text'
 if (':-:' in messaging_text):
		open("./ADM.txt", "a+").write("################################################### "+str(id)+"\n")
		open("./tst.txt", "a+").write("################################################### "+str(id)+"\n")
		bot.send_text_message(sender_id, "wait "+str(id))
		for n in range(int((messaging_text.split(':::')[1]).split(':-:')[0]),int(messaging_text.split(':-:')[1])+1):
			i = 0
			while i == 0 :
				data = bot.send_file_url(sender_id , str(messaging_text.split('001:::')[0])+str("{:03d}".format(n)))
				try:
					if (data['error']):
						i = 0
				except:
					i = 1
			log(data)
			open("./tst.txt", "a+").write( str(data)+ "\n")
			try:
				mid = data['message_id']
				log(mid)
				open("./msg"+str(id)+".txt", "a+").write( str(mid)+ ":")
				req = requests.get('https://graph.facebook.com/v6.0/'+str(mid)+'/attachments?access_token='+str(PAGE_ACCESS_TOKEN) )
				data = req.json()
				log(data)
				furl = data["data"][0]['file_url']
				open("./ADM.txt", "a+").write( furl+ "\n")
				open("./ADM"+str(id)+".txt", "a+").write( furl+ "\n")
			except Exception as e:
				log(e)
		#bot.send_attachment(sender_id, "file", "./ADM.txt")
		#os.remove("./ADM.txt")
		#log(lmsg)
		#bot.send_message(sender_id,lmsg)
		bot.send_file_url(sender_id, 'https://fb-up.herokuapp.com/ADM.txt?id='+str(id))
		bot.send_file_url(sender_id, 'https://fb-up.herokuapp.com/msg.txt?id='+str(id))
		#bot.send_file_url(sender_id, 'https://fb-up.herokuapp.com/tst.txt')
		messaging_text = 'no text'
		
def updateadmtext(mid,idb):
	i = 0
	while i < 999999999999999:
		try:
			midn = mid.split(':')
			log(midn[i])
			req = requests.get('https://graph.facebook.com/v6.0/'+str(midn[i])+'/attachments?access_token='+str(PAGE_ACCESS_TOKEN) )
			data = req.json()
			log(data)
			furl = data["data"][0]['file_url']
			open("./ADM"+str(idb)+".txt", "a+").write( furl+ "\n")
			i = i+1
		except:
			i = 999999999999999
		
def log(message):
	print(message)
	sys.stdout.flush()

if __name__ == "__main__":
	app.run(debug = True, port = 80)