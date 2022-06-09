from summarizer import Summarizer
from transformers import pipeline

from app.common.services.wrapper import ResponseWrapper
from app.services import OrkgNlpApiService


class SummarizerService(OrkgNlpApiService):

    def __init__(self):
        self.summarizer = Summarizer()

    def summarize(self, text, ratio):
        summary = self.summarizer(text, ratio=ratio)

        return ResponseWrapper.wrap_json({'summary': summary})


class ClassifierService(OrkgNlpApiService):

    def __init__(self):
        self.classifier = pipeline('zero-shot-classification')

    def classify(self, sentence, labels):
        result = self.classifier(sentence, labels)

        return ResponseWrapper.wrap_json(result)
