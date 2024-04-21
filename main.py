import os

import uvicorn
from dotenv import load_dotenv

from core.chatbot.train_bot import train_bot
from core.config import config

if __name__ == "__main__":
    load_dotenv()
    if os.environ.get("TRAIN", False) in ["True", "true", "t"]:
        train_bot()

    uvicorn.run(
        app="core.server:app",
        reload=True if config.ENVIRONMENT != "production" else False,
        workers=1,
    )