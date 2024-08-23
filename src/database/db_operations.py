import psycopg2
from psycopg2 import sql

class DatabaseManager:
    def __init__(self, dbname, user, password, host='localhost'):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        self.cur = self.conn.cursor()
        self.create_tables()

        #criando as tabelas
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


        ##read
    def get_all_alunos(self):
        query = "SELECT id, nome, idade, genero FROM alunos"
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_aluno(self, aluno_id):
        query = "SELECT * FROM alunos WHERE id = %s"
        self.cur.execute(query, (aluno_id,))
        return self.cur.fetchone()

    def get_aluno_measurements(self, aluno_id):
        query = """
        SELECT data, peso, altura, imc, percentual_gordura
        FROM medicoes
        WHERE aluno_id = %s
        ORDER BY data
        """
        self.cur.execute(query, (aluno_id,))
        return self.cur.fetchall()

    # Adicione este método para depuração
    def debug_print_medicoes(self, aluno_id):
        medicoes = self.get_aluno_measurements(aluno_id)
        print(f"Medições para aluno ID {aluno_id}:")
        for medicao in medicoes:
            print(medicao)

    def get_ultima_medicao(self, aluno_id):
        query = """
        SELECT * FROM medicoes
        WHERE aluno_id = %s
        ORDER BY data DESC
        LIMIT 1
        """
        self.cur.execute(query, (aluno_id,))
        return self.cur.fetchone()

    def add_medicao(self, aluno_id, data, peso, altura, percentual_gordura):
        imc = peso / (altura ** 2)
        query = """
        INSERT INTO medicoes (aluno_id, data, peso, altura, imc, percentual_gordura)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cur.execute(query, (aluno_id, data, peso, altura, imc, percentual_gordura))
        self.conn.commit()

    def delete_aluno(self, aluno_id):
        try:
            # Primeiro, excluir todas as medições associadas ao aluno
            self.cur.execute("DELETE FROM medicoes WHERE aluno_id = %s", (aluno_id,))
            
            # Em seguida, excluímos o aluno
            self.cur.execute("DELETE FROM alunos WHERE id = %s", (aluno_id,))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao excluir aluno: {e}")
            self.conn.rollback()
            return False

    def close(self):
        self.cur.close()
        self.conn.close()