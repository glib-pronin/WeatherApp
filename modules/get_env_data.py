from .get_resource_path import get_path
import dotenv

env_path = get_path(".env")

api_key = dotenv.get_key(dotenv_path=env_path, key_to_get="API_KEY")