# -*- coding: utf-8 -*-
import json
import os
from json.decoder import JSONDecodeError
from typing import Dict

import openai
from summarizer import Summarizer
from transformers import Pipeline, pipeline

from app.common.errors import OrkgNlpApiError
from app.common.services.wrapper import ResponseWrapper
from app.services import OrkgNlpApiService
from app.services.llm.tasks import (
    CheckDescriptivenessTask,
    CheckIfLiteralTypeIsCorrectTask,
    CheckPropertyLabelGuidelinesTask,
    CheckResourceDestructuringTask,
    RecommendMaterialsTask,
    RecommendMethodsTask,
    RecommendPropertiesFromTextTask,
    RecommendPropertiesTask,
    RecommendResearchProblemsTask,
)


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
            "recommendProperties": RecommendPropertiesTask(),
            "recommendResearchProblems": RecommendResearchProblemsTask(),
            "recommendMethods": RecommendMethodsTask(),
            "recommendMaterials": RecommendMaterialsTask(),
            # Used for the ORKG Chrome Plugin
            "recommendPropertiesFromText": RecommendPropertiesFromTextTask(),
            "checkDescriptiveness": CheckDescriptivenessTask(),
            "checkResourceDestructuring": CheckResourceDestructuringTask(),
            "checkIfLiteralTypeIsCorrect": CheckIfLiteralTypeIsCorrectTask(),
            "checkPropertyLabelGuidelines": CheckPropertyLabelGuidelinesTask(),
        }

    def completion(
        self,
        task_name: str,
        placeholders: Dict,
        temperature: float = 0.2,
    ):
        task = self.tasks.get(task_name)
        if task is None:
            raise OrkgNlpApiError(f"Task with name '{task_name}' does not exist", self.__class__)

        try:
            user_message = task.format_user_prompt(**placeholders)
        except KeyError as exception:
            raise OrkgNlpApiError(
                "The placeholder specification does not match the requirements", self.__class__
            ) from exception

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=temperature,
                messages=[
                    {"role": "system", "content": task.system_prompt},
                    {"role": "user", "content": user_message},
                ],
                functions=task.functions,
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
