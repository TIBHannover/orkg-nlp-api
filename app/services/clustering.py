from orkgnlp.clustering import PredicatesRecommender, BioassaysSemantifier

from app.common.services.wrapper import ResponseWrapper
from app.services import OrkgNlpApiService


class PredicatesService(OrkgNlpApiService):

    def __init__(self):
        self.recommender = PredicatesRecommender()

    def recommend(self, title: str, abstract: str):
        predicates = self.recommender(title, abstract)

        return ResponseWrapper.wrap_json({'predicates': predicates})


class BioassaysService(OrkgNlpApiService):

    def __init__(self):
        self.semantifier = BioassaysSemantifier()

    def semantify(self, text: str):
        labels = self.semantifier(text)

        return ResponseWrapper.wrap_json({'labels': labels})
