# -*- coding: utf-8 -*-
import enum
import logging
import os

import dotenv

# needed for local development; Inside docker the .env is loaded anyway.
dotenv.load_dotenv()


__version__ = "0.6.2"


class AppConfig:
    service_mapping = {
        "PREDICATES_CLUSTERING": "/clustering/predicates",
        "BIOASSAYS_SEMANTIFICATION": "/clustering/bioassays",
        "CS_NER": "/annotation/csner",
        "AGRI_NER": "/annotation/agriner",
        "RESEARCH_FIELD_CLASSIFICATION": "/annotation/rfclf",
        "TEMPLATES_RECOMMENDATION": "/nli/templates",
        "TABLE_EXTRACTION": "/tools/pdf/table/extraction",
        "PDF_CONVERSION": "/tools/pdf/convert",
        "TEXT_SUMMARIZATION": "/tools/text/summarize",
        "TEXT_CLASSIFICATION": "/tools/text/classify",
    }

    @classmethod
    def get_service_names_as_enum(cls):
        key_values = {key: key for key in cls.service_mapping.keys()}
        enum_cls = enum.Enum("ServiceName", key_values, type=str)
        return enum_cls


# Root logger configuration
level = logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG").upper())

logger = logging.getLogger(__name__)
logger.setLevel(level=level)

stdout = logging.StreamHandler()
stdout.setLevel(level=level)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
stdout.setFormatter(formatter)

logger.addHandler(stdout)
