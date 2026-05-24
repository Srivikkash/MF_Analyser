import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "mf_analyzer")
    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", "120"))
    MFAPI_BASE_URL = "https://api.mfapi.in"
    FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"
    FMP_API_KEY = os.getenv("FMP_API_KEY", "demo")
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "12"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
