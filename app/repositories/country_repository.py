from app.models import Country
from core.repository import BaseRepository


class CountryRepository(BaseRepository[Country]):

    async def get_by_name(self, name: str) -> list[Country]:
        query = self._query()
        query = await self._get_by(query, "country", name)
        return await self._all(query)