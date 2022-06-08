import datetime
import uuid

from orkgnlp.clustering import PredicatesRecommender, BioassaysSemantifier

from app.services import OrkgNlpApiService


class PredicatesService(OrkgNlpApiService):

    def __init__(self):
        self.recommender = PredicatesRecommender()

    def recommend(self, title: str, abstract: str):
        predicates = self.recommender(title, abstract)

        return {
            'timestamp': datetime.datetime.now(),
            'uuid': uuid.uuid4(),
            'predicates': predicates
        }


class BioassaysService(OrkgNlpApiService):

    def __init__(self):
        self.semantifier = BioassaysSemantifier()

    def semantify(self, text: str):
        labels = self.semantifier(text)

        return {
            'timestamp': datetime.datetime.now(),
            'uuid': uuid.uuid4(),
            'labels': labels
        }
