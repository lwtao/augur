from sqlalchemy import Column, String, Float ,INT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class StockHist(Base):
    __tablename__ = 'hist_data'
    id = Column(INT(), primary_key=True)
    code = Column(String(20))
    date = Column(String(20))
    open = Column(Float())
    high = Column(Float())
    close = Column(Float())
    low = Column(Float())
    volume = Column(Float())
    price_change = Column(Float())
    p_change = Column(Float())
    ma5 = Column(Float())
    ma10 = Column(Float())
    ma20 = Column(Float())
    v_ma5 = Column(Float())
    v_ma10 = Column(Float())
    v_ma20 = Column(Float())
    ktype = Column(String(20))

