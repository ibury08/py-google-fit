from flask import Flask
import os
#delete from here
import sys
from py_google_fit.GoogleFit import GFitDataType
from py_google_fit.GoogleFit import GoogleFit

app = Flask(__name__)

@app.route('/')
def hello_world():
	client_id = os.environ['client_id']
	client_secret = os.environ['client_secret']
	fit = GoogleFit(client_id, client_secret)
	fit.authenticate()
	#fit.authenticate should only store credentials on s3, no need to retrieve them.
	return fit.average_today(GFitDataType.STEPS)

if __name__ == '__main__':
    app.run()
