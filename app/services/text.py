# -*- coding: utf-8 -*-
import json
import os
from json.decoder import JSONDecodeError

import openai
from summarizer import Summarizer
from transformers import Pipeline, pipeline

from app.common.errors import OrkgNlpApiError
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


class ChatgptService(OrkgNlpApiService):
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY", "")
        openai.organization = os.getenv("OPENAI_ORGANIZATION", "")

        self.tasks = {
            "recommendComparisonProperties": {
                "systemPrompt": "A comparison is a tabular overview of literature, "
                "where in the rows properties of paper are compared. "
                "Your task is to recommend additional related properties based on "
                "the set of user provided properties. Provide maximum 5 properties.",
                "userPrompt": lambda placeholders: f"The existing properties are: "
                f"{', '.join([placeholders['properties'][key]['label'] for key in placeholders['properties']])}",
                "functions": [
                    {
                        "name": "getProperties",
                        "description": "Get a array of newly recommended comparison properties",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "comparisonProperties": {
                                    "type": "array",
                                    "description": "The new comparison property",
                                    "items": {
                                        "type": "string",
                                    },
                                },
                            },
                            "required": ["comparisonProperties"],
                        },
                    },
                ],
            },
            "recommendResearchProblem": {
                "systemPrompt": "A research problem contains a maximum of approximately 5 words "
                "to explain the research task or topic. Provide a list of maximum 5 research problem "
                "based on the title and abstract provided by the user.",
                "userPrompt": lambda placeholders: placeholders["paperTitle"],
                "functions": [
                    {
                        "name": "getResearchProblems",
                        "description": "Get a array of research problems",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "researchProblems": {
                                    "type": "array",
                                    "description": "The research problems",
                                    "items": {
                                        "type": "string",
                                    },
                                },
                            },
                            "required": ["researchProblems"],
                        },
                    },
                ],
            },
            "checkDescriptiveness": {
                "systemPrompt": "Is the user-provided comparison description descriptive enough? "
                "A description should explain at least the contents and objectives. "
                "Return in JSON, return 'isDescriptive' true or false for the descriptiveness, "
                "and 'reason' then add a brief explanation.",
                "userPrompt": lambda placeholders: placeholders["value"],
                "functions": [
                    {
                        "name": "getDescriptiveness",
                        "description": "Determine whether a provided description is descriptive enough",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "isDescriptive": {
                                    "type": "boolean",
                                    "description": "Whether the description is descriptive enough",
                                },
                                "explanation": {
                                    "type": "string",
                                    "description": "A brief one paragraph explanation explaining how "
                                    "the descriptiveness was determined",
                                },
                            },
                            "required": ["isDescriptive", "explanation"],
                        },
                    },
                ],
            },
        }

    def completion(
        self,
        task_name,
        placeholders,
        temperature=0.2,
    ):
        task = self.tasks.get(task_name)
        if task is None:
            raise OrkgNlpApiError(f"Task with name '{task_name}' does not exist", self.__class__)

        try:
            user_message = task["userPrompt"](placeholders)
        except KeyError as exception:
            raise OrkgNlpApiError(
                "The placeholder specification does not match the requirements", self.__class__
            ) from exception

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=temperature,
                messages=[
                    {"role": "system", "content": task["systemPrompt"]},
                    {"role": "user", "content": user_message},
                ],
                functions=task["functions"],
                function_call="auto",
            )

            return ResponseWrapper.wrap_json(
                {"arguments": json.loads(completion.choices[0].message.function_call.arguments)}
            )
        except openai.error.RateLimitError as exception:
            raise OrkgNlpApiError("OpenAI quota exceeded", self.__class__) from exception
        except JSONDecodeError as exception:
            raise OrkgNlpApiError(
                "Something went wrong with parsing the ChatGPT response in JSON", self.__class__
            ) from exception
