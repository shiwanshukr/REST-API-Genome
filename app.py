from flask import Flask, render_template, request, flash, url_for, jsonify, make_response, abort
from task import main_encode
from flask_restful import Resource, Api
import requests
from datetime import date
import json
app = Flask(__name__)
api = Api(app)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')

@app.route('/GO_ID', methods=['GET', 'POST'])
def calc():
    if request.method == "POST":
        id_value = request.form['ont_name']
        # get url that the user has entered
        id_value1 = id_value.replace(':', '_')
        url = 'https://www.ebi.ac.uk/ols/api/ontologies/go/terms?iri=http://purl.obolibrary.org/obo/'
        test_url = url + id_value1
        response = requests.get(test_url)
        if response.status_code >= 400:
            return render_template('error.html', output='Either something wrong with the ID format or the GO ID doesnot exist!')

        response = requests.get(test_url)
        json_data = response.json()['_embedded']['terms']

        detail_value = main_encode(json_data)


        return render_template('result.html', name=detail_value[0], description=detail_value[1],
                               synonyms=detail_value[2], dcr=detail_value[3].split('*'))

def makeJSON(id_value):
        # API request
        id_value1 = id_value.replace(':', '_')
        url = 'https://www.ebi.ac.uk/ols/api/ontologies/go/terms?iri=http://purl.obolibrary.org/obo/'
        test_url = url + id_value1
        response = requests.get(test_url)
        if response.status_code >= 400:
            return render_template('error.html',
                                   output='Either something wrong with the ID format or the GO ID doesnot exist!')

        response = requests.get(test_url)
        json_data = response.json()['_embedded']['terms']

        detail_value = main_encode(json_data)
        name = detail_value[0]
        description = detail_value[1]
        synonyms = detail_value[2]
        dcr = detail_value[3].split('*')

        return name, description, synonyms, dcr

class GenomeID(Resource):
    def get(self,id):
        try:
            name, description, synonyms,dcr = makeJSON(id)
            id_result = {'name':name,'description':description,'synonyms':synonyms,'data_base_cross_reference:':dcr}
            if len(id_result) == 0:
                return abort(400)
            return jsonify(id_result)
        except:
            error = {
                  "timestamp" : date.today(),
                  "status" : 404,
                  "error" : "Not Found",
                  "message" : "Resource not found"}

            return jsonify(message=error)

class ErrorGenome(Resource):
    def get(self):
        error = {
            "timestamp": date.today(),
            "status": 404,
            "error": "Not Found",
            "message": "Resource not found"}
        # return json.dumps(error, indent = 5)
        return make_response(render_template('error.html',output=error), 404)



api.add_resource(GenomeID,'/api/<string:id>')
api.add_resource(ErrorGenome,'/api/')


if __name__ == '__main__':
    app.run(debug=True)
