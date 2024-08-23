from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter
from .cadastro_aluno import CadastroAlunoDialog

class MainWindow(QMainWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("Sistema de Cadastro de Alunos")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.label = QLabel("Bem-vindo ao Sistema de Cadastro de Alunos")
        layout.addWidget(self.label)

        self.add_aluno_button = QPushButton("Adicionar Aluno")
        self.add_aluno_button.clicked.connect(self.open_cadastro_aluno)
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

    def open_cadastro_aluno(self):
        dialog = CadastroAlunoDialog(self)
        dialog.aluno_cadastrado.connect(self.cadastrar_aluno)
        dialog.exec_()

    def cadastrar_aluno(self, aluno_data):
        try:
            aluno_id = self.db_manager.add_aluno(**aluno_data)
            print(f"Aluno cadastrado com sucesso. ID: {aluno_id}")
        except Exception as e:
            print(f"Erro ao cadastrar aluno: {e}")

    def view_alunos(self):
        print("Funcionalidade de visualizar alunos ainda não implementada")