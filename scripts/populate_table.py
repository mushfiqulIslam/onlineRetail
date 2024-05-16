import pandas as pd
from dotenv import load_dotenv

from app.models import Country, Product, Customer, Invoice
from core.database import get_session
from core.factory import Factory

load_dotenv()
session = get_session()


countries_dict = {}
products_dict = {}
customers_dict = {}

invoices = []

df = pd.read_excel('M:\\projects\OnlineRetailDataset\Online Retail Data Set.xlsx')
df = df.drop_duplicates()

for _, row in df.iterrows():
    if row["Country"] not in countries_dict:
        country = Country(
            country=row["Country"]
        )
        session.add(country)
        session.flush()
        countries_dict[row["Country"]] = country.id

    country_id = countries_dict[row["Country"]]

    if row["Description"] not in products_dict and not (
            pd.isna(row["Description"]) or pd.isnull(row["Description"])
    ):
        product = Product(
            description=row["Description"],
            unit_price=float(row['UnitPrice'])
        )
        session.add(product)
        session.flush()
        products_dict[row["Description"]] = product.id

    product_id = products_dict[row["Description"]]

    if row["CustomerID"] not in customers_dict and not (
            pd.isna(row["CustomerID"]) or pd.isnull(row["CustomerID"])
    ):
        customer = Customer(
            uuid=row["CustomerID"],
            country_id=country_id,
            recency=0.0,
            frequency=0.0,
            total_purchase=0.0
        )
        session.add(customer)
        session.flush()
        customers_dict[row["CustomerID"]] = customer.id

    customer_id = customers_dict[row["CustomerID"]]

    invoice = Invoice(
        uuid=row["InvoiceNo"],
        stock_code=row['StockCode'],
        created_at=row["InvoiceDate"],
        customer_id=customer.id,
        product_id=product_id,
        quantity=int(row['Quantity']),
        total_sales=float(row['UnitPrice']) * int(row['Quantity'])
    )
    invoices.append(invoice)

reference_date = df['InvoiceDate'].max()

recency_df = df.groupby('CustomerID')['InvoiceDate'].max().reset_index()
recency_df['recency'] = (reference_date - recency_df['InvoiceDate']).dt.days
frequency_df = df.groupby('CustomerID').size().reset_index(name='frequency')
df['TotalSales'] = df['Quantity'] * df['UnitPrice']
monetary_df = df.groupby('CustomerID')['TotalSales'].sum().reset_index()

rfm_df = pd.merge(recency_df, frequency_df, on='CustomerID')
rfm_df = pd.merge(rfm_df, monetary_df, on='CustomerID')
customer_controller = Factory().get_customer_controller(db_session=session)

for _, row in rfm_df.iterrows():
    if not (
            pd.isna(rfm_df["CustomerID"]) or pd.isnull(rfm_df["CustomerID"])
    ):
        customer_id = customers_dict[row["CustomerID"]]
        customer = customer_controller.get_by_id(int(customer_id))
        customer.recency = float(row['recency'])
        customer.frequency = float(row['frequency'])
        customer.total_purchase = float(row['TotalSales'])
        customer.save()

session.bulk_save_objects(invoices)

session.commit()
session.close()
