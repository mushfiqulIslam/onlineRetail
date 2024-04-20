from sqlalchemy import Column, BigInteger, Unicode

from core.database import Base
from core.database.mixins import TimestampMixin


class Country(Base, TimestampMixin):
    __tablename__ = "countries"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    country = Column(Unicode(255), nullable=False, unique=True)
    customer_count = Column(BigInteger)