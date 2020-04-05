from flask import request
from api.BioguideImageScraper import get_missing_img


def missing_routes(app):
    @app.route("/missing", methods=['POST'])
    def get_missing():
        data = request.get_json()
        if 'first' in data and 'last' in data:
            return get_missing_img(data['first'], data['last'])
        else:
            print('information missing from request')
            return ''