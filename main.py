import sys
from urllib.request import urlopen

from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPalette, QBrush, QShowEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMessageBox, QMenu, QAction, qApp

from qt_material import apply_stylesheet

from pyui.main_window_design import Ui_MainWindow

from settings_widget import SettingsWidget
from favorites_widget import FavoriteCities

from weather_parsing.parsing import get_current_weather_data
from weather_parsing.config import TOKEN

from db_manager import DbManager

import ctypes


class WeatherApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.settings_window = SettingsWidget()
        self.stackedWidget.addWidget(self.settings_window)

        self.favorites_window = FavoriteCities()
        self.stackedWidget.addWidget(self.favorites_window)

        self.db = DbManager()
        self.db.add_all_parameters(list(self.settings_window.check_box_map.values()))  # init parameters

        self.shown = False  # bool for function showEvent

        self.initUI()

        self.set_checked_parameters()

    def initUI(self):
        WIDTH, HEIGHT = 570, 600

        self.setWindowTitle('Weather App')
        self.setFixedSize(WIDTH, HEIGHT)
        self.setWindowIcon(QIcon('./assets/icons/app_icon.png'))

        self.settings_icon = QIcon('./assets/icons/settings_icon.png')
        self.favorites_icon = QIcon('./assets/icons/favorites_icon.png')

        self.settingsPushButton.setIcon(self.settings_icon)
        self.favoritesPushButton.setIcon(self.favorites_icon)

        # Setting background image
        image = QImage('./assets/background.jpg')
        palette = QPalette()
        palette.setBrush(10, QBrush(image))
        self.setPalette(palette)

        THEME = 'light_blue.xml'

        apply_stylesheet(self.lineEdit, THEME)
        apply_stylesheet(self.searchButton, THEME)
        apply_stylesheet(self.settingsPushButton, THEME)
        apply_stylesheet(self.favoritesPushButton, THEME)

        apply_stylesheet(self.settings_window, THEME)
        apply_stylesheet(self.favorites_window, THEME)

        self.init_tray()

        self.searchButton.clicked.connect(self.display_weather_data)
        self.settingsPushButton.clicked.connect(self.open_settings)
        self.settings_window.backLinkButton.clicked.connect(self.back)
        self.addToFavoritesLinkButton.clicked.connect(self.add_to_favorites)
        self.favoritesPushButton.clicked.connect(self.open_favorites)
        self.favorites_window.backLinkButton.clicked.connect(self.back)

        self.favorites_window.comboBox.currentIndexChanged.connect(self.set_default_city)

    def show_default_city(self):
        self.city = self.db.get_default_favorite_city()
        self.lineEdit.setText(self.city)

        if self.city:
            self.lineEdit.setText(self.city.capitalize())
            self.display_weather_data()

    def open_settings(self):
        self.stackedWidget.setCurrentWidget(self.settings_window)

    def back(self):
        if self.stackedWidget.currentWidget() == self.settings_window:
            self.display_weather_data()

        self.stackedWidget.setCurrentWidget(self.weatherApp)

    def change_current_city(self, new_name: str):
        self.back()
        self.city = new_name
        self.lineEdit.setText(new_name)
        self.display_weather_data()

    def get_unit_for_parameter(self, param: str):
        units_map = {
            'humidity': '%',
            'pressure': 'bar',
            'wind azimuth': '°'
        }

        if self.settings_window.get_units() == 'metric':
            units_map['temp'] = '°C'
            units_map['wind speed'] = 'm/sec'
        else:
            units_map['temp'] = '°F'
            units_map['wind speed'] = 'miles/h'

        if param == 'feels like' or 'temp' in param:
            return units_map['temp']

        return units_map.get(param, '')

    def get_string_data(self, d: dict, keys: list) -> str:
        string = ''
        keys = ["temperature", "feels like"] + keys  # default + selected

        for key in keys:
            unit = self.get_unit_for_parameter(key)
            string += f'{key.capitalize()}: {d[key]} {unit}\n'

        return string

    def set_checked_parameters(self):
        selected_parameters = self.db.get_selected_parameters()
        check_box_map = self.settings_window.check_box_map

        if selected_parameters:
            for parameter in selected_parameters:
                parameter = parameter[0]

                for check_box, value in check_box_map.items():
                    if value == parameter:
                        check_box.setChecked(True)

    @staticmethod
    def show_error_message_box(message: str):
        message_box = QMessageBox()
        message_box.setText(message)
        message_box.setWindowTitle("Error")
        message_box.setIcon(QMessageBox.Critical)
        message_box.exec_()

    def get_weather_map_from_input(self):
        self.city = self.lineEdit.text()
        weather_map = get_current_weather_data(self.city, TOKEN, self.settings_window.get_units())

        return weather_map

    def display_weather_data(self):
        weather_map = self.get_weather_map_from_input()

        if type(weather_map) != dict:
            self.show_error_message_box(weather_map)
            return

        style = "border: 1px solid (10, 10, 10)"

        url = weather_map['icon url']
        weather_icon = QPixmap()
        data = urlopen(url).read()
        weather_icon.loadFromData(data)

        self.weatherImageLabel.setPixmap(weather_icon)

        self.dataLabel.setText(self.get_string_data(weather_map, self.settings_window.get_selected_parameters()))

        self.groupBox.setStyleSheet(style)
        self.groupBox.setTitle(f"Results for {weather_map['city']}, {weather_map['country']}")

    def add_to_favorites(self):
        # Check if the city exists
        self.city = self.lineEdit.text().lower()
        weather_map = get_current_weather_data(self.city, TOKEN, self.settings_window.get_units())

        if type(weather_map) != dict:
            self.show_error_message_box(weather_map)
            return

        if not self.db.add_to_favorites(self.city):
            self.favorites_window.add_to_favorites(self.city)

        if not self.db.get_default_favorite_city():
            self.db.set_default(self.city)

    def open_favorites(self):
        self.stackedWidget.setCurrentWidget(self.favorites_window)

        for button in self.favorites_window.city_buttons:
            button.clicked.connect(partial(self.change_current_city, button.text()))

        for index, button in enumerate(self.favorites_window.delete_buttons):
            button.clicked.connect(partial(self.favorites_window.remove_favorite_city_and_button, index))

    def keyPressEvent(self, event):
        key = event.key()
        modifier = int(event.modifiers())

        # 2 different enter keys
        if key == Qt.Key_Enter or key == Qt.Key_Enter - 1:
            self.display_weather_data()

        # Shift + F2 -> settings and back from settings
        if key == Qt.Key_F2 and modifier == Qt.ShiftModifier:
            if self.stackedWidget.currentWidget() == self.weatherApp:
                self.open_settings()
            else:
                self.back()

        # Ctrl + F1 -> favorites and back
        if key == Qt.Key_F1 and modifier == Qt.ShiftModifier:
            if self.stackedWidget.currentWidget() == self.weatherApp:
                self.open_favorites()
            else:
                self.back()

        if key == Qt.Key_S and modifier == Qt.ControlModifier:
            self.add_to_favorites()

    def add_settings_data_to_db(self):
        check_box_map = self.settings_window.check_box_map

        for check_box, value in check_box_map.items():
            if check_box.isChecked():
                self.db.select_parameter(value)
            else:
                self.db.unselect_parameter(value)

    def set_default_city(self):
        city = self.favorites_window.comboBox.currentText().lower()

        if city != self.db.get_default_favorite_city():
            self.db.set_default(city)

        self.show_default_city()

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('./assets/icons/app_icon.png'))

        open_action = QAction("Open", self)
        exit_action = QAction("Exit", self)

        open_action.triggered.connect(self.show)
        exit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu()

        tray_menu.addAction(open_action)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def closeEvent(self, event) -> None:
        self.add_settings_data_to_db()

        # Minimizing the app to tray if the check box is checked
        if self.settings_window.trayCheckBox.isChecked():
            event.ignore()
            self.hide()

            self.tray_icon.showMessage(
                "Tray Program",
                "Application was minimized to Tray",
                QSystemTrayIcon.Information,
                2000
            )

    def showEvent(self, event: QShowEvent) -> None:
        if not self.shown:
            self.favorites_window.display_favorites()
            self.shown = True

        self.show_default_city()
        self.show()


def set_up_taskbar_image():
    # This function lets you display the app icon in the taskbar(which isn't being displayed by default)
    app_id = u'mycompany.myproduct.subproduct.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    # Thank you, StackOverflow users <3


if __name__ == '__main__':
    set_up_taskbar_image()

    app = QApplication(sys.argv)

    wa = WeatherApp()
    wa.show()

    sys.exit(app.exec_())
