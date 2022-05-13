import datetime
import uuid

from orkgnlp.clustering import PredicatesRecommender
from orkgnlp.util.decorators import singleton


@singleton
class PredicatesService:

    def __init__(self):
        self.recommender = PredicatesRecommender()

    def recommend(self, title: str, abstract: str):
        predicates = self.recommender.recommend(title, abstract)

        return {
            'timestamp': datetime.datetime.now(),
            'uuid': uuid.uuid4(),
            'predicates': predicates
        }
