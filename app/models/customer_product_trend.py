from sqlalchemy import BigInteger, Column, ForeignKey, Float, Integer

from core.database import Base
from core.database.mixins import TimestampMixin


class CustomerProductTrend(Base, TimestampMixin):
    __tablename__ = 'customer_product_trends'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    customer_id = Column(
        BigInteger, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False
    )
    product_id = Column(
        BigInteger, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    recency = Column(Float, nullable=False)
    frequency = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_purchase = Column(Float, nullable=False)