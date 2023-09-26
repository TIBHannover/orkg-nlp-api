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
        openai.organization = os.getenv("OPENAI_ORGANIZATION_ID", "")

        self.tasks = {
            "recommendProperties": {
                "systemPrompt": "You are an assistant for building a knowledge graph for science. "
                "Your task is to recommend additional related predicates based on "
                "the set of existing predicates. Recommend a list maximum 5 additional predicates.",
                "userPrompt": lambda placeholders: f"The existing predicates are: "
                f"{', '.join(placeholders['properties'])}",
                "functions": [
                    {
                        "name": "getProperties",
                        "description": "The array of additionally recommended properties",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "properties": {
                                    "type": "array",
                                    "description": "The recommended properties",
                                    "items": {
                                        "type": "string",
                                    },
                                },
                            },
                            "required": ["properties"],
                        },
                    },
                ],
            },
            "recommendResearchProblems": {
                "systemPrompt": "A research problem contains a maximum of approximately 4 words "
                "to explain the research task or topic of a paper. Provide a list of maximum 5 research problems "
                "based on the title and optionally abstract provided by the user.",
                "userPrompt": lambda placeholders: placeholders["paperTitle"]
                + " "
                + placeholders["abstract"],
                "functions": [
                    {
                        "name": "getResearchProblems",
                        "description": "Get a array of research problems",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "values": {
                                    "type": "array",
                                    "description": "The research problems",
                                    "items": {
                                        "type": "string",
                                    },
                                },
                            },
                            "required": ["values"],
                        },
                    },
                ],
            },
            "recommendMethods": {
                "systemPrompt": "Extract a list of maximum 5 methods from a scientific paper "
                "based on the title and optionally abstract provided by the user. "
                "if no methods are found, return an empty array.",
                "userPrompt": lambda placeholders: placeholders["paperTitle"]
                + " "
                + placeholders["abstract"],
                "functions": [
                    {
                        "name": "getMethods",
                        "description": "Get a array of methods",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "values": {
                                    "type": "array",
                                    "description": "The methods",
                                    "items": {
                                        "type": "string",
                                    },
                                },
                            },
                            "required": ["values"],
                        },
                    },
                ],
            },
            "recommendMaterials": {
                "systemPrompt": "Extract a list of maximum 5 materials that are used in a scientific paper."
                "Extract it from the title and optionally abstract provided by the user. "
                "if no materials are found, return an empty array.",
                "userPrompt": lambda placeholders: placeholders["paperTitle"]
                + " "
                + placeholders["abstract"],
                "functions": [
                    {
                        "name": "getMaterials",
                        "description": "Get a array of materials",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "values": {
                                    "type": "array",
                                    "description": "The materials",
                                    "items": {
                                        "type": "string",
                                    },
                                },
                            },
                            "required": ["values"],
                        },
                    },
                ],
            },
            "checkDescriptiveness": {
                "systemPrompt": "Provide feedback to a user on how to improve a provided description text. The "
                "description text should give information about the objectives and topics of a scientific "
                "tabular related work overview. ",
                "userPrompt": lambda placeholders: placeholders["value"],
                "functions": [
                    {
                        "name": "getFeedback",
                        "description": "Get feedback for the provided description",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "feedback": {
                                    "type": "string",
                                    "description": "The feedback for the provided description",
                                },
                            },
                            "required": ["feedback"],
                        },
                    },
                ],
            },
            "checkResourceDestructuring": {
                "systemPrompt": "You are an assistant for building a knowledge graph for science. Provide advice on if "
                "and how to decompose a provided resource label into separate resources. Only provide feedback is "
                "decomposing makes sense. Return the feedback in JSON.",
                "userPrompt": lambda placeholders: placeholders["label"],
                "functions": [
                    {
                        "name": "provideDecomposeFeedback",
                        "description": "Provide feedback on how a resource label can be decomposed",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "feedback": {
                                    "type": "string",
                                    "description": "A brief one paragraph explanation explaining how "
                                    "the resource can be decomposed",
                                },
                            },
                            "required": ["feedback"],
                        },
                    },
                ],
            },
            "checkIfLiteralTypeIsCorrect": {
                "systemPrompt": "You are an assistant in building a knowledge graph for science. You task is to advice "
                "users whether they should use a RDF resource or RDF literal. Based on a user-provided label, advice "
                "whether the type should be 'literal' or 'resource'. Literals are generally larger pieces of text and "
                "are not reusable, resource are atomic and can be reused. Return in JSON.",
                "userPrompt": lambda placeholders: placeholders["label"],
                "functions": [
                    {
                        "name": "getFeedback",
                        "description": "Provide feedback on whether the label should be a 'literal' or 'resource'",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "feedback": {
                                    "type": "string",
                                    "description": "Brief one paragraph explanation why the type should be literal or "
                                    "resource",
                                },
                            },
                            "required": ["feedback"],
                        },
                    },
                ],
            },
            "checkPropertyLabelGuidelines": {
                "systemPrompt": "You are an assistant in building a knowledge graph for science. Provide feedback "
                "whether the provided predicate label is generic enough to make it reusable in the graph and explain "
                "how to make it more generic. Examples of properties that are not reusable: population in Berlin "
                "(because it contains a location), temperature in degrees Celsius (because it contains a unit). "
                "Return in JSON.",
                "userPrompt": lambda placeholders: f"The label is: '{placeholders['label']}'",
                "functions": [
                    {
                        "name": "getFeedback",
                        "description": "Determine whether the label is generic enough to make it reusable in the graph",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "feedback": {
                                    "type": "string",
                                    "description": "Feedback whether the property is reusable or not",
                                }
                            },
                            "required": ["feedback"],
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
