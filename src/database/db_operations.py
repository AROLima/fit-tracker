import psycopg2
from psycopg2 import sql

class DatabaseManager:
    def __init__(self, dbname, user, password, host='localhost'):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        create_alunos_table = """
        CREATE TABLE IF NOT EXISTS alunos (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            idade INTEGER NOT NULL,
            genero CHAR(1) NOT NULL,
            tipo_protocolo VARCHAR(50)
        );
        """
        create_medicoes_table = """
        CREATE TABLE IF NOT EXISTS medicoes (
            id SERIAL PRIMARY KEY,
            aluno_id INTEGER REFERENCES alunos(id),
            data DATE NOT NULL,
            peso DECIMAL(5,2) NOT NULL,
            altura DECIMAL(3,2) NOT NULL,
            imc DECIMAL(4,2) NOT NULL,
            percentual_gordura DECIMAL(4,2)
        );
        """
        self.cur.execute(create_alunos_table)
        self.cur.execute(create_medicoes_table)
        self.conn.commit()

    def add_aluno(self, nome, idade, genero, protocolo, peso, altura, data_medicao, percentual_gordura):
        # Inserir aluno
        aluno_query = """
        INSERT INTO alunos (nome, idade, genero, tipo_protocolo)
        VALUES (%s, %s, %s, %s) RETURNING id
        """
        self.cur.execute(aluno_query, (nome, idade, genero, protocolo))
        aluno_id = self.cur.fetchone()[0]

        # Calcular IMC
        imc = peso / (altura ** 2)

        # Inserir medição
        medicao_query = """
        INSERT INTO medicoes (aluno_id, data, peso, altura, imc, percentual_gordura)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cur.execute(medicao_query, (aluno_id, data_medicao, peso, altura, imc, percentual_gordura))

        self.conn.commit()
        return aluno_id

    def close(self):
        self.cur.close()
        self.conn.close()