import os
import dotenv

env_path = os.path.abspath(__file__ + "/../../.env")

api_key = dotenv.get_key(dotenv_path=env_path, key_to_get="API_KEY")