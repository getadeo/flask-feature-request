from datetime import datetime

from flask import Blueprint, request, jsonify

from feature_requests.models import FeatureRequest, db

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    return 'from api'


@bp.route('/feature_requests', methods=['GET', 'POST'])
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

    if request.method == 'DELETE':

        return 'DELETE'

@bp.route('/feature_requests/<id>', methods=['GET', 'PATCH', 'DELETE'])
def feature_request_resource_via_id(id):

    if request.method == 'GET':
        try:
            fr = FeatureRequest.query.get(id)
            resp_data = {
                "featureRequestData": fr.to_dict()
            }
            return jsonify(resp_data)

        except AttributeError:
            return jsonify({"message": "Feature Request not found"}), 404

    if request.method == 'PATCH':

        data = request.get_json()

        # * Target date convert to datetime object before saving
        data['target_date'] = datetime.strptime(data['target_date'], '%Y-%m-%d')

        # * Add ID to data
        data['id'] = id

        fr = FeatureRequest.edit(**data)

        if fr is None:
            return jsonify({"message": "Feature Request not found"}), 404

        resp_data = {
            "message": "updated",
            "featureRequestData": fr.to_dict()
        }

        return jsonify(resp_data), 200

    if request.method == 'DELETE':

        fr = FeatureRequest.query.filter_by(id=id).first()

        if fr is None:
            return jsonify({"message": "Feature Request not found"}), 404

        db.session.delete(fr)
        db.session.commit()

        return jsonify({"message": "deleted"})
