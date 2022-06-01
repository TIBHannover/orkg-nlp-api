import datetime
import uuid

from orkgnlp.common.util.decorators import singleton
from orkgnlp.annotation import CSNer


class CSNerService:

    @singleton
    def __new__(cls):
        pass

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
