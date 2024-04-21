from app.models import Invoice
from app.repositories import InvoiceRepository
from core.controller import BaseController


class InvoiceController(BaseController[Invoice]):

    def __init__(self, invoice_repository: InvoiceRepository):
        super().__init__(model=Invoice, repository=invoice_repository)
        self.invoice_repository = invoice_repository

    async def get_by_id(self, id: int) -> list[Invoice]:
        return await self.invoice_repository.get_by_id(id)