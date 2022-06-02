import datetime
import uuid

from orkgnlp.clustering import PredicatesRecommender, BioassaysSemantifier
from orkgnlp.common.util.decorators import singleton


class PredicatesService:

    @singleton
    def __new__(cls):
        pass

    def __init__(self):
        self.recommender = PredicatesRecommender()

    def recommend(self, title: str, abstract: str):
        predicates = self.recommender(title, abstract)

        return {
            'timestamp': datetime.datetime.now(),
            'uuid': uuid.uuid4(),
            'predicates': predicates
        }


class BioassaysService:

    @singleton
    def __new__(cls):
        pass

    def __init__(self):
        self.semantifier = BioassaysSemantifier()

    def semantify(self, text: str):
        labels = self.semantifier(text)

        return {
            'timestamp': datetime.datetime.now(),
            'uuid': uuid.uuid4(),
            'labels': labels
        }
