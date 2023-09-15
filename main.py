from flask import Flask, request, jsonify, send_from_directory, render_template
from config.flask_config import AppConfig
from config.mongodb_config import MongoConnector
from controllers import events_controller as controller
from models.event_model import EventsModel
from flask_cors import CORS, cross_origin

app = Flask(__name__, template_folder='web')
cors = CORS(app, resource={r'/*': {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/modify_events/<string:id>', methods=["DELETE", "PATCH"])
def modifyEvents(id): 
    if request.method == "DELETE": 
        return controller.deleteEvent(id)
    elif request.method == "PATCH":
        requestBody = request.get_json()
        return controller.updateEvent(requestBody, id)
    else: 
        return "not yet implemented"

@app.route('/api/events', methods=["GET", "POST"])
def events():
    if request.method == "POST": 
        requestBody = request.get_json()
        return controller.insertEvent(requestBody)
    elif request.method == "GET":
        requestArgs = request.args
        return controller.getEvent(requestArgs)
    else: 
        return "not yet implemented"

@app.route('/api/health-check', methods=["GET"])
def healthCheck():
    return {"status": "Alive"}

# @app.route('/')
# def render_page():
#     return render_template('index.html')

@app.route('/web/')
def render_page_web():
    return render_template('index.html')

@app.route('/web/<path:name>')
def return_flutter_doc(name):

    datalist = str(name).split('/')
    DIR_NAME = "web"

    if len(datalist) > 1:
        for i in range(0, len(datalist) - 1):
            DIR_NAME += '/' + datalist[i]

    return send_from_directory(DIR_NAME, datalist[-1])

if __name__ == "__main__":
    app.run(AppConfig.host, AppConfig.port, True)


