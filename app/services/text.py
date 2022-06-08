import datetime
import uuid

from summarizer import Summarizer

from app.services import OrkgNlpApiService


class TextService(OrkgNlpApiService):

    def __init__(self):
        self.summarizer = Summarizer()

    def summarize(self, text, ratio):
        summary = self.summarizer(text, ratio=ratio)

        return {
            'timestamp': datetime.datetime.now(),
            'uuid': uuid.uuid4(),
            'summary': summary
        }
