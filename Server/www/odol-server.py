import os, random
from flask import Flask, Blueprint, render_template, url_for, jsonify
from gevent.wsgi import WSGIServer

import odol
from odol import *

data_path = odol.config.get('data', 'data_path')
logfile = os.path.join(data_path, "odol.Sensor.log")

app = Flask(__name__, static_folder=data_path)
app.register_blueprint(Blueprint('css', __name__, static_folder='templates/css'))
app.debug = True	

def create_image():
	global logfile
	draw = Draw.new(logfile)
	return draw.createImage()
	
@app.route('/')
def index():
	global data_path, logfile
	for column, data in enumerate(odol.Sensor.Sensor.load_logfile(logfile, max=1023)):
		message = data
	history = eval(open(os.path.join(data_path, 'history.txt'), 'r').read())
	return render_template('index.html', history=history, messages=message)

@app.route('/_get_image_src')
def _get_image_src():
	imglocation = create_image()
	imgsrc = url_for('static', filename=os.path.join("images", os.path.basename(imglocation)), ts=random.random())
	return jsonify(src=imgsrc)

	
if __name__ == '__main__':
	http_server = WSGIServer(('', 5000), app)
	http_server.serve_forever()