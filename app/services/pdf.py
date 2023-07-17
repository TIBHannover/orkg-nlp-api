# -*- coding: utf-8 -*-
import os
import re
import shutil
import tempfile
import zlib
from subprocess import CalledProcessError
from typing import Any, BinaryIO, Dict

import pikepdf
import tabula
from bs4 import BeautifulSoup
from tabula.errors import JavaNotFoundError

from app.common.errors import OrkgNlpApiError
from app.common.services import runner
from app.common.services.wrapper import ResponseWrapper
from app.common.util import io
from app.services import OrkgNlpApiService
from app.services.backend import OrkgBackendService


class PdfService(OrkgNlpApiService):
    def __init__(self):
        self.encoding = "utf-8"
        self.DEFAULT_PDF_ZOOM = "1.33"

    def extract_table(self, file, page_number, region, lattice):
        table = {}

        try:
            dataframes = tabula.read_pdf(
                file,
                pages=page_number,
                area=region,
                lattice=lattice,
                multiple_tables=False,
                encoding=self.encoding,
                pandas_options={"header": None},
            )
        except JavaNotFoundError:
            raise OrkgNlpApiError(
                "In order to use the table extraction service you need to install Java on your machine.",
                self.__class__,
            )
        except CalledProcessError:
            raise OrkgNlpApiError(
                "Something went wrong when calling tabula JAR file. Please check your input and try again.",
                self.__class__,
            )

        if len(dataframes) > 0:
            table = dataframes[0].to_dict(orient="list")

        return ResponseWrapper.wrap_json({"table": table})

    def convert_pdf(self, file):
        # Temporarily save the file
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.write(file.read())
        temp_file.seek(0)

        # Make a temp directory for saving the parsed pdf (so the html)
        temp_dir = tempfile.mkdtemp()
        output_file = "output.html"

        # Execute pdf2htmlEX and save the output in output_file
        args = [
            "pdf2htmlEX",
            "--dest-dir",
            temp_dir,
            "--zoom",
            self.DEFAULT_PDF_ZOOM,
            "--printing",
            "0",
            "--embed-outline",
            "0",
            temp_file.name,
            output_file,
        ]

        runner.run(args)

        # Open the created html file and return output as response
        html = io.read_file(os.path.join(temp_dir, output_file))

        # Cleanup the temp dir
        shutil.rmtree(temp_dir)

        return html

    @staticmethod
    def _extract_metadata(file_bytes: bytes) -> str:
        metadata_key = b"/Type /(SciKGMetadata|Metadata)"
        metadata_pattern = re.compile(b"(" + metadata_key + b".*?)stream(.*?)endstream", re.S)

        for header, data in re.findall(metadata_pattern, file_bytes):
            if "/FlateDecode" in header.decode("utf-8"):
                return zlib.decompress(data.strip(b"\r\n")).decode("utf-8").strip()
            else:
                return data.decode("utf-8").strip()

    def extract_scikgtex_annotations(self, file: BinaryIO) -> Dict[str, Any]:
        # Temporarily save the file
        temp_file = tempfile.NamedTemporaryFile()
        with temp_file:
            temp_file.write(file.read())
            temp_file.seek(0)

            try:
                with pikepdf.Pdf.open(temp_file) as pdf_file:
                    # Extraction the metadata from the pdf file
                    if isinstance(pdf_file, pikepdf.Pdf):
                        metadata = (
                            pdf_file.Root.SciKGMetadata.read_bytes().decode()
                            if "SciKGMetadata" in dir(pdf_file.Root)
                            else pdf_file.Root.Metadata.read_bytes().decode()
                        )
                    else:
                        metadata = self._extract_metadata(file.read())

                    # parse the metadata
                    metadata = BeautifulSoup(metadata, "xml")

                    # collecting the annotations
                    title = metadata.find("hasTitle").get_text()
                    authors = metadata.find_all("hasAuthor")
                    authors = [{"label": x.get_text()} for x in authors]
                    research_field = metadata.find("hasResearchField").get_text()
                    contributions_description = metadata.find("ResearchContribution")
                    predicates = contributions_description.find_all()

                    # Get IDs from the backend
                    service = OrkgBackendService()
                    research_field_id = service.lookup_orkg_research_field(research_field)
                    contributions_ids = {}
                    for predicate in predicates:
                        predicate_id = service.lookup_orkg_predicate(predicate.name)
                        if predicate_id:
                            contributions_ids[predicate_id] = [{"text": predicate.get_text()}]

                    # Generate the paper request object
                    result = {
                        "predicates": [],
                        "paper": {
                            "title": title,
                            "authors": authors,
                            "researchField": research_field_id,
                            "contributions": [
                                {"name": "Contribution 1", "values": contributions_ids},
                            ],
                        },
                    }
                    return ResponseWrapper.wrap_json(result)
            except AttributeError:
                # Following EAFP principle
                raise OrkgNlpApiError(
                    "Seems the PDF doesn't have any SciKGTeX annotations.", self.__class__
                )
