class PredicatesRecommenderMock:

    def __call__(self, *args, **kwargs):
        return [
            {
                'id': 'some_id',
                'label': 'some_label'
            }
        ] * 10

    @staticmethod
    def get_recommender():
        return PredicatesRecommenderMock()


class BioAssaysSemantifierMock:

    def __call__(self, *args, **kwargs):
        resource = {
            'id': 'some_id',
            'label': 'some_label'
        }

        return [
            {
                'property': resource,
                'resources': [resource] * 10
            }
        ] * 10

    @staticmethod
    def get_semantifier():
        return BioAssaysSemantifierMock()
