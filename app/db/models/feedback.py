from sqlalchemy import Column, String, JSON

from app.db.connection import Base
from app.db.models.common import BaseTable


class Feedback(Base, BaseTable):
    __tablename__ = 'feedbacks'

    service_name = Column(String, nullable=False)
    request = Column(JSON, nullable=False)
    response = Column(JSON, nullable=False)
