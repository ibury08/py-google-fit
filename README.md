# py_google_fit

A convenience package for accessing your Google Fit data. It wraps the google python into a few function to easy access your data. This library is witting with read-only intention in mind. There are no helper functions to write to your Google Fit data.

## Getting started
Clone this repo and install it into your python environment

```bash
git clone ...
cd py-google-fit && python setup.py install
```

## Authentication
Start by creating an instance of the `GoogleFit` object:

```python
from py_google_fit.GoogleFit import GoogleFit
fit = GoogleFit(client_id, client_secret)
```
Fill in your own `client_id` and `client_secret`, create them in your [Google developer console](https://console.developers.google.com/apis/credentials)

To authenticate, call the authenticate function:
```python
fit.authenticate()
```
By default it will request read access to three [google fit scopes](https://developers.google.com/identity/protocols/googlescopes#fitnessv1) of your account: `body`, `activity` and `nutrition`.
If you haven't ran this function before. A browser will open asking you to give access.

## Getting your data
To get your stepcount for today up till now:

```python
from py_google_fit.GoogleFit import GFitDataType
fit.average_today(GFitDataType.STEPS)
```

And similar for your weight:
```python
fit.average_today(GFitDataType.WEIGHT)
```

To get some trend data, a rolling average is usually a good metric:
```python
fit.rolling_daily_average(GFitDataType.STEPS, n=14)
```