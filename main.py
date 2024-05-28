import uvicorn
from dotenv import load_dotenv


from core.config import config

if __name__ == "__main__":
    load_dotenv()

    uvicorn.run(
        app="core.server:app",
        reload=True if config.ENVIRONMENT != "production" else False,
        workers=1,
    )