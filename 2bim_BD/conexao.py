import mysql.connector

# Conexao global usada pelo programa.
conexao = None
cursor = None


# Lista com os triggers que o sistema recria quando necessario.
trigger_consulta = [
    # Se o pagamento for "Pago", o pedido correspondente muda de status.
    (
        "trg_pagamento_pago",
        """
        CREATE TRIGGER trg_pagamento_pago
        AFTER INSERT ON pagamento
        FOR EACH ROW
        BEGIN
            -- So atualiza o pedido quando o pagamento estiver pago.
            IF NEW.status_pagamento = 'Pago' THEN
                UPDATE pedido
                SET id_statusped = 2
                WHERE id_pedido = NEW.id_pedido;
            END IF;
        END
        """
    ),
    # Se o pedido entrar sem data, o sistema coloca a data atual.
    (
        "trg_pedido_data_padrao",
        """
        CREATE TRIGGER trg_pedido_data_padrao
        BEFORE x ON pedido
        FOR EACH ROW
        BEGIN
            -- Preenche a data quando o campo vier vazio.
            IF NEW.data_pedido IS NULL THEN
                SET NEW.data_pedido = CURDATE();
            END IF;
        END
        """
    ),
    # Quando a entrega ficar concluida, o pedido tambem muda de status.
    (
        "trg_entrega_finalizada",
        """
        CREATE TRIGGER trg_entrega_finalizada
        AFTER UPDATE ON entrega
        FOR EACH ROW
        BEGIN
            -- Usa o status 4 da entrega como sinal de finalizacao.
            IF NEW.id_statusEtre = 4 THEN
                UPDATE pedido
                SET id_statusped = 5
                WHERE id_pedido = NEW.id_pedido;
            END IF;
        END
        """
    ),
]

# Lista com as stored procedures que o sistema consegue recriar.
stored_procedure_consulta = [
    # Relatorio simples com a quantidade de pedidos por cliente.
    (
        "proc_relatorio_cliente",
        0,
        """
        CREATE PROCEDURE proc_relatorio_cliente()
        BEGIN
            -- Junta cliente e pedido usando a sintaxe antiga.
            SELECT
                cliente.id_cliente,
                cliente.nome_cliente,
                COUNT(pedido.id_pedido) AS total_pedidos

            FROM cliente, pedido

            WHERE cliente.id_cliente = pedido.id_cliente

            GROUP BY cliente.id_cliente, cliente.nome_cliente

            ORDER BY total_pedidos DESC;
        END
        """
    ),
    # Grava um pagamento e devolve o ultimo registro inserido.
    (
        "sp_registrar_pagamento",
        3,
        """
        CREATE PROCEDURE sp_registrar_pagamento(
            IN p_id_pedido INT,
            IN p_status_pagamento VARCHAR(50),
            IN p_id_forma_pagamento INT
        )
        BEGIN
            -- Gera o proximo id usando uma subquery derivada para evitar o erro 1093.
            INSERT INTO pagamento (
                id_pagamento,
                id_pedido,
                status_pagamento,
                id_formaPagamento
            )
            SELECT
                dados.proximo_id,
                p_id_pedido,
                p_status_pagamento,
                p_id_forma_pagamento
            FROM (
                SELECT COALESCE(MAX(id_pagamento) + 1, 1) AS proximo_id
                FROM pagamento
            ) AS dados;

            -- Retorna o ultimo pagamento criado para montar a tabela no Tkinter.
            SELECT *
            FROM pagamento
            ORDER BY id_pagamento DESC
            LIMIT 1;
        END
        """
    ),
    # Lista os pedidos de um cliente especifico.
    (
        "proc_pedidos_por_cliente",
        1,
        """
        CREATE PROCEDURE proc_pedidos_por_cliente(
            IN p_id_cliente INT
        )
        BEGIN
            -- Mostra os pedidos do cliente informado na tela.
            SELECT
                pedido.id_pedido AS "ID do Pedido",
                pedido.valor_pedido AS "Valor do Pedido",
                pedido.data_pedido AS "Data do Pedido",
                status_pedido.status_pedido AS "Status do Pedido"

            FROM pedido, status_pedido

            WHERE pedido.id_statusped = status_pedido.id_statusped
            AND pedido.id_cliente = p_id_cliente

            ORDER BY pedido.data_pedido DESC;
        END
        """
    ),
    # Lista os produtos de uma categoria especifica.
    (
        "proc_produtos_por_categoria",
        1,
        """
        CREATE PROCEDURE proc_produtos_por_categoria(
            IN p_id_categoria INT
        )
        BEGIN
            -- Filtra somente os produtos da categoria escolhida.
            SELECT
                produto.id_produto AS "ID do Produto",
                produto.nome_produto AS "Nome do Produto",
                produto.valor_produto AS "Valor do Produto"

            FROM produto

            WHERE produto.id_categoria = p_id_categoria

            ORDER BY produto.nome_produto;
        END
        """
    ),
    # Lista os pagamentos filtrando pelo status informado.
    (
        "proc_pagamentos_por_status",
        1,
        """
        CREATE PROCEDURE proc_pagamentos_por_status(
            IN p_status_pagamento VARCHAR(50)
        )
        BEGIN
            -- Mostra pagamentos usando o status que o usuario digitou.
            SELECT
                pagamento.id_pagamento AS "ID do Pagamento",
                pagamento.id_pedido AS "ID do Pedido",
                pagamento.status_pagamento AS "Status do Pagamento",
                forma_pagamento.formaPagamento AS "Forma de Pagamento"

            FROM pagamento, forma_pagamento

            WHERE pagamento.id_formaPagamento = forma_pagamento.id_formaPagamento
            AND pagamento.status_pagamento = p_status_pagamento;
        END
        """
    ),

]


