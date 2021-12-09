import sys
from functools import partial

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox

from pyui.settings_widget_design import Ui_Form


class SettingsWidget(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

        self.check_box_map = {
            self.maxTempCheckBox: "max temperature",
            self.minTempCheckBox: "min temperature",

            self.descriptionCheckBox: "description",

            self.humidityCheckBox: "humidity",
            self.pressureCheckBox: "pressure",

            self.sunsetCheckBox: "sunset time",
            self.sunriseCheckBox: "sunrise time",
            self.dayLengthCheckBox: "day length",

            self.windSpeedCheckBox: "wind speed",
            self.windAzimuthCheckBox: "wind azimuth",

            self.metricRadioButton: "metric",
            self.imperialRadioButton: "imperial",

            self.trayCheckBox: "tray"
        }

        self.counter = 0

    def initUI(self):
        WIDTH, HEIGHT = 570, 600
        self.setFixedSize(WIDTH, HEIGHT)

        self.setWindowTitle('Settings')
        self.setWindowIcon(QIcon('./assets/icons/settings_icon.png'))

        self.check_boxes = [
            self.maxTempCheckBox, self.minTempCheckBox, self.descriptionCheckBox,
            self.humidityCheckBox, self.pressureCheckBox,
            self.windSpeedCheckBox, self.windAzimuthCheckBox,
            self.sunsetCheckBox, self.sunriseCheckBox, self.dayLengthCheckBox
        ]

        self.metricRadioButton.setChecked(True)  # default value

        self.allCheckBox.stateChanged.connect(self.select_all)

        for check_box in self.check_boxes:
            check_box.stateChanged.connect(partial(self.count, check_box))

    def count(self, check_box: QCheckBox):
        if check_box.isChecked():
            self.counter += 1
        else:
            self.counter -= 1

        if self.counter == len(self.check_boxes):
            self.allCheckBox.setChecked(True)
        else:
            self.allCheckBox.setChecked(False)

    def select_all(self):
        if self.allCheckBox.isChecked():
            for check_box in self.check_boxes:
                check_box.setChecked(True)
        elif self.counter == len(self.check_boxes):
            for check_box in self.check_boxes:
                check_box.setChecked(False)

    def get_selected_parameters(self):
        selected = []
        keys = []

        for check_box in self.check_boxes:
            if check_box.isChecked():
                selected.append(check_box)

        for check_box in selected:
            keys.append(self.check_box_map[check_box])

        return keys

    def get_units(self):
        if self.metricRadioButton.isChecked():
            return "metric"

        return "imperial"


if __name__ == '__main__':
    app = QApplication(sys.argv)

    settings = SettingsWidget()
    settings.show()

    sys.exit(app.exec_())
