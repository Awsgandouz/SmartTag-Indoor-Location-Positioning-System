import sys
import math
import random

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtWidgets import QApplication, QWidget


class Simulation(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Indoor Tracking System Simulation'
        self.width = 1200
        self.height = 800
        self.anchor_positions = [(10, 10), (10, 590), (990, 10), (990, 590), (500, 300)]
        self.tag_position = (self.width//2, self.height//2)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, self.width, self.height)
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
        qp.drawText(self.tag_position[0]+10, self.tag_position[1]+10, f"Tag ({self.tag_position[0]},{self.tag_position[1]})")

    def draw_lines(self, qp):
        pen = QPen(QColor(255, 0, 0), 2, Qt.SolidLine)

        for pos in self.anchor_positions:
            dx = pos[0] - self.tag_position[0]
            dy = pos[1] - self.tag_position[1]
            dist = math.sqrt(dx*dx + dy*dy)
            qp.setPen(pen)
            qp.drawLine(pos[0], pos[1], self.tag_position[0], self.tag_position[1])
            qp.drawText((pos[0]+self.tag_position[0])/2,(pos[1]+self.tag_position[1])/2, f"{dist:.2f}")
    def update_simulation(self):
        # Update tag position randomly
        self.tag_position = (random.randint(0, self.width), random.randint(0, self.height))

        # Redraw the simulation
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sim = Simulation()
    sys.exit(app.exec_())





