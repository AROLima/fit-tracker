import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter
from models.protocolo_treinamento import TipoProtocolo

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Cadastro de Alunos")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.label = QLabel("Bem-vindo ao Sistema de Cadastro de Alunos")
        layout.addWidget(self.label)

        self.protocolo_combo = QComboBox()
        self.protocolo_combo.addItems([tipo.value for tipo in TipoProtocolo])
        layout.addWidget(self.protocolo_combo)

        self.add_aluno_button = QPushButton("Adicionar Aluno")
        self.add_aluno_button.clicked.connect(self.add_aluno)
        layout.addWidget(self.add_aluno_button)

        self.view_alunos_button = QPushButton("Ver Alunos")
        self.view_alunos_button.clicked.connect(self.view_alunos)
        layout.addWidget(self.view_alunos_button)

        self.create_example_chart(layout)

    def create_example_chart(self, layout):
        chart = QChart()
        series = QLineSeries()
        series.append([QPointF(0, 70), QPointF(1, 72), QPointF(2, 71), QPointF(3, 69)])
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setTitle("Progresso do Aluno")

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(chart_view)

    def add_aluno(self):
        protocolo_selecionado = TipoProtocolo(self.protocolo_combo.currentText())
        print(f"Adicionar aluno com protocolo: {protocolo_selecionado.value}")

    def view_alunos(self):
        print("Visualizar alunos")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())