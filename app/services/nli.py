# -*- coding: utf-8 -*-
from orkgnlp.nli import TemplatesRecommender

from app.common.services.wrapper import ResponseWrapper
from app.services import OrkgNlpApiService


class TemplatesService(OrkgNlpApiService):
    _recommender: TemplatesRecommender = None

    def __init__(self, recommender: TemplatesRecommender):
        self.recommender = recommender

    def recommend(self, title: str, abstract: str, top_n: int):
        templates = self.recommender(title, abstract, top_n)

        return ResponseWrapper.wrap_json({"templates": templates})

    @classmethod
    def get_recommender(cls):
        if not cls._recommender:
            cls._recommender = TemplatesRecommender()

        return cls._recommender
