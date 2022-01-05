from sqlalchemy import Column, DateTime, Float, Index, Text

from .metadata import Base


class SQM(Base):
    __tablename__ = "SQM"
    time = Column(DateTime, primary_key=True)
    brightness = Column(Float)


Index("timestamp", SQM.time, unique=True)
