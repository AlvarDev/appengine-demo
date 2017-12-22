import  logging
import  flask_cors
import  google.auth.transport.requests
import  google.oauth2.id_token
import  json as js
from    flask import Flask, jsonify, request

HTTP_REQUEST = google.auth.transport.requests.Request()
app = Flask(__name__)
flask_cors.CORS(app)

@app.route('/gifs', methods=['GET'])
def cpf():
    return jsonify(success=True, message="This is a message from App Engine Flexible"), 200




@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return jsonify(success=False, message='Internal Error'), 500

@app.errorhandler(404)
def server_error(e):
    logging.exception('Endpoint not found.')
    return jsonify(success=False, message='Not found'), 404

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]
