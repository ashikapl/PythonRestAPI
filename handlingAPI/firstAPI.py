import requests

url = "https://api.freeapi.app/api/v1/public/randomusers/user/random"

response = requests.get(url)

data = response.json()

user_first_name = data["data"]["name"]["first"]
user_last_name = data["data"]["name"]["last"]
user_email = data["data"]["email"]
user_login_name = data["data"]["login"]["username"]
user_picture = data["data"]["picture"]["large"]
user_message = data["message"]

print(user_first_name + " " + user_last_name)
print(user_email)
print(user_login_name)
print(user_picture)
print(user_message)
