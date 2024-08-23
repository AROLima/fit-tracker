from PyQt5.QtWidgets import (QDialog, QFormLayout, QLineEdit, QComboBox, 
                             QPushButton, QVBoxLayout, QDialogButtonBox,
                             QDoubleSpinBox, QDateEdit)
from PyQt5.QtCore import pyqtSignal, QDate

class CadastroAlunoDialog(QDialog):
    aluno_cadastrado = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cadastro de Aluno")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.nome_edit = QLineEdit()
        self.idade_edit = QLineEdit()
        self.genero_combo = QComboBox()
        self.genero_combo.addItems(['M', 'F', 'Outro'])
        self.protocolo_combo = QComboBox()
        self.protocolo_combo.addItems(['Emagrecimento', 'Ganho de massa muscular', 'Definição'])
        
        # Novos campos
        self.peso_spin = QDoubleSpinBox()
        self.peso_spin.setRange(30, 300)  # Intervalo razoável de peso em kg
        self.peso_spin.setSuffix(" kg")
        
        self.altura_spin = QDoubleSpinBox()
        self.altura_spin.setRange(1.00, 2.50)  # Intervalo razoável de altura em metros
        self.altura_spin.setSuffix(" m")
        self.altura_spin.setDecimals(2)
        
        self.data_medicao = QDateEdit()
        self.data_medicao.setDate(QDate.currentDate())
        
        self.percentual_gordura_spin = QDoubleSpinBox()
        self.percentual_gordura_spin.setRange(1, 70)  # Intervalo razoável de percentual de gordura
        self.percentual_gordura_spin.setSuffix(" %")

        form_layout.addRow("Nome:", self.nome_edit)
        form_layout.addRow("Idade:", self.idade_edit)
        form_layout.addRow("Gênero:", self.genero_combo)
        form_layout.addRow("Protocolo:", self.protocolo_combo)
        form_layout.addRow("Peso:", self.peso_spin)
        form_layout.addRow("Altura:", self.altura_spin)
        form_layout.addRow("Data da Medição:", self.data_medicao)
        form_layout.addRow("Percentual de Gordura:", self.percentual_gordura_spin)

        layout.addLayout(form_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def accept(self):
        aluno_data = {
            'nome': self.nome_edit.text(),
            'idade': int(self.idade_edit.text()),
            'genero': self.genero_combo.currentText(),
            'protocolo': self.protocolo_combo.currentText(),
            'peso': self.peso_spin.value(),
            'altura': self.altura_spin.value(),
            'data_medicao': self.data_medicao.date().toString("yyyy-MM-dd"),
            'percentual_gordura': self.percentual_gordura_spin.value()
        }
        self.aluno_cadastrado.emit(aluno_data)
        super().accept()