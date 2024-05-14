from app.models import Customer
from core.repository import BaseRepository


class CustomerRepository(BaseRepository[Customer]):

    async def get_by_id(self, id: int) -> list[Customer]:
        query = self._query()
        query = await self._get_by(query, "id", id)
        return await self._all(query)