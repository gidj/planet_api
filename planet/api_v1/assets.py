from flask import abort, current_app, jsonify, request, url_for
from flask.views import MethodView

from ..models import Asset
from errors import InvalidNameError, MethodNotAllowedError, \
        InvalidAssetTypeError, InvalidAssetClassError

from . import api

def get_urls_list():
    """ Return a list of tuples, each containing an api endpoint and a method
        that is allowed to access it. In a production scheme, we would also
        add documentation about other contraints. """
    FILTERED_METHODS = ('HEAD', 'OPTIONS',)
    domain = current_app.config.get('PREFERRED_URL_SCHEME', 'http') + '://' + \
            current_app.config.get('SERVER_NAME', 'localhost')
    urls = []
    for rule in current_app.url_map.iter_rules():
        if rule.endpoint != 'static':
            urls.append((domain + rule.rule, filter(lambda x: x not in FILTERED_METHODS, rule.methods)))
    return urls

@api.route('/')
def index():
    # Add links to all endpoints here, to aid in discoverability.
    urls_list = get_urls_list()
    json_body = {
        u'Description': u"This is the base directory of our API; see 'links' for valid endpoints and methods.",
        u'links': [
            {u'url':url, u'method': ', '.join(methods)} for url, methods in urls_list
        ],
    }
    return jsonify(json_body)

class AssetAPI(MethodView):
    def get(self, asset_name):
        """ If an asset_name is provided, ensure its name is valid and that it exists
            before serving it. If no asset_name, return a list of assets. """
        if asset_name is None:
            page = request.args.get('page', 1, type=int)
            asset_type = request.args.get('type', None)
            asset_class = request.args.get('class', None)

            query = Asset.query
            params = {}
            if asset_type is not None:
                if asset_type in Asset.VALID_TYPES:
                    query = query.filter_by(asset_type=asset_type)
                    params.update({'type':asset_type})
                else:
                    raise InvalidAssetTypeError
            if asset_class is not None:
                if asset_class in Asset.VALID_CLASSES:
                    query = query.filter_by(asset_class=asset_class)
                    params.update({'type':asset_class})
                else:
                    raise InvalidAssetClassError

            pagination = query.paginate(page, per_page=current_app.config['PAGE_SLICE'], error_out=False)

            if pagination.has_prev:
                previous_url = url_for('api.assets', page=page-1, _external=True, **params)
            else:
                previous_url = None

            if pagination.has_next:
                next_url = url_for('api.assets', page=page+1, _external=True, **params)
            else:
                next_url = None

            json_assets = {
                u'assets': [asset.to_json() for asset in pagination.items],
                u'previous': previous_url,
                u'next': next_url,
                u'total': pagination.total,
            }
            return jsonify(json_assets)

        else:
            if not Asset.valid_name(asset_name):
                raise InvalidNameError
            asset = Asset.query.filter_by(name=asset_name).first()
            if not asset:
                abort(404)
            return jsonify(asset.to_json())

    def post(self):
        asset = Asset.from_json(request.json)
        response = jsonify(asset.to_json())
        response.status_code = 201
        return response

    def delete(self, asset_name):
        raise MethodNotAllowedError

    def put(self, asset_name):
        raise MethodNotAllowedError


asset_view = AssetAPI.as_view('assets')
api.add_url_rule('/assets/', defaults={'asset_name': None}, view_func=asset_view, methods=['GET',])
api.add_url_rule('/assets/', view_func=asset_view, methods=['POST',])
api.add_url_rule('/assets/<asset_name>', view_func=asset_view, methods=['GET',])
