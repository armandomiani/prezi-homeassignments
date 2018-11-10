from exceptions import BadRequestException
from bottle import request, response
from urllib.parse import urlencode, quote_plus
import logging


DEFAULT_ROWS_PER_PAGE = 30
NON_VALID_INTEGER_MESSAGE = 'No valid integer provided.'


def get_query_arg(arg, default_value=None):
    """Return a querystring parameter. 
    If no arg is found the default_value is returned."""
    if arg not in request.params:
        return default_value
    return request.params[arg]


def get_pagination_params():
    """Return a tuple with limit and offset querystrings.
    If some arg is not found, returns the default parameters
    """
    try:
        limit = int(get_query_arg('limit', DEFAULT_ROWS_PER_PAGE))
        offset = int(get_query_arg('offset', 0))
        return (limit, offset)
    except ValueError as e:
        logging.warning(e)
        raise BadRequestException(NON_VALID_INTEGER_MESSAGE)


def abort(exception):
    """Return the proper http status code based on the exception received"""
    response.status = exception.status_code
    return {
        'error': {'message': str(exception)}
    }


def envelope_paging(data, count, offset, limit):
    """Return a default response for paginations"""
    previous_link, next_link = build_paging_links(
        offset, limit, path=request.fullpath, params=dict(request.query))

    return {
        'data': data,
        'paging': {
            'total_count': count,
            'page_count': len(data),
            'previous': previous_link,
            'next': next_link
        }
    }


def build_paging_links(offset, limit, path, params={}):
    """Return the pagination links based on current page"""
    next_offset = offset + limit
    previous_offset = offset - limit if offset > limit else 0

    next_link = __build_paging_link(next_offset, limit, path, params.copy())
    previous_link = __build_paging_link(
        previous_offset, limit, path, params.copy())

    return previous_link, next_link


def __build_paging_link(offset, limit, path, params):
    """Return a single pagination link"""
    params['offset'] = offset
    return '{}?{}'.format(
        path, urlencode(params, quote_via=quote_plus))
