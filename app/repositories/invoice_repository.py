from app.models import Invoice
from core.repository import BaseRepository


class InvoiceRepository(BaseRepository[Invoice]):

    async def get_by_id(self, id: int) -> list[Invoice]:
        query = self._query()
        query = self._get_by(query, "id", id)
        return await self._all(query)