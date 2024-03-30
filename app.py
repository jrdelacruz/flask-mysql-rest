
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL
from werkzeug.exceptions import HTTPException

# Load environment variables from .env file
load_dotenv()

# Flask app configuration
app = Flask(__name__)

from config import Config
app.config.from_object(Config)

## Initialize CORS
CORS(app, resources={r"/rest/*": {"origins": [app.config['ALLOWED_DOMAINS']]}})

## Initialize MySQL
mysql = MySQL(app)

## Error handler
@app.errorhandler(Exception)
def handle_error(e):
    message = "An error occurred"
    code = 500
    data = e

    if isinstance(e, HTTPException):
        data = e.name
        code = e.code
        message = e.description
    if isinstance(e, KeyError):
        data = str(e).strip("'")
        code = 400
        message = str(e).strip("'") + " field is required"
    return jsonify(status=code,data=data,message=message), code

# Execute SQL query and return results
def execute_query(sql, params=None):
    cur = mysql.connection.cursor(dictionary=True)
    if params:
        cur.execute(sql, params)
    else:
        cur.execute(sql)
    mysql.connection.commit()
    if sql.strip().lower().startswith('select'):
        result = cur.fetchall()
    else:
        result = {'message': 'Query executed successfully'}
    cur.close()
    return result

# Custom query endpoint
@app.route('/rest/query', methods=['POST'])
def custom_query():
    data = request.json
    if 'query' not in data:
        response = {'status': 400, 'message': 'Please provide a query in the JSON data'}
        return jsonify(response), 400
    sql = data['query']
    result = execute_query(sql)
    response = {'data': result, 'status': 200, 'message': 'Custom query executed successfully'}
    return jsonify(response), 200

# Create a new record
@app.route('/rest/query/<table>', methods=['POST'])
def add_record(table):
    data = request.json
    fields = ', '.join(data.keys())
    values_template = ', '.join(['%s'] * len(data))
    sql = f"INSERT INTO {table} ({fields}) VALUES ({values_template})"
    params = tuple(data.values())
    execute_query(sql, params)
    response = {'data': data, 'status': 201, 'message': 'Record created successfully'}
    return jsonify(response), 201

# Retrieve records
@app.route('/rest/query/<table>', methods=['GET'])
def get_records(table):
    sql = f"SELECT * FROM {table}"
    records = execute_query(sql)
    response = {'data': records, 'status': 200, 'message': 'Records retrieved successfully'}
    return jsonify(response), 200

# Retrieve a single record
@app.route('/rest/query/<table>/<field>/<value>', methods=['GET'])
def get_record(table, field, value):
    sql = f"SELECT * FROM {table} WHERE {field} = %s"
    record = execute_query(sql, (value,))
    if record:
        response = {'data': record, 'status': 200, 'message': 'Record retrieved successfully'}
        return jsonify(response), 200
    else:
        response = {'status': 404, 'message': 'Record not found'}
        return jsonify(response), 404
    
# Update a record
@app.route('/api/<table>/<field>/<value>', methods=['PUT'])
def update_record(table, field, value):
    data = request.json
    fields = ', '.join([f"{key} = %s" for key in data.keys()])
    sql = f"UPDATE {table} SET {fields} WHERE {field} = %s"
    params = tuple(data.values()) + (value,)
    execute_query(sql, params)
    response = {'status': 200, 'message': 'Record updated successfully'}
    return jsonify(response), 200

# Delete a record
@app.route('/api/<table>/<field>/<value>', methods=['DELETE'])
def delete_record(table, field, value):
    sql = f"DELETE FROM {table} WHERE {field} = %s"
    execute_query(sql, (value,))
    response = {'status': 200, 'message': 'Record deleted successfully'}
    return jsonify(response), 200

@app.route('/')
def hello_world():
    return jsonify({"message": "Hello, World!"})

if __name__ == "__main__":
    app.run(port=app.config['SERVER_PORT'], debug=app.config['DEBUG'])

