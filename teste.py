import os
import dotenv

dotenv.load_dotenv()
token=os.getenv("HOST")
print(token)

