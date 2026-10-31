import os, requests

text = "Salom! Bu sinov xabari. Bugungi vazifa: ..."

r = requests.post(
    f"https://api.telegram.org/bot{os.environ['TG_TOKEN']}/sendMessage",
    data={"chat_id": os.environ["TG_CHAT_ID"], "text": text},
)
r.raise_for_status()
