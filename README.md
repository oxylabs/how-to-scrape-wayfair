# How to Scrape Product Data from Wayfair: A Step-by-Step Guide

## Introduction

In this tutorial, we will learn how to scrape product data from Wayfair, a popular online furniture and home goods retailer. We will explore Wayfair’s Page Layout, prepare our project, fetch the Wayfair product page to extract necessary data, and export it in CSV or JSON format.

## Overview of Wayfair Page Layout

Before we dive into the technical detail, it's essential to understand the Wayfair page layout. Wayfair has different types of page layouts. Let’s explore a few relevant ones:

### 1. Search Result Page

This page appears when we search for products. For example, if we search the term "Sofa", the search result will be similar to the below:
![search result](images/Wayfair_search_results.png)

We can extract all the products for the search term "Sofa". And, we can also extract their links, titles, prices, ratings, etc.

### 2. Product Listing

This page appears when we click on a product to see the detail. It shows all the product information and images with title, price, rating, etc. We will learn how to extract information from this page in detail in the next few steps.
![product](images/wayfair_product_page.png)

### 3. reCAPTCHA Protection Page

Last but not least, Wayfair also has a reCAPTCHA Protection page. This is a hidden page that only appears when Wayfair detects unusual browsing behaviors such as repeated or too-fast navigation from page to page, automated scripts or scrapers, etc. The page looks similar to below:

![recaptcha](images/recaptcha_protection.png)

## Bypassing Wayfair Scraping Challenges

As you can see, Wayfair is using Google’s reCAPTCHA protection service to block automated scrapers. It is an advanced Anti-bot protection service that uses sophisticated fingerprinting algorithms, and behavioral pattern recognition to protect websites from scrapers and web crawlers. Evading Wayfair’s Antibot measure is not a walk in the park.

Manually crafting a scraper that can send requests as an actual browser and mimic human browsing behavior is quite difficult. Also, you will have to maintain it and keep it up to date with the constant changes and updates. Managing all these requires in-depth knowledge and robust scraping experience.

Oxylabs Wayfair API provides out of the box support for bypassing the anti-bot measures by providing proxies, custom headers, user agents, and other features. This immensely eases the process and simplifies the scraper.

Now, let’s see how we can use Oxylabs Wayfair API to extract data from Wayfair Product Page.

## Step 1 - Setting up the project environment

To begin scraping Wayfair data, we need to prepare our project environment. This involves installing Python and the necessary dependencies. If you already have python installed you can skip the Python installation and only install the dependencies in your active python environment.

### 1. Install Python

This tutorial is written using Python 3.11.2, however, it should also work with the older or latest version of Python 3. You can download the latest version and install Python from the oﬃcial website.

### 2. Install Dependencies

Once you have downloaded and installed python. Install the following dependencies by executing the below command in the terminal or command prompt:

```bash
python -m pip install requests bs4 pandas
```

The above command will install Requests, Beautiful Soup, and Pandas libraries. We will use these modules to interact with the Oxylabs Wayfair API and store data.

## Step 2 - Fetching Wayfair Webpage

We will be using the Wayfair product page for the demonstration. We will also use the Oxylabs Wayfair API to fetch the Wayfair product data and parse it using the Beautifulsoup library.

### 1. Signup for an Oxylabs account

