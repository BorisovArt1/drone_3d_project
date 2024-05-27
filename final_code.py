import random

from PyQt5 import QtWidgets
from direct.showbase.ShowBase import ShowBase
from PyQt5.QtCore import Qt, QTimer
from panda3d.core import *
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QPushButton, QSlider,
                             QVBoxLayout, QWidget,
                             QHBoxLayout, QMessageBox, QCheckBox,
                             )
import sys
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        filename = "Data"
        with open(filename, 'w') as file:
            file.truncate()

        self.setWindowTitle("Project")
        self.setGeometry(400, 600, 600, 700)

        widget = QWidget()
        self.setCentralWidget(widget)

        self.button_start = QPushButton("Старт", self)
        self.button_start.clicked.connect(self.start_message)

        self.button_save = QPushButton("Применить данные", self)
        self.button_save.clicked.connect(self.data_save)

        self.weight = QSlider()
        self.weight.setOrientation(Qt.Horizontal)
        self.weight.setRange(1, 6)
        self.weight.setTickPosition(QSlider.TicksAbove)
        self.weight.valueChanged.connect(self.update_weight)
        self.result_label_weight = QLabel('')

        self.length = QSlider()
        self.length.setOrientation(Qt.Horizontal)
        self.length.setRange(200, 1800)
        self.length.setTickPosition(QSlider.TicksAbove)
        self.length.valueChanged.connect(self.update_length)
        self.result_label_length = QLabel('')

        self.q_width = QSlider()
        self.q_width.setOrientation(Qt.Horizontal)
        self.q_width.setRange(100, 700)
        self.q_width.setTickPosition(QSlider.TicksAbove)
        self.q_width.valueChanged.connect(self.update_q_width)
        self.result_label_q_width = QLabel('')

        self.q_heigth = QSlider()
        self.q_heigth.setOrientation(Qt.Horizontal)
        self.q_heigth.setRange(100, 700)
        self.q_heigth.setTickPosition(QSlider.TicksAbove)
        self.q_heigth.valueChanged.connect(self.update_q_heigth)
        self.result_label_q_heigth = QLabel('')

        layout = QVBoxLayout()

        layout_q_weight = QHBoxLayout()
        layout_q_weight.addWidget(QLabel("Масса: "))
        layout_q_weight.addWidget(self.weight)
        layout.addLayout(layout_q_weight)
        layout_result_label_weight = QHBoxLayout()
        layout_result_label_weight.addWidget(self.result_label_weight)
        layout.addLayout(layout_result_label_weight)

        layout_q_length = QHBoxLayout()
        layout_q_length.addWidget(QLabel("Длина: "))
        layout_q_length.addWidget(self.length)
        layout.addLayout(layout_q_length)
        layout_result_label_q_length = QHBoxLayout()
        layout_result_label_q_length.addWidget(self.result_label_length)
        layout.addLayout(layout_result_label_q_length)

        layout_qq_width = QHBoxLayout()
        layout_qq_width.addWidget(QLabel("Ширина: "))
        layout_qq_width.addWidget(self.q_width)
        layout.addLayout(layout_qq_width)
        layout_result_label_qq_width = QHBoxLayout()
        layout_result_label_qq_width.addWidget(self.result_label_q_width)
        layout.addLayout(layout_result_label_qq_width)

        layout_qq_heigth = QHBoxLayout()
        layout_qq_heigth.addWidget(QLabel("Высота: "))
        layout_qq_heigth.addWidget(self.q_heigth)
        layout.addLayout(layout_qq_heigth)
        layout_result_label_qq_heigth = QHBoxLayout()
        layout_result_label_qq_heigth.addWidget(self.result_label_q_heigth)
        layout.addLayout(layout_result_label_qq_heigth)

        layout.addWidget(self.button_save)
        layout.addWidget(self.button_start)

        widget.setLayout(layout)
        self.show()

    def update_weight(self, value):
        self.result_label_weight.setText(f'Масса: {value}')

    def update_length(self, value):
        self.result_label_length.setText(f'Длина: {value}')

    def update_q_width(self, value):
        self.result_label_q_width.setText(f'Ширина: {value}')

    def update_q_heigth(self, value):
        self.result_label_q_heigth.setText(f'Высота: {value}')

    def start_message(self):
        self.button_start.clicked.connect(self.data_save)

        panda_app = PandaApp()
        camera_control_slider = Camera(panda_app)
        panda_app.camera_control_slider = camera_control_slider
        panda_app.slider = camera_control_slider.traction
        panda_app.run()

        self.button_start.clicked.connect(self.close)

    def data_save(self):
        dict_data = {"Масса": self.weight.value(), "Длина": self.length.value(), "Ширина": self.q_width.value(),
                     "Высота": self.q_heigth.value()}

        with open("Data", "a") as file:
            for key, value in dict_data.items():
                file.write(f"{key}: {value}\n")


