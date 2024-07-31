from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib.parse

# Path to the downloaded ChromeDriver
chrome_driver_path = r"C:\Users\vekar\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Function to initialize the webdriver
def initialize_webdriver():
    try:
        service = ChromeService(executable_path=chrome_driver_path)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--start-maximized')
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        exit(1)

# Function to search product on Google and get URLs
def get_product_urls(wd, product_name):
    base_url = "https://www.google.com/search?q="
    search_url = base_url + urllib.parse.quote_plus(product_name)
    wd.get(search_url)
    urls = {"flipkart": None, "amazon": None, "croma": None}
    try:
        results = WebDriverWait(wd, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[@href]"))
        )
        for result in results:
            url = result.get_attribute('href')
            if url:
                if "flipkart.com" in url and not urls["flipkart"]:
                    urls["flipkart"] = url
                elif "amazon.in" in url and not urls["amazon"]:
                    urls["amazon"] = url
                elif "croma.com" in url and not urls["croma"]:
                    urls["croma"] = url
            if all(urls.values()):
                break
    except Exception as e:
        print(f"Error finding URLs on Google: {e}")
    return urls

# Prompt the user to enter the product name
product_name = input("Enter the product name: ")

# Initialize the Chrome driver
wd = initialize_webdriver()

print("*************************************************************************** \n")
print("                     Starting Program, Please wait ..... \n")

product = "Unknown Product"
r_price = "Not available"
raw_p = "Not available"
raw_c = "Not available"

# Google Search
print("Searching on Google")
urls = get_product_urls(wd, product_name)
flipkart_url = urls["flipkart"]
amazon_url = urls["amazon"]
croma_url = urls["croma"]

# Flipkart
if flipkart_url:
    print(f"Connecting to Flipkart: {flipkart_url}")
    wd.get(flipkart_url)
    try:
        f_price = WebDriverWait(wd, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div[1]/div/div[1]'))
        )
        pr_name = WebDriverWait(wd, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span'))
        )
        product = pr_name.text
        r_price = f_price.text
        print(" ---> Successfully retrieved the price from Flipkart \n")
    except Exception as e:
        print(f"Error retrieving price from Flipkart: {e}")
else:
    print(" ---> Flipkart URL not found\n")

time.sleep(2)

# Amazon
if amazon_url:
    print(f"Connecting to Amazon: {amazon_url}")
    wd.get(amazon_url)
    try:
        a_price = WebDriverWait(wd, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[2]'))
        )
        raw_p = a_price.text
        pr_name_amazon = WebDriverWait(wd, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="productTitle"]'))
        )
        product_amazon = pr_name_amazon.text
        if product == "Unknown Product":
            product = product_amazon
        print(" ---> Successfully retrieved the price from Amazon \n")
    except Exception as e:
        print(f"Error retrieving price from Amazon: {e}")
else:
    print(" ---> Amazon URL not found\n")

time.sleep(2)

# Croma
if croma_url:
    print(f"Connecting to Croma: {croma_url}")
    wd.get(croma_url)
    try:
        c_price = WebDriverWait(wd, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='amount']"))
        )
        raw_c = c_price.text
        print(" ---> Successfully retrieved the price from Croma\n")
    except Exception as e:
        print(f"Error retrieving price from Croma: {e}")
else:
    print(" ---> Croma URL not found\n")

time.sleep(2)

# Final display
print("#------------------------------------------------------------------------#")
print(f"Price for [{product}] on all websites, Prices are in INR \n")
print(f"Price available at Flipkart is: {r_price}")
print(f"  Price available at Amazon is: {raw_p}")
print(f"   Price available at Croma is: {raw_c}")

wd.quit()
