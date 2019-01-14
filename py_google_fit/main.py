import sys
import config
try:
	sys.path.insert(0,os.environ.API_CONFIG['local_path'])
except:
	pass
from py_google_fit.GoogleFit import GFitDataType
from py_google_fit.GoogleFit import GoogleFit
client_id = os.environ['client_id']
client_secret = os.environ['client_secret']
fit = GoogleFit(client_id, client_secret)
fit.authenticate()
fit.average_by_hour_n_days_ago(GFitDataType.STEPS,0,0)