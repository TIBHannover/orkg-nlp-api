import os
import shutil
import uuid
import datetime
import tempfile
import tabula

from subprocess import CalledProcessError
from fastapi import HTTPException
from tabula.errors import JavaNotFoundError

from app.common.services import runner
from app.common.services.wrapper import ResponseWrapper
from app.common.util import io
from app.services import OrkgNlpApiService


class PdfService(OrkgNlpApiService):

    def __init__(self):
        self.encoding = 'utf-8'
        self.DEFAULT_PDF_ZOOM = '1.33'

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
                pandas_options={'header': None}
            )
        except JavaNotFoundError:
            raise HTTPException(
                status_code=500,
                detail='In order to use the table extraction service you need to install Java on your machine.'
            )
        except CalledProcessError:
            raise HTTPException(
                status_code=500,
                detail='Something went wrong when calling tabula JAR file. Please check your input and try again.'
            )

        if len(dataframes) > 0:
            table = dataframes[0].to_dict(orient='list')

        return ResponseWrapper.wrap_json({'table': table})

    def convert_pdf(self, file):

        # Temporarily save the file
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.write(file.read())
        temp_file.seek(0)

        # Make a temp directory for saving the parsed pdf (so the html)
        temp_dir = tempfile.mkdtemp()
        output_file = 'output.html'

        # Execute pdf2htmlEX and save the output in output_file
        args = ['pdf2htmlEX',
                '--dest-dir', temp_dir,
                '--zoom', self.DEFAULT_PDF_ZOOM,
                '--printing', '0',
                '--embed-outline', '0',
                temp_file.name,
                output_file]

        runner.run(args)

        # Open the created html file and return output as response
        html = io.read_file(os.path.join(temp_dir, output_file))

        # Cleanup the temp dir
        shutil.rmtree(temp_dir)

        return html
