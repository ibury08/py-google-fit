from setuptools import setup

setup(
    name="py_google_fit",
    version="0.0.2",
    author="Tim van Cann",
    author_email="timvancann@gmail.com",
    description="Utility library to easily access your Google Fit data",
    url="https://github.com/timvancann/py-google-fit.git",
    packages=['py_google_fit', 'tests'],
    python_requires='>3.5.0',
    install_requires=[
        'google-api-python-client==1.6.6',
    ]
)
