from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView
from PyQt5.QtCore import pyqtSignal

class ListaAlunosWindow(QWidget):
    aluno_selecionado = pyqtSignal(int)

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Tabela de alunos
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Nome', 'Idade', 'Gênero'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.table)

        # Layout para botões
        button_layout = QHBoxLayout()
        
        self.view_button = QPushButton("Ver Detalhes")
        self.view_button.clicked.connect(self.view_aluno_details)
        button_layout.addWidget(self.view_button)

        self.refresh_button = QPushButton("Atualizar Lista")
        self.refresh_button.clicked.connect(self.load_alunos)
        button_layout.addWidget(self.refresh_button)

        layout.addLayout(button_layout)

        self.load_alunos()

    def load_alunos(self):
        self.table.clearContents()
        alunos = self.db_manager.get_all_alunos()
        self.table.setRowCount(len(alunos))
        for row, aluno in enumerate(alunos):
            self.table.setItem(row, 0, QTableWidgetItem(str(aluno[0])))
            self.table.setItem(row, 1, QTableWidgetItem(aluno[1]))
            self.table.setItem(row, 2, QTableWidgetItem(str(aluno[2])))
            self.table.setItem(row, 3, QTableWidgetItem(aluno[3]))

    def view_aluno_details(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            aluno_id = int(self.table.item(selected_rows[0].row(), 0).text())
            self.aluno_selecionado.emit(aluno_id)
        else:
            print("Nenhum aluno selecionado")

    def showEvent(self, event):
        super().showEvent(event)
        self.load_alunos()  # Recarrega a lista de alunos sempre que a janela é mostrada