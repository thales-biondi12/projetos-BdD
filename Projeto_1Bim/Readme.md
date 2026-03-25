🏢 Sistema de Gestão de Condomínio (Banco de Dados)

Projeto de Banco de Dados desenvolvido para simular a gestão de um condomínio, incluindo controle de unidades, moradores, cobranças, pagamentos, ocorrências e reservas de áreas comuns.

📌 Descrição

Este projeto tem como objetivo modelar e implementar um banco de dados relacional capaz de gerenciar informações essenciais de um condomínio, permitindo consultas para análise, auditoria e controle administrativo.

🛠️ Tecnologias Utilizadas

🗄️ MySQL

💻 SQL

📂 Estrutura do Banco de Dados

O sistema é composto pelas seguintes entidades:

unidades → controle de ocupação (ocupada/vazia)

moradores → dados dos residentes

his_moradores → histórico de moradores por unidade

cobrancas → valores cobrados por unidade

pagamentos → controle de pagamentos

funcionarios → funcionários do condomínio

ocorrencias → registros de incidentes

reservas → reservas de áreas comuns

🔗 Relacionamentos

Uma unidade pode ter vários moradores ao longo do tempo

Uma cobrança pertence a uma unidade

Um pagamento está vinculado a uma cobrança

Uma ocorrência envolve uma unidade e um funcionário

Uma reserva está associada a uma unidade

📚 Funcionalidades (Consultas SQL)

O projeto inclui consultas para:

📌 Listar unidades e seus status

📌 Exibir histórico de moradores

📌 Listar moradores ativos

📌 Consultar reservas por data

📌 Identificar conflitos de reservas (auditoria)

📌 Exibir ocorrências por período

📌 Calcular arrecadação mensal

📌 Identificar unidades inadimplentes

📌 Ranking de unidades com mais ocorrências

📌 Detectar mudanças de moradores

🎯 Objetivo

Praticar modelagem de banco de dados

Aplicar conceitos de SQL na prática

Simular um sistema real de gestão condominial

Desenvolver consultas analíticas e de auditoria

🚀 Como Executar

Clone o repositório:
git clone https://github.com/thales-biondi12/projetos-BdD.git

Abra o MySQL Workbench (ou outro SGBD)

Execute o script SQL presente no projeto

Rode as consultas para análise dos dados

👨‍💻 Autor

Thales Andrade Biondi