from controllers import prezies

import bottle

api = application = bottle.Bottle()
bottle.debug(True)
resources = [
    {'e': '/prezies', 'a': prezies.api}
]
[api.mount(r['e'], r['a']) for r in resources]


@api.route('/')
def index():
    return {
        "title": "Prezi Exam API!",
        "version": "0.0.x!",
        "resources": [r['e'] for r in resources]
    }
