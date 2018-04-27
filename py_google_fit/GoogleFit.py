from datetime import timedelta, datetime
from typing import List

import httplib2
from apiclient.discovery import build
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from enum import Enum


class GFitDataType(Enum):
    WEIGHT = 'com.google.weight'
    STEPS = 'com.google.step_count.delta'


class GoogleFit(object):
    """
    Manages the service to access your Google Fit account data.
    """

    _AUTH_SCOPES = ['https://www.googleapis.com/auth/fitness.body.read',
                    'https://www.googleapis.com/auth/fitness.activity.read',
                    'https://www.googleapis.com/auth/fitness.nutrition.read']

    _AGGREGATE_FUNCTIONS = {
        GFitDataType.STEPS: '_count_total_steps',
        GFitDataType.WEIGHT: '_average_weight',
    }

    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 auth_scopes: List[str] = _AUTH_SCOPES,
                 credentials_file: str = '.google_fit_credentials'):
        """

        :param client_id: Your google client id
        :param client_secret: Your google client secret
        :param auth_scopes: [optional] google auth scopes: https://developers.google.com/identity/protocols/googlescopes#fitnessv1
        :param credentials_file: [optional] path to credentials file
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._credentials_file = credentials_file
        self._auth_scopes = auth_scopes
        self._service = None

    def authenticate(self):
        """
        Authenticate and give access to google auth scopes. If no valid credentials file is found, a browser will open
        requesting access.
        """
        flow = OAuth2WebServerFlow(self._client_id, self._client_secret, self._auth_scopes)
        storage = Storage(self._credentials_file)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = tools.run_flow(flow, storage)
        http = httplib2.Http()
        http = credentials.authorize(http)
        self._service = build('fitness', 'v1', http=http)

    def _execute_aggregate_request(self, data_type, start_date: datetime, end_date: datetime):
        def to_epoch(dt: datetime) -> int:
            return int(dt.timestamp()) * 1000

        body = {
            "aggregateBy": [{"dataTypeName": data_type}],
            "endTimeMillis": str(to_epoch(end_date)),
            "startTimeMillis": str(to_epoch(start_date)),
        }
        return self._service.users().dataset().aggregate(userId='me', body=body).execute()

    @staticmethod
    def _count_total_steps(steps_response):
        cum = 0
        points = steps_response['bucket'][0]['dataset'][0]['point']
        if len(points) == 0:
            return 'no step data found'
        for _ in points:
            cum = cum + int(_['value'][0]['intVal'])
        return cum

    @staticmethod
    def _average_weight(weight_response):
        cum = 0
        points = weight_response['bucket'][0]['dataset'][0]['point']
        if len(points) == 0:
            return 'no weight data found'
        for _ in points:
            cum = cum + int(_['value'][0]['fpVal'])
        return cum / len(points)

    def _avg(self, data_type, begin, end):
        response = self._execute_aggregate_request(data_type, begin, end)
        return getattr(self, self._AGGREGATE_FUNCTIONS[data_type])(response)

    def average_today(self, data_type: GFitDataType):
        """
        :param data_type: A data type from GFitDataType
        :return: the average for the specified datatype for today up to now
        """
        begin_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_today = begin_today + timedelta(days=1)
        return self._avg(data_type, begin_today, end_today)

    def average_for_date(self, data_type: GFitDataType, dt: datetime):
        """
        This function will calculate the boundaries for the given date for you
        :param dt: A specific datetime
        :param data_type: A data type from GFitDataType
        :return: the average for the specified datatype for the given date
        """
        begin = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        end = begin + timedelta(days=1)
        return self._avg(data_type, begin, end)

    def rolling_daily_average(self, data_type: GFitDataType, n: int = 7):
        """
        Calculate the average over the last n days, excluding today
        :param data_type: A data type from GFitDataType
        :param n: The number of days to go back
        :return: The rolling average for the specified datatype
        """
        begin_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        begin_period = begin_today - timedelta(days=n)
        avg = self._avg(data_type, begin_period, begin_today)
        if data_type == self.STEPS:
            return avg / n
        else:
            return avg

    def average_for_n_days_ago(self, data_type: GFitDataType, n=1):
        """
        Wrapper around `average_for_date`. This will calculate the date for you, given a number of days to go back.
        Easy function to compare the steps for a specific day in the week.
        :param data_type: A data type from GFitDataType
        :param n: The number of days to go back
        :return: the average for the specified datatype
        """
        n_days_ago = datetime.now() - timedelta(days=n)
        return self.average_for_date(data_type, n_days_ago)
