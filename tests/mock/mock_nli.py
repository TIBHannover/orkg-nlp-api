# -*- coding: utf-8 -*-
class TemplatesRecommenderMock:
    def __call__(self, *args, **kwargs):
        return [{"id": "some_id", "label": "some_label", "score": 0.99}] * 10

    @staticmethod
    def get_recommender():
        return TemplatesRecommenderMock()
