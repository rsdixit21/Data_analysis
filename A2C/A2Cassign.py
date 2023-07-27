import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

!apt install chromium-chromedriver
!pip install selenium
# set options to be headless, ..
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

from google.colab import drive 

# empty list for scrap data
product_link_list = []
ean_sku_list = []
rank_list = []

position_1_list = []
name_list = []
brand_list = []
average_rating_list = []
rating_count_list = []
currency_list = []
price_list = []
sales_price_list = []
fbn_list = []
store_name_list = []
partner_rating_value_list = []
partner_rating_count_list = []

#loop for 61 pages

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}  #header for requests.get


for i in range(1, 62):                                # iterating over number of pages you want to scrap

   # Scraping
  response = requests.get("https://www.noon.com/egypt-en/sports-and-outdoors/exercise-and-fitness/yoga-16328/?limit=50&page={}&sort%5Bby%5D=popularity&sort%5Bdir%5D=desc".format(i), headers = headers)    # get response from page 
  urlinfo = response.content
  soup = BeautifulSoup(urlinfo, 'html.parser')

  class1 = soup.find_all("span", class_="sc-5e739f1b-0 gEERDr wrapper productContainer ")     # find tag from soup content
  
# Product_half_link 
  site_link = "http://www.noon.com"

# Link data list

  for i in range(len(class1)):
    children = class1[i].findChildren("a")
    for child in children:
      child_link = child.get('href')
      product_link_list.append(site_link + child_link)
      
# EAN/SKU data list

      ean_sku = child_link.split("/")[3]
      ean_sku_list.append(ean_sku)

# Rank data list

unique_ean_sku_set = set(ean_sku_list)   #set of unique EAN/SKUs
rank_sum = 0

for i in unique_ean_sku_set:
  for j in ean_sku_list:
    if i == j:
      rank_sum+=1
      rank_list.append(rank_sum)
  rank_sum = 0
      
# scrap other data lists


# Position 1, Name, Brand, Average Rating, Rating Count, Currency, Price, Sales Price, FBN, Store Name, Partner Rating Value , Partner Rating Count

driver = webdriver.Chrome(options=options)   #chromedriver 

for i in range(len(product_link_list)):      # loop for per product lists(Iterate len(product_link_list) times)

  driver.get(product_link_list[i])     #get page info using driver.get

#Scraping data

  # Position 1

  try:
    pos_1 = driver.find_element("xpath",'//div[@class="sc-54ed93c4-2 elMEYP"]').text
    pos_1 = pos_1.split("\n")
    pos_1 = pos_1[::-1][-3:]

    position_1 = "/".join(pos_1) + "/"
    position_1_list.append(position_1)
  except:
    position_1_list.append("None")

  # Name, Brand

  try:
    main_info =driver.find_element("xpath",'//div[@class="sc-c44e3e2d-2 cZCIgF"]').text.split("\n")
    
    if 'USE CODE' in main_info[0]:
      name_list.append(main_info[2])
      brand_list.append(main_info[1])
    elif 'Best Seller' in main_info[0:2]:
      name_list.append(main_info[2])
      brand_list.append(main_info[1])

    else:
      name_list.append(main_info[1])
      brand_list.append(main_info[0])

  except:
    name_list.append("None")
    brand_list.append("None")


  # Average Rating, Rating Count

  try:
    class1 =  driver.find_element("xpath",'//div[@class="sc-c44e3e2d-9 eXovWl"]').text.split("\n")
    average_rating = class1[1]
    rating_count = class1[2].split(" ")[0]
    average_rating_list.append(average_rating)
    rating_count_list.append(rating_count)
  except:
    average_rating_list.append("None")
    rating_count_list.append("None")

  # Currency, Price, Sales Price

  try:
    price_info = driver.find_element("xpath",'//div[@class="sc-bceb34d0-0 geSARh"]').text.split("\n")
    currency = price_info[1].split(" ")[0]
    currency_list.append(currency)
    price = price_info[1].split(" ")[1]
    price_list.append(price)
    sales_price = price_info[3].split(" ")[1]
    sales_price_list.append(sales_price) 
  except:
    sales_price_list.append("None")
  
  # FBN

  try:
    fbn_info = driver.find_element("xpath",'//img[@class="sc-b51db3f-1 bGljQY"]').get_attribute("alt")
    fbn = str(fbn_info).split("-")[1]
    if fbn[0:6] == "market":
      fbn = "market"
    fbn_list.append(fbn)
  except:
    fbn_list.append("None")

  # Store Name

  try:
    store_name = driver.find_element("xpath",'//div[@class="sc-53a159dc-0 jjLefX"]').text
    store_name_list.append(store_name)
  except:
    store_name_list.append("None")

  # Partner Rating Value, Partner Rating Count

  try:
    store_partner_info = driver.find_element("xpath",'//div[@class="sc-d711b2ac-0 hfDBZg"]')
    store_partner_info.click()
    driver.implicitly_wait(1)
    # Partner Rating Value
    partner_rating_value  = driver.find_element("xpath",'//div[@class="sc-f818072d-18 jowpia"]').text
    partner_rating_value_list.append(partner_rating_value)
    # Partner Rating Count
    partner_rating_count = driver.find_element("xpath",'//div[@class="sc-f818072d-22 emzLwZ"]').text
    partner_rating_count_list.append(partner_rating_count)
  except:
    partner_rating_value_list.append("None")
    partner_rating_count_list.append("None")


#  Creating DataFrame from data lists

df = pd.DataFrame(
    {
        'EAN/SKU' : ean_sku_list,
        'Postion 1': position_1_list,
        'Name': name_list,
        'Brand' : brand_list,
        'Average Rating' : average_rating_list,
        'Rating Count' :  rating_count_list,
        'Currency' : currency_list,
        'Store Name' : store_name_list,
        'Partner Rating value' : partner_rating_value_list,
        'Partner Rating Count' : partner_rating_count_list,
        'Price' : price_list,
        'Sales Price' : sales_price_list, 
        'fbn' : fbn_list,
        'Link' : product_link_list
     })




# Adding Date & Time column
df.insert(loc = 0,
          column = 'Date & Time',
          value = pd.Timestamp.today().strftime('%d-%b-%Y'))

# Adding Rank Column

df.sort_values(by=['EAN/SKU'], inplace=True) #sort DataFrame values using EAN/SKU column

df.insert(loc = 14,
          column = 'Rank',
          value = rank_list)

# Saving data file to google drive

drive.mount('/content/drive')
df.to_csv("/content/drive/MyDrive/Assignment/A2C/assignment_output.csv", index=False)
