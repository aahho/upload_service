import flask

def respond_with_item(statusCode, data, transformer):
    response = {}
    response['data'] = transformer.transform(data)

    response['notification'] = {}
    response['notification']['hint'] = "Response Sent"
    response['notification']['message'] = "Response sent successfully"
    response['notification']['responseCode'] = statusCode
    response['notification']['type'] = "Success"

    response = flask.jsonify(response)
    response.status_code = statusCode
    return response

def respond_with_success(statusCode, message, hint="Response Sent"):
    response = {}
    response['data'] = str(message)
    
    response['notification'] = {}
    response['notification']['hint'] = hint
    response['notification']['message'] = "Response sent successfully"
    response['notification']['responseCode'] = statusCode
    response['notification']['type'] = "Success"
    
    response = flask.jsonify(response)
    response.status_code = statusCode
    return response

def respond_with_error(statusCode, message, hint="Failed To Respond"):
    response = {}
    response['data'] = str(message)
    
    response['notification'] = {}
    response['notification']['hint'] = hint
    response['notification']['message'] = "Failed To Respond"
    response['notification']['responseCode'] = statusCode
    response['notification']['type'] = "Failed"
    
    response = flask.jsonify(response)
    response.status_code = statusCode
    return response

def respond_with_list(statusCode, data, hint="Response Sent"):
    response = {}
    response['data'] = data
    
    response['notification'] = {}
    response['notification']['hint'] = hint
    response['notification']['message'] = "Response sent successfully"
    response['notification']['responseCode'] = statusCode
    response['notification']['type'] = "Success"
    
    response = flask.jsonify(response)
    response.status_code = statusCode
    return response

def respond_with_transformed_list(statusCode, data, transformer):
    response = {}
    response['data'] = fetch_data_from_transformer(transformer, data)
    transformed = response['data']
    response['notification'] = {}
    response['notification']['hint'] = "Response Sent"
    response['notification']['message'] = "Response sent successfully"
    response['notification']['responseCode'] = statusCode
    response['notification']['type'] = "Success"
    
    response = flask.jsonify(response)
    response.status_code = statusCode
    return response, transformed

def respond_with_paginated_collection(request, statusCode, data, transformer):
    total_length = len(data)
    items = request.GET.get('items', '10')
    page = request.GET.get('page', '1')
    valid_page = total_length/int(items)

    if valid_page < int(page):
        page = 1

    if int(items) <= 0:
        items = 10

    if int(page) <= 0:
        page = 1     

    pages_possible = total_length/int(page)

    if not pages_possible:
        page = 1    

    url = 'http://' + request.META['HTTP_HOST'] + request.META['PATH_INFO'] + '?'

    meta = {}
    meta['total'] = total_length
    meta['count'] = total_length
    meta['current_page'] = page
    meta['per_page'] = items
    meta['next_link'] = ''
    meta['previous_link'] = ''

    paginator = Paginator(data, items)
    results = paginator.page(page)

    if results.has_next():
        if (total_length - int(items)) < int(items):
            new_items = total_length - int(items)
        else:
            new_items = items   
        new_page = int(page) + 1
        next_link =  url + 'items' + '=' + str(new_items) + '&' + 'page' + '=' + str(new_page)
        meta['next_link'] = next_link

    if results.has_previous:
        page = int(page) - 1
        if not page:
            page = 1
        previous_link =  url + 'items' + '=' + str(items) + '&' + 'page' + '=' + str(page)
        meta['previous_link'] = previous_link

    results = results.object_list

    response = {}
    response['data'] = fetch_data_from_transformer(transformer, results)
    response['meta'] = meta

    response = flask.jsonify(response)
    response.status_code = statusCode
    return response
    
def fetch_data_from_transformer(transformer, data):
    result = []
    for key, value in enumerate(data):
        result.append(transformer.transform(value))
    return result