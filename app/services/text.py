# -*- coding: utf-8 -*-
from summarizer import Summarizer
from transformers import Pipeline, pipeline

from app.common.services.wrapper import ResponseWrapper
from app.services import OrkgNlpApiService


class SummarizerService(OrkgNlpApiService):
    _summarizer: Summarizer = None

    def __init__(self, summarizer: Summarizer):
        self.summarizer = summarizer

    def summarize(self, text, ratio):
        summary = self.summarizer(text, ratio=ratio)

        return ResponseWrapper.wrap_json({"summary": summary})

    @classmethod
    def get_summarizer(cls):
        if not cls._summarizer:
            cls._summarizer = Summarizer()

        return cls._summarizer


class ClassifierService(OrkgNlpApiService):
    _classifier: Pipeline = None

    def __init__(self, classifier: Pipeline):
        self.classifier = classifier

    def classify(self, sentence, labels):
        result = self.classifier(sentence, labels)

        return ResponseWrapper.wrap_json(result)

    @classmethod
    def get_classifier(cls):
        if not cls._classifier:
            cls._classifier = pipeline("zero-shot-classification")

        return cls._classifier
