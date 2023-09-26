from django.shortcuts import render
from pymongo import MongoClient


# Connect to MongoDB
client = MongoClient('mongodb+srv://capstonesummer1:9Q8SkkzyUPhEKt8i@cluster0.5gsgvlz.mongodb.net/')
db = client['Product_Comparison_System']
collection = db['NP_Final_Data']


def supermarket_page(request, supermarket_name):
    # Retrieve products from the selected supermarket
    # products = collection.find({'supermarket': supermarket_name})
    all_products =list(collection.find({'supermarket': supermarket_name}))
   
    context = {
        'supermarket_name': supermarket_name,
        'all_products': all_products,
        # 'product_by_category': product_by_category,
    }

    return render(request, 'supermarket/supermarket_page.html', context)



def supermarket_category(request, supermarket_name, category_name):
    categories = collection.distinct('category', {'supermarket': supermarket_name})
    
    # Create a dictionary to store product by category
    product_by_category = {}

    # Retrieve products for each category
    for category in categories:
        products = collection.find({'supermarket': supermarket_name, 'category': category})
        product_by_category[category] = list(products)


    products = collection.find({'supermarket': supermarket_name, 'category': category_name})

    context = {
        'supermarket': supermarket_name,
        'category': category_name,
        'categories': categories,
        'products': products,

    }

    return render(request, 'supermarket/supermarket_category.html', context)



# Add more view functions as needed for other pages related to the supermarket
