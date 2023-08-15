from pydantic import BaseSettings


class Settings(BaseSettings):
    PINECONE_API_KEY: str = None
    PINECONE_API_ENV: str = None
    HUGGINGFACEHUB_API_TOKEN: str = None
    OPENAI_API_KEY: str = None

    class Config:
        env_file = ".env"


settings = Settings()
