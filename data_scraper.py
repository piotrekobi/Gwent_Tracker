from bs4 import BeautifulSoup
from operator import itemgetter
import requests
import json

from pprint import pprint


def deck_data(url):
    try:
        r = requests.get(url)
        deck_site = r.text
        soup = BeautifulSoup(deck_site, "lxml")
        root_div = soup.find(id="root")
        card_data = root_div.attrs
        data = json.loads(card_data.get("data-state"))
        if "guide" in url:
            card_dictionary = data.get("guide").get("deck").get("cards")
        else:
            card_dictionary = data.get("deck").get("cards")
        # pprint(data)
        card_info = []
        for card in card_dictionary:
            path = card.get("slotImg").get("small")
            image = requests.get(f"https://www.playgwent.com{path}",
                                 stream=True)
            card_info.append({
                "power": card.get("power"),
                "type": card.get("type"),
                "provisions": card.get("provisionsCost"),
                "name": card.get("name"),
                "local_name": card.get("localizedName"),
                "count": card.get("repeatCount") + 1,
                "image": image.content,
            })

        card_info.sort(key=itemgetter("power"), reverse=True)
        card_info.sort(key=itemgetter("type"))
        card_info.sort(key=itemgetter("provisions"), reverse=True)
        return card_info
    except (requests.RequestException, TypeError):
        return
