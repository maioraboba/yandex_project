from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys


class Meteo:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.siteUrl = "https://meteolabs.org/погода_хабаровск/10_дней/"
        self.driver.get(self.siteUrl)
        self.weather = None
        self.t = None
        self.sunday = None
        self.pars_weather()
        self.wind = None
        self.hum = None

    def pars_weather(self):
        print("Starting...")
        while not self.weather:
            try:
                time.sleep(0.1)
                self.weather = self.driver.find_elements(By.CLASS_NAME, "wthSBlock__commonWth")
                self.t = self.driver.find_elements(By.CLASS_NAME, "wthSBlock__interdayItem")
                self.sunday = self.driver.find_elements(By.CLASS_NAME, "sunTime__data")
                self.t = self.driver.find_elements(By.CLASS_NAME, "wthSBlock__interdayItem")
                self.wind = self.driver.find_elements(By.CLASS_NAME, "wthSBlock__paramVal")[::4]
                self.hum = self.driver.find_elements(By.CLASS_NAME, "wthSBlock__paramVal")[2::4]
                for i in self.hum:
                    print(i.text)
            except Exception as e:
                print("exception")


if __name__ == '__main__':
    ex = Meteo()
    sys.exit()
