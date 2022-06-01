import datetime
import uuid

from orkgnlp.clustering import PredicatesRecommender, BioassaysSemantifier
from orkgnlp.common.util.decorators import singleton


@singleton
class PredicatesService:

    def __init__(self):
        self.recommender = PredicatesRecommender()

    def recommend(self, title: str, abstract: str):
        predicates = self.recommender(title, abstract)

        return {
            'timestamp': datetime.datetime.now(),
            'uuid': uuid.uuid4(),
            'predicates': predicates
        }


@singleton
class BioassaysService:

    def __init__(self):
        self.semantifier = BioassaysSemantifier()

    def semantify(self, text: str):
        labels = self.semantifier(text)

        return {
            'timestamp': datetime.datetime.now(),
            'uuid': uuid.uuid4(),
            'labels': labels
        }
