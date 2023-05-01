import sys
import math
import random

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout


class Simulation(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Indoor Tracking System Simulation'
        self.width = 1200
        self.height = 800
        self.anchor_positions = [(10, 10), (10, 590), (990, 10), (990, 590)]
        self.tag_position = (self.width//2, self.height//2)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, self.width, self.height)

        # Create the UI elements
        self.distance_labels = []
        for i in range(len(self.anchor_positions)):
            label = QLabel(f"Anchor {i+1}")
            self.distance_labels.append(label)

        self.x_label = QLabel("X:")
        self.x_value_label = QLabel(str(self.tag_position[0]))
        self.y_label = QLabel("Y:")
        self.y_value_label = QLabel(str(self.tag_position[1]))

        # Set up the layout
        grid = QGridLayout()
        grid.setSpacing(10)
        for i, pos in enumerate(self.anchor_positions):
            grid.addWidget(self.distance_labels[i], i, 0)
        grid.addWidget(self.x_label, len(self.anchor_positions), 0)
        grid.addWidget(self.x_value_label, len(self.anchor_positions), 1)
        grid.addWidget(self.y_label, len(self.anchor_positions)+1, 0)
        grid.addWidget(self.y_value_label, len(self.anchor_positions)+1, 1)

        hbox = QHBoxLayout()
        hbox.addLayout(grid)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.show()

        # Set up a timer to update the simulation every 100ms
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(1500)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_background(qp)
        self.draw_anchors(qp)
        self.draw_tag(qp)
        self.draw_lines(qp)
        qp.end()

    def draw_background(self, qp):
        brush = QBrush(Qt.green)
        qp.setBrush(brush)
        qp.drawRect(0, 0, self.width, self.height)

    def draw_anchors(self, qp):
        brush = QBrush(Qt.SolidPattern)
        pen = QPen(QColor(0, 0, 0), 2, Qt.SolidLine)

        for pos in self.anchor_positions:
            qp.setBrush(brush)
            qp.setPen(pen)
            qp.drawEllipse(pos[0]-5, pos[1]-5, 10, 10)
            qp.drawText(pos[0]+10, pos[1]+10, f"Anchor ({pos[0]},{pos[1]})")

    def draw_tag(self, qp):
        brush = QBrush(Qt.SolidPattern)
        pen = QPen(QColor(0, 0, 255), 2, Qt.SolidLine)

        qp.setBrush(brush)
        qp.setPen(pen)
        qp.drawEllipse(self.tag_position[0]-5, self.tag_position[1]-5, 10, 10)
        qp.drawText(self.tag_position[0]+10, self.tag_position[1]+10, "Tag")
    
    def update_simulation(self):
        # Update the tag position with random noise
        x_noise = random.gauss(0, 10)
        y_noise = random.gauss(0, 10)
        self.tag_position = (self.tag_position[0] + x_noise, self.tag_position[1] + y_noise)
        self.x_value_label.setText(str(self.tag_position[0]))
        self.y_value_label.setText(str(self.tag_position[1]))
        self.update()

    def draw_lines(self, qp):
        pen = QPen(QColor(255, 0, 0), 2, Qt.SolidLine)
        for i, pos in enumerate(self.anchor_positions):
            distance = math.sqrt((self.tag_position[0]-pos[0])**2 + (self.tag_position[1]-pos[1])**2)
            self.distance_labels[i].setText(f"Anchor {i+1}: {distance:.2f}m")
            qp.setPen(pen)
            qp.drawLine(pos[0], pos[1], self.tag_position[0], self.tag_position[1])
if __name__ == '__main__':
    app = QApplication(sys.argv)
    sim = Simulation()
    sys.exit(app.exec_())
