from datetime import datetime

from flask import Blueprint, request, jsonify

from feature_requests.models import FeatureRequest

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    return 'from api'


@bp.route('/feature_requests', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def feature_request_resource():

    if request.method == 'GET':

        frs = FeatureRequest.query.all()

        frs = [fr.to_dict() for fr in frs]

        resp_data = {
            "featureRequests": frs
        }

        return jsonify(resp_data)

    if request.method == 'POST':

        data = request.get_json()

        # * Target date convert to datetime object before saving
        data['target_date'] = datetime.strptime(data['target_date'], '%Y-%m-%d')

        fr = FeatureRequest.save(**data)

        resp_data = {
            "message": "created",
            "featureRequestData": fr.to_dict()
        }

        return jsonify(resp_data), 201

    if request.method == 'PATCH':

        return 'PATCH'

    if request.method == 'DELETE':

        return 'DELETE'

@bp.route('/feature_requests/<id>')
def feature_request_resource_via_id(id):

    try:
        fr = FeatureRequest.query.get(id)
        resp_data = {
            "featureRequestData": fr.to_dict()
        }
        return jsonify(resp_data)

    except AttributeError:
        return jsonify({"message": "Feature Request not found"}), 404