CONSULTAS_BASE = [
    ("Clientes", """
        SELECT *
        FROM cliente
    """),
    ("Enderecos", """
        SELECT *
        FROM endereco
    """),
    ("Categorias", """
        SELECT *
        FROM categoria
    """),
    ("Produtos", """
        SELECT *
        FROM produto
    """),
    ("Avaliacoes", """
        SELECT *
        FROM avaliacao
    """),
    ("Status pedido", """
        SELECT *
        FROM status_pedido
    """),
    ("Pedidos", """
        SELECT *
        FROM pedido
    """),
    ("Entregas", """
        SELECT *
        FROM entrega
    """),
    ("Pagamentos", """
        SELECT *
        FROM pagamento
    """),
    ("Nome e valor dos produtos", """
        SELECT nome_produto, valor_produto
        FROM produto
    """),
    ("Cliente e endereco", """
        SELECT *
        FROM cliente, endereco
        WHERE cliente.id_cliente = endereco.id_cliente
    """),
    ("Produto e categoria", """
        SELECT *
        FROM produto, categoria
        WHERE produto.id_categoria = categoria.id_categoria
    """),
    ("Pedido e cliente", """
        SELECT *
        FROM pedido, cliente
        WHERE pedido.id_cliente = cliente.id_cliente
    """),
    ("Pedido e status", """
        SELECT *
        FROM pedido, status_pedido
        WHERE pedido.id_statusped = status_pedido.id_statusped
    """),
    ("Pagamento e forma pagamento", """
        SELECT *
        FROM pagamento, forma_pagamento
        WHERE pagamento.id_formaPagamento = forma_pagamento.id_formaPagamento
    """),
    ("Entrega e status entrega", """
        SELECT *
        FROM entrega, status_entrega
        WHERE entrega.id_statusEtre = status_entrega.id_statusEtre
    """),
    ("Avaliacao e cliente", """
        SELECT *
        FROM avaliacao, cliente
        WHERE avaliacao.id_cliente = cliente.id_cliente
    """),
    ("Avaliacao e produto", """
        SELECT *
        FROM avaliacao, produto
        WHERE avaliacao.id_produto = produto.id_produto
    """),
    ("Item pedido e pedido", """
        SELECT *
        FROM item_pedido, pedido
        WHERE item_pedido.id_pedido = pedido.id_pedido
    """),
    ("Item pedido e produto", """
        SELECT *
        FROM item_pedido, produto
        WHERE item_pedido.id_produto = produto.id_produto
    """),
    ("Produtos caros", """
        SELECT *
        FROM produto
        WHERE valor_produto > 100
    """),
    ("Cliente Ana", """
        SELECT *
        FROM cliente
        WHERE nome_cliente = 'Ana Costa'
    """),
    ("Pedidos recentes", """
        SELECT *
        FROM pedido
        WHERE data_pedido > '2026-05-10'
    """),
    ("Pagamentos pagos", """
        SELECT *
        FROM pagamento
        WHERE status_pagamento = 'Pago'
    """),
    ("Avaliacoes boas", """
        SELECT *
        FROM avaliacao
        WHERE nota >= 4.0
    """),
    ("Clientes ordenados", """
        SELECT *
        FROM cliente
        ORDER BY nome_cliente
    """),
    ("Produtos preco desc", """
        SELECT *
        FROM produto
        ORDER BY valor_produto DESC
    """),
    ("Pedidos por data", """
        SELECT *
        FROM pedido
        ORDER BY data_pedido
    """),
    ("Avaliacoes por nota", """
        SELECT *
        FROM avaliacao
        ORDER BY nota DESC
    """),
    ("Categorias ordenadas", """
        SELECT *
        FROM categoria
        ORDER BY categoria
    """),
    ("Quantidade de produtos por categoria", """
        SELECT id_categoria, COUNT(*) AS quantidade
        FROM produto
        GROUP BY id_categoria
    """),
    ("Total status pagamento", """
        SELECT status_pagamento, COUNT(*) AS total
        FROM pagamento
        GROUP BY status_pagamento
    """),
    ("Total pedidos cliente", """
        SELECT id_cliente, COUNT(*) AS pedidos
        FROM pedido
        GROUP BY id_cliente
    """),
    ("Total forma pagamento", """
        SELECT id_formaPagamento, COUNT(*) AS pagamentos
        FROM pagamento
        GROUP BY id_formaPagamento
    """),
    ("Total status pedido", """
        SELECT id_statusped, COUNT(*) AS total
        FROM pedido
        GROUP BY id_statusped
    """),
]


