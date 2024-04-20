from sqlalchemy import Column, BigInteger, ForeignKey, Float, Integer

from core.database import Base
from core.database.mixins import TimestampMixin


class CountryProductTrend(Base, TimestampMixin):
    __tablename__ = 'country_product_trends'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    country_id = Column(
        BigInteger, ForeignKey("countries.id", ondelete="CASCADE"), nullable=False
    )
    product_id = Column(
        BigInteger, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    recency = Column(Float, nullable=False)
    frequency = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_sales = Column(Float, nullable=False)