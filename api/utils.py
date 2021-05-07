import json
import sqlite3

from flask import make_response


def get_conn():
    conn = sqlite3.connect('./testDB.db')
    return conn


def get_data_for_recommend(customer_id, logger):
    """
    Load customer data from sqlite db.

    @args:
        customer_id: (str), customer ID.

    @return:
        data: (dictionary), customer data.
    """
    try:
        with get_conn() as conn:
            sql = f"""
                    SELECT product_code
                    FROM cm_cust_product_code
                    WHERE customer_id = '{customer_id}'
                   """
            cur = conn.cursor()
            cur.execute(sql)
            product_code = cur.fetchone()[0]
    except Exception as e:
        logger.error('Failed to load data from sqlite db, {}'.format(e))
        raise e
    finally:
        if conn:
            conn.close()

    # --- some logical decision. --- #
    if product_code == 'BNDF':
        cust_type = '00'
    else:
        cust_type = '01'
    # ------------------------------ #

    data = {
            'id': customer_id,
            'product_codes': product_code,
            'cust_type': cust_type
           }

    return data


def get_response(status, status_code, data=None):
    """
    Make response according to status, status_code.

    @args:
        status: (str), Description of status.
        status_code: (str), User defined status_code.
        data: (json), Returned data.

    @return:
        resp: Flask response.
    """
    resp_dict = dict()
    resp_dict['status'] = status
    resp_dict['status_code'] = status_code
    if data is not None:
        resp_dict['data'] = data

    resp = make_response(
        json.dumps(resp_dict),
        200,
    )
    resp.mimetype = 'application/json'
    return resp
