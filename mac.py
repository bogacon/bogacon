import requests
import pandas as pd
from bs4 import BeautifulSoup


product_group = {"13854": "Ruj", "13839": "Maskara", "13838": "Eyeliner","13840":"Göz Farı","13844":"Kapatıcı","13847":"Fondoten","13842":"Allık"}
product_name_list=[]
product_id_list=[]
content_list=[]
product_group_list=[]

for key in product_group.keys():
    
    macurl1 = f"https://www.maccosmetics.com.tr/products/{key}"
    r = requests.get(macurl1)
    soup = BeautifulSoup(r.content, "html.parser")

    products = soup.find_all("h3", {"class": "product__name"})
    product_ids = [element.get('data-product-id') for element in soup.find_all(attrs={'data-product-id': True})]
        
    for product in products:
        product_name = product.text.strip().replace(" ", "-")
        product_name_list.append([product_name])
        product_group_list.append([product_group[key]])

    for products_id in product_ids:
        product_id_name = products_id.strip().removeprefix("PROD")    
        product_id_list.append([product_id_name])      

        macurl2 = f"https://www.maccosmetics.com.tr/product/{key}/{product_id_name}"
        r2 = requests.get(macurl2)
        soup2 = BeautifulSoup(r2.content, "html.parser")
        span_elements = soup2.find_all("span", {"class": "js-product-full-iln-listing"})
        
        if not span_elements:
                    
            content_list.extend(["BOS"])
        
        else:
            for span in span_elements:
            
                content = span.text.strip().replace("Ingredients:", "")
                content_list.extend([content])  

df = pd.DataFrame({'Brand':['Mac']* len(product_name_list),'Product': product_name_list,'Group': ['Yüz'] * len(product_name_list),'Group2':product_group_list,'Id': product_id_list,'Content': content_list})
print(df)

df.to_excel("mac_data.xlsx")


