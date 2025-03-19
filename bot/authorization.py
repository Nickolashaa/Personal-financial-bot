import os
from dotenv import load_dotenv


load_dotenv()

def authorization(id):
    return id == int(os.getenv("NICKOLAY_ID")) or id == int(os.getenv("MAKS_ID")) or id == int(os.getenv("VLADISLAV_ID"))