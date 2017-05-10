import os
import logging
import logging.config
from flask import Flask, request, jsonify, render_template, session

app = Flask(__name__, template_folder="../client")

@app.route('/')
def index():
    return render_template('uptime_alerts.html')	

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
