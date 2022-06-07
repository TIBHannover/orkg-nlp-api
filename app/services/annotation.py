import datetime
import uuid

from orkgnlp.annotation import CSNer

from app.services import OrkgNlpService


class CSNerService(OrkgNlpService):

    def __init__(self):
        self.annotator = CSNer()

    def annotate(self, title=None, abstract=None):
        annotations = {'title': [], 'abstract': []}

        if title and abstract:
            annotations.update(self.annotator(title=title, abstract=abstract))

        elif title:
            annotations['title'] = self.annotator(title=title)

        elif abstract:
            annotations['abstract'] = self.annotator(abstract=abstract)

        return {
            'timestamp': datetime.datetime.now(),
            'uuid': uuid.uuid4(),
            'annotations': annotations
        }
