import requests
from bs4 import BeautifulSoup
import pandas as pd

product_url = "https://www.wayfair.com/furniture/pdp/wade-logan-freetown-885-wide-reversible-sleeper-sofa-chaise-w010379019.html"
payload = {
    "source": "wayfair",
    "url": product_url,
    "user_agent_type": "desktop",
}
username = "USERNAME"
password = "PASSWORD"

response = requests.post(
    "https://realtime.oxylabs.io/v1/queries",
    auth=("USERNAME", "PASSWORD"),
    json=payload,
)
print(response.status_code)

content = response.json()["results"][0]["content"]
soup = BeautifulSoup(content, "html.parser")

title = soup.find("h1", {"data-hb-id": "heading"}).text
price = soup.find("div", {"class": "SFPrice"}).find("span", {"class":"oakhm64z_6101"}).text
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