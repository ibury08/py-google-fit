from py_google_fit.GoogleFit import GoogleFit, GFitDataType


def test_count_total_steps():
    fit = GoogleFit('foo', 'bar')
    response = {
        'bucket': [
            {'dataset': [
                {'point': [
                    {'value': [{'intVal': 5}]},
                    {'value': [{'intVal': 2}]},
                ]},
            ]}
        ]}
    assert fit._count_total(GFitDataType.STEPS, response) == 7


def test_count_weight():
    fit = GoogleFit('foo', 'bar')
    response = {
        'bucket': [
            {'dataset': [
                {'point': [
                    {'value': [{'fpVal': 50.0}]},
                    {'value': [{'fpVal': 100.0}]},
                ]},
            ]}
        ]}
    assert fit._count_total(GFitDataType.WEIGHT, response) == 75.
