from flask import request, url_for,make_response
from flask import Flask,jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
import subprocess
import datetime
import time
import urllib
import logging
import os

app = Flask(__name__)

log=None
pid=[]
@app.route('/',methods =['GET','POST'])
def index():
    return make_response(jsonify({
                            "message": "Required field not specified",
                            "status": 500,
			    "Example":"curl -i -X POST --header \"AUTHTOKEN: kjhgfghj\" -H \"Content-Type: application/json\" -d \'{\"TO\":\"12345678098\",\"REMOTEIP\":\"192.168.1.41\",\"REMOTEPORT\":\"5060\",\"SIPPXML\":\"https://raw.githubusercontent.com/sipp_xml/master/sipp_uac_basic.xml\"}\' http://127.0.0.1:5000/Call/\""
                        }), 500)

@app.route('/Call/', methods =['POST'])
def MakeSIPPCall():
    AUTH = request.headers.get('AUTHTOKEN')
    content = request.get_json()
    app.logger.info("Got a Request for AUTH %s and content %s"%(AUTH,content))
    if AUTH is not None and AUTH=='chandra':
    	#START THE SIPP
    	TO = request.json.get('TO')
    	IP = request.json.get('REMOTEIP')
    	PORT = request.json.get('REMOTEPORT')
    	XMLPATH = request.json.get('SIPPXML')
	if TO is not None and IP is not None and PORT is not None and XMLPATH is not None:
		EXTRAAUGMENT = request.json.get('EXTRAAUGMENT')
		fname = XMLPATH.split('/')[-1]
		try:
			urllib.urlretrieve(XMLPATH, '/tmp/'+fname)
			app.logger.info("Downloaded file %s is store at /tmp/"%(XMLPATH))
		except Exception as e:
			app.logger.info("unable to download file %s"%(XMLPATH)) 
		command='sipp -sf /tmp/'+fname+' -s '+TO+' '+IP+':'+PORT+' -m 1'
		if EXTRAAUGMENT is not None:
			command=command+' '+EXTRAAUGMENT
		app.logger.info("Running command %s"%(command))
		try:
			now = datetime.datetime.now()
   			timeString = now.strftime("%Y-%m-%d %H:%M:%S")
			result_success = subprocess.call([command], shell=True)
			now = datetime.datetime.now()
   			timeString2 = now.strftime("%Y-%m-%d %H:%M:%S")
			app.logger.info("Functional SIPP Output is %s"%(result_success)) 
			return make_response(jsonify({"Message":"Call Started and End successfully","TriggerTime":timeString,"EndTime":timeString2}),200)
		except subprocess.CalledProcessError as e:
			return make_response(jsonify({"Message":"Call Started But Failed","CallResponse":e.returncode}),e.returncode)
    	else:
		return make_response(jsonify(Message='TO or REMOTEIP or REMOTEPORT or SIPPXML parameter is missing'),400)
		
    else:
	return make_response(jsonify({"Message":"Username or Password is wrong","Status":401}), 401)



@app.route('/Load/', methods =['POST'])
def BulkSIPPCall():
    AUTH = request.headers.get('AUTHTOKEN')
    content = request.get_json()
    app.logger.info("Got a Request for AUTH %s and content %s"%(AUTH,content))
    if AUTH is not None and AUTH=='chandra':
    	#START THE SIPP
    	TO = request.json.get('TO')
    	IP = request.json.get('REMOTEIP')
    	PORT = request.json.get('REMOTEPORT')
    	XMLPATH = request.json.get('SIPPXML')
	if TO is not None and IP is not None and PORT is not None and XMLPATH is not None:
		EXTRAAUGMENT = request.json.get('EXTRAAUGMENT')
		fname = XMLPATH.split('/')[-1]
		try:
			urllib.urlretrieve(XMLPATH, '/tmp/'+fname)
			app.logger.info("Downloaded file %s is store at /tmp/"%(XMLPATH))
		except Exception as e:
			app.logger.info("unable to download file %s"%(XMLPATH)) 
		command='sipp -sf /tmp/'+fname+' -s '+TO+' '+IP+':'+PORT
		if EXTRAAUGMENT is not None:
			command=command+' '+EXTRAAUGMENT
		app.logger.info("Running command %s"%(command))
		try:
			now = datetime.datetime.now()
   			timeString = now.strftime("%Y-%m-%d %H:%M:%S")
			global log
			log = open(IP+PORT, 'w')
			log.flush()
			result_success = subprocess.Popen([command], shell=True,universal_newlines = True, stderr=subprocess.STDOUT, stdout=log)
			app.logger.info("Load SIPP PID is %s"%(result_success.pid))
			global pid
			pid.append(result_success.pid)
			LoadURL='/Load/Stop/'+str(result_success.pid)
			app.logger.info("Load SIPP Output is %s"%(result_success)) 
			return make_response(jsonify({"Message":"Load Started Successfully","TriggerTime":timeString,"LoadURL":LoadURL}),202)
		except subprocess.CalledProcessError as e:
			return make_response(jsonify({"Message":"Call Started But Failed","CallResponse":e.returncode}),e.returncode)
    	else:
		return make_response(jsonify(Message='TO or REMOTEIP or REMOTEPORT or SIPPXML parameter is missing'),400)
		
    else:
	return make_response(jsonify({"Message":"Username or Password is wrong","Status":401}), 401)


@app.route('/Load/Output/', methods=['GET','POST'])
def Return_log():
    IP = request.json.get('REMOTEIP')
    PORT = request.json.get('REMOTEPORT')
    if IP is not None and PORT is not None:
    	return open(IP+PORT).read()
    else:
	return make_response(jsonify(Message='REMOTEIP and REMOTEPORT parameter is missing'),400) 

@app.route('/Load/Stop/<pid>', methods=['GET','POST'])
def StopLoad(pid):
    app.logger.info("Stoping SIPP PID %s"%(pid)) 
    if pid is not None:
	try:
		kill_string = 'kill -9 '+str(pid)
   		result_success = subprocess.check_output([kill_string], shell=True)
    		return make_response(jsonify({"Message":"Load Stopped with PID"}))
	except subprocess.CalledProcessError as e:	
    		return make_response(jsonify({"Message":"No Active Load Running with PID"}))


if __name__ == '__main__':
    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(format = logFormatStr, filename = "global.log", level=logging.DEBUG)
    formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')
    fileHandler = logging.FileHandler("summary.log")
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
    app.logger.addHandler(fileHandler)
    app.logger.addHandler(streamHandler)
    app.logger.info("Logging is set up.")
    app.run(host='0.0.0.0', port=5000, threaded=True)    