To use the Oxylabs Wayfair API you will have to create an Oxylabs account. You will find all the available APIs [here](https://oxylabs.io/products). Oxylabs also provides a **1-week free trial at no cost!** This should be sufficient to fine-tune the scraper. After the trial ends, you can keep on using the service by upgrading to your preferred paid plan seamlessly.

Once you create your account, you will get your sub-account credentials which we will be using to send network requests to the API.

### 2. Oxylabs Wayfair API Overview

Before we begin, let’s discuss some of the most useful query parameters of Oxylabs Wayfair API. The API operates in two modes:

#### Scrape using URL

Using this method, you can scrape any Wayfair url. You will only have to pass two required parameters `url` & `source`. The source parameter should be set to `wayfair`, and the `url` should be a Wayfair Website URL. 

It also takes optional parameters such as `user_agent_type`, & `callback_url`.
The `user_agent_type` tells the API which device the user agent will use, i.e., desktop. Lastly, the `callback_url` parameter is used to specify a URL to which the server should send a response after processing the request. Let’s take a look at an example payload:

```python
payload = {
    "source": "wayfair",
    "url": "https://www.wayfair.com/furniture/pdp/wade-logan-freetown-885-wide-reversible-sleeper-sofa-chaise-w010379019.html",
    "user_agent_type": "desktop",
    "callback_url": "<URL to your callback endpoint.>"
}
```

#### Scrape using Query

This is another method to scrape Wayfair search results. It also needs two parameters: `source` & `query`. We set the source to `wayfair_search` this time and we also put the search terms in the query parameter. This endpoint also supports some additional parameters such as `start_page`, `pages`, `limit`, `callback_url`, and `user_agent_type`.

```python
payload = {
'source': 'wayfair_search',
'query': 'sofa',
'start_page': 1,
'pages': 5,
'limit': 48
}
```

The result will start from the page number mentioned in the `start_page` parameter. We can retrieve several pages from the search result using the `pages` parameter and we can control how many search results per page to fetch using the `limit` parameter.

### 3. Sending Network Requests

Now, we will start writing our Wayfair scraper. We will first import the necessary Libraries, create payload and necessary variables:

```python
import requests
from bs4 import BeautifulSoup

product_url = "https://www.wayfair.com/furniture/pdp/wade-logan-freetown-885-wide-reversible-sleeper-sofa-chaise-w010379019.html"
payload = {
    "source": "wayfair",
    "url": product_url,
    "user_agent_type": "desktop",
}
username = "USERNAME"
password = "PASSWORD"
```

Notice, we have also created a few variables username, password and product_url. You will have to use your Oxylabs sub-account’s username and password and also if you wish you can replace the product url with your desired product url.

Next, we will send a POST request using the requests module to Oxylabs' realtime API endpoint: <https://realtime.oxylabs.io/v1/queries>

```python
response = requests.post(
    "https://realtime.oxylabs.io/v1/queries",
    auth=("USERNAME", "PASSWORD"),
    json=payload,
)
print(response.status_code)
```

In the above code, we are using the post method of requests module to send a POST request to Oxylabs API and we are also passing the sub-account credentials for auth and sending the payload in JSON format. If you run this code, you will see 200 as output which indicates everything is working. If you get any other status code make sure your credentials and payload are all correct.

## Step 3 - Parsing Data

Now, we can parse the content of the JSON response from the API. This JSON object will have the content of the webpage in HTML format. We will use the BeautifulSoup library to parse the HTML from the response.

```python
content = response.json()["results"][0]["content"]
soup = BeautifulSoup(content, "html.parser")
```

For now, we are using the default `html.parser`, you can also use a different parser if you want. The soup object will have the parsed HTML content. We will now parse the title, price, and rating from this object.

### 1. Parsing Title

We will use the Google Chrome browser to inspect the HTML properties of the product title. To open the inspect tab, you can right-click on the product title and click "inspect". You will see something similar to the below:
![title](images/wayfair_product_page_title.png)
Based on the HTML property we can write the following code to extract the title of this product:

```python
title = soup.find("h1", {"data-hb-id": "heading"}).text
```

### 2. Parsing Price

We can also extract the price by inspecting the price element and finding the proper class attributes to locate the element.
![price](images/wayfair_product_page_inspect.png)

```python
price = soup.find("div", {"class": "SFPrice"}).find("span", {"class":"oakhm64z_6101"}).text
```

### 3. Parsing Rating

Similarly, we can parse the rating element with the below code:

```python
rating = soup.find("span", {"class": "ProductRatingNumberWithCount-rating"}).text
```

We are using the class attribute of the span element to identify the rating element and extract the text content.

## Step 4 - Exporting Data

Now that we have parsed all the necessary information from the product page, we will start exporting this data in different formats. We will use the pandas library to export the data in CSV and JSON format. We will create a list of dict objects with the parsed data and, create a data frame using the data:

```python
import pandas as pd
data = [{
   "Product Title": title,
   "Price": price,
   "Rating": rating,
   "Link": product_url,
}]
df = pd.DataFrame(data)
```

### 1. Exporting Data in CSV Format

Using the data frame object, we can export the data in a CSV file with a single line of code. Since we don’t need an index we can set the index to False.

```python
df.to_csv("product_data.csv", index=False)
```

Once, we execute this, the script will create a file named "product_data.csv" in the current folder which will contain the product data.

### 2. Exporting Data in JSON Format

Similarly, we can use the data frame to export the data in JSON format. We will pass an additional parameter orient to indicate we want the JSON data in records format.

```python
df.to_json("product_data.json", orient="records")
```

The script will create another file named "product_data.json" in the current folder with the exported JSON data.

## Conclusion

This tutorial taught us how to scrape product data from Wayfair. Following the step-by-step guide, you can extract and analyze product data to gain valuable insights from Wayfair's product pricing strategies, reviews, and ratings. We also learned how to leverage Oxylabs API to scrape data bypassing the anti-bot protection measures. If you have any questions or face any issues get in touch with our 24/7 available support team.
