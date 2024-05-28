from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from .models import Product
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.common.exceptions import NoSuchElementException,TimeoutException


class DataCollectingView(APIView):
    def post(self, request, product_name):
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )  # Ensure ChromeDriverManager is used correctly
        url = f"https://shop.sprouts.com/search?search_term={product_name}"
        driver.get(url)
        driver.maximize_window()

        wait = WebDriverWait(driver, 10)  # Set a 10-second timeout

        time.sleep(5)

        try:
            element = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "icon-delete"))
            )
            if element:
                element.click()
        except NoSuchElementException:
            pass
        try:
                products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.product-wrapper')))

                # Click on the first product to open the modal (you can modify this to click any specific product)
                products[0].click()
                time.sleep(5)
                # Wait for the modal to be visible
                prd=wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-jzzf3p')))
                time.sleep(14)
                element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "css-qx8mhw")))

        # Get the outer HTML of the element
                element_html = element.get_attribute('outerHTML')

                element_html = element.get_attribute('outerHTML')

                # Print the HTML content

                if element_html:
                            full_url =  element.get_attribute("href")
                            print("Full URL:", full_url)
                else:
                            print("Href value is None")

                try:
                    close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="modal-close-button"]')))
                    close_button.click()
                    print("Modal closed successfully.")
                except (NoSuchElementException, TimeoutException) as e:
                        print("Error while closing the modal:", e)            

        except (NoSuchElementException) as e:
                print("Error:", e)

        # Scrape the HTML content of the modal

        self.slow_scroll(driver)

        time.sleep(2)  

        max_page_number = self.get_max_page_number(driver.page_source)


        product_collection = []
        for page_number in range(1, max_page_number + 1):
            url = f"https://shop.sprouts.com/search?search_term={product_name}&page={page_number}"
            driver.get(url)

            wait = WebDriverWait(driver, 10)  
            time.sleep(5)

            try:
                element = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "icon-delete"))
                )
                if element:
                    element.click()
            except NoSuchElementException:
                pass
        
            self.slow_scroll(driver)

            time.sleep(2)  
            products = wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "css-1u1k9gp"))
            )
            for product in products:
                product_extracted = self.extract_products(
                    product, url, product_search=product_name
                )
                if product_extracted: 
                    product_collection.extend(product_extracted)

        driver.quit()
       
        if product_collection:
            df = pd.DataFrame(product_collection)
            self.save_to_db(df)
            return Response(product_collection, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "No products found"}, status=status.HTTP_204_NO_CONTENT
            )

    def extract_products(self, product_list, url, product_search):
        products = [] 
        try:
            name_tag = product_list.find_element(By.CLASS_NAME, "css-15uwigl")
        except NoSuchElementException:
            name_tag = None

        try:
            quantity_tag = product_list.find_element(By.CLASS_NAME, "css-1kh7mkb")
        except NoSuchElementException:
            quantity_tag = None

        try:
            price_tag = product_list.find_element(By.CLASS_NAME, "css-coqxwd")
        except NoSuchElementException:
            price_tag = None

        try:
            img_tag = product_list.find_element(By.CLASS_NAME, "css-1eer7o2")
            img_src = img_tag.get_attribute("src")
        except NoSuchElementException:
            img_src = None

        try:
            discounted_price_tag = product_list.find_element(By.CLASS_NAME, "css-7k236")
        except NoSuchElementException:
            discounted_price_tag = None

        if (
            name_tag
            and img_src
            and str(product_search).lower() in name_tag.text.lower()
        ):
            
           

                    indx = name_tag.text.lower().index(product_search.lower())
                    if indx == 0 or name_tag.text[indx-1] == " ":  

                        title = name_tag.text.split('(')[0].strip()
                       
                             
                        quantity, unit, price_per_unit = self.extract_quantity_and_unit(
                            quantity_tag.text if quantity_tag else "",
                            price_tag.text if price_tag else "",
                        )
                        price, discounted_price = self.extract_prices(
                             
                            price_tag.text if price_tag else "",
                            discounted_price_tag.text if discounted_price_tag else ""
                        )
                        img_url = str(img_src).strip()
                        product_url = url

                        if title and img_url:
                            products.append(
                                {
                                    "name": title,
                                    "price": (
                                        discounted_price if discounted_price is not None else price
                                    ),
                                    "stock": True,
                                    "quantity": quantity if quantity else 0.0,
                                    "unit": unit if unit else "",
                                    "price_per_unit": price_per_unit if price_per_unit else "",
                                    "product_url": product_url,
                                    "image_url": img_url,
                                }
                            )
                            return products

    def extract_quantity_and_unit(self, quantity_str, price_str):
        try:
            if not quantity_str:  # Handle empty quantity_str
                print("quantity_str is empty, price_str:", price_str)
                quantity_str = price_str
                quantity = 1

                unit = ''
                found_letter = False
                for char in quantity_str:
                    if char.isalpha():
                        found_letter = True
                        unit += char
                    elif found_letter:
                        break

                price_per_unit = ''
                found_digit = False
                for char in price_str:
                    if char.isdigit() or char == '.':
                        found_digit = True
                        price_per_unit += char
                    elif found_digit and char == ' ':
                        break

            else:
                quantity_match = ''
                quantity_str1=quantity_str.split('(')[0]
                for char in quantity_str1:
                    if char.isdigit() :
                        quantity_match += char
                    else:
                        break
                quantity = float(quantity_match) if quantity_match else None
                
                unit = ''
                for char in quantity_str.split('(')[1]:
                    if char.isalpha():
                        unit += char
                   

                price_per_unit = ''
                found_digit = False
                for char in quantity_str.split('(')[1]:
                    if char.isdigit() or char == '.':
                        price_per_unit += char
                    

        except Exception as e:
            quantity = None
            unit = None
            price_per_unit = None
            print({"exception in quantity extraction": str(e), "price_per_unit": price_per_unit})

        return quantity, unit, price_per_unit

        
    def get_max_page_number(self, page_source):
        soup = BeautifulSoup(page_source, "html.parser")
        pagination_ul = soup.find("ul", class_="pagination")
        if not pagination_ul:
            return 1
        pagination_li = pagination_ul.find_all("li")
        page_numbers = []
        for li in pagination_li:
            button = li.find("button")
            if button and button.text:
                page_number = int(button.text.strip())
                page_numbers.append(page_number)
        max_page_number = max(page_numbers)
        return max_page_number

    def extract_prices(self, price_text, discounted_price_text):
        try:
            price = None
            
            discounted_price = None
            if price_text :
                
                    
                price_text_clean = (
                    price_text.replace("$", "")
                    .replace("/lb", "")
                    .replace("/ea", "")
                    .replace("/oz","")
                    .replace("/ct","")
                    .strip()
                )
                if price_text_clean:

                    price = float(price_text_clean)

           
            if discounted_price_text:
                discounted_price = float(
                    discounted_price_text.replace("/ea", "").strip().replace("$", "")
                )
        except Exception as e:
            print(
                {
                    "exception in price extraction in price": str(e),
                }
            )
        return price, discounted_price

    def slow_scroll(self, driver):
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        scroll_step = 200
        current_position = 0
        while current_position < scroll_height:
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            time.sleep(0.1)
            current_position += scroll_step

    def save_to_db(self, df):
        for index, row in df.iterrows():
            if not Product.objects.filter(name=row["name"]).exists():
                product = Product(
                    name=row["name"],
                    price=row["price"],
                    stock=row["stock"],
                    quantity=row["quantity"],
                    quantity_unit=row["unit"],
                    product_url=row["product_url"],
                    image_url=row["image_url"],
                    price_unit=row["price_per_unit"],
                )
                product.save()
