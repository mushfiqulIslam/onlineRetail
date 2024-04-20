from uuid import uuid4

from sqlalchemy import Column, BigInteger, UUID, Unicode, Float

from core.database import Base
from core.database.mixins import TimestampMixin


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    description = Column(Unicode(255), nullable=False, unique=True)
    unit_price = Column(Float, nullable=False)