from flask import Flask, send_file, send_from_directory, request
from Souper import get_missing_img
from config.ConfReader import conf

app = Flask(__name__, static_url_path='/client/static')
app.debug = True


@app.route("/", methods=['GET'])
def index_route():
	return send_file('client/html/index.html')


@app.route("/about", methods=['GET'])
def about_route():
	return send_file('client/html/about.html')


@app.route("/filter", methods=['GET'])
def filter_route():
	return send_file('client/html/filter.html')


@app.route("/result", methods=['POST'])
def get_result_and_send_new_title():
	global m
	data = request.get_json()
	if data['init']:
		return m.get_next()
	else:
		m.set_result(data['res'])
		return m.get_next()


@app.route("/bill", methods=['POST'])
def get_a_bill():
	data = request.get_json()
	bill = bill_manager.parse_request(data)
	return bill.get_json()


@app.route("/missing", methods=['POST'])
def get_missing():
	data = request.get_json()
	if 'first' in data and 'last' in data:
		return get_missing_img(data['first'], data['last'])
	else:
		print('information missing from request')
		return ''

@app.route('/js/<path:path>')
def send_js(path):
	return send_from_directory('client/static/js', path)


@app.route('/css/<path:path>')
def send_css(path):
	return send_from_directory('client/static/css', path)


@app.route('/assets/<path:path>')
def send_asset(path):
	return send_from_directory('client/static/assets', path)


@app.route('/ca/', methods=['GET'])
def canadian_root():
	return send_file('client/html/ca/index.html')


app.run(port=conf.PORT)