# Views criadas no banco.
DEFINICOES_VIEWS = [
    # View principal com pedido, cliente e status do pedido.
    ("vw_pedido_cliente_status", """
        CREATE OR REPLACE VIEW vw_pedido_cliente_status AS
        SELECT
            pedido.id_pedido AS "ID do Pedido",
            pedido.valor_pedido AS "Valor do Pedido",
            pedido.data_pedido AS "Data do Pedido",
            cliente.nome_cliente AS "Nome do Cliente",
            status_pedido.status_pedido AS "Status do Pedido"
        FROM pedido, cliente, status_pedido
        WHERE pedido.id_cliente = cliente.id_cliente
        AND pedido.id_statusped = status_pedido.id_statusped
    """),
    # View com produto, categoria e item do pedido.
    ("vw_produto_categoria_item", """
        CREATE OR REPLACE VIEW vw_produto_categoria_item AS
        SELECT
            produto.id_produto AS "ID do Produto",
            produto.nome_produto AS "Nome do Produto",
            produto.valor_produto AS "Valor do Produto",
            categoria.categoria AS "Categoria do Produto",
            item_pedido.id_itens AS "ID do Item",
            item_pedido.id_pedido AS "ID do Pedido",
            item_pedido.qtd_produto AS "Quantidade do Item"
        FROM produto, categoria, item_pedido
        WHERE produto.id_categoria = categoria.id_categoria
        AND produto.id_produto = item_pedido.id_produto
    """),
    # View com pedido, pagamento e forma de pagamento.
    ("vw_pedido_pagamento_forma", """
        CREATE OR REPLACE VIEW vw_pedido_pagamento_forma AS
        SELECT
            pedido.id_pedido AS "ID do Pedido",
            pedido.valor_pedido AS "Valor do Pedido",
            pedido.data_pedido AS "Data do Pedido",
            pagamento.id_pagamento AS "ID do Pagamento",
            pagamento.status_pagamento AS "Status do Pagamento",
            forma_pagamento.formaPagamento AS "Forma de Pagamento"
        FROM pedido, pagamento, forma_pagamento
        WHERE pedido.id_pedido = pagamento.id_pedido
        AND pagamento.id_formaPagamento = forma_pagamento.id_formaPagamento
    """),
    # View com entrega, pedido e status da entrega.
    ("vw_entrega_pedido_status", """
        CREATE OR REPLACE VIEW vw_entrega_pedido_status AS
        SELECT
            entrega.id_entrega AS "ID da Entrega",
            entrega.id_pedido AS "ID do Pedido",
            pedido.valor_pedido AS "Valor do Pedido",
            pedido.data_pedido AS "Data do Pedido",
            status_entrega.estado_entrega AS "Status da Entrega"
        FROM entrega, pedido, status_entrega
        WHERE entrega.id_pedido = pedido.id_pedido
        AND entrega.id_statusEtre = status_entrega.id_statusEtre
    """),
    # View com entrega, endereco e cliente.
    ("vw_entrega_endereco_cliente", """
        CREATE OR REPLACE VIEW vw_entrega_endereco_cliente AS
        SELECT
            entrega.id_entrega AS "ID da Entrega",
            cliente.nome_cliente AS "Nome do Cliente",
            endereco.rua AS "Rua",
            endereco.numero AS "Numero da Casa",
            endereco.bairro AS "Bairro",
            endereco.cidade AS "Cidade",
            endereco.estado AS "Estado",
            endereco.cep AS "CEP"
        FROM entrega, endereco, cliente
        WHERE entrega.id_endereco = endereco.id_endereco
        AND endereco.id_cliente = cliente.id_cliente
    """),
    # View com avaliacao, cliente e produto.
    ("vw_avaliacao_cliente_produto", """
        CREATE OR REPLACE VIEW vw_avaliacao_cliente_produto AS
        SELECT
            avaliacao.id_avaliacao AS "ID da Avaliacao",
            cliente.nome_cliente AS "Nome do Cliente",
            produto.nome_produto AS "Nome do Produto",
            avaliacao.nota AS "Nota",
            produto.valor_produto AS "Valor do Produto"
        FROM avaliacao, cliente, produto
        WHERE avaliacao.id_cliente = cliente.id_cliente
        AND avaliacao.id_produto = produto.id_produto
    """),
    # View com pedido, cliente e pagamento.
    ("vw_pedido_cliente_pagamento", """
        CREATE OR REPLACE VIEW vw_pedido_cliente_pagamento AS
        SELECT
            pedido.id_pedido AS "ID do Pedido",
            cliente.nome_cliente AS "Nome do Cliente",
            pagamento.id_pagamento AS "ID do Pagamento",
            pagamento.status_pagamento AS "Status do Pagamento"
        FROM pedido, cliente, pagamento
        WHERE pedido.id_cliente = cliente.id_cliente
        AND pedido.id_pedido = pagamento.id_pedido
    """),
    # View com item do pedido e cliente.
    ("vw_item_pedido_cliente", """
        CREATE OR REPLACE VIEW vw_item_pedido_cliente AS
        SELECT
            item_pedido.id_itens AS "ID do Item",
            cliente.nome_cliente AS "Nome do Cliente",
            pedido.id_pedido AS "ID do Pedido",
            item_pedido.qtd_produto AS "Quantidade",
            pedido.valor_pedido AS "Valor do Pedido",
            pedido.data_pedido AS "Data do Pedido"
        FROM item_pedido, pedido, cliente
        WHERE item_pedido.id_pedido = pedido.id_pedido
        AND pedido.id_cliente = cliente.id_cliente
    """),
    # View com item do pedido, produto e categoria.
    ("vw_item_produto_categoria", """
        CREATE OR REPLACE VIEW vw_item_produto_categoria AS
        SELECT
            item_pedido.id_itens AS "ID do Item",
            produto.nome_produto AS "Nome do Produto",
            produto.valor_produto AS "Valor do Produto",
            categoria.categoria AS "Categoria do Produto",
            item_pedido.qtd_produto AS "Quantidade do Item"
        FROM item_pedido, produto, categoria
        WHERE item_pedido.id_produto = produto.id_produto
        AND produto.id_categoria = categoria.id_categoria
    """),
    # View com entrega, pedido, cliente e endereco.
    ("vw_entrega_pedido_cliente_endereco", """
        CREATE OR REPLACE VIEW vw_entrega_pedido_cliente_endereco AS
        SELECT
            entrega.id_entrega AS "ID da Entrega",
            cliente.nome_cliente AS "Nome do Cliente",
            pedido.id_pedido AS "ID do Pedido",
            pedido.valor_pedido AS "Valor do Pedido",
            pedido.data_pedido AS "Data do Pedido",
            endereco.rua AS "Rua",
            endereco.numero AS "Numero da Casa",
            endereco.bairro AS "Bairro",
            endereco.cidade AS "Cidade",
            endereco.estado AS "Estado",
            endereco.cep AS "CEP"
        FROM entrega, pedido, cliente, endereco
        WHERE entrega.id_pedido = pedido.id_pedido
        AND pedido.id_cliente = cliente.id_cliente
        AND entrega.id_endereco = endereco.id_endereco
    """),
    # View dos produtos mais caros.
    ("vw_produtos_caros", """
        CREATE OR REPLACE VIEW vw_produtos_caros AS
        SELECT
            produto.id_produto AS "ID do Produto",
            produto.nome_produto AS "Nome do Produto",
            produto.valor_produto AS "Valor do Produto"
        FROM produto
        WHERE valor_produto > 100
    """),
    # View que filtra a cliente Ana Costa.
    ("vw_cliente_ana", """
        CREATE OR REPLACE VIEW vw_cliente_ana AS
        SELECT
            cliente.id_cliente AS "ID do Cliente",
            cliente.nome_cliente AS "Nome do Cliente"
        FROM cliente
        WHERE nome_cliente = 'Ana Costa'
    """),
    # View com pedidos recentes.
    ("vw_pedidos_recentes", """
        CREATE OR REPLACE VIEW vw_pedidos_recentes AS
        SELECT
            pedido.id_pedido AS "ID do Pedido",
            pedido.valor_pedido AS "Valor do Pedido",
            pedido.data_pedido AS "Data do Pedido"
        FROM pedido
        WHERE data_pedido > '2026-05-10'
    """),
    # View com pagamentos pagos.
    ("vw_pagamentos_pagos", """
        CREATE OR REPLACE VIEW vw_pagamentos_pagos AS
        SELECT
            pagamento.id_pagamento AS "ID do Pagamento",
            pagamento.id_pedido AS "ID do Pedido",
            pagamento.status_pagamento AS "Status do Pagamento"
        FROM pagamento
        WHERE status_pagamento = 'Pago'
    """),
    # View com avaliacoes boas.
    ("vw_avaliacoes_boas", """
        CREATE OR REPLACE VIEW vw_avaliacoes_boas AS
        SELECT
            avaliacao.id_avaliacao AS "ID da Avaliacao",
            avaliacao.nota AS "Nota"
        FROM avaliacao
        WHERE nota >= 4.0
    """),
    # View com pedido, pagamento, cliente e status.
    ("vw_pedido_pagamento_cliente_status", """
        CREATE OR REPLACE VIEW vw_pedido_pagamento_cliente_status AS
        SELECT
            pedido.id_pedido AS "ID do Pedido",
            cliente.nome_cliente AS "Nome do Cliente",
            status_pedido.status_pedido AS "Status do Pedido",
            pagamento.status_pagamento AS "Status do Pagamento",
            forma_pagamento.formaPagamento AS "Forma de Pagamento"
        FROM pedido, cliente, status_pedido, pagamento, forma_pagamento
        WHERE pedido.id_cliente = cliente.id_cliente
        AND pedido.id_statusped = status_pedido.id_statusped
        AND pedido.id_pedido = pagamento.id_pedido
        AND pagamento.id_formaPagamento = forma_pagamento.id_formaPagamento
    """),
    # View com clientes em ordem alfabetica.
    ("vw_clientes_ordenados", """
        CREATE OR REPLACE VIEW vw_clientes_ordenados AS
        SELECT
            cliente.id_cliente AS "ID do Cliente",
            cliente.nome_cliente AS "Nome do Cliente"
        FROM cliente
        ORDER BY nome_cliente
    """),
    # View com produtos em ordem de valor decrescente.
    ("vw_produtos_preco_desc", """
        CREATE OR REPLACE VIEW vw_produtos_preco_desc AS
        SELECT
            produto.id_produto AS "ID do Produto",
            produto.nome_produto AS "Nome do Produto",
            produto.valor_produto AS "Valor do Produto"
        FROM produto
        ORDER BY valor_produto DESC
    """),
    # View com pedidos ordenados por data.
    ("vw_pedidos_data", """
        CREATE OR REPLACE VIEW vw_pedidos_data AS
        SELECT
            pedido.id_pedido AS "ID do Pedido",
            pedido.valor_pedido AS "Valor do Pedido",
            pedido.data_pedido AS "Data do Pedido"
        FROM pedido
        ORDER BY data_pedido
    """),
    # View com avaliacoes ordenadas pela nota.
    ("vw_avaliacoes_nota", """
        CREATE OR REPLACE VIEW vw_avaliacoes_nota AS
        SELECT
            avaliacao.id_avaliacao AS "ID da Avaliacao",
            avaliacao.nota AS "Nota"
        FROM avaliacao
        ORDER BY nota DESC
    """),
    # View com categorias em ordem alfabetica.
    ("vw_categoria_ordem", """
        CREATE OR REPLACE VIEW vw_categoria_ordem AS
        SELECT
            categoria.id_categoria AS "ID da Categoria",
            categoria.categoria AS "Nome da Categoria"
        FROM categoria
        ORDER BY categoria
    """),
    # View com quantidade de produtos por categoria.
    ("vw_qtd_produtos_categoria", """
        CREATE OR REPLACE VIEW vw_qtd_produtos_categoria AS
        SELECT
            id_categoria AS "ID da Categoria",
            COUNT(*) AS "Quantidade de Produtos"
        FROM produto
        GROUP BY id_categoria
    """),
    # View com total de pagamentos por status.
    ("vw_total_status_pagamento", """
        CREATE OR REPLACE VIEW vw_total_status_pagamento AS
        SELECT
            status_pagamento AS "Status do Pagamento",
            COUNT(*) AS "Total de Pagamentos"
        FROM pagamento
        GROUP BY status_pagamento
    """),
    # View com total de pedidos por cliente.
    ("vw_total_pedidos_cliente", """
        CREATE OR REPLACE VIEW vw_total_pedidos_cliente AS
        SELECT
            id_cliente AS "ID do Cliente",
            COUNT(*) AS "Total de Pedidos"
        FROM pedido
        GROUP BY id_cliente
    """),
    # View com total de pagamentos por forma.
    ("vw_total_forma_pagamento", """
        CREATE OR REPLACE VIEW vw_total_forma_pagamento AS
        SELECT
            id_formaPagamento AS "ID da Forma de Pagamento",
            COUNT(*) AS "Total de Pagamentos"
        FROM pagamento
        GROUP BY id_formaPagamento
    """),
    # View com total de pedidos por status.
    ("vw_total_status_pedido", """
        CREATE OR REPLACE VIEW vw_total_status_pedido AS
        SELECT
            id_statusped AS "ID do Status do Pedido",
            COUNT(*) AS "Total de Pedidos"
        FROM pedido
        GROUP BY id_statusped
    """),
]


