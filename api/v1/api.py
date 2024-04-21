import json
import random

from fastapi import APIRouter, Depends
from pydantic import BaseModel

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


@bot_router.post("/assistant/chat")
async def chat(
        message: Message,
        customer_controller: CustomerController = Depends(Factory().get_customer_controller),
        country_controller: CountryController = Depends(Factory().get_country_controller),
        invoice_controller: InvoiceController = Depends(Factory().get_invoice_controller),
):
    intent = chatbot.predict_class(message.message)
    tag = intent[0]["intent"]
    for i in intents["intents"]:
        if i["tag"] == tag:
            msg = random.choice(i["responses"])
            break

    if tag == "product suggestion":
        _, customer_id = message.message.split(":")
        customer = await customer_controller.get_by_id(int(customer_id))
        response = Response(msg, customer)
    elif tag == "query3":
        country = message.message.replace("My country name is", "")
        country = country.replace(" ", "")
        country = await country_controller.get_by_name(country)
        response = Response(msg, country)
    elif tag == "orders status2":
        _, invoice_id = message.message.split(":")
        invoice = invoice_controller.get_by_id(int(invoice_id))
        response = Response(msg, invoice)


    return response