from orkgnlp.clustering import PredicatesRecommender, BioassaysSemantifier

from app.common.services.wrapper import ResponseWrapper
from app.services import OrkgNlpApiService


class PredicatesService(OrkgNlpApiService):
    _recommender: PredicatesRecommender = None

    def __init__(self, recommender: PredicatesRecommender):
        self.recommender = recommender

    def recommend(self, title: str, abstract: str):
        predicates = self.recommender(title, abstract)

        return ResponseWrapper.wrap_json({'predicates': predicates})

    @classmethod
    def get_recommender(cls):
        if not cls._recommender:
            cls._recommender = PredicatesRecommender()

        return cls._recommender


class BioassaysService(OrkgNlpApiService):
    _semantifier: BioassaysSemantifier = None

    def __init__(self, semantifier: BioassaysSemantifier):
        self.semantifier = semantifier

    def semantify(self, text: str):
        labels = self.semantifier(text)

        return ResponseWrapper.wrap_json({'labels': labels})

    @classmethod
    def get_semantifier(cls):
        if not cls._semantifier:
            cls._semantifier = BioassaysSemantifier()

        return cls._semantifier