def conectar():
    # Abre a conexao se ela ainda nao existir.
    global conexao, cursor

    if conexao is not None and conexao.is_connected():
        # Se ja existe uma conexao aberta, reaproveita ela.
        return True

    try:
        # Configura a conexao com o banco local do projeto.
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="loja_virtual",
        )

        if conexao.is_connected():
            # Cria o cursor para executar os comandos SQL.
            cursor = conexao.cursor()
            print("Conectado com sucesso")
            return True

        print("Nao conectou")
        return False

    except Exception as erro:
        print("ERRO:")
        print(erro)
        return False


def garantir_conexao():
    # Reusa a conexao aberta; se precisar, conecta de novo.
    if conexao is not None and conexao.is_connected():
        return True
    return conectar()


def listar_consultas(usar_views=False):
    # Lista os nomes que aparecem na tela.
    if usar_views:
        # Quando a tela estiver em views, devolve so as views.
        return [nome for nome, _ in DEFINICOES_VIEWS]

    # Caso contrario, devolve as consultas normais.
    return [nome for nome, _ in CONSULTAS_BASE]


def executar_sql(sql):
    # Executa uma query e devolve colunas + linhas.
    if not garantir_conexao():
        raise RuntimeError("Nao foi possivel conectar ao banco de dados")

    # Envia o SQL para o banco.
    cursor.execute(sql)

    if cursor.description is None:
        # Se a query nao devolver linhas, apenas confirma a alteracao.
        conexao.commit()
        return [], []

    # Monta a lista de colunas retornadas.
    colunas = [descricao[0] for descricao in cursor.description]
    # Pega todas as linhas do resultado.
    linhas = cursor.fetchall()
    return colunas, linhas


