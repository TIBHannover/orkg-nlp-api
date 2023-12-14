# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Union

JSON = Union[Dict[str, Any], List[Any]]


class Task:
    """
    Base class for all tasks.
    """

    # The system prompt that controls the behaviour of the model.
    system_prompt: str

    # The user prompt that is formatted with the named placeholders unless you override the format_user_prompt function.
    user_prompt: str

    # The functions that are used to extract the arguments from the model output, can be set to [] if not used.
    functions: JSON

    def __init__(self, system_prompt: str, user_prompt: str, functions: JSON):
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.functions = functions

    def format_user_prompt(self, **kwargs) -> str:
        return self.user_prompt.format(**kwargs)


########################
# Recommendation Tasks #
########################


class RecommendPropertiesTask(Task):
    def __init__(self):
        super().__init__(
            system_prompt="You are an assistant for building a knowledge graph for science. "
            "Your task is to recommend additional related predicates based on "
            "the set of existing predicates. Recommend a list maximum 5 additional predicates.",
            user_prompt="The existing predicates are: {0}",
            functions=[
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
        )

    def format_user_prompt(self, **kwargs) -> str:
        """
        This is a special case where the user prompt is formatted with a list of properties.
        Hence, we need to override the default behaviour of the base class formatting function.
        """
        return self.user_prompt.format(", ".join(kwargs["properties"]))


class RecommendResearchProblemsTask(Task):
    def __init__(self):
        super().__init__(
            system_prompt="A research problem contains a maximum of approximately 4 words "
            "to explain the research task or topic of a paper. Provide a list of maximum 5 research problems "
            "based on the title and optionally abstract provided by the user.",
            user_prompt="{paperTitle} {abstract}",
            functions=[
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
        )


class RecommendMethodsTask(Task):
    def __init__(self):
        super().__init__(
            system_prompt="Extract a list of maximum 5 methods from a scientific paper "
            "based on the title and optionally abstract provided by the user. "
            "if no methods are found, return an empty array.",
            user_prompt="{paperTitle} {abstract}",
            functions=[
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
        )


class RecommendMaterialsTask(Task):
    def __init__(self):
        super().__init__(
            system_prompt="Extract a list of maximum 5 materials that are used in a scientific paper."
            "Extract it from the title and optionally abstract provided by the user. "
            "if no materials are found, return an empty array.",
            user_prompt="{paperTitle} {abstract}",
            functions=[
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
        )


class RecommendPropertiesFromTextTask(Task):
    def __init__(self):
        super().__init__(
            system_prompt="Act as an ORKG researcher. Return in JSON. Provide only property names "
            "without values or extra information. Recommend a maximum of 3 to 4 properties for each text "
            "selection.",
            user_prompt="Find the best property names for the selected text: {selectedText}",
            functions=[
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
        )


########################
#  Verification Tasks  #
########################


class CheckDescriptivenessTask(Task):
    def __init__(self):
        super().__init__(
            system_prompt="Provide feedback to a user on how to improve a provided description text. The "
            "description text should give information about the objectives and topics of a scientific "
            "tabular related work overview. ",
            user_prompt="{value}",
            functions=[
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
        )


class CheckResourceDestructuringTask(Task):
    def __init__(self):
        super().__init__(
            system_prompt="You are an assistant for building a knowledge graph for science. Provide advice on if "
            "and how to decompose a provided resource label into separate resources. Only provide feedback is "
            "decomposing makes sense. Return the feedback in JSON.",
            user_prompt="{label}",
            functions=[
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
        )


class CheckIfLiteralTypeIsCorrectTask(Task):
    def __init__(self):
        super().__init__(
            system_prompt="You are an assistant in building a knowledge graph for science. You task is to advice "
            "users whether they should use a RDF resource or RDF literal. Based on a user-provided label, advice "
            "whether the type should be 'literal' or 'resource'. Literals are generally larger pieces of text and "
            "are not reusable, resource are atomic and can be reused. Return in JSON.",
            user_prompt="{label}",
            functions=[
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
        )


class CheckPropertyLabelGuidelinesTask(Task):
    def __init__(self):
        super().__init__(
            system_prompt="You are an assistant in building a knowledge graph for science. Provide feedback "
            "whether the provided predicate label is generic enough to make it reusable in the graph and explain "
            "how to make it more generic. Examples of properties that are not reusable: population in Berlin "
            "(because it contains a location), temperature in degrees Celsius (because it contains a unit). "
            "Return in JSON.",
            user_prompt="The label is: {label}",
            functions=[
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
        )
