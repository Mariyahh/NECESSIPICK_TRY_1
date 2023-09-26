
from typing import Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from django.shortcuts import render
import time
from pymongo import MongoClient
from chatbot_module import generate_description



# Your webdriver path and Chrome options
webdriver_path = r'C:\Users\jenne\Desktop\chromedriver_win32\chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument(f"webdriver.chrome.driver={webdriver_path}")

# Connect to MongoDB
client = MongoClient('mongodb+srv://capstonesummer1:9Q8SkkzyUPhEKt8i@cluster0.5gsgvlz.mongodb.net/')
db = client['Product_Comparison_System']
collection = db['NP_Final_Data']



def scrape_website_1(url,category):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html_content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')
    product_containers = soup.find_all('div', class_='product-small')

    product_details = []

    for container in product_containers:
        image_element = container.find('img', class_='attachment-woocommerce_thumbnail')
        image = image_element['src'] if image_element else ''

        title_element = container.find('p', class_='name')
        title = title_element.a.text.strip() if title_element and title_element.a else ''

        url_element = container.find('a', class_='woocommerce-LoopProduct-link')
        url = url_element['href'] if url_element else ''

        original_price_element = container.find('span', class_='price').find('bdi')
        original_price = original_price_element.text.strip() if original_price_element else ''
        
        discounted_price_element = container.find('ins').find('bdi') if container.find('ins') else None
        discounted_price = discounted_price_element.text.strip() if discounted_price_element else ''

        if any(product['title'] == title for product in product_details):
            continue
       
        description = generate_description(title, original_price)  # Generate description using ChatGPT
        product_id = container.get('id')  # Use the "id" field from MongoDB as the product ID

        product_details.append({
            'id': product_id,
            'image': image,
            'title': title,
            'url': url,
            'category': category,
            'supermarket': 'ShopMetro', 
            'original_price': original_price,
            'discounted_price': discounted_price,
            'description': description,

        })
        collection.insert_one({
            'id': product_id,
            'image': image,
            'title': title,
            'url': url,
            'category': category,
            'supermarket': 'ShopMetro',
            'original_price': original_price,
            'discounted_price': discounted_price,
            'description': description,

        })

    return product_details


def home(request):
    product_details_list = {}
    website_data = [
        {'url': 'https://shopmetro.ph/marketmarket-supermarket/product-category/pantry-essentials/canned-goods/',
         'category': 'Canned Goods'},
        {'url': 'https://shopmetro.ph/marketmarket-supermarket/product-category/pantry-essentials/milk/',
         'category': 'Milk'},
        {'url': 'https://shopmetro.ph/marketmarket-supermarket/product-category/breakfast-world/coffee/',
         'category': 'Coffee'},
        {'url': 'https://shopmetro.ph/marketmarket-supermarket/product-category/pantry-essentials/noodles/',
         'category': 'Noodles'},
        {'url': 'https://shopmetro.ph/marketmarket-supermarket/product-category/home-care/laundry-aids/',
         'category': 'Laundry Aids'},
        {'url': 'https://shopmetro.ph/marketmarket-supermarket/product-category/breakfast-world/bread/',
         'category': 'Bread'},
        {'url': 'https://shopmetro.ph/marketmarket-supermarket/product-category/beverage-wines-liquor-and-spirits/water/',
         'category': 'Water'},
        {'url': 'https://shopmetro.ph/marketmarket-supermarket/?s=candle&post_type=product&type_aws=true&aws_id=1&aws_filter=1&awscat=Form%3A1+Filter%3AAll',
         'category': 'Candle'},
        {'url': 'https://shopmetro.ph/marketmarket-supermarket/product-category/pantry-essentials/condiments/fish-sauce/',
         'category': 'Fish Sauce'},
        {'url': 'https://shopmetro.ph/marketmarket-supermarket/product-category/pantry-essentials/condiments/soy-sauce/',
         'category': 'Soy Sauce'},
        {'url': 'https://shopmetro.ph/marketmarket-supermarket/product-category/pantry-essentials/condiments/vinegar/',
         'category': 'Vinegar'}
        # Add more websites and categories here
    ]

    #for scraping
    """
    product_details_list = []
    for website in website_data:
        category = website['category']
        product_details = scrape_website_1(website['url'], category)
        product_details_list.append(product_details)

    context = {
        'product_details_list': product_details_list,
    }
    return render(request, 'index.html', context)
    """
    #for viewing
    for website in website_data:
        category = website['category']
        products = collection.find({'category': category})
        product_details_list[category] = list(products)
    print(product_details_list)  # Add this line to check the product_details list


    context = {
      # Add the new random products with discounted prices
    }
    return render(request, 'index.html', context)