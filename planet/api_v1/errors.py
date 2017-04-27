# -*- coding: utf-8 -*-

from flask import jsonify
from . import api
from ..errors import InvalidNameError, InvalidAssetTypeError, InvalidAssetClassError

class MethodNotAllowedError(Exception):
    pass

class ResourceExistsError(Exception):
    pass

@api.errorhandler(400)
def generic_invalid_error(e):
    response = jsonify({u'error': u'Your request was malformed.'})
    response.status_code = 400
    return response

@api.errorhandler(InvalidNameError)
def invalid_name_error(e):
    error_message = u"""The name you supplied is invalid. Valid names conform to the following conditions:
- They are globally unique
- They can only contain alphanumeric ascii characters, underscores, and dashes
- They cannot start with an underscore or dash
- They must be between 4 and 64 characters long"""
    response = jsonify({u'error': error_message})
    response.status_code = 400
    return response

@api.errorhandler(InvalidAssetTypeError)
def invalid_asset_type_error(e):
    error_message = u'The asset type you supplied is invalid.'
    response = jsonify({u'error': error_message})
    response.status_code = 400
    return response

@api.errorhandler(InvalidAssetClassError)
def invalid_asset_class_error(e):
    error_message = u'The asset class you supplied is invalid.'
    response = jsonify({u'error': error_message})
    response.status_code = 400
    return response

@api.errorhandler(ResourceExistsError)
def resource_exists_error(e):
    error_message = u'A resource with that name already exists, and editing existing resources is not allowed.'
    response = jsonify({u'error': error_message})
    response.status_code = 403
    return response

@api.errorhandler(404)
def resource_not_found(e):
    response = jsonify({'error': 'Resource not found.'})
    response.status_code = 404
    return response

@api.errorhandler(405)
def method_not_allowed(e):
    response = jsonify({'error': 'Method not allowed.'})
    response.status_code = 405
    return response

@api.errorhandler(500)
def generic_server_error(e):
    response = jsonify({'error': 'There was an error processing your request.'})
    response.status_code = 500
    return response

@api.errorhandler(Exception)
def programming_error(e):
    # This is a catch-all error; in production, we would log what happened.
    response = jsonify({'error': 'There was an error processing your request.'})
    response.status_code = 500
    return response
