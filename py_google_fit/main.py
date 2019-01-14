import sys
import config
try:
	sys.path.insert(0,config.API_CONFIG['local_path'])
except:
	pass
from py_google_fit.GoogleFit import GFitDataType
from py_google_fit.GoogleFit import GoogleFit
client_id = config.API_CONFIG['client_id']
client_secret = config.API_CONFIG['client_secret']
fit = GoogleFit(client_id, client_secret)
fit.authenticate()
fit.average_by_hour_n_days_ago(GFitDataType.STEPS,0,0)