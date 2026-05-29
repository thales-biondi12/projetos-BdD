import tkinter as tk
from tkinter import messagebox, simpledialog

from prettytable import PrettyTable

import conexao


# Evita nomes repetidos quando a query traz colunas iguais.
def nomes_unicos(colunas):
    # Guarda quantas vezes cada nome apareceu.
    usados = {}
    # Lista final com nomes ajustados.
    resultado = []

    for coluna in colunas:
        # Converte o nome para texto para evitar erro com valores nulos.
        nome = str(coluna)
        # Conta a ocorrencia da coluna.
        usados[nome] = usados.get(nome, 0) + 1

        if usados[nome] == 1:
            # Primeira vez que aparece: usa o nome normal.
            resultado.append(nome)
        else:
            # Se repetir, adiciona um numero no final.
            resultado.append(f"{nome}_{usados[nome]}")

    return resultado


# Converte a string digitada pelo usuario em uma lista de valores.
def separar_parametros(texto):
    # Transforma a string digitada em valores de verdade.
    # Exemplo: "1, Pago, 2" vira [1, "Pago", 2].
    parametros = []

    for item in texto.split(","):
        # Remove espacos antes e depois do valor.
        valor = item.strip()

        if valor == "":
            # Ignora pedacos vazios.
            continue

        try:
            # Tenta converter para inteiro primeiro.
            parametros.append(int(valor))
            continue
        except ValueError:
            pass

        try:
            # Se nao for inteiro, tenta converter para decimal.
            parametros.append(float(valor))
            continue
        except ValueError:
            pass

        # Se nao for numero, deixa como texto.
        parametros.append(valor)

    return parametros


# Monta uma ajuda simples para a procedure escolhida.
def texto_parametros_procedure(nome_procedure):
    # Procedure de pagamento.
    if nome_procedure == "sp_registrar_pagamento":
        return (
            "Digite os parametros nesta ordem:\n"
            "1. id_pedido\n"
            "2. status_pagamento\n"
            "3. id_formaPagamento\n\n"
            "Exemplo: 1, Pago, 2"
        )

    # Procedure de pedidos por cliente.
    if nome_procedure == "proc_pedidos_por_cliente":
        return (
            "Digite o ID do cliente.\n\n"
            "Exemplo: 4"
        )

    # Procedure de produtos por categoria.
    if nome_procedure == "proc_produtos_por_categoria":
        return (
            "Digite o ID da categoria.\n\n"
            "Exemplo: 1"
        )

    # Procedure de pagamentos por status.
    if nome_procedure == "proc_pagamentos_por_status":
        return (
            "Digite o status do pagamento.\n\n"
            "Exemplo: Pago"
        )

    # Ajuda padrao para procedures simples.
    return "Digite os parametros separados por virgula."



def carregar_consultas():
    # Limpa a lista antes de carregar outro tipo de consulta.
    lista.delete(0, tk.END)

    if tipo_var.get() == "views":
        # Carrega os nomes das views.
        consultas = conexao.listar_consultas(True)

    elif tipo_var.get() == "stored_procedures":
        # Carrega os nomes das procedures.
        consultas = conexao.listar_stored_procedures()

    else:
        # Carrega as consultas normais.
        consultas = conexao.listar_consultas(False)

    # Coloca cada nome dentro da lista da tela.
    for consulta in consultas:
        lista.insert(tk.END, consulta)

    if consultas:
        # Seleciona a primeira opcao por padrao.
        lista.selection_set(0)
        lista.activate(0)

    # Atualiza o texto de status.
    status_var.set("Lista carregada")


def mostrar_resultado(colunas, linhas):
    # Mostra o retorno da consulta em tabela no campo de texto.
    saida.delete("1.0", tk.END)

    if not colunas:
        # Quando nao ha colunas, a consulta nao retornou linhas de leitura.
        saida.insert(tk.END, "Consulta executada, mas sem retorno.\n")
        return

    # Cria a tabela bonita do PrettyTable.
    tabela = PrettyTable()
    # Ajusta nomes duplicados para nao quebrar o PrettyTable.
    tabela.field_names = nomes_unicos(colunas)
    # Deixa as colunas alinhadas pela esquerda.
    tabela.align = "l"

    # Adiciona cada linha retornada pela consulta.
    for linha in linhas:
        tabela.add_row([str(valor) for valor in linha])

    # Escreve a tabela pronta no campo de texto.
    saida.insert(tk.END, str(tabela))
    saida.insert(tk.END, "\n")


def criar_views():
    # Cria ou atualiza as views antes de consultar.
    if conexao.criar_views():
        # Mostra mensagem se deu certo.
        messagebox.showinfo("Views", "Views criadas com sucesso.")
        status_var.set("Views prontas")
    else:
        # Mostra mensagem se algo falhou.
        messagebox.showerror("Erro", "Nao foi possivel criar as views.")


