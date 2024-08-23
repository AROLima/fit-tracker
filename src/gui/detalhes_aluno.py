from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QPainter
from .atualizar_aluno import AtualizarAlunoDialog

class DetalhesAlunoWindow(QWidget):
    def __init__(self, db_manager, aluno_id):
        super().__init__()
        self.db_manager = db_manager
        self.aluno_id = aluno_id
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.info_label = QLabel()
        layout.addWidget(self.info_label)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Data', 'Peso', 'Altura', 'IMC', '% Gordura'])
        layout.addWidget(self.table)

        self.chart_view = QChartView()
        layout.addWidget(self.chart_view)

        self.atualizar_button = QPushButton("Atualizar Medidas")
        self.atualizar_button.clicked.connect(self.abrir_atualizar_dialog)
        layout.addWidget(self.atualizar_button)

        self.carregar_dados_aluno()

    def carregar_dados_aluno(self):
        aluno_info = self.db_manager.get_aluno(self.aluno_id)
        self.info_label.setText(f"Nome: {aluno_info[1]}, Idade: {aluno_info[2]}, Gênero: {aluno_info[3]}")
        
        self.load_medicoes()
        self.update_chart()

    def load_medicoes(self):
        medicoes = self.db_manager.get_aluno_measurements(self.aluno_id)
        self.table.setRowCount(len(medicoes))
        for row, medicao in enumerate(medicoes):
            self.table.setItem(row, 0, QTableWidgetItem(str(medicao[0])))
            self.table.setItem(row, 1, QTableWidgetItem(f"{medicao[1]:.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(f"{medicao[2]:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{medicao[3]:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{medicao[4]:.2f}" if medicao[4] else "N/A"))

    def update_chart(self):
        chart = QChart()
        chart.setTitle("Progresso do Aluno")

        peso_series = QLineSeries()
        peso_series.setName("Peso")

        imc_series = QLineSeries()
        imc_series.setName("IMC")

        medicoes = self.db_manager.get_aluno_measurements(self.aluno_id)
        for medicao in medicoes:
            date = QDateTime.fromString(str(medicao[0]), "yyyy-MM-dd").toMSecsSinceEpoch()
            peso_series.append(date, medicao[1])
            imc_series.append(date, medicao[3])

        chart.addSeries(peso_series)
        chart.addSeries(imc_series)

        date_axis = QDateTimeAxis()
        date_axis.setTickCount(5)
        date_axis.setFormat("dd/MM/yyyy")
        chart.addAxis(date_axis, Qt.AlignBottom)

        value_axis = QValueAxis()
        chart.addAxis(value_axis, Qt.AlignLeft)

        peso_series.attachAxis(date_axis)
        peso_series.attachAxis(value_axis)
        imc_series.attachAxis(date_axis)
        imc_series.attachAxis(value_axis)

        self.chart_view.setChart(chart)

    def abrir_atualizar_dialog(self):
        print("Iniciando abrir_atualizar_dialog")
        print(f"self.db_manager: {self.db_manager}")
        print(f"Métodos disponíveis em self.db_manager: {dir(self.db_manager)}")
        
        aluno_data = self.db_manager.get_aluno(self.aluno_id)
        print(f"aluno_data: {aluno_data}")
        
        try:
            ultima_medicao = self.db_manager.get_ultima_medicao(self.aluno_id)
            print(f"ultima_medicao: {ultima_medicao}")
        except Exception as e:
            print(f"Erro ao obter última medição: {e}")
            import traceback
            traceback.print_exc()
        
        dados_atuais = {
            'id': self.aluno_id,
            'peso': float(ultima_medicao[3]) if ultima_medicao else 0,
            'altura': float(ultima_medicao[4]) if ultima_medicao else 0,
            'percentual_gordura': float(ultima_medicao[6]) if ultima_medicao else 0
        }
        
        dialog = AtualizarAlunoDialog(dados_atuais, self)
        dialog.dados_atualizados.connect(self.atualizar_dados_aluno)
        dialog.exec_()

    def atualizar_dados_aluno(self, dados_atualizados):
        self.db_manager.add_medicao(
            aluno_id=dados_atualizados['aluno_id'],
            data=dados_atualizados['data_medicao'],
            peso=dados_atualizados['peso'],
            altura=dados_atualizados['altura'],
            percentual_gordura=dados_atualizados['percentual_gordura']
        )
        self.carregar_dados_aluno()