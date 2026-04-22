from google import genai

API_KEY = "AIzaSyB50o_tSTOnbjwHPk5nD7VdjEh67aQ2hjs"

client = genai.Client(api_key=API_KEY)

for model in client.models.list():
    print(model.name)