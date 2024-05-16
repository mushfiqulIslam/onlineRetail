from uuid import uuid4

from sqlalchemy import Column, BigInteger, UUID, Unicode, ForeignKey, Integer, Float

from core.database import Base
from core.database.mixins import TimestampMixin


class Invoice(Base, TimestampMixin):
    __tablename__ = "invoices"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    stock_code = Column(Unicode(255), nullable=False)
    customer_id = Column(
        BigInteger, ForeignKey("customers.id", ondelete="CASCADE"), nullable=True
    )
    product_id = Column(
        BigInteger, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    quantity = Column(Integer, nullable=False)
    total_sales = Column(Float, nullable=False)