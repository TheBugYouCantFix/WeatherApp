import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

from pyui.favorite_cities_widget import Ui_Form

from db_manager import DbManager

from functools import partial


class FavoriteCities(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

        self.db = DbManager()

        self.city_buttons = []
        self.delete_buttons = []

    def initUI(self):
        WIDTH, HEIGHT = 570, 600
        self.setFixedSize(WIDTH, HEIGHT)

        self.setWindowTitle('Favorite cities')
        self.setWindowIcon(QIcon('./assets/icons/favorites_icon.png'))

        self.verticalLayoutWidget.setStyleSheet("background-color: rgb(255, 255, 255, 0)")
        self.verticalLayoutWidget_2.setStyleSheet("background-color: rgb(255, 255, 255, 0)")

    @staticmethod
    def clear_layout(layout):
        while layout.count():

            child = layout.takeAt(0)
            child_widget = child.widget()

            if child_widget:
                child_widget.setParent(None)
                child_widget.deleteLater()

    def create_city_button(self, city: str):
        self.city_button = QPushButton(city.capitalize(), self)
        self.city_button.setStyleSheet("""
                            font-size: 18px;
                            background-color: rgb(125, 179, 206);
                        """)

        self.citiesVerticalLayout.addWidget(self.city_button)
        self.city_buttons.append(self.city_button)

    def create_remove_button(self):
        self.delete_button = QPushButton(text='')

        icon = QIcon('./assets/icons/remove_icon.png')
        self.delete_button.setIcon(icon)

        self.delete_button.setStyleSheet("background-color: rgb(125, 179, 206);")

        self.buttonsVerticalLayout.addWidget(self.delete_button)
        self.delete_buttons.append(self.delete_button)

    def display_favorites(self):
        default_city = self.db.get_default_favorite_city()

        for city in self.db.get_favorite_cities():
            city = city[0]

            self.comboBox.addItem(city.capitalize())

            # Creating widgets
            self.create_city_button(city)
            self.create_remove_button()

        if default_city:
            self.comboBox.setCurrentText(default_city.capitalize())

    def add_to_favorites(self, city: str):
        self.create_city_button(city)
        self.create_remove_button()
        self.comboBox.addItem(city.capitalize())

    def remove_favorite_city_and_button(self, index: int):
        city_button = self.city_buttons[index]
        delete_button = self.delete_buttons[index]

        city_name = city_button.text()

        self.citiesVerticalLayout.removeWidget(city_button)
        self.buttonsVerticalLayout.removeWidget(delete_button)
        self.comboBox.removeItem(index)

        city_button.setParent(None)
        delete_button.setParent(None)

        del self.city_buttons[index]
        del self.delete_buttons[index]

        self.db.delete_from_favorites(city_name.lower())

        for i, button in enumerate(self.delete_buttons):
            button.disconnect()
            button.clicked.connect(partial(self.remove_favorite_city_and_button, i))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    fav_cities = FavoriteCities()
    fav_cities.show()

    sys.exit(app.exec_())

