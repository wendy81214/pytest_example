import json

import pytest
import requests

from api import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.mark.parametrize('api_query, worker_status_code, api_status_code, api_status',
                         [({'customer_id': 1}, '1313', '200', '[Success] Finish recommend process.'),
                          ({'customer_id': 1}, '500', '500', '[Error] MLaaS internal error.'),
                          ({}, '1313', '401', '[Error] Customer ID not specified.'),
                          ({}, '500', '401', '[Error] Customer ID not specified.')])
def test_recommend_by_customer_id(mocker, app, client,
                                  api_query,
                                  worker_status_code,
                                  api_status_code,
                                  api_status):
    # === patch get_data_for_recommend ===
    mocker.patch('api.get_data_for_recommend', return_value=dict())

    # === patch requests.post ===
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    mocker.patch('api.requests.post',
                 return_value=MockResponse({'status_code': worker_status_code,
                                            'status': 'ok'},
                                           200))
    res = client.post('/recommend_by_customer_id', query_string=api_query)
    assert res.status_code == 200
    assert json.loads(res.get_data(as_text=True))['status_code'] == api_status_code
    assert json.loads(res.get_data(as_text=True))['status'] == api_status


@pytest.mark.parametrize('api_query, worker_status_code, api_status_code, api_status',
                         [({'customer_id': 1}, '1313', '500', '[Error] MLaaS internal error.'),
                          ({'customer_id': 1}, '500', '500', '[Error] MLaaS internal error.'),
                          ({}, '1313', '401', '[Error] Customer ID not specified.'),
                          ({}, '500', '401', '[Error] Customer ID not specified.')])
def test_recommend_by_customer_id_exception(mocker, app, client,
                                            api_query,
                                            worker_status_code,
                                            api_status_code,
                                            api_status):
    # === patch get_data_for_recommend ===
    mocker.patch('api.get_data_for_recommend', return_value=dict())

    # === patch api.requests.post with HTTPError ===
    mocker.patch('api.requests.post',
                 side_effect=requests.exceptions.HTTPError())

    res = client.post('/recommend_by_customer_id', query_string=api_query)
    assert res.status_code == 200
    assert json.loads(res.get_data(as_text=True))['status_code'] == api_status_code
    assert json.loads(res.get_data(as_text=True))['status'] == api_status
