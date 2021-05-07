import json
import time

from flask import Flask, request
import requests

from my_log import config_logger
from utils import get_data_for_recommend, get_response

WORKER_URL = 'http://localhost:5000'

# Initialize app
app = Flask(__name__)

# Initialize logger
logger = config_logger('driver')


@app.route('/recommend_by_customer_id', methods=['POST'])
def recommend_by_customer_id():
    """
    Load information from db and call worker to recommend portfolio for the customer.

    @args:
        customer_id (str): customer id

    @returns:
        recommended portfolio
    """
    customer_id = request.args.get('customer_id')

    if customer_id:
        headers = {
            'Content-type': 'application/json',
        }

        # Prepare data for 3rd party API (Load data from sqlite db).
        logger.info('Start to prepare data')
        time_start = time.time()
        data = get_data_for_recommend(customer_id, logger)
        spent_time = time.time() - time_start
        logger.info('End preparing data, spend %s secs' % str(spent_time))

        try:
            # ------ Call 3rd party API. ----- #
            r = requests.post(WORKER_URL + '/portfolio/recommend',
                              headers=headers,
                              data=json.dumps(data))

            res = r.json()
            # -------------------------------- #

            # Make response according to response from 3rd party API.
            if res['status_code'] == '1313':
                return get_response('[Success] Finish recommend process.', '200')
            else:
                return get_response('[Error] MLaaS internal error.', '500')
        except requests.exceptions.RequestException as e:
            logger.error(e)
            return get_response('[Error] MLaaS internal error.', '500')
    else:
        return get_response('[Error] Customer ID not specified.', '401')


if __name__ == '__main__':
    app.run(debug=True, port=5100)
    logger.info('Server is running..')
