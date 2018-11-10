from boddle import boddle
import pytest

from controllers import prezies


@pytest.mark.parametrize("params", [
    ({'sort': 'utcCreatedAt'}),
    ({'sort': '-utcCreatedAt'}),
    ({'title': 'dolore'}),
    ({})
])
def test_list(params):
    with boddle(params=params, method='get'):
        result = prezies.list()
        assert len(result['data']) > 0


def test_list_error():
    with boddle(params={'limit': 'x'}, method='get'):
        result = prezies.list()
        assert {'error': {'message': "'No valid integer provided.'"}} == result


def test_get():
    with boddle(params={}, method='get'):
        result = prezies.list()
        prezi_id = result['data'][0]['id']
        result = prezies.get(prezi_id)
        assert result is not None


def test_get_error():
    with boddle(params={}, method='get'):
        result = prezies.get('xxx')
        assert {'error': {'message': "'Resource not found.'"}} == result
