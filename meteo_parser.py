from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

siteUrl = "https://meteolabs.org/погода_хабаровск/завтра/"
driver.get(siteUrl)

print("Starting...")
while True:
    try:
        time.sleep(0.1)
        weather = driver.find_element(By.CLASS_NAME, "wthSBlock__commonWth").text
        print(weather)
    except Exception as e:
        print("exception")
