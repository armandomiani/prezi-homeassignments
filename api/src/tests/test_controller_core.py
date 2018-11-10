from boddle import boddle
import pytest

from exceptions import PreziException, ServerErrorException
import controllers as c
import main


def test_building_links():
    previous_link, next_link = c.build_paging_links(0, 10, '/resource', {
        'limit': 10
    })

    pos_previous_link = previous_link.find('offset=0')
    pos_next_link = next_link.find('offset=10')

    assert pos_next_link > 0
    assert pos_previous_link > 0


@pytest.mark.parametrize("params, expected", [
    ({'name': 'test'}, 'test'),
    ({}, 'no_exists')
])
def test_query_args(params, expected):
    with boddle(params=params, method='get'):
        param = c.get_query_arg('name', 'no_exists')
        assert param == expected


def test_get_pagination_params():
    params = {
        'limit': 10,
        'offset': 20
    }

    with boddle(params=params, method='get'):
        limit, offset = c.get_pagination_params()
        assert limit > 0
        assert offset > 0


def test_get_pagination_params_error():
    import pprint
    params = {
        'offset': 'a_string',
        'limit': 'a_string'
    }
    
    with boddle(params=params, method='get'):        
        with pytest.raises(PreziException) as e:            
            limit, offset = c.get_pagination_params()            
        assert e.value.status_code == 400


def test_abort():
    message = 'Error Message'
    result = c.abort(ServerErrorException(message))
    assert result['error']['message'] == '\'{}\''.format(message)


def test_envelope_paging():
    data = ['item1', 'item2']
    result = c.envelope_paging(
        data=data,
        count=len(data) * 5,
        offset=0,
        limit=10)
    assert result['paging']['page_count'] == len(data)
    assert result['paging']['total_count'] == 10


def test_main():
    result = main.index()
    assert result['version'] is not None
