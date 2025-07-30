import dotenv, os 

env_path = os.path.abspath(__file__ + "/../../.env")

api_key = dotenv.get_key(env_path, "API_KEY")