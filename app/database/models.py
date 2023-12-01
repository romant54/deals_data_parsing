from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB
from .engine import Base, engine

class PreprocessingDeal(Base):
    __tablename__ = 'preprocessing_deals'
    
    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSONB)


class Deal(Base):
    __tablename__ = 'deals'

    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSONB)


Base.metadata.create_all(bind=engine)
