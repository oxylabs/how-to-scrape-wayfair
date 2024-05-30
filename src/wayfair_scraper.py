import requests
from bs4 import BeautifulSoup
import pandas as pd

product_url = "https://www.wayfair.com/furniture/pdp/ebern-designs-adryel-98-wide-microfibermicrosuede-right-hand-facing-sofa-chaise-w003629953.html"
payload = {
    "source": "universal_ecommerce",
    "url": product_url,
    "user_agent_type": "desktop_safari",
    "geo_location": "United States",
    "render": "html",
    "browser_instructions": [
        {
            "type": "wait_for_element",
            "selector": {
                "type": "css",
                "value": "div.SFPrice span.oakhm64z_6112"
            },
            "timeout_s": 10
        }
    ]
}

username = "USERNAME"
password = "PASSWORD"

response = requests.post(
    "https://realtime.oxylabs.io/v1/queries",
    auth=(username, password),
    json=payload,
    timeout=180
)
print(response.status_code)

content = response.json()["results"][0]["content"]
soup = BeautifulSoup(content, "html.parser")

title = soup.find("h1", {"data-hb-id": "Heading"}).text
price = soup.find("div", {"class": "SFPrice"}).find("span", {"class": "oakhm64z_6112"}).text
rating = soup.find("span", {"class": "ProductRatingNumberWithCount-rating"}).text

data = [{
   "Product Title": title,
   "Price": price,
   "Rating": rating,
   "Link": product_url,
}]
df = pd.DataFrame(data)
df.to_csv("product_data.csv", index=False)
df.to_json("product_data.json", orient="records")
