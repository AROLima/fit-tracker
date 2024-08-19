import psycopg2
from psycopg2 import sql
from models.protocolo_treinamento import TipoProtocolo

class DatabaseManager:
    def __init__(self, dbname, user, password, host='localhost'):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        self.cur = self.conn.cursor()

    def add_aluno(self, nome, idade, genero, tipo_protocolo=None, descricao_protocolo=None):
        query = sql.SQL("""
            INSERT INTO alunos (nome, idade, genero, tipo_protocolo, descricao_protocolo)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        """)
        self.cur.execute(query, (nome, idade, genero, tipo_protocolo.value if tipo_protocolo else None, descricao_protocolo))
        aluno_id = self.cur.fetchone()[0]
        self.conn.commit()
        return aluno_id

    def update_protocolo_treinamento(self, aluno_id, tipo_protocolo, descricao_protocolo=None):
        query = sql.SQL("""
            UPDATE alunos
            SET tipo_protocolo = %s, descricao_protocolo = %s
            WHERE id = %s
        """)
        self.cur.execute(query, (tipo_protocolo.value, descricao_protocolo, aluno_id))
        self.conn.commit()

    def add_measurement(self, aluno_id, data, peso, altura, imc, percentual_gordura=None):
        query = sql.SQL("""
            INSERT INTO measurements (aluno_id, data, peso, altura, imc, percentual_gordura)
            VALUES (%s, %s, %s, %s, %s, %s)
        """)
        self.cur.execute(query, (aluno_id, data, peso, altura, imc, percentual_gordura))
        self.conn.commit()

    def get_aluno_measurements(self, aluno_id, limit=5):
        query = sql.SQL("""
            SELECT data, peso, imc, percentual_gordura
            FROM measurements
            WHERE aluno_id = %s
            ORDER BY data DESC
            LIMIT %s
        """)
        self.cur.execute(query, (aluno_id, limit))
        return self.cur.fetchall()

    def get_aluno(self, aluno_id):
        query = sql.SQL("""
            SELECT id, nome, idade, genero, tipo_protocolo, descricao_protocolo
            FROM alunos
            WHERE id = %s
        """)
        self.cur.execute(query, (aluno_id,))
        return self.cur.fetchone()

    def close(self):
        self.cur.close()
        self.conn.close()