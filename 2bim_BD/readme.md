# Sistema de Banco de Dados — Loja Virtual

## 📌 Descrição do Projeto

Este projeto consiste na modelagem e implementação de um banco de dados relacional para uma loja virtual utilizando MySQL.

O sistema foi desenvolvido com o objetivo de gerenciar informações relacionadas a:

- Clientes
- Endereços
- Produtos
- Categorias
- Pedidos
- Pagamentos
- Entregas
- Avaliações de produtos

A estrutura foi organizada seguindo conceitos de modelagem relacional, utilizando chaves primárias e estrangeiras para garantir integridade e relacionamento entre os dados.

---

# 🛠️ Tecnologias Utilizadas

- MySQL
- SQL
- XAMPP
- MySQL Workbench

---

# 📂 Estrutura do Banco de Dados

O banco de dados `loja_virtual` possui as seguintes tabelas:

| Tabela | Descrição |
|---|---|
| `cliente` | Armazena informações dos clientes |
| `endereco` | Guarda os endereços dos clientes |
| `categoria` | Categorias dos produtos |
| `produto` | Cadastro de produtos |
| `avaliacao` | Avaliações feitas pelos clientes |
| `status_pedido` | Status dos pedidos |
| `pedido` | Informações dos pedidos |
| `item_pedido` | Produtos presentes em cada pedido |
| `status_entrega` | Status das entregas |
| `entrega` | Controle das entregas |
| `forma_pagamento` | Métodos de pagamento |
| `pagamento` | Registro dos pagamentos |

---

# 🔗 Relacionamentos

O projeto utiliza relacionamentos entre tabelas através de `FOREIGN KEY`, garantindo consistência dos dados.

### Exemplos:
- Um cliente pode possuir vários endereços
- Um pedido pertence a um cliente
- Um pedido pode conter vários produtos
- Um produto pertence a uma categoria
- Um pagamento está vinculado a um pedido

---

# 📋 Funcionalidades do Banco

✔ Cadastro de clientes  
✔ Cadastro de produtos  
✔ Controle de categorias  
✔ Gerenciamento de pedidos  
✔ Controle de entregas  
✔ Registro de pagamentos  
✔ Avaliações de produtos  
✔ Integridade relacional com chaves estrangeiras  

---

# 🗄️ Modelo Relacional

## Principais Entidades

### Cliente
Responsável por armazenar os dados dos usuários da loja.

### Produto
Contém os produtos disponíveis para venda.

### Pedido
Armazena informações sobre compras realizadas.

### Pagamento
Gerencia os pagamentos efetuados.

### Entrega
Controla o processo de envio dos pedidos.

---

# 🚀 Como Executar o Projeto

## 1️⃣ Criar o banco de dados

```sql
CREATE DATABASE loja_virtual;
```

## 2️⃣ Selecionar o banco

```sql
USE loja_virtual;
```

## 3️⃣ Executar o script SQL

Execute todo o script de criação das tabelas.

## 4️⃣ Inserir os dados

Execute os comandos `INSERT INTO` para popular o banco de dados.

---

# 📊 Exemplo de Consultas SQL

## Listar todos os produtos

```sql
SELECT * FROM produto;
```

## Listar pedidos com clientes

```sql
SELECT 
    pedido.id_pedido,
    cliente.nome_cliente,
    pedido.valor_pedido
FROM pedido
INNER JOIN cliente
ON pedido.id_cliente = cliente.id_cliente;
```

## Mostrar produtos e categorias

```sql
SELECT
    produto.nome_produto,
    categoria.categoria
FROM produto
INNER JOIN categoria
ON produto.id_categoria = categoria.id_categoria;
```

---

# 🎯 Objetivo Acadêmico

Este projeto foi desenvolvido para fins educacionais, com foco no aprendizado de:

- Modelagem de banco de dados
- Relacionamentos SQL
- Chaves primárias e estrangeiras
- Consultas SQL
- Estruturação de sistemas relacionais

---

# 👨‍💻 Autor

**Thales Biondi**  
**Italo garavelo** 
**Pedro Antoniassi** 
Desenvolvedor e estudante de programação.

---

# 📄 Licença

Este projeto é de uso educacional e livre para estudos e modificações.