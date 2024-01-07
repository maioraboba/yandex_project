import time
import sys
# импорт библиотек времени и системы

from selenium import webdriver
from selenium.webdriver.common.by import By
# импорт библиотек selenium для парсинга погоды


# запись данных в удобном для использования виде
def sort_data(data):
    res = []
    first_line = data[::3]
    second_line = data[1::3]
    third_line = data[2::3]
    for i in range(len(first_line)):
        res.append((first_line[i].text, second_line[i].text, third_line[i].text))
    return res


# запись данных температуры в удобном для использования виде
def sort_data_temp(data):
    res = []
    first_line = data[::3]
    second_line = data[1::3]
    third_line = data[2::3]
    for i in range(len(first_line)):
        res.append((first_line[i].text.split()[1], second_line[i].text.split()[1], third_line[i].text.split()[1]))
    return res


# преобразование полученных данных в текст
def format_data(data):
    return [i.text for i in data]


# класс парсера погоды
class Meteo:
    def __init__(self):
        # настройка парсинга сайта без открытия окна браузера
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        # инициализация парсера
        self.driver = webdriver.Chrome(options=option)
        self.siteUrl = "https://meteolabs.org/погода_хабаровск/10_дней/"
        self.driver.get(self.siteUrl)
        # объекты класса и время от начала эпохи
        self.temperature, self.hum, self.temp_parts, self.sunday, self.wind = [None] * 5
        self.date = time.time()

    # получение данных о погоде с сайта и их обработка
    def pars_weather(self):
        print("Starting...")
        try:
            time.sleep(0.1)
            self.temperature = format_data(self.driver.find_elements(By.CLASS_NAME,
                                                                          "wthSBlock__commonWth"))
            self.sunday = sort_data(self.driver.find_elements(By.CLASS_NAME, "sunTime__data"))
            self.temp_parts = sort_data_temp(self.driver.find_elements(By.CLASS_NAME,
                                                                            "wthSBlock__interdayItem"))
            self.wind = format_data(self.driver.find_elements(By.CLASS_NAME, "wthSBlock__paramVal")[::4])
            self.hum = format_data(self.driver.find_elements(By.CLASS_NAME, "wthSBlock__paramVal")[2::4])
            return self.return_pars()

        except Exception:
            print("Ошибка получения данных погоды.")

    # функция возвращает финальный словарь с данными для использования в основном коде
    def return_pars(self):
        data_weather = dict()
        for i in range(len(self.temperature)):
            date_today = self.date + i * 86400
            mon, day = str(time.localtime(date_today).tm_mon), str(time.localtime(date_today).tm_mday)
            if len(mon) == 1:
                mon = '0' + mon
            if len(day) == 1:
                day = '0' + day
            date_today = (f'{time.localtime(date_today).tm_year}_{mon}_'
                          f'{day}')
            data_weather[date_today] = {'temperature': self.temperature[i], 'sunday': self.sunday[i],
                                        'temp_parts': self.temp_parts[i], 'wind': self.wind[i], 'hum': self.hum[i]}
        return data_weather


if __name__ == '__main__':
    ex = Meteo()
    sys.exit()
