import flask

def http_response(self, status_code, data, message='Success', type='success'):
    response = {}
    response = flask.jsonify({
            'notification': {
            'hint':'Reponse Sent', 
            'message':message, 
            'aahho_code':'SE-'+str(status_code), 
            'type':type
            }, 
            'data': data
        })
    response.status_code = status_code
    return response