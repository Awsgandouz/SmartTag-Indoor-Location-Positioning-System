import sys
import math
import random

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout


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
            label.setStyleSheet("color: white")
            self.distance_labels.append(label)

        self.x_label = QLabel("X:")
        self.x_value_label = QLabel(str(self.tag_position[0]))
        self.x_value_label.setStyleSheet("color: white")
        self.y_label = QLabel("Y:")
        self.y_value_label = QLabel(str(self.tag_position[1]))
        self.y_value_label.setStyleSheet("color: white")

        # Set up the layout
        
        hbox = QHBoxLayout()

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
        brush = QBrush(QColor(50, 50, 50))
        qp.setBrush(brush)
        qp.drawRect(0, 0, self.width, self.height)

    def draw_anchors(self, qp):
        brush = QBrush(Qt.SolidPattern)
        pen = QPen(QColor(255, 255, 255), 2, Qt.SolidLine)

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
    def update_simulation(self):
        # Calculate the distances from the tag to the anchors (with some noise)
        distances = []
        for pos in self.anchor_positions:
            distance = math.sqrt((pos[0]-self.tag_position[0])**2 + (pos[1]-self.tag_position[1])**2)
            noise = random.uniform(-0.2, 0.2)*distance
            distances.append(distance + noise)
            self.distance_labels[self.anchor_positions.index(pos)].setText(f"Anchor {self.anchor_positions.index(pos)+1}: {distance:.2f}m")

        # Estimate the tag position using trilateration
        x1, y1 = self.anchor_positions[0]
        x2, y2 = self.anchor_positions[1]
        x3, y3 = self.anchor_positions[2]

        r1, r2, r3 = distances[0], distances[1], distances[2]

        A = 2*x2 - 2*x1
        B = 2*y2 - 2*y1
        C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
        D = 2*x3 - 2*x2
        E = 2*y3 - 2*y2
        F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2

        x = (C*E - F*B) / (E*A - B*D)
        y = (C*D - A*F) / (B*D - A*E)

        self.tag_position = (x, y)

        # Update the UI
        self.x_value_label.setText(str(self.tag_position[0]))
        self.y_value_label.setText(str(self.tag_position[1]))
        self.update()


        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    sim = Simulation()
    sys.exit(app.exec_())
