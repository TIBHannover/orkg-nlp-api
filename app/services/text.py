import datetime
import uuid

from summarizer import Summarizer
from transformers import pipeline

from app.common.services.wrapper import ResponseWrapper
from app.services import OrkgNlpApiService


class TextService(OrkgNlpApiService):

    def __init__(self):
        self.summarizer = Summarizer()
        self.classifier = pipeline('zero-shot-classification')

    def summarize(self, text, ratio):
        summary = self.summarizer(text, ratio=ratio)

        return ResponseWrapper.wrap_json({'summary': summary})

    def classify(self, sentence, labels):
        result = self.classifier(sentence, labels)

        return ResponseWrapper.wrap_json(result)