def criar_triggers():
    # Cria ou atualiza os triggers antes de consultar.
    if conexao.criar_triggers():
        # Mostra mensagem se deu certo.
        messagebox.showinfo("Triggers", "Triggers criados com sucesso.")
        status_var.set("Triggers prontos")
    else:
        # Mostra mensagem se algo falhou.
        messagebox.showerror("Erro", "Nao foi possivel criar os triggers.")



def criar_stored_procedures():
    # Cria ou atualiza as stored procedures antes de consultar.
    if conexao.criar_stored_procedures():
        # Mostra mensagem quando as procedures ficam prontas.
        messagebox.showinfo("Stored Procedures", "Stored Procedures criadas com sucesso.")
        status_var.set("Stored Procedures prontas")
    else:
        # Mostra mensagem de erro.
        messagebox.showerror("Erro", "Nao foi possivel criar as stored procedures.")


def executar():
    # Executa a consulta selecionada pelo usuario.
    # Pega a posicao selecionada na lista.
    selecao = lista.curselection()

    if not selecao:
        # Se nada foi selecionado, avisa o usuario.
        messagebox.showwarning("Aviso", "Selecione uma consulta.")
        return

    # Recupera o nome da consulta clicada.
    nome_consulta = lista.get(selecao[0])

    # Descobre o tipo atual escolhido na tela.
    usar_views = tipo_var.get() == "views"
    usar_procedures = tipo_var.get() == "stored_procedures"

    try:
        # Se for view, recria as views antes de consultar.
        if usar_views:
            # Executa a consulta da view.
            colunas, linhas = conexao.executar_consulta(
                nome_consulta,
                True
            )

        # Se for procedure, trata parametros antes de chamar.
        elif usar_procedures:
            # Descobre quantos parametros a procedure espera.
            qtd_parametros = conexao.obter_qtd_parametros_procedure(nome_consulta)

            # Lista vazia usada quando nao ha parametros.
            parametros = []

            # Se a procedure tiver parametros, pede ao usuario na tela.
            if qtd_parametros > 0:
                # Abre a caixinha de texto com uma explicacao.
                texto = simpledialog.askstring(
                    "Parametros da procedure",
                    texto_parametros_procedure(nome_consulta)
                )

                if texto is None:
                    # Se o usuario cancelar, para a execucao.
                    status_var.set("Execucao cancelada")
                    return

                # Separa o texto digitado em parametros reais.
                parametros = separar_parametros(texto)

                # Garante que a quantidade digitada bate com a procedure.
                if len(parametros) != qtd_parametros:
                    # Mostra erro se a quantidade estiver errada.
                    messagebox.showerror(
                        "Erro",
                        f"Essa procedure precisa de {qtd_parametros} parametro(s)."
                    )
                    status_var.set("Quantidade de parametros invalida")
                    return

            # Valida as chaves estrangeiras antes de inserir.
            if nome_consulta == "sp_registrar_pagamento":
                # A procedure de pagamento precisa de IDs que existam no banco.
                # O primeiro parametro eh o id do pedido.
                id_pedido = parametros[0]
                # O terceiro parametro eh o id da forma de pagamento.
                id_forma_pagamento = parametros[2]

                if not conexao.valor_existe_em_tabela("pedido", "id_pedido", id_pedido):
                    # Busca os IDs validos para mostrar ao usuario.
                    ids_pedido = conexao.listar_valores_coluna("pedido", "id_pedido")
                    messagebox.showerror(
                        "Erro",
                        f"Pedido invalido. IDs existentes: {ids_pedido}"
                    )
                    status_var.set("Pedido invalido")
                    return

                if not conexao.valor_existe_em_tabela("forma_pagamento", "id_formaPagamento", id_forma_pagamento):
                    ids_forma = conexao.listar_valores_coluna("forma_pagamento", "id_formaPagamento")
                    messagebox.showerror(
                        "Erro",
                        f"Forma de pagamento invalida. IDs existentes: {ids_forma}"
                    )
                    status_var.set("Forma de pagamento invalida")
                    return

            if nome_consulta == "proc_pedidos_por_cliente":
                # A procedure de pedidos precisa de um cliente valido.
                # O unico parametro eh o id do cliente.
                id_cliente = parametros[0]

                if not conexao.valor_existe_em_tabela("cliente", "id_cliente", id_cliente):
                    # Mostra os IDs validos da tabela cliente.
                    ids_cliente = conexao.listar_valores_coluna("cliente", "id_cliente")
                    messagebox.showerror(
                        "Erro",
                        f"Cliente invalido. IDs existentes: {ids_cliente}"
                    )
                    status_var.set("Cliente invalido")
                    return

            if nome_consulta == "proc_produtos_por_categoria":
                # A procedure de produtos precisa de uma categoria valida.
                # O unico parametro eh o id da categoria.
                id_categoria = parametros[0]

                if not conexao.valor_existe_em_tabela("categoria", "id_categoria", id_categoria):
                    # Mostra os IDs validos da tabela categoria.
                    ids_categoria = conexao.listar_valores_coluna("categoria", "id_categoria")
                    messagebox.showerror(
                        "Erro",
                        f"Categoria invalida. IDs existentes: {ids_categoria}"
                    )
                    status_var.set("Categoria invalida")
                    return

            # Executa a procedure com os parametros tratados.
            colunas, linhas = conexao.executar_stored_procedure(
                nome_consulta,
                parametros
            )

        else:
            # Executa uma consulta normal.
            colunas, linhas = conexao.executar_consulta(
                nome_consulta,
                False
            )

        # Mostra o resultado na tela.
        mostrar_resultado(colunas, linhas)

        # Atualiza a barra de status com o nome executado.
        status_var.set(f"Executado: {nome_consulta}")

    except Exception as erro:
        # Mostra qualquer erro que acontecer na execucao.
        messagebox.showerror("Erro", str(erro))

        # Marca o status como erro.
        status_var.set("Erro ao executar")




