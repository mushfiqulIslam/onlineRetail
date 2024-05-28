from app.models import Country
from app.repositories import CountryRepository
from core.controller import BaseController
from core.database import Transactional, Propagation


class CountryController(BaseController[Country]):

    def __init__(self, country_repository: CountryRepository):
        super().__init__(model=Country, repository=country_repository)
        self.country_repository = country_repository

    async def get_by_name(self, name: str) -> list[Country]:
        return await self.country_repository.get_by_name(name)

    @Transactional(propagation=Propagation.REQUIRED)
    async def add(self, country: str) -> Country:
        return await self.country_repository.create({
                "country": country
        })