from flask import Flask, Blueprint, request, session, json, jsonify

cloud = Blueprint('cloud', __name__, template_folder='templates', url_prefix='/uploads')

@cloud.route('cloud', methods=['POST'])
def upload():
	pass