import uuid
import datetime
from subprocess import CalledProcessError

import tabula
from fastapi import HTTPException
from tabula.errors import JavaNotFoundError

from app.services import OrkgNlpService


class PdfService(OrkgNlpService):

    def __init__(self):
        self.encoding = 'utf-8'

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

        return {
            'timestamp': datetime.datetime.now(),
            'uuid': uuid.uuid4(),
            'table': table
        }