def listar_valores_coluna(tabela, coluna):
    # Retorna os valores existentes de uma coluna para validar chave estrangeira.
    if not garantir_conexao():
        raise RuntimeError("Nao foi possivel conectar ao banco de dados")

    # Busca todos os valores da coluna informada.
    cursor.execute(f"SELECT {coluna} FROM {tabela}")
    return [linha[0] for linha in cursor.fetchall()]


def valor_existe_em_tabela(tabela, coluna, valor):
    # Usa a lista de valores da tabela para confirmar se o ID existe.
    valores = listar_valores_coluna(tabela, coluna)
    return valor in valores


def executar_consulta(nome_consulta, usar_views=False):
    # Procura a consulta pelo nome e executa.
    consultas = DEFINICOES_VIEWS if usar_views else CONSULTAS_BASE

    for nome, sql in consultas:
        if nome == nome_consulta:
            if usar_views:
                # Em views, executa sempre SELECT * FROM view.
                sql = f"SELECT * FROM {nome}"
            return executar_sql(sql)

    raise ValueError(f"Consulta nao encontrada: {nome_consulta}")


def criar_views():
    # Cria ou atualiza todas as views do projeto.
    if not garantir_conexao():
        return False

    try:
        # Percorre todas as definicoes e recria as views.
        for nome, sql in DEFINICOES_VIEWS:
            # Executa a definicao da view no banco.
            cursor.execute(sql)
            print(f"{nome} criada com sucesso")

        # Confirma a criacao das views.
        conexao.commit()
        return True

    except Exception as erro:
        print("ERRO:")
        print(erro)
        return False
    


