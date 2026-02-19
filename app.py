from flask import Flask, render_template, request, redirect, url_for
from models.item_desejo import ItemDesejo
from models.database import init_db

app = Flask(__name__)

init_db()


@app.route("/")
def home():
    return render_template("home.html", titulo="Home")


@app.route('/lista', methods=['GET', 'POST'])
def lista():
    if request.method == 'POST':
        titulo_item = request.form['titulo_item']
        tipo_item = request.form['tipo_item']
        indicado = request.form.get('indicado_por')

        item = ItemDesejo(titulo_item, tipo_item, indicado) 
        item.salvar_item()

        return redirect(url_for('lista'))

    itens = ItemDesejo.obter_itens()
    return render_template('lista.html', titulo='Lista de Desejos', itens=itens)


@app.route('/delete/<int:idItem>')
def delete(idItem):
    item = ItemDesejo.id(idItem)
    item.excluir_item()
    return redirect(url_for('lista'))


@app.route('/update/<int:idItem>', methods=['GET', 'POST'])
def update(idItem):
    if request.method == 'POST':
        titulo = request.form['titulo_item']
        tipo = request.form['tipo_item']
        indicado = request.form['indicado_por']

        item = ItemDesejo(titulo, tipo, indicado, idItem)
        item.atualizar_item()

        return redirect(url_for('lista'))

    itens = ItemDesejo.obter_itens()
    item_selecionado = ItemDesejo.id(idItem)

    return render_template(
        'lista.html',
        titulo=f'Editando o item ID: {idItem}',
        itens=itens,
        item_selecionado=item_selecionado
    )