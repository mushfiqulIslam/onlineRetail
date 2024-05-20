import json

from fastapi import APIRouter, Depends
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langchain.memory import ChatMessageHistory

from app.controllers import CustomerController, CountryController, InvoiceController
from core.chatbot import ChatBot
from core.factory import Factory

intents = json.loads(open("intents.json").read())
chatbot = ChatBot()
bot_router = APIRouter()


@bot_router.get("/")
async def root():
    return {"message": "Hello World"}


class Message(BaseModel):
    message: str


class Response(BaseModel):
    message: str
    values: list


# Define prompt template
system_prompt = """
You are a customer service representative for a company selling products. We have product information, country information,
customers purchase information. Your duty is to first identify customers query. If query is related to product suggestions,
 you must ask customerId first, if not available then Country name. If customer wants to know about their order's status
 ask them invoiceID, if not available CustomerID, for CustomerID we will send last orders information.  Here is a format of 
 your reply:
ProvidedCustomerIDorCountryorInvoiceID: {True if customer provided any of CustomerID, Country or InvoiceID else False}
Purpose: {Order If customer wants orders information, Suggestion if customer wants product suggestion, ignore otherwise}
CustomerID : {CustomerID}
Country: {Country}
InvoiceID: {InvoiceID}
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


@bot_router.post("/assistant/chat")
async def chat(
        message: Message,
        customer_controller: CustomerController = Depends(Factory().get_customer_controller),
        country_controller: CountryController = Depends(Factory().get_country_controller),
        invoice_controller: InvoiceController = Depends(Factory().get_invoice_controller),
):
    # intent = chatbot.predict_class(message.message)
    demo_ephemeral_chat_history.add_user_message(message.message)
    msg = chain.invoke({
        "messages": demo_ephemeral_chat_history.messages,
        "system_prompt": system_prompt
    }).content
    lines = [line for line in msg.split('\n') if line.strip()]
    results = {}
    for line in lines:
        key, value = line.split(':')
        results[key] = value

    if results.get("NextMessage", "False") != "False":
        msg = results["NextMessage"]
    else:
        msg = "Sorry! I did not understand your query. Can your repeat?"

    if results.get("ProvidedCustomerIDorCountryorInvoiceID", "False") == "True":
        if results.get("CustomerID", "False") != "False":
            customer = await customer_controller.get_by_id(int(results["CustomerID"]))
            if not customer:
                if results.get("NegativeResponseMessage", "False") != "False":
                    msg = results["NegativeResponseMessage"]
                else:
                    msg = "CustomerID is not correct"

            if results.get("Purpose", "False") == "Order":
                if results.get("PositiveResponseMessage", "False") != "False":
                    msg = results["PositiveResponseMessage"]
                else:
                    msg = "Here is your orders information"
            elif results.get("Purpose", "False") == "Suggestion":
                if customer:
                    if results.get("PositiveResponseMessage", "False") != "False":
                        msg = results["PositiveResponseMessage"]
                    else:
                        msg = "You might try these products"

        elif results.get("Country", "False") != "False":
            country = await country_controller.get_by_name(results["Country"])
            if results.get("Purpose", "False") == "Suggestion":
                if country:
                    if results.get("PositiveResponseMessage", "False") != "False":
                        msg = results["PositiveResponseMessage"]
                    else:
                        msg = "You might try these products"
                else:
                    if results.get("NegativeResponseMessage", "False") != "False":
                        msg = results["NegativeResponseMessage"]
                    else:
                        msg = "We don't sell on your region"
        elif results.get("InvoiceID", "False") != "False":
            invoice = await invoice_controller.get_by_id(int(results.get["InvoiceID"]))
            if results.get("Purpose", "False") == "Order":
                if invoice:
                    if results.get("PositiveResponseMessage", "False") != "False":
                        msg = results["PositiveResponseMessage"]
                    else:
                        msg = "Here is your orders information"
                else:
                    if results.get("NegativeResponseMessage", "False") != "False":
                        msg = results["NegativeResponseMessage"]
                    else:
                        msg = "No invoice found with this id."



    # tag = intent[0]["intent"]
    # for i in intents["intents"]:
    #     if i["tag"] == tag:
    #         msg = random.choice(i["responses"])
    #         break
    #
    # if tag == "product suggestion":
    #     _, customer_id = message.message.split(":")
    #     customer = await customer_controller.get_by_id(int(customer_id))
    #     response = Response(message=msg, values=customer)
    # elif tag == "query3":
    #     country = message.message.replace("My country name is", "")
    #     country = country.replace(" ", "")
    #     country = await country_controller.get_by_name(country)
    #     response = Response(message=msg, values=country)
    # elif tag == "orders status2":
    #     _, invoice_id = message.message.split(":")
    #     invoice = await invoice_controller.get_by_id(int(invoice_id))
    #     response = Response(message=msg, values=invoice)
    # else:
    #     response = Response(message=msg, values=[])

    return Response(message=msg, values=[])