def criar_triggers():
    # Cria ou atualiza os triggers do projeto.
    if not garantir_conexao():
        return False

    try:
        # Apaga o trigger antigo e cria de novo com a definicao atual.
        for nome, sql in trigger_consulta:
            # Remove a versao antiga antes de recriar.
            cursor.execute(f"DROP TRIGGER IF EXISTS {nome}")
            # Cria o trigger com a definicao atual.
            cursor.execute(sql)
            print(f"{nome} criada com sucesso")

        # Confirma a criacao dos triggers.
        conexao.commit()
        return True

    except Exception as erro:
        print("ERRO:")
        print(erro)
        return False


def criar_stored_procedures():
    # Cria ou atualiza as stored procedures do projeto.
    if not garantir_conexao():
        return False

    try:
        # Apaga cada procedure antiga para evitar conflito ao recriar.
        for nome, _qtd_parametros, sql in stored_procedure_consulta:
            # Remove a procedure antiga antes de criar a nova.
            cursor.execute(f"""
                DROP PROCEDURE IF EXISTS {nome}
            """)

            # Cria a procedure atualizada.
            cursor.execute(sql)

            print(f"{nome} criada com sucesso")

        # Confirma a criacao das procedures.
        conexao.commit()
        return True

    except Exception as erro:
        print("ERRO:")
        print(erro)
        return False

