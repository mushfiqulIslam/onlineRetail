# onlineRetail
This a sales chatbot that helps customer to track their order, getting product suggestions based on data available on the database. 

To build this project I used a layered architecture that includes a model layer, a repository layer, a controller layer,
and an API layer. The schema of this project contains Country, Product, Customer, Invoice, Customer-Product Trend and
Country-Product Trend class with information related to how frequently a product bought, what is the latency between buying 
more than one time and total amount of money spent for a product. This will help bot to find out what are the targeted products
 of a client. Country-Product Trend table will help to provide additional suggestions based on other citizens preferences.  
The bot basically works with the help of ChatGPT. using LangChain, I developed a prompt format which is used to give ChatGPT
proper guidance on replying any query to the user. Based on pre-defined response our bot process the additional information
required to reply a customer's query and send suitable message to the customer.


---

## Detailed Setup Instructions

Below are the detailed commands you will need to execute to set up and run the application. These steps cover environment setup, dependency installation, database migrations, and running the application.

### Create Virtual Environment

Create virtual environment using python 3.10.

```bash
python3 -m venv venv
```

### Activating the Virtual Environment

Activate your previously created virtual environment using the following command:

```bash
source venv/bin/activate
```

This command activates the virtual environment.

### Installing Dependencies

Once your environment is activated, install all required Python dependencies listed in the `requirements.txt` file:

```bash
# Install project dependencies
pip install -r requirements.txt
```

This command reads the `requirements.txt` file in your project directory and installs all the listed packages. This file includes FastAPI, Uvicorn for running the server, and other necessary libraries.

### Initializing Database Migrations

To initialize database with the correct tables, create an initial migration file with the following command. Initial 
migration file is already available. Run this to 
get the updates:

```bash
alembic revision --autogenerate -m "Initial migrations"
```


### Applying Migrations to the Database

After generating the migration scripts, apply them to your database to create the necessary tables and relationships:

```bash
alembic upgrade head
```

### Update environment variables

To train the model and run fastapi on the server, please configure 
environment variables properly by following the commands.

```bash
cp example.env .env
```

```bash
TRAIN=True or False
POSTGRES_URL=postgresql+asyncpg://myuser:mypass@127.0.0.1:5432/mydatabase

```

TRAIN takes boolean value to define train before starting server or not. Ensure that you replace myuser, mypass, and mydatabase with your actual database username, password, and database name, respectively. This information is crucial for the application to connect and interact with your PostgreSQL database securely and efficiently.


### Running the Application

Finally, start your FastAPI application by running the Python script that contains your FastAPI app instance:

```bash

python main.py
```

This command will start the server, making your application accessible on the configured port (usually http://localhost:8000). If your FastAPI application utilizes Uvicorn directly in the `main.py`, it will also handle ASGI server initialization.

---

**Note:** Ensure each step is executed in the order given to avoid runtime errors or dependency conflicts. This structured approach helps maintain clarity and usability, crucial for effective project documentation.