class Camera(QtWidgets.QWidget):
    def __init__(self, camera_mover):
        super(Camera, self).__init__()
        self.camera_mover = camera_mover
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Drone Control")
        self.setGeometry(400, 600, 700, 1000)

        self.figure = Figure(figsize=(8, 8))
        self.canvas = FigureCanvas(self.figure)
        self.ax1 = self.figure.add_subplot(411)
        self.ax2 = self.figure.add_subplot(412)
        self.ax3 = self.figure.add_subplot(413)
        self.ax4 = self.figure.add_subplot(414)

        self.figure.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, hspace=0.5, wspace=0.5)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        # тяга
        self.traction = QSlider()
        self.traction.setOrientation(Qt.Horizontal)
        self.traction.setRange(0, 1000)
        self.traction.setTickPosition(QSlider.TicksAbove)
        self.traction.valueChanged.connect(self.on_slide)
        self.traction_label = QLabel('')

        layout_traction = QHBoxLayout()
        layout_traction.addWidget(QLabel("Тяга"))
        layout_traction.addWidget(self.traction)
        layout.addLayout(layout_traction)
        layout_result_traction = QHBoxLayout()
        layout_result_traction.addWidget(self.traction_label)
        layout.addLayout(layout_result_traction)

        # тангаж
        self.pitch = QSlider()
        self.pitch.setMaximum(1000)
        self.pitch.setMinimum(-1000)
        self.pitch.setValue(0)
        self.pitch.setTickInterval(10)
        self.pitch.setOrientation(Qt.Horizontal)
        self.pitch.setTickPosition(QSlider.TicksBelow)
        self.pitch.valueChanged.connect(self.pitch_change)
        self.pitch.sliderReleased.connect(self.reset_pitch_slider)
        self.pitch_label = QLabel('')

        layout_pitch = QHBoxLayout()
        layout_pitch.addWidget(QLabel("Тангаж: "))
        layout_pitch.addWidget(self.pitch)
        layout.addLayout(layout_pitch)
        layout_result_pitch = QHBoxLayout()
        layout_result_pitch.addWidget(self.pitch_label)
        layout.addLayout(layout_result_pitch)

        # крен
        self.bank = QSlider()
        self.bank.setMaximum(1000)
        self.bank.setMinimum(-1000)
        self.bank.setValue(0)
        self.bank.setTickInterval(10)
        self.bank.setOrientation(Qt.Horizontal)
        self.bank.setTickPosition(QSlider.TicksBelow)
        self.bank.valueChanged.connect(self.bank_change)
        self.bank.sliderReleased.connect(self.reset_bank_slider)
        self.bank_label = QLabel('')

        layout_bank = QHBoxLayout()
        layout_bank.addWidget(QLabel("Крен: "))
        layout_bank.addWidget(self.bank)
        layout.addLayout(layout_bank)
        layout_result_bank = QHBoxLayout()
        layout_result_bank.addWidget(self.bank_label)
        layout.addLayout(layout_result_bank)

        # рыскание
        self.yaw = QSlider()
        self.yaw.setMaximum(360)
        self.yaw.setMinimum(-360)
        self.yaw.setValue(0)
        self.yaw.setTickInterval(10)
        self.yaw.setOrientation(Qt.Horizontal)
        self.yaw.setTickInterval(QSlider.TicksBelow)
        self.yaw.valueChanged.connect(self.yaw_change)
        self.yaw.sliderReleased.connect(self.reset_yaw_slider)
        self.yaw_label = QLabel('')

        layout_yaw = QHBoxLayout()
        layout_yaw.addWidget(QLabel("Рыскание: "))
        layout_yaw.addWidget(self.yaw)
        layout.addLayout(layout_yaw)
        layout_result_yaw = QHBoxLayout()
        layout_result_yaw.addWidget(self.yaw_label)
        layout.addLayout(layout_result_yaw)

        # включение ветра (кнопка)
        self.toggle_btn = QPushButton('Выключено', self)
        self.toggle_btn.setCheckable(True)  # Делаем кнопку переключаемой
        self.toggle_btn.toggled.connect(self.toggle_function)

        layout.addWidget(self.toggle_btn, alignment=Qt.AlignBottom)  # Добавляем кнопку в самый низ

        self.setLayout(layout)

        self.setLayout(layout)
        self.show()

        self.camera_mover.traction = self.traction

        self.x_data = []
        self.y1_data = []
        self.y2_data = []
        self.y3_data = []
        self.y4_data = []

        # Создание пустых графиков
        self.line1 = self.ax1.plot([1000], [1000], color='blue')[0]
        self.line2 = self.ax2.plot([], [], color='red')[0]
        self.line3 = self.ax3.plot([], [], color='green')[0]
        self.line4 = self.ax4.plot([], [], color='yellow')[0]

        # Создание таймера обновления графиков
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(100)

    def on_slide(self, z_slider_value):
        self.update_values(z_slider_value, self.pitch.value(), self.bank.value(), self.yaw.value())

    def pitch_change(self, y_slider_value):
        self.update_values(self.traction.value(), y_slider_value, self.bank.value(), self.yaw.value())

    def reset_pitch_slider(self):
        self.pitch.setValue(0)

    def reset_bank_slider(self):
        self.bank.setValue(0)

    def bank_change(self, x_slider_value):
        self.update_values(self.traction.value(), self.pitch.value(), x_slider_value, self.yaw.value())

    def yaw_change(self, yaw_slider_value):
        self.update_values(self.traction.value(), self.pitch.value(), self.bank.value(), yaw_slider_value)

    def reset_yaw_slider(self):
        self.yaw.setValue(0)

    def toggle_function(self, checked):
        if checked:
            self.toggle_btn.setText('Включено')
            print('Function enabled')
            self.camera_mover.enable_wind(True)
        else:
            self.toggle_btn.setText('Выключено')
            print('Function disabled')
            self.camera_mover.enable_wind(False)

    def update_values(self, z_slider_value, y_slider_value, x_slider_value, yaw_slider_value):
        print("Slider Z: ", z_slider_value)
        print("Slider Y: ", y_slider_value)
        print("Slider X: ", x_slider_value)
        self.traction_label.setText(f'Значение тяги: {abs(z_slider_value)}')
        self.pitch_label.setText(f'Значение тангажа: {abs(y_slider_value)}')
        self.bank_label.setText(f'Значение крена: {abs(x_slider_value)}')
        self.yaw_label.setText(f'Значение рыскания: {abs(yaw_slider_value)}')
        self.camera_mover.move_model(z_slider_value, y_slider_value,
                                     x_slider_value,
                                     self.traction.minimum(), self.traction.maximum(),
                                     self.pitch.minimum(), self.pitch.maximum(),
                                     self.bank.minimum(), self.bank.maximum(),
                                     yaw_slider_value)

    def update_graph(self):
        x = len(self.x_data)
        y1 = self.traction.value()
        y2 = self.pitch.value()
        y3 = self.bank.value()
        y4 = self.yaw.value()

        # Добавление новых данных в списки
        self.x_data.append(x)
        self.y1_data.append(y1)
        self.y2_data.append(y2)
        self.y3_data.append(y3)
        self.y4_data.append(y4)

        # Обновление данных на графиках
        self.line1.set_data(self.x_data, self.y1_data)
        self.line2.set_data(self.x_data, self.y2_data)
        self.line3.set_data(self.x_data, self.y3_data)
        self.line4.set_data(self.x_data, self.y4_data)

        # Определение пределов осей графиков
        self.ax1.relim()
        self.ax1.autoscale_view()
        self.ax2.relim()
        self.ax2.autoscale_view()
        self.ax3.relim()
        self.ax3.autoscale_view()
        self.ax4.relim()
        self.ax4.autoscale_view()

        # Перерисовка графиков
        self.canvas.draw()


class PandaApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.wind_enabled = False
        self.wind_speed = 0.5
        self.wind_direction = None

        with open("Data", "r") as file:
            lines = file.readlines()
            for line in lines:
                key, value = line.strip().split(":")

                if key == "Масса":
                    self.mass = float(value)
                if key == "Длина":
                    self.long = float(value)
                if key == "Ширина":
                    self.shir = float(value)
                if key == "Высота":
                    self.height = float(value)

        self.environ = self.loader.loadModel("models/environment")
        self.environ.reparentTo(self.render)

        self.scene = self.loader.loadModel("drone_costum.bam")
        self.scene.reparentTo(self.render)

        self.scene.setScale(0.0005 * self.long, 0.0005 * self.shir, 0.0005 * self.height)
        self.scene.setPos(0, -30, 0.5)

        self.cam.setPos(-0.1, 5, 1)
        self.cam.lookAt(self.scene)

        self.plight = PointLight('plight')
        self.plight.setColor(VBase4(255, 255, 255, 255))
        self.plightNodePath = self.render.attachNewNode(self.plight)
        self.plightNodePath.setPos(70, 70, 70)
        self.render.setLight(self.plightNodePath)

        self.myTexture = self.loader.loadTexture("untitled.png")
        self.scene.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
        self.scene.setTexture(self.myTexture)

        self.z_pos = 0.0
        self.y_pos = 0.0
        self.x_pos = 0.0
        self.angle_pos = 0.0
        self.previous_y = 0.0
        self.previous_x = 0.0
        self.previous_angle = 0.0
        self.traction = None

    def move_model(self, z_slider_value, y_slider_value, x_slider_value,
                   z_range_min, z_range_max,
                   y_range_min, y_range_max,
                   x_range_min, x_range_max,
                   angle_value):
        normalized_value_z = z_slider_value / z_range_max
        range_max_half = z_range_max / 2
        normalized_value_y = (y_slider_value - range_max_half) / range_max_half
        normalized_value_x = (x_slider_value - x_range_min) / (x_range_max - x_range_min)

        new_z = -normalized_value_z * 30
        new_y = -normalized_value_y * 30
        new_x = normalized_value_x * 30

        print("Env pos: ", self.environ.getPos())

        self.y_pos = self.previous_y + new_y
        self.previous_y = new_y

        self.x_pos = self.previous_x + new_x
        self.previous_x = new_x

        self.angle_pos = angle_value + self.previous_angle
        self.previous_angle = angle_value

        self.environ.setPos(self.x_pos, self.y_pos, new_z)
        self.environ.setH(self.angle_pos)

    def enable_wind(self, enabled):
        if enabled:
            if not self.wind_enabled:
                self.wind_enabled = True
                self.wind_direction = random.choice([
                    Vec3(0, 1, 0),  # вперед
                    Vec3(0, -1, 0),  # назад
                    Vec3(-1, 0, 0),  # влево
                    Vec3(1, 0, 0)  # вправо
                ])
                self.taskMgr.doMethodLater(1, self.move_wind, "WindTask")
        else:
            if self.wind_enabled:
                self.wind_enabled = False
                self.taskMgr.remove("WindTask")

    def move_wind(self, task):
        if self.wind_enabled:
            self.environ.setPos(self.environ.getPos() + self.wind_direction * self.wind_speed)
            return task.again
        else:
            return task.done


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
