import dotenv, os 

env_path = os.path.abspath(__file__ + "/../../../.env")
if not os.path.exists(env_path):
    with open (env_path, mode="w") as f:
        f.write("API_KEY_W_MAP='Enter your API_KEY from OpenWeatherMap'\nAPI_KEY_W_API='Enter your API_KEY from WeatherApi'\nUSER_NAME='Enter your nUSER_NAME from GeoNames'")
api_key_w_map = dotenv.get_key(env_path, "API_KEY_W_MAP")
api_key_w_api = dotenv.get_key(env_path, "API_KEY_W_API")
user_name = dotenv.get_key(env_path, "USER_NAME")