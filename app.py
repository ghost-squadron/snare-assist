import json
import sys
import time

import numpy
import pyautogui
from loguru import logger
from pynput import keyboard
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QLabel,
    QMainWindow,
    QMessageBox,
)

from calypso.backend.snare import Snare, location_to_str, pretty_print_dist

WIDTH = 450
HEIGHT = 160

ROUTE_KEY = keyboard.Key.f11


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.X11BypassWindowManagerHint
        )

        self.setWindowTitle("Press a Key")

        # Create a label to display the prompt
        self.prompt_label = QLabel(
            "Press the key you want to use for macro activation", self
        )
        self.prompt_label.setStyleSheet("color: yellow; font-size: 18px;")
        self.prompt_label.setAlignment(QtCore.Qt.AlignCenter)
        self.prompt_label.resize(WIDTH - 20, 40)
        self.prompt_label.move(10, 60)

        self.label_1 = QtWidgets.QLabel("", self)
        self.label_1.setStyleSheet("color: yellow")
        self.label_1.resize(WIDTH - 20, 20)  # Set an initial size for the label
        self.label_1.move(10, 0)

        self.label_2 = QtWidgets.QLabel("", self)
        self.label_2.setStyleSheet("color: yellow")
        self.label_2.resize(WIDTH - 20, 20)  # Set an initial size for the label
        self.label_2.move(10, 20)

        self.sep = QtWidgets.QLabel("", self)
        self.sep.setStyleSheet("color: yellow")
        self.sep.resize(WIDTH - 20, 20)  # Set an initial size for the label
        self.sep.move(10, 40)

        self.label_3 = QtWidgets.QLabel("", self)
        self.label_3.setStyleSheet("color: yellow")
        self.label_3.resize(WIDTH - 20, 20)  # Set an initial size for the label
        self.label_3.move(10, 60)

        self.label_4 = QtWidgets.QLabel("", self)
        self.label_4.setStyleSheet("color: yellow")
        self.label_4.resize(WIDTH - 20, 20)  # Set an initial size for the label
        self.label_4.move(10, 80)

        self.label_5 = QtWidgets.QLabel("", self)
        self.label_5.setStyleSheet("color: yellow")
        self.label_5.resize(WIDTH - 20, 20)  # Set an initial size for the label
        self.label_5.move(10, 100)

        self.label_6 = QtWidgets.QLabel("", self)
        self.label_6.setStyleSheet("color: yellow")
        self.label_6.resize(WIDTH - 20, 20)  # Set an initial size for the label
        self.label_6.move(10, 120)

        self.label_7 = QtWidgets.QLabel("", self)
        self.label_7.setStyleSheet("color: yellow")
        self.label_7.resize(WIDTH - 20, 20)  # Set an initial size for the label
        self.label_7.move(10, 140)

        self.alignCenter()

        # Set the window size
        self.resize(WIDTH, HEIGHT)

        self.setWindowOpacity(0.7)
        self.setStyleSheet("background:transparent")

        # Start listening for the key press in the background
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

    def start(self):
        self.prompt_label.setText("")
        self.label_1.setText(f"Macro key: {self.key}")
        self.sep.setText("-" * 100)
        self.alignBottomRight()

    def alignCenter(self):
        # Use QDesktopWidget to get the desktop information
        desktop = QApplication.desktop()

        # Get the primary screen's geometry
        screenGeometry = desktop.screenGeometry(desktop.primaryScreen())

        # Calculate the x and y positions for the center of the primary screen
        x = screenGeometry.x() + (screenGeometry.width() - WIDTH) // 2
        y = screenGeometry.y() + (screenGeometry.height() - HEIGHT) // 2

        self.move(x, y)  # Move the window to the center

    def alignBottomRight(self):
        # Use QScreen to get the geometry of the primary screen
        screenGeometry = QApplication.primaryScreen().geometry()

        # Calculate the x and y positions for the bottom-right corner
        x = screenGeometry.width() - self.width() + screenGeometry.x()
        y = screenGeometry.height() - self.height() + screenGeometry.y()

        self.move(x, y)  # Move the window to the bottom right

    def mousePressEvent(self, event):
        QtWidgets.qApp.quit()

    def update_route(self):
        if "location" in self.__dict__ and "snare" in self.__dict__:
            logger.info("Updating route")
            route = self.snare.get_route(self.location)

            if not route:
                self.label_3.setText("WARNING: Inside physics grid!")
            else:
                self.label_3.setText(
                    f"Route: {location_to_str(self.snare.source)} -> {location_to_str(self.snare.destination)}"
                )
                self.label_4.setText(
                    "✅ Within snare cone!"
                    if route.snare_cone_dist < 0
                    else f"❌ {pretty_print_dist(route.snare_cone_dist)} outside snare cone!"
                )
                self.label_5.setText(
                    f"Travel {pretty_print_dist(abs(route.z_mag))} {route.z_dir}"
                )
                self.label_6.setText(
                    f"Travel {pretty_print_dist(abs(route.s_mag))} {route.s_dir}"
                )
                self.label_7.setText(
                    f"Finally, to optimal pullout: {pretty_print_dist(abs(route.f_mag))} {route.f_dir}"
                )

    def on_press(self, key):
        if "key" not in self.__dict__:
            self.key = key
            self.start()
            return

        try:
            match key:
                case self.key:
                    self.perform_macro()
                case ROUTE_KEY:
                    value = QApplication.clipboard().text().strip()
                    if " -> " in value:
                        source, destination = value.split(" -> ")
                        self.snare = Snare(source.strip(), destination.strip())
                        self.update_route()

        except AttributeError:
            pass  # Handle other special keys here if you like

    def perform_macro(self):
        logger.info("Performing macro.")
        pyautogui.press("enter")  # Press Enter
        time.sleep(0.1)
        pyautogui.hotkey("shift", "7")  # Press Shift+7 to type "/"
        pyautogui.write("showlocation", interval=0.001)  # Type the rest of the command
        pyautogui.press("enter")  # Press Enter again
        time.sleep(1)
        value = QApplication.clipboard().text()
        if value.startswith("Coordinates: x:"):
            self.location = numpy.array(
                [float(l.split(":")[-1]) for l in value.split()[1:]]
            )
            self.label_2.setText(f"Location: {self.location}")
            self.update_route()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MainWindow()
    mywindow.show()
    app.exec_()
