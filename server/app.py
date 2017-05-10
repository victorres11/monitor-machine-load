import os
from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder="../client")

@app.route('/')
def index():
    return render_template('uptime_alerts.html')

@app.route('/uptime_stats')
def uptime_stats():
	uptime_data = None
	with open('uptime_data.txt') as uptime_file:
		uptime_data = uptime_file.readlines()


	return jsonify({'uptime_messages': uptime_data})



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
