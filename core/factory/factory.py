from functools import partial

from fastapi import Depends

from app.controllers import CustomerController, CountryController, InvoiceController
from app.models import Customer, Country, Invoice
from app.repositories import CustomerRepository, CountryRepository, InvoiceRepository
from core.database import get_session


class Factory:
    """
    This is the factory container that will instantiate all the controllers and
    repositories which can be accessed by the rest of the application.
    """

    # Repositories
    customer_repository = partial(CustomerRepository, Customer)
    country_repository = partial(CountryRepository, Country)
    invoice_repository = partial(InvoiceRepository, Invoice)

    def get_customer_controller(self, db_session=Depends(get_session)):
        return CustomerController(
            customer_repository=self.customer_repository(db_session=db_session)
        )

    def get_country_controller(self, db_session=Depends(get_session)):
        return CountryController(
            country_repository=self.country_repository(db_session=db_session)
        )

    def get_invoice_controller(self, db_session=Depends(get_session)):
        return InvoiceController(
            invoice_repository=self.invoice_repository(db_session=db_session)
        )
