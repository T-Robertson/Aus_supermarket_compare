import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver import Keys

class lookup():
    def __init__(self, website1_url, website2_url, item):
        self.price_find = []
        self.urls = [website1_url,website2_url]
        
        self.compare_prices(website1_url, website2_url, item)
        
        
    def get_price(self, website_url, product):
        firefox_options = FirefoxOptions()
        # Uncomment the next line if you want to run the browser in headless mode
        firefox_options.add_argument("--headless")
        
        service = FirefoxService(executable_path='geckodriver.exe')  # Replace with the path to your geckodriver executable
        driver = webdriver.Firefox(service=service, options=firefox_options)

        try:
            driver.get(website_url)
            
            # Wait for the page to load, adjust the timeout as needed
            driver.implicitly_wait(5)
            
            #Enter product 
            try:
                driver.find_element(By.ID, "search-text-input").send_keys(f"{product}", Keys.ENTER)
            except:
                driver.find_element(By.ID, "wx-headerSearch").send_keys(f"{product}", Keys.ENTER)
            # Extract the price element, update this based on the structure of the website
            try:
                price_element = driver.find_element(By.CLASS_NAME, 'price__value')
            except:
                price_element = driver.find_element(By.CLASS_NAME, 'primary')
            
            if price_element:
                price = price_element.get_attribute('aria-label')
                
                if price == None:
                    self.price_find.append(price_element.text.strip())
                else:
                    self.price_find.append(price)
            else:
                self.price_find.append('Price not found')
        except Exception as e:
            return f'Error: {str(e)}'
        finally:
            driver.quit()

    def compare_prices(self, website1_url, website2_url, item):     
        website1 = threading.Thread(target=self.get_price, args=(website1_url, item))
        website2 = threading.Thread(target=self.get_price, args=(website2_url, item))

        website1.start()
        website2.start()
        
        website1.join()
        website2.join()
        
        print(item)
        i = 0
        for price in self.price_find:
            print(f'{self.urls[i]} - {price}')
            i = i + 1

if __name__ == "__main__":
    website1_url = 'https://www.coles.com.au/'  
    website2_url = 'https://www.woolworths.com.au/'
    item = "Cadbury Dairy Milk Marvellous Creations Rocky Road Chocolate Block 190g"
    
    start_time = time.time()
    
    lookup(website1_url, website2_url, item)
    
    end_time = time.time()
    print(f'Time taken: {end_time - start_time} seconds')
