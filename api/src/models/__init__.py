from exceptions import ResourceNotFoundException
import mongoengine as mdb
import datetime
import os


API_DB_HOST = os.environ['API_DB_HOST']


class ModelExtension(object):
    EXPORTABLE = []
    ID_ATTRIBUTE = 'id'

    def to_dict(self):
        result = {}
        for exp in self.EXPORTABLE:
            label = exp
            target = exp

            if type(exp) is dict:
                label = exp['label']
                target = exp['value']

            v = getattr(self, target)
            if type(v) == str:
                result[label] = v
            elif type(v) == datetime.datetime:
                result[label] = v.isoformat()
            else:
                if hasattr(v, 'to_dict'):
                    result[label] = v.to_dict()
        return result

    @classmethod
    def find_by_id(self, id):
        result = self.objects(**{
            self.ID_ATTRIBUTE: id
        })
        if result:
            return result[0]
        else:
            raise ResourceNotFoundException("Resource not found.")


class Creator(mdb.EmbeddedDocument, ModelExtension):
    name = mdb.StringField(required=True)

    EXPORTABLE = ['name']


class Prezi(mdb.Document, ModelExtension):
    meta = {'collection': 'prezies'}
    picture = mdb.StringField(required=True)
    title = mdb.StringField(required=True)
    createdAt = mdb.StringField(required=True)
    utcCreatedAt = mdb.DateTimeField(required=True)
    creator = mdb.EmbeddedDocumentField(Creator)
    prezi_id = mdb.StringField(required=True)

    EXPORTABLE = [
        'title',
        'picture',
        'utcCreatedAt',
        'creator',
        {'label': 'id', 'value': 'prezi_id'}
    ]
    ID_ATTRIBUTE = 'prezi_id'
    DEFAULT_SORTING = '-utcCreatedAt'

    @classmethod
    def search(self, title='', sort=DEFAULT_SORTING, offset=0, limit=0):
        sorting = Prezi.build_sorting_according_parameters(title, sort)
        query_command = Prezi.get_query_command(title, sorting)

        data = [p for p in query_command(title).limit(limit).skip(offset)]
        count = query_command(title).count()

        return data, count

    @classmethod
    def build_sorting_according_parameters(self, title, sort):
        if sort:
            return sort
        if title and not sort:
            return '$text_score'
        return self.DEFAULT_SORTING

    @classmethod
    def get_query_command(self, title, sort):
        if title:
            return lambda x: Prezi.objects.search_text(x).order_by(sort)
        else:
            return lambda x: Prezi.objects().order_by(sort)


db_params = {
    'host': 'mongodb://{}/prezi'.format(API_DB_HOST),
    'maxpoolsize': 1
}
mdb.register_connection('default', **db_params)
