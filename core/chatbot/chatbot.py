from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_openai import ChatOpenAI

load_dotenv()


system_prompt = """
You are a customer service representative for a company selling products. We have product information, country information,
customers purchase information. Your duty is to first identify customers query. If query is related to product suggestions,
 you must ask customerId first, if not available then Country name. If customer wants to know about their order's status
 ask them invoiceID, if not available CustomerID, for CustomerID we will send last orders information.  Here is a format of 
 your reply:
ProvidedCustomerIDorCountryorInvoiceID: {True if customer provided any of CustomerID, Country or InvoiceID else False}
Purpose: {Order If customer wants orders information, Suggestion if customer wants product suggestion, ignore otherwise}
CustomerID : {CustomerID or False}
Country: {Country or False}
InvoiceID: {InvoiceID or False}
PositiveResponseMessage: {If customer provided CustomerID, Country or InvoiceID. Example: Here is our suggestions}
NegativeResponseMessage: {If customer provided CustomerID, Country or InvoiceID. Example: Sorry! we don't have the 
information you are looking for}
NextMessage: {If customer did not provided any of CustomerID, Country or InvoiceID, put customer's reply message here}
"""

chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer customer's query based on using this format: {system_prompt}",
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)

chain = prompt | chat
demo_ephemeral_chat_history = ChatMessageHistory()