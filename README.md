# onlineRetail
The notebook folder contains a notebook where I did Part 1: Machine Learning Model Implementation.
Rest of the part is under Part 2: Chatbot Development.

To build this project I used a layered architecture that includes a model layer, a repository layer, a controller layer,
and an API layer. The schema of this project contains Country, Product, Customer, Invoice, Customer-Product Trend and
Country-Product Trend class with information related to how frequently a product bought, what is the latency between buying 
more than one time and total amount of money spent for a product. This will help bot to find out what are the targeted products
 of a client. Country-Product Trend table will help to provide additional suggestions based on other citizens preferences.  
The bot was build using Dense Neural Network

## Installation Guide
source venv venv
pip install -r requirements.txt
 alembic revision --autogenerate -m "Initial migrations
 alembic upgrade head
python main.py