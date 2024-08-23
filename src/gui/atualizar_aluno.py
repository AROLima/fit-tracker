from PyQt5.QtWidgets import (QDialog, QFormLayout, QDoubleSpinBox, 
                             QDateEdit, QPushButton, QVBoxLayout, QDialogButtonBox)
from PyQt5.QtCore import pyqtSignal, QDate

class AtualizarAlunoDialog(QDialog):
    dados_atualizados = pyqtSignal(dict)

    def __init__(self, aluno_data, parent=None):
        super().__init__(parent)
        self.aluno_data = aluno_data
        self.setWindowTitle("Atualizar Dados do Aluno")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.peso_spin = QDoubleSpinBox()
        self.peso_spin.setRange(30, 300)
        self.peso_spin.setSuffix(" kg")
        self.peso_spin.setValue(self.aluno_data['peso'])

        self.altura_spin = QDoubleSpinBox()
        self.altura_spin.setRange(1.00, 2.50)
        self.altura_spin.setSuffix(" m")
        self.altura_spin.setDecimals(2)
        self.altura_spin.setValue(self.aluno_data['altura'])

        self.data_medicao = QDateEdit()
        self.data_medicao.setDate(QDate.currentDate())

        self.percentual_gordura_spin = QDoubleSpinBox()
        self.percentual_gordura_spin.setRange(1, 70)
        self.percentual_gordura_spin.setSuffix(" %")
        self.percentual_gordura_spin.setValue(self.aluno_data['percentual_gordura'])

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
        dados_atualizados = {
            'aluno_id': self.aluno_data['id'],
            'peso': self.peso_spin.value(),
            'altura': self.altura_spin.value(),
            'data_medicao': self.data_medicao.date().toString("yyyy-MM-dd"),
            'percentual_gordura': self.percentual_gordura_spin.value()
        }
        self.dados_atualizados.emit(dados_atualizados)
        super().accept()