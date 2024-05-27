from flask import Flask, request, jsonify
import os
from flask_restful import Resource, Api
import pickle
import os,sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import easyocr
import logging
from werkzeug.utils import secure_filename
from PIL import Image
import requests
import numpy




logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)
ROOT = os.getcwd()
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'message':"Hi"}

class BillPredict(Resource):
    def post(self):
        data = request.get_json()
        url_image = data['image_url']
        image = Image.open(requests.get(url_image, stream=True).raw) # image object
        image = numpy.array(image) # pil2cv2 numpy array
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(image, detail=0)
        return {
            "result": result
        }
         
api.add_resource(HelloWorld,'/test')
api.add_resource(BillPredict,'/predict')
if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-port", type = str, default="1412", help="port")
    args = vars(parser.parse_args())
    app_port = args["port"]
    app.run(debug=True, host='0.0.0.0', port=app_port)