def listar_stored_procedures():
    # Retorna apenas os nomes das procedures para a tela.
    return [nome for nome, _, _ in stored_procedure_consulta]


def obter_qtd_parametros_procedure(nome_procedure):
    # A interface usa isso para decidir se precisa pedir parametros.
    for nome, qtd_parametros, _ in stored_procedure_consulta:
        if nome == nome_procedure:
            return qtd_parametros

    # Se nao achar a procedure, assume zero parametros.
    return 0


def executar_stored_procedure(nome_procedure, parametros=None):
    # Executa a procedure com ou sem parametros.

    if not garantir_conexao():
        raise RuntimeError("Nao foi possivel conectar ao banco")

    # Se nada for passado, usa lista vazia para nao quebrar o callproc.
    if parametros is None:
        parametros = []

    # Chama a procedure com os parametros informados.
    cursor.callproc(nome_procedure, parametros)

    # Lê o resultado devolvido pela procedure para mostrar no Tkinter.
    for resultado in cursor.stored_results():

        colunas = [desc[0] for desc in resultado.description]

        linhas = resultado.fetchall()

        return colunas, linhas

    return [], []


def fecharConexao():
    # Fecha a conexao quando o programa sair.
    global conexao, cursor

    try:
        if conexao is not None and conexao.is_connected():
            conexao.close()
            print("Conexao fechada com sucesso")

        cursor = None
        conexao = None

    except Exception as erro:
        print("ERRO:")
        print(erro)
