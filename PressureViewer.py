#!/usr/bin/python3
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui, uic
import pyqtgraph as pg
from mks640 import MKS640

class PressureViewer():

	def __init__(self, controller=None):
		if controller is None:
			self.controller = MKS640()
		else:
			self.controller = controller
		self.app = QtGui.QApplication([])
		self.ui = uic.loadUi("/home/xmas/Documents/Python/xmas/controllers/mks640.ui")
		self.plot_ui = uic.loadUi("/home/xmas/Documents/Python/xmas/controllers/mks640_plot.ui")
		self.plot_ui.shown = True
		plot_closeEvent = self.plot_ui.closeEvent
		def closeEvent_plot(*args):
			self.plot_ui.shown = False
			plot_closeEvent(*args)
		self.plot_ui.closeEvent = closeEvent_plot

		self.debug()

		self.plot_last_curve = pg.PlotCurveItem()
		self.plot_full_curve = pg.PlotCurveItem()
		self.plot_ui.plot_last.addItem(self.plot_last_curve)
		self.plot_ui.plot_full.addItem(self.plot_full_curve)
		self.ui.setWindowTitle("MKS640 Pressure Controller")
		self.ui.control_dial.setMaximum(self.controller.max_pressure)
		self.ui.show()
		self.plot_ui.show()

		self.ui.open_button.clicked.connect(self.open_cb)
		self.ui.close_button.clicked.connect(self.close_cb)
		self.ui.control_button.clicked.connect(self.control_cb)
		self.ui.control_dial.valueChanged.connect(self.set_cb)
		self.ui.reset_button.clicked.connect(self.reset)
		self.ui.show_button.clicked.connect(self.show_plot)

		self.reset()

		self.timer = pg.QtCore.QTimer()
		self.timer.timeout.connect(self.update_plot)
		self.timer.start(5)

		self.lcd_timer = pg.QtCore.QTimer()
		self.lcd_timer.timeout.connect(self.update_lcd)
		self.lcd_timer.start(1000)
        
		self.app.exec_()

	def show_plot(self):
		self.plot_ui.shown = True
		self.plot_ui.show()

	def reset(self):
		self.len = 100
		self.ptr = 0
		self.pressures = np.empty(self.len)

	def update_lcd(self):
		self.ui.pressure_lcd.display(int(self.last_pressure))

	def debug(self):
		timeout, self.controller.dev.timeout = self.controller.dev.timeout, 0.06
		while True:
			try:
				self.controller.get_pressure()
				break
			except TimeoutError:
				pass
		self.controller.dev.timeout = timeout

	def update_plot(self):
		self.last_pressure = self.controller.get_pressure()
		self.pressures[self.ptr] = self.last_pressure
		self.ptr += 1
		if self.ptr >= self.len:
			self.len *= 2
			if self.len >= 100 * 2**14:
				self.reset()
			else:
				pressures = np.empty(self.len)
				pressures[:self.ptr] = self.pressures
				self.pressures = pressures
		if self.plot_ui.shown:
			self.plot_last_curve.setData(self.pressures[max(0,self.ptr-200):self.ptr])
			self.plot_full_curve.setData(self.pressures[:self.ptr])
		
	def button_on(self, button):
		if button.isChecked(): button.toggle()

	def button_off(self, button):
		if not button.isChecked(): button.toggle()
		
	def open_cb(self):
		self.controller.open_valve()
		self.ui.open_button.setEnabled(False)
		self.ui.close_button.setEnabled(True)
		self.button_on(self.ui.close_button)
		self.ui.control_button.setEnabled(True)
		self.button_on(self.ui.control_button)
		
	def close_cb(self):
		self.controller.close_valve()
		self.ui.open_button.setEnabled(True)
		self.button_on(self.ui.open_button)
		self.ui.close_button.setEnabled(False)
		self.ui.control_button.setEnabled(True)
		self.button_on(self.ui.control_button)
		
	def control_cb(self):
		self.controller.control_pressure(self.ui.control_dial.value())
		self.ui.open_button.setEnabled(True)
		self.button_on(self.ui.open_button)
		self.ui.close_button.setEnabled(True)
		self.button_on(self.ui.close_button)
		self.ui.control_button.setEnabled(False)

	def set_cb(self):
		self.controller.set_pressure(self.ui.control_dial.value())

if __name__ == "__main__":
    pviewer = PressureViewer()