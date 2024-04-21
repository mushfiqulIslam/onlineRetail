from app.models import Customer
from app.repositories import CustomerRepository
from core.controller import BaseController


class CustomerController(BaseController[Customer]):

    def __init__(self, customer_repository: CustomerRepository):
        super().__init__(model=Customer, repository=customer_repository)
        self.customer_repository = customer_repository

    async def get_by_id(self, id: int) -> list[Customer]:
        return await self.customer_repository.get_by_id(id)