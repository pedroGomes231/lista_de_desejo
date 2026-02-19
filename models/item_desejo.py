from sqlite3 import Cursor
from models.database import Database
from typing import Optional, Self, Any


class ItemDesejo:
    """
    Classe para representar um item da lista de desejos (Must Watch),
    com métodos para salvar, obter, excluir e atualizar itens no banco de dados.
    """

    def __init__(
        self: Self,
        titulo_item: Optional[str],
        tipo_item: Optional[str],
        indicado_por: Optional[str] = None,
        id_item: Optional[int] = None
    ) -> None:
        self.titulo_item: Optional[str] = titulo_item
        self.tipo_item: Optional[str] = tipo_item
        self.indicado_por: Optional[str] = indicado_por
        self.id_item: Optional[int] = id_item

    # ItemDesejo.id(1)
    @classmethod
    def id(cls, id: int) -> Self:
        with Database() as db:
            query: str = """
                SELECT titulo_item, tipo_item, indicado_por
                FROM lista_desejos
                WHERE id = ?;
            """
            params: tuple = (id,)
            resultado: list[Any] = db.buscar_tudo(query, params)

            [[titulo, tipo, indicado]] = resultado

        return cls(
            titulo_item=titulo,
            tipo_item=tipo,
            indicado_por=indicado,
            id_item=id
        )

    # ItemDesejo("Matrix", "Filme", "João")
    def salvar_item(self: Self) -> None:
        with Database() as db:
            query: str = """
                INSERT INTO lista_desejos (titulo_item, tipo_item, indicado_por)
                VALUES (?, ?, ?);
            """
            params: tuple = (
                self.titulo_item,
                self.tipo_item,
                self.indicado_por
            )
            db.executar(query, params)

    @classmethod
    def obter_itens(cls) -> list[Self]:
        with Database() as db:
            query: str = """
                SELECT titulo_item, tipo_item, indicado_por, id
                FROM lista_desejos;
            """
            resultados: list[Any] = db.buscar_tudo(query)

            itens: list[Self] = [
                cls(titulo, tipo, indicado, id)
                for titulo, tipo, indicado, id in resultados
            ]

            return itens

    def excluir_item(self) -> Cursor:
        with Database() as db:
            query: str = 'DELETE FROM lista_desejos WHERE id = ?;'
            params: tuple = (self.id_item,)
            return db.executar(query, params)

    def atualizar_item(self) -> Cursor:
        with Database() as db:
            query: str = """
                UPDATE lista_desejos
                SET titulo_item = ?, tipo_item = ?, indicado_por = ?
                WHERE id = ?;
            """
            params: tuple = (
                self.titulo_item,
                self.tipo_item,
                self.indicado_por,
                self.id_item
            )
            return db.executar(query, params)


            