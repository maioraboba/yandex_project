import sys
import csv
import time
import datetime
# импорт библиотек даты, времени, системы, csv файлов

from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtGui import QPixmap, QFont, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QLabel, QPushButton, QListWidgetItem, QWidget
from PyQt5.QtWidgets import QFileDialog, QMessageBox
# импорт библиотек PyQt

from meteo_parser import Meteo
# импорт парсера сайта с погодой

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
# адаптация интерфейса


# класс окна планировщика
class Planner(QMainWindow):
    def __init__(self):
        super().__init__()
        # переменные экземпляра класса
        self.city_weather_data = dict()
        self.data_plans = dict()
        self.today_data = time.time()
        self.dict_month = {'1': 'января', '2': 'февраля', '3': 'марта', '4': 'апреля',
                           '5': 'мая', '6': 'июня', '7': 'июля', '8': 'августа', '9': 'сентября',
                           '10': 'октября', '11': 'ноября', '12': 'декабря'}
        self.plane, self.time, self.worker, self.date = "", "", "", ""
        self.sc = 1
        self.max_plan_line, self.max_name_line = 33, 27

        # загрузка интерфейса
        try:
            self.name = "plan.ui"
            uic.loadUi(self.name, self)
        except FileNotFoundError:
            print(f"Отсутствует файл {self.name}")

        # загрузка изображений
        self.image_up = QPixmap('images/sun_up.png')
        self.image_sun_up.setPixmap(self.image_up)

        self.image_down = QPixmap('images/sun_down.png')
        self.image_sun_down.setPixmap(self.image_down)

        self.image_update = QIcon('images/updat.png')
        self.updat.setIcon(self.image_update)

        # привязка кнопок планировщика
        self.updat.clicked.connect(self.update_list)
        self.clear_list.clicked.connect(self.clear_plans)
        self.put_csv.clicked.connect(self.put_csvfile)
        self.take_csv.clicked.connect(self.save_csvfile)
        self.addEventBtn.clicked.connect(self.push_plan)

        # инициализация парсера и получение данных о погоде на 10 дней
        meteo = Meteo()
        today_forecast = meteo.pars_weather()
        self.city_weather_data.update(today_forecast)

        # инициализация строки состояния
        self.statusbar = self.statusBar()
        self.statusBar().setFont(QFont('Times', 12))

    # добавление плана в список планов
    def push_plan(self):
        # проверка наличия и размера заполненных полей, иначе вывод пользователю подсказок в строку состояния
        plan_line, name_line = self.lineEdit.text(), self.lineEdit_2.text()
        if plan_line and name_line:
            if len(plan_line) <= self.max_plan_line and len(name_line) <= self.max_name_line:
                # получение данных о погоде
                date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
                plane = self.lineEdit.text()
                time_plan = self.timeEdit.time().toString()
                worker = self.lineEdit_2.text()

                flag_have_not_plan = self.append_plans_to_data([date, plane, time_plan, worker])
                # если такого плана нет в списке, то он добавляется в список
                if flag_have_not_plan:
                    self.statusbar.showMessage('')
                    item = QListWidgetItem()
                    item_widget = QWidget()
                    line_text = QLabel(f'{date} {time_plan}\n'
                                       f'{plane}\n'
                                       f'Выполняет: {worker}')
                    line_push_button = QPushButton("Погода")
                    line_push_button.setObjectName(f'{date}_{time_plan}_{plane}_{worker}_{str(self.sc)}')
                    line_push_button.clicked.connect(self.weather_clicked)

                    del_line = QPushButton("X")
                    del_line.setObjectName(str(self.sc))
                    del_line.clicked.connect(self.del_clicked)

                    item_layout = QHBoxLayout()
                    item_layout.addWidget(line_text)
                    item_layout.addWidget(line_push_button)
                    item_layout.addWidget(del_line)
                    item_widget.setLayout(item_layout)
                    item.setSizeHint(item_widget.sizeHint())

                    self.ListWidget.addItem(item)
                    self.ListWidget.setItemWidget(item, item_widget)
                    self.sc += 1
                    self.update_list()
                else:
                    self.statusbar.showMessage('Такая задача уже записана!')
            elif len(name_line) > self.max_name_line:
                self.statusbar.showMessage(f'Длина имени выполняющего должна быть меньше {self.max_name_line} символов')
            else:
                self.statusbar.showMessage(f'Длина задачи должна быть меньше {self.max_plan_line} символов')
        elif not self.lineEdit_2.text():
            self.statusbar.showMessage('Введите имя выполняющего.')
        else:
            self.statusbar.showMessage('Введите задачу.')

    # проверка на наличие плана в списке
    def append_plans_to_data(self, plan):
        line = dict()
        line['date'], line['plane'], line['time'], line['worker'] = plan
        if line not in self.data_plans.values():
            self.data_plans[self.sc] = line
            return True
        return False

    # запись плана из csv файла
    def push_csv(self):
        flag = self.append_plans_to_data([self.date, self.plane, self.time, self.worker])
        if flag:
            item = QListWidgetItem()
            item_widget = QWidget()
            line_text = QLabel(f'{self.date} {self.time}\n'
                               f'{self.plane}\n'
                               f'Выполняет: {self.worker}')
            line_push_button = QPushButton("Погода")
            line_push_button.setObjectName(f'{self.date}_{self.time}_{self.plane}_{self.worker}_{str(self.sc)}')
            line_push_button.clicked.connect(self.weather_clicked)

            del_line = QPushButton("X")
            del_line.setObjectName(str(self.sc))
            del_line.clicked.connect(self.del_clicked)

            item_layout = QHBoxLayout()
            item_layout.addWidget(line_text)
            item_layout.addWidget(line_push_button)
            item_layout.addWidget(del_line)
            item_widget.setLayout(item_layout)
            item.setSizeHint(item_widget.sizeHint())

            self.ListWidget.addItem(item)
            self.ListWidget.setItemWidget(item, item_widget)
            self.sc += 1

    # проверка наличия данных о погоде в день плана
    def weather_clicked(self):
        # получение названия кнопки, которое содержит информацию о плане
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
        button_info = push_button.objectName()
        day_weather = "_".join(button_info[:10].split("-"))
        print(f'click: {day_weather}')

        if day_weather in self.city_weather_data.keys():
            self.put_info(day_weather)
        else:
            self.put_default()
            self.statusbar.showMessage('Прогноз погоды на данный день отсутствует.')

        dw = day_weather.split("_")
        dw = f"{int(dw[2])} {self.dict_month[str(int(dw[1]))]} {dw[0]} года"
        self.weather_printed.setText(dw)

        self.update_list()

    # запись информации о погоде в поля, если есть данные
    def put_info(self, day_weather):
        self.statusbar.showMessage('')

        sunday = self.city_weather_data[day_weather]['sunday']
        self.start_sunday.setText(sunday[0])
        self.end_sunday.setText(sunday[1])
        sd = sunday[2].split()[::2]
        sd.insert(1, "ч")
        sd.insert(3, "мин")
        self.sunday.setText(' '.join(sd))

        temp_parts = self.city_weather_data[day_weather]['temp_parts']
        self.morning_temp.setText(temp_parts[0])
        self.evening_temp.setText(temp_parts[1])
        self.night_temp.setText(temp_parts[2])

        self.wind.setText(self.city_weather_data[day_weather]['wind'])
        self.humidity.setText(self.city_weather_data[day_weather]['hum'])
        self.temperature.setText(self.city_weather_data[day_weather]['temperature'])

    # запись пустых полей, если данных на этот день нет
    def put_default(self):
        self.start_sunday.setText('...')
        self.end_sunday.setText('...')
        self.sunday.setText('         ...')

        self.morning_temp.setText('   ...')
        self.evening_temp.setText('   ...')
        self.night_temp.setText('   ...')

        self.wind.setText('               ...')
        self.humidity.setText('                 ...')
        self.temperature.setText('                 ...')

    # сохранение списка планов в csv
    def save_csvfile(self):
        # проверка на пустоту списка планов
        if self.data_plans:
            fname = QFileDialog.getSaveFileName(self, 'Выберите путь и введите название'
                                                      ' файла для сохранения задач', '')[0]
            if fname[-4:] != '.csv' and fname:
                fname += '.csv'
            if fname:
                # запись в файл, если получено имя
                with open(fname, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=list(self.data_plans[1].keys()), delimiter=';',
                                            quoting=csv.QUOTE_NONNUMERIC)
                    writer.writeheader()
                    for d in self.data_plans.values():
                        writer.writerow(d)
            self.update_list()
        else:
            self.statusbar.showMessage('Таблица пуста!')

    # загрузка планов из csv файла
    def put_csvfile(self):
        # инициализация диалогового окна
        fname = QFileDialog.getOpenFileName(self, 'Выбрать файл для загрузки задач', '', 'Файл (*.csv)')[0]

        if fname:
            message_box = QMessageBox()
            message_box.setText(f'При загрузке нового файла планов будет стерт текущий список.'
                                f' Вы действительно хотите загрузить {fname}?')
            message_box.setIcon(QMessageBox.Question)
            message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            message_box.setDefaultButton(QMessageBox.No)

            ret = message_box.exec()
            if ret == QMessageBox.Yes:
                self.clear_plans()
                self.sc = 1
                with open(fname, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
                    try:
                        for i in reader:
                            self.date = i['date']
                            self.plane = i['plane']
                            self.time = i['time']
                            self.worker = i['worker']
                            self.push_csv()
                    except Exception:
                        print('Файл csv неверного формата!')
            self.update_list()
            self.statusbar.showMessage('')

    # удаление плана из списка задач
    def del_clicked(self):
        sender = self.sender()
        button_key = self.findChild(QPushButton, sender.objectName())
        button_key = int(button_key.objectName())
        keys_plans = list(self.data_plans.keys())
        index_plan = keys_plans.index(button_key)
        self.ListWidget.takeItem(index_plan)
        del self.data_plans[button_key]

        self.sc -= 1
        self.put_default()
        if self.data_plans:
            self.update_list()

    # очистить список задач
    def clear_plans(self):
        self.ListWidget.clear()
        self.data_plans = dict()
        self.sc = 1
        self.put_default()

    # обновление списка задач
    def update_list(self):
        self.today_data = time.time()
        keys_plans = list(self.data_plans.keys())
        for i in keys_plans:
            year, mon, day = list(map(int, self.data_plans[i]['date'].split("-")))
            hour, minute, sec = list(map(int, self.data_plans[i]['time'].split(":")))
            plan_time = datetime.datetime(year, mon, day, hour, minute, sec)
            plan_time = time.mktime(plan_time.timetuple())

            if plan_time < self.today_data:
                index_plan = keys_plans.index(i)
                self.ListWidget.item(index_plan).setBackground(QColor(255, 0, 0))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Planner()
    ex.show()
    sys.exit(app.exec())
