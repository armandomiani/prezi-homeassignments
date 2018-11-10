from bottle import Bottle
from models import Prezi
from exceptions import PreziException
from controllers import (
    get_pagination_params, abort, envelope_paging, get_query_arg)


api = Bottle()


@api.route('/', method='GET')
def list():
    """Endpoint for listing prezies"""
    try:
        limit, offset = get_pagination_params()
        title = get_query_arg('title')
        sort = get_query_arg('sort')

        prezies, prezies_count = Prezi.search(title, sort, offset, limit)

        return envelope_paging(
            data=[p.to_dict() for p in prezies],
            count=prezies_count,
            offset=offset,
            limit=limit
        )
    except PreziException as e:
        return abort(e)


@api.route('/<item_id>', method='GET')
def get(item_id):
    """Endpoint for getting a single prezi"""
    try:
        return Prezi.find_by_id(item_id).to_dict()
    except PreziException as e:
        return abort(e)
