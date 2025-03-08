import time
import random
import requests
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Pokémon Center product URL
product_url = "https://www.pokemoncenter.com/product-url-here"

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")  # Helps avoid bot detection
options.headless = False  # Keep browser visible for manual CAPTCHA
driver = webdriver.Chrome(options=options)

# Function to log in
def login():
    print("[INFO] Logging in...")
    
    driver.get("https://www.pokemoncenter.com/account/login")

    email_field = driver.find_element(By.ID, "email")
    email_field.send_keys("your-email@example.com")  # Replace with your email

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("yourpassword")  # Replace with your password

    login_button = driver.find_element(By.XPATH, '//button[contains(text(), "Sign In")]')
    login_button.click()

    time.sleep(3)
    print("[INFO] Logged in successfully!")

# Function to manually solve CAPTCHA
def solve_recaptcha_manually():
    print("[INFO] CAPTCHA detected! Please solve it manually in the browser.")
    input("Press Enter after solving the CAPTCHA manually...")
    print("[INFO] Continuing bot execution...")

# Function to check stock with smart refresh delay
def check_stock():
    driver.get(product_url)
    
    try:
        add_to_cart_button = driver.find_element(By.XPATH, '//button[contains(text(), "Add to Cart")]')
        return True
    except:
        return False

# Function to add item to cart and checkout
def auto_buy():
    driver.get(product_url)

    # Click Add to Cart
    add_to_cart_button = driver.find_element(By.XPATH, '//button[contains(text(), "Add to Cart")]')
    add_to_cart_button.click()
    time.sleep(2)

    # Solve CAPTCHA manually if required
    solve_recaptcha_manually()

    # Proceed to checkout
    driver.get("https://www.pokemoncenter.com/cart")
    checkout_button = driver.find_element(By.XPATH, '//button[contains(text(), "Checkout")]')
    checkout_button.click()

    print("[INFO] Proceeding to payment!")

# Function to introduce random delays (to avoid bans)
def smart_refresh_delay():
    delay = random.randint(10, 30)  # Random delay between 10-30 seconds
    print(f"[INFO] Waiting {delay} seconds before next refresh to avoid detection...")
    time.sleep(delay)

# Start the bot
login()  # Log in first

# Limit stock checking to 50 attempts to avoid bans
for i in range(50):
    if check_stock():
        print("[INFO] Item in stock! Buying now...")
        auto_buy()
        break
    else:
        print(f"[INFO] Attempt {i+1}/50: Still out of stock... retrying.")
    
    smart_refresh_delay()  # Introduce a random delay

print("[INFO] Stopping bot. Product not available after 50 tries.")
driver.quit()  # Close browser when done
