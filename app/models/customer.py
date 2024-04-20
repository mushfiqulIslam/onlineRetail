from uuid import uuid4

from sqlalchemy import BigInteger, Column, UUID, ForeignKey, Float

from core.database import Base
from core.database.mixins import TimestampMixin


class Customer(Base, TimestampMixin):
    __tablename__ = "customers"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    country_id = Column(
        BigInteger, ForeignKey("countries.id", ondelete="CASCADE"), nullable=False
    )
    recency = Column(Float, nullable=False)
    frequency = Column(Float, nullable=False)
    total_purchase = Column(Float, nullable=False)