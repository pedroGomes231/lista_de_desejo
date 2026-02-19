from sqlite3 import Connection, connect, Cursor
from types import TracebackType
from typing import Any, Optional, Self, Type
# from dotenv import load_dotenv
import os

# load_dotenv()

DB_PATH = os.getenv('DATABASE', './data/lista_desejos.sqlite3')


def init_db(db_name: str = DB_PATH) -> None:
    with connect(db_name) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS lista_desejos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo_item TEXT NOT NULL,
            tipo_item TEXT NOT NULL,
            indicado_por TEXT
        );
        """)


class Database:
    """
    Classe que gerencia conexões e operações com um banco de dados SQLite.
    """
    def __init__(self, db_name: str = DB_PATH) -> None:
        self.connection: Connection = connect(db_name)
        self.cursor = self.connection.cursor()

    def executar(self, query: str, params: tuple = ()) -> Cursor:
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor
    
    def buscar_tudo(self, query: str, params: tuple = ()) -> list[Any]:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> Self:
        return self
    
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        tb: Optional[TracebackType]
    ) -> None:
        if exc_type is not None:
            print('Exceção capturada no contexto:')
            print(f'Tipo: {exc_type.__name__}')
            print(f'Mensagem: {exc_value}')
        self.close()