class SummarizerMock:

    def __call__(self, body, ratio=None):
        return 'summarized body'

    @staticmethod
    def get_summarizer():
        return SummarizerMock()


class ClassifierMock:

    def __call__(self, *args, **kwargs):
        return {
            'labels': ['some_label'] * 10,
            'scores': [0.123] * 10,
            'sequence': 'same_input'
        }

    @staticmethod
    def get_classifier():
        return ClassifierMock()
