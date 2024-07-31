from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to the downloaded ChromeDriver
chrome_driver_path = r"C:\Users\vekar\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Function to initialize the webdriver
def initialize_webdriver():
    try:
        # Ensure correct installation of ChromeDriver
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

# Prompt the user to enter URLs
source1 = input("Enter the Flipkart URL: ")
source2 = input("Enter the Amazon URL: ")
source3 = input("Enter the Croma URL: ")

# Initialize the Chrome driver
wd = initialize_webdriver()

print("*************************************************************************** \n")
print("                     Starting Program, Please wait ..... \n")

product = "Unknown Product"
r_price = "Not available"
raw_p = "Not available"
raw_c = "Not available"

# Flipkart
print("Connecting to Flipkart")
wd.get(source1)
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

time.sleep(2)

# Amazon
print("Connecting to Amazon")
wd.get(source2)
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

time.sleep(2)

# Croma
print("Connecting to Croma")
wd.get(source3)
try:
    c_price = WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='amount']"))
    )
    raw_c = c_price.text
    print(" ---> Successfully retrieved the price from Croma\n")
except Exception as e:
    print(f"Error retrieving price from Croma: {e}")

time.sleep(2)

# Final display
print("#------------------------------------------------------------------------#")
print(f"Price for [{product}] on all websites, Prices are in INR \n")
print(f"Price available at Flipkart is: {r_price}")
print(f"  Price available at Amazon is: {raw_p}")
print(f"   Price available at Croma is: {raw_c}")

wd.quit()
