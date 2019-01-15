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
	return average_by_hour_n_days_ago(GFitDataType.STEPS,1,0)

if __name__ == '__main__':
    app.run()
