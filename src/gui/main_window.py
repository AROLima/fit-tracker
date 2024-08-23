from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from .cadastro_aluno import CadastroAlunoDialog
from .lista_alunos import ListaAlunosWindow
from .detalhes_aluno import DetalhesAlunoWindow

class MainWindow(QMainWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("Sistema de Cadastro de Alunos")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()
        self.lista_alunos_window = ListaAlunosWindow(self.db_manager)
        self.lista_alunos_window.aluno_selecionado.connect(self.view_aluno_details)
        self.stacked_widget.addWidget(self.lista_alunos_window)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Barra superior com botão de voltar
        top_bar = QWidget()
        top_layout = QHBoxLayout(top_bar)
        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.hide()  # Inicialmente escondido
        top_layout.addWidget(self.back_button)
        top_layout.addStretch()
        main_layout.addWidget(top_bar)

        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Página inicial
        home_page = QWidget()
        home_layout = QVBoxLayout(home_page)
        self.label = QLabel("Bem-vindo ao Fit tracker")
        home_layout.addWidget(self.label)
        self.label.setAlignment(Qt.AlignCenter)  # Centraliza o texto no label
        home_layout.addWidget(self.label)

        self.add_aluno_button = QPushButton("Adicionar Aluno")
        self.add_aluno_button.clicked.connect(self.open_cadastro_aluno)
        home_layout.addWidget(self.add_aluno_button)

        self.view_alunos_button = QPushButton("Ver Alunos")
        self.view_alunos_button.clicked.connect(self.view_alunos)
        home_layout.addWidget(self.view_alunos_button)

        self.stacked_widget.addWidget(home_page)

        # Página de lista de alunos
        self.lista_alunos_window = ListaAlunosWindow(self.db_manager)
        self.lista_alunos_window.aluno_selecionado.connect(self.view_aluno_details)
        self.stacked_widget.addWidget(self.lista_alunos_window)

    def go_back(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index > 0:
            self.stacked_widget.setCurrentIndex(current_index - 1)
        if self.stacked_widget.currentIndex() == 0:
            self.back_button.hide()

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
        self.lista_alunos_window.load_alunos()
        self.stacked_widget.setCurrentWidget(self.lista_alunos_window)
        self.back_button.show()

    def view_aluno_details(self, aluno_id):
        detalhes_window = DetalhesAlunoWindow(self.db_manager, aluno_id)
        self.stacked_widget.addWidget(detalhes_window)
        self.stacked_widget.setCurrentWidget(detalhes_window)
        self.back_button.show()
    def view_aluno_details(self, aluno_id):
        detalhes_window = DetalhesAlunoWindow(self.db_manager, aluno_id)
        self.stacked_widget.addWidget(detalhes_window)
        self.stacked_widget.setCurrentWidget(detalhes_window)
        self.back_button.show()