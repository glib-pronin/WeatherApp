import dotenv, os 

env_path = os.path.abspath(__file__ + "/../../../.env")
if not os.path.exists(env_path):
    with open (env_path, mode="w") as f:
        f.write("API_KEY='Enter you API_KEY'")
api_key = dotenv.get_key(env_path, "API_KEY")