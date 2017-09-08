from flask import Blueprint

aws_s3 = Blueprint('aws_s3', __name__, url_prefix='/upload')

@aws_s3.route('', methods=['GET'])
def get():
    print "came to route"
    return 'True'