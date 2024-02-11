import sys
import json
import time
import numpy
import pyautogui
from loguru import logger
from pynput import keyboard
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow
from calypso.backend.snare import Snare, pretty_print_dist, location_to_str


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.X11BypassWindowManagerHint
        )

        # Set the window size
        self.resize(450, 160)

        self.setWindowOpacity(0.7)
        self.setStyleSheet("background:transparent")

        self.label_1 = QtWidgets.QLabel("Macro key: None", self)
        self.label_1.setStyleSheet("color: yellow")
        self.label_1.resize(430, 20)  # Set an initial size for the label
        self.label_1.move(10, 0)

        self.label_2 = QtWidgets.QLabel("", self)
        self.label_2.setStyleSheet("color: yellow")
        self.label_2.resize(430, 20)  # Set an initial size for the label
        self.label_2.move(10, 20)

        sep = QtWidgets.QLabel("-" * 100, self)
        sep.setStyleSheet("color: yellow")
        sep.resize(430, 20)  # Set an initial size for the label
        sep.move(10, 40)

        self.label_3 = QtWidgets.QLabel("", self)
        self.label_3.setStyleSheet("color: yellow")
        self.label_3.resize(430, 20)  # Set an initial size for the label
        self.label_3.move(10, 60)

        self.label_4 = QtWidgets.QLabel("", self)
        self.label_4.setStyleSheet("color: yellow")
        self.label_4.resize(430, 20)  # Set an initial size for the label
        self.label_4.move(10, 80)

        self.label_5 = QtWidgets.QLabel("", self)
        self.label_5.setStyleSheet("color: yellow")
        self.label_5.resize(430, 20)  # Set an initial size for the label
        self.label_5.move(10, 100)

        self.label_6 = QtWidgets.QLabel("", self)
        self.label_6.setStyleSheet("color: yellow")
        self.label_6.resize(430, 20)  # Set an initial size for the label
        self.label_6.move(10, 120)

        self.label_7 = QtWidgets.QLabel("", self)
        self.label_7.setStyleSheet("color: yellow")
        self.label_7.resize(430, 20)  # Set an initial size for the label
        self.label_7.move(10, 140)

        self.alignBottomRight()

        # Start listening for the key press in the background
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

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
            self.label_1.setText(f"Macro key: {self.key}")
            return

        try:
            match key:
                case self.key:
                    self.perform_macro()
                case keyboard.Key.f11:
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
