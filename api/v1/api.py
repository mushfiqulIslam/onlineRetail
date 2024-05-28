from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.controllers import CustomerController, CountryController, InvoiceController
from core.chatbot.chatbot import demo_ephemeral_chat_history, chain, system_prompt
from core.factory import Factory

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
    demo_ephemeral_chat_history.add_user_message(message.message)
    msg = chain.invoke({
        "messages": demo_ephemeral_chat_history.messages,
        "system_prompt": system_prompt
    }).content
    lines = [line for line in msg.split('\n') if line.strip()]
    results = {}
    for line in lines:
        key, value = line.split(':')
        value = value.lstrip()
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

    return Response(message=msg, values=[])