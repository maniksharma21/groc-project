from binascii import Error
from socket import create_connection
from flask import Flask, request, jsonify, json
import product_dao
from backend import sales_dao, customers_dao
from backend.customers_dao import insert_customer
from sql_connection import get_sql_connection
from flask_cors import CORS  # To allow cross-origin requests

app = Flask(__name__)
CORS(app)
connection = get_sql_connection()


@app.route('/getproducts', methods=['GET'])
def get_all_products():
    products = product_dao.get_all_products(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


#below work all done by myself
@app.route('/getsales', methods=['GET'])
def show_sales():
    sales = sales_dao.show_sales(connection)
    response = jsonify(sales)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getsalesdetails', methods=['GET'])
def show_salesdetails():
    sales = sales_dao.show_salesdetails(connection)
    response = jsonify(sales)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = product_dao.insert_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    request_payload = request.get_json()
    product_dao.delete_product(connection, request_payload['product'])
    response = jsonify({'message': 'Product deleted successfully'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/orders', methods=['GET'])
def show_orders():
    products = sales_dao.show_orders(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/processSale', methods=['POST'])
def process_sale():
    request_payload = json.loads(request.form['data'])
    result = sales_dao.process_sale(connection, request_payload)
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/customers', methods=['GET'])
def get_customers():
    products = customers_dao.get_customers(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/addcustomer', methods=['POST'])
def insert_customer():
    request_payload = json.loads(request.form['data'])
    result = customers_dao.insert_customer(connection, request_payload)
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deletecustomer', methods=['POST'])
def delete_customer():
    request_payload = request.get_json()
    customers_dao.delete_customer(connection, request_payload['product'])
    response = jsonify({'message': 'customer deleted successfully'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    print("starting python server for groc")
    app.run(port=5000)