def trocar_tipo():
    # Recarrega as consultas quando troca entre normal e views.
    carregar_consultas()
    saida.delete("1.0", tk.END)


def fechar():
    # Fecha a conexao do banco e fecha a janela do programa.
    conexao.fecharConexao()
    janela.destroy()


janela = tk.Tk()
# Titulo principal da janela.
janela.title("Loja Virtual")
# Tamanho inicial da tela.
janela.geometry("1000x700")

# Barra superior simples do programa.
topo = tk.Frame(janela)
topo.pack(fill="x", padx=10, pady=10)

# Nome do sistema.
tk.Label(topo, text="Sistema de Consultas", font=("Arial", 16, "bold")).pack(anchor="w")
# Texto de status que aparece na parte de cima.
status_var = tk.StringVar(value="Pronto")
tk.Label(topo, textvariable=status_var).pack(anchor="w")

# Faixa de botoes principais.
linha_botoes = tk.Frame(janela)
linha_botoes.pack(fill="x", padx=10)

# Acoes principais do sistema.
tk.Button(linha_botoes, text="Criar views", command=criar_views).pack(side="left", padx=(0, 5))
tk.Button(linha_botoes, text="criar stored procedures", command=conexao.criar_stored_procedures).pack(side="left", padx=(0, 5))
tk.Button(linha_botoes, text="criar triggers", command=conexao.criar_triggers).pack(side="left", padx=(0, 5))
tk.Button(linha_botoes, text="Executar", command=executar).pack(side="left", padx=(0, 5))
tk.Button(linha_botoes, text="Sair", command=fechar).pack(side="right")

tipo_var = tk.StringVar(value="normal")

# Linha dos tipos de consulta, logo abaixo dos botoes.
linha_tipo = tk.Frame(janela)
linha_tipo.pack(fill="x", padx=10, pady=(8, 0))

# Tipos de consulta lado a lado.
tk.Radiobutton(
    linha_tipo,
    text="Consultas normais",
    variable=tipo_var,
    value="normal",
    command=trocar_tipo,
).pack(side="left")
tk.Radiobutton(
    linha_tipo,
    text="Consultas com views",
    variable=tipo_var,
    value="views",
    command=trocar_tipo,
).pack(side="left", padx=(10, 0))
tk.Radiobutton(
    linha_tipo,
    text="stored procedures",
    variable=tipo_var,
    value="stored_procedures",
    command=trocar_tipo,
).pack(side="left", padx=(10, 0))

# Area principal da tela.
meio = tk.Frame(janela)
meio.pack(fill="both", expand=True, padx=10, pady=10)

# Painel da esquerda.
esquerda = tk.Frame(meio)
esquerda.pack(side="left", fill="y")

# Lista com os nomes das consultas/procedures/views.
tk.Label(esquerda, text="Consultas").pack(anchor="w", pady=(12, 0))
lista = tk.Listbox(esquerda, width=40, height=25)
lista.pack(fill="y", expand=False)

# Painel do resultado.
direita = tk.Frame(meio)
direita.pack(side="right", fill="both", expand=True)

# Titulo da area de saida.
tk.Label(direita, text="Resultado").pack(anchor="w")
# Campo de texto que mostra o PrettyTable.
saida = tk.Text(direita, wrap="none")
saida.pack(fill="both", expand=True)

# Carrega a lista inicial.
carregar_consultas()
# Fecha corretamente a conexao quando a janela fechar.
janela.protocol("WM_DELETE_WINDOW", fechar)
# Inicia o loop da interface.
janela.mainloop()
