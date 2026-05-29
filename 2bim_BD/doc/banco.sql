create database loja_virtual;
use loja_virtual;

create table cliente(
	id_cliente int primary key,
    nome_cliente varchar(50) not null
);

create table endereco(
	id_endereco int primary key,
    id_cliente int,
	rua varchar(100),
    numero varchar(10),
    bairro varchar(50),
    cidade varchar(50),
    estado varchar(30),
    cep varchar(10),
	foreign key (id_cliente) references cliente(id_cliente)
);

create table categoria(
	id_categoria int primary key,
	categoria varchar(20)
);

create table produto(
	id_produto int primary key,
    nome_produto varchar(50),
    valor_produto decimal(10, 2),
	id_categoria int,
    foreign key (id_categoria) references categoria(id_categoria)
);

create table avaliacao(
	id_avaliacao int primary key,
    id_cliente int,
    id_produto int,
    nota decimal(2,1),
	foreign key (id_cliente) references cliente(id_cliente),
	foreign key (id_produto) references produto(id_produto)
);

create table status_pedido(
	id_statusped int primary key,
    status_pedido varchar(50)
);

create table pedido(
	id_pedido int primary key,
    valor_pedido decimal(10, 2),
    id_statusped int,
    id_cliente int,
    data_pedido date,
	foreign key (id_cliente) references cliente(id_cliente),
	foreign key (id_statusped) references status_pedido(id_statusped)
);

create table item_pedido(
	id_itens int primary key,
    id_pedido int,
    id_produto int,
    qtd_produto int,
	foreign key (id_pedido) references pedido(id_pedido),
    foreign key (id_produto) references produto(id_produto)
);

create table status_entrega(
	id_statusEtre int primary key,
    estado_entrega varchar(30)
);

create table entrega(
	id_entrega int primary key,
    id_endereco int,
    id_pedido int,
    id_statusEtre int,
	foreign key (id_statusEtre) references status_entrega(id_statusEtre),
	foreign key (id_endereco) references endereco(id_endereco),
	foreign key (id_pedido) references pedido(id_pedido)
);

create table forma_pagamento(
	id_formaPagamento int primary key,
    formaPagamento varchar(50)
);

create table pagamento(
	id_pagamento int primary key auto_increment,
    id_pedido int,
    status_pagamento varchar(50),
    id_formaPagamento int,
    foreign key (id_pedido) references pedido(id_pedido),
	foreign key (id_formaPagamento) references forma_pagamento(id_formaPagamento)
);


#CLIENTE 
insert into cliente values
(1,'João Silva'),
(2,'Maria Souza'),
(3,'Carlos Lima'),
(4,'Ana Costa'),
(5,'Pedro Santos'),
(6,'Lucas Alves'),
(7,'Fernanda Rocha'),
(8,'Juliana Gomes'),
(9,'Ricardo Pereira'),
(10,'Patricia Mendes');

#ENDERECO 
insert into endereco values
(1,1,'Rua Buenos Aires','144','Centro','São Paulo','SP','01001-000'),
(2,2,'Rua Santa Maria','122','Jardim América','Rio de Janeiro','RJ','22010-000'),
(3,3,'Rua Guilhermino','99','Vila Nova','Belo Horizonte','MG','30110-000'),
(4,4,'Rua Sampaio Correia','156','Centro','Curitiba','PR','80010-000'),
(5,5,'Rua John Kennedy','78','Jardim Paulista','Campinas','SP','13010-000'),
(6,6,'Rua Detroit','211','Industrial','Sorocaba','SP','18010-000'),
(7,7,'Rua Diamante Branco','94','Boa Vista','Salvador','BA','40010-000'),
(8,8,'Rua Bosnia','47','São José','Florianópolis','SC','88010-000'),
(9,9,'Rua João Da Silva','201','Centro','Recife','PE','50010-000'),
(10,10,'Rua D. Pedro','187','Vila Mariana','São Paulo','SP','04010-000');

#CATEGORIA 
insert into categoria values
(1,'Eletronico'),
(2,'Roupa'),
(3,'Livro'),
(4,'Casa'),
(5,'Esporte');

#PRODUTO 
insert into produto values
(1,'Mouse Gamer',120.00,1),
(2,'Teclado Mecânico',250.00,1),
(3,'Camiseta',50.00,2),
(4,'Calça Jeans',120.00,2),
(5,'Livro SQL',70.00,3),
(6,'Livro C++',80.00,3),
(7,'Panela',90.00,4),
(8,'Ventilador',200.00,4),
(9,'Bola Futebol',60.00,5),
(10,'Tênis Corrida',300.00,5);

#AVALIACAO
insert into avaliacao values
(1,1,1,4.5),
(2,2,2,5.0),
(3,3,5,4.0),
(4,4,8,2.5),
(5,5,10,5.0);

#STATUS_PEDIDO 
insert into status_pedido values
(1,'Em análise'),
(2,'Pago'),
(3,'Separando'),
(4,'Enviado'),
(5,'Entregue');

#STATUS_ENTREGA 
insert into status_entrega values
(1,'Preparando'),
(2,'Em trânsito'),
(3,'Saiu entrega'),
(4,'Entregue'),
(5,'Cancelada');

#FORMA_PAGAMENTO 
insert into forma_pagamento values
(1,'Pix'),
(2,'Cartão Crédito'),
(3,'Cartão Débito'),
(4,'Boleto'),
(5,'Dinheiro');

#PEDIDO 
insert into pedido values
(1,120,1,1,'2026-05-01'),
(2,250,2,2,'2026-05-02'),
(3,50,3,3,'2026-05-03'),
(4,120,4,4,'2026-05-04'),
(5,70,5,5,'2026-05-05'),
(6,80,1,6,'2026-05-06'),
(7,90,2,7,'2026-05-07'),
(8,200,3,8,'2026-05-08'),
(9,60,4,9,'2026-05-09'),
(10,300,5,10,'2026-05-10'),
(11,120,1,1,'2026-05-11'),
(12,250,2,2,'2026-05-12'),
(13,50,3,3,'2026-05-13'),
(14,120,4,4,'2026-05-14'),
(15,70,5,5,'2026-05-15'),
(16,80,1,6,'2026-05-16'),
(17,90,2,7,'2026-05-17'),
(18,200,3,8,'2026-05-18'),
(19,60,4,9,'2026-05-19'),
(20,300,5,10,'2026-05-20');

#ITEM_PEDIDO
insert into item_pedido values
(1,1,1,1),
(2,2,2,1),
(3,3,3,1),
(4,4,4,1),
(5,5,5,1),
(6,6,6,1),
(7,7,7,1),
(8,8,8,1),
(9,9,9,1),
(10,10,10,1),
(11,11,1,1),
(12,12,2,1),
(13,13,3,1),
(14,14,4,1),
(15,15,5,1),
(16,16,6,1),
(17,17,7,1),
(18,18,8,1),
(19,19,9,1),
(20,20,10,1);

#ENTREGA 
insert into entrega values
(1,1,1,1),
(2,2,2,2),
(3,3,3,3),
(4,4,4,4),
(5,5,5,1),
(6,6,6,2),
(7,7,7,3),
(8,8,8,4),
(9,9,9,1),
(10,10,10,2),
(11,1,11,3),
(12,2,12,4),
(13,3,13,1),
(14,4,14,2),
(15,5,15,3),
(16,6,16,4),
(17,7,17,1),
(18,8,18,2),
(19,9,19,3),
(20,10,20,4);

#PAGAMENTO
insert into pagamento values
(1,1,'Pendente',1),
(2,2,'Pago',2),
(3,3,'Pago',3),
(4,4,'Pendente',4),
(5,5,'Pago',5),
(6,6,'Pago',1),
(7,7,'Pendente',2),
(8,8,'Pago',3),
(9,9,'Pago',4),
(10,10,'Pendente',5),
(11,11,'Pago',1),
(12,12,'Pago',2),
(13,13,'Pendente',3),
(14,14,'Pago',4),
(15,15,'Pago',5),
(16,16,'Pendente',1),
(17,17,'Pago',2),
(18,18,'Pago',3),
(19,19,'Pendente',4),
(20,20,'Pago',5);

select * from cliente;

select * from endereco;

select * from categoria;

select * from produto;

select * from avaliacao;

select * from status_pedido;

select * from pedido;

select * from entrega;

select * from pagamento;

select nome_produto, valor_produto from produto;

select * from cliente, endereco where cliente.id_cliente = endereco.id_cliente;

select * from produto, categoria where produto.id_categoria = categoria.id_categoria;

select * from pedido, cliente where pedido.id_cliente = cliente.id_cliente;

select * from pedido, status_pedido where pedido.id_statusped = status_pedido.id_statusped;

select * from pagamento, forma_pagamento where pagamento.id_formaPagamento = forma_pagamento.id_formaPagamento;

select * from entrega, status_entrega where entrega.id_statusEtre = status_entrega.id_statusEtre;

select * from avaliacao, cliente where avaliacao.id_cliente = cliente.id_cliente;

select * from avaliacao, produto where avaliacao.id_produto = produto.id_produto;

select * from item_pedido, pedido where item_pedido.id_pedido = pedido.id_pedido;

select * from item_pedido, produto where item_pedido.id_produto = produto.id_produto;

create view vw_pedido_cliente_status as select * from pedido, cliente, status_pedido where 
pedido.id_cliente = cliente.id_cliente and pedido.id_statusped = status_pedido.id_statusped;

create view vw_produto_categoria_item as select * from produto, categoria, item_pedido where 
produto.id_categoria = categoria.id_categoria and produto.id_produto = item_pedido.id_produto;

create view vw_pedido_pagamento_forma as select * from pedido, pagamento, forma_pagamento where 
pedido.id_pedido = pagamento.id_pedido and pagamento.id_formaPagamento = forma_pagamento.id_formaPagamento;

create view vw_entrega_pedido_status as select * from entrega, pedido, status_entrega where
entrega.id_pedido = pedido.id_pedido and entrega.id_statusEtre = status_entrega.id_statusEtre;

create view vw_entrega_endereco_cliente as select * from entrega, endereco, cliente where 
entrega.id_endereco = endereco.id_endereco and endereco.id_cliente = cliente.id_cliente;

create view vw_avaliacao_cliente_produto as select * from avaliacao, cliente, produto where 
avaliacao.id_cliente = cliente.id_cliente and avaliacao.id_produto = produto.id_produto;

create view vw_pedido_cliente_pagamento as select * from pedido, cliente, pagamento where 
pedido.id_cliente = cliente.id_cliente and pedido.id_pedido = pagamento.id_pedido;

create view vw_item_pedido_cliente as select * from item_pedido, pedido, cliente where 
item_pedido.id_pedido = pedido.id_pedido and pedido.id_cliente = cliente.id_cliente;

create view vw_item_produto_categoria as select * from item_pedido, produto, categoria where 
item_pedido.id_produto = produto.id_produto and produto.id_categoria = categoria.id_categoria;

create view vw_entrega_pedido_cliente_endereco as select * from entrega, pedido, cliente, endereco where 
entrega.id_pedido = pedido.id_pedido and pedido.id_cliente = cliente.id_cliente and entrega.id_endereco = endereco.id_endereco;


create view vw_produtos_caros as select * from produto where valor_produto > 100;

create view vw_cliente_ana as select * from cliente where nome_cliente = 'Ana Costa';

create view vw_pedidos_recentes as select * from pedido where data_pedido > '2026-05-10';

create view vw_pagamentos_pagos as select * from pagamento where status_pagamento = 'Pago';

create view vw_avaliacoes_boas as select * from avaliacao where nota >= 4.0;


create view vw_clientes_ordenados as select * from cliente order by nome_cliente;

create view vw_produtos_preco_desc as select * from produto order by valor_produto desc;

create view vw_pedidos_data as select * from pedido order by data_pedido;

create view vw_avaliacoes_nota as select * from avaliacao order by nota desc;

create view vw_categoria_ordem as select * from categoria order by categoria;

create view vw_qtd_produtos_categoria as select id_categoria, count(*) as quantidade from produto group by id_categoria;

create view vw_total_status_pagamento as select status_pagamento, count(*) as total from pagamento group by status_pagamento;

create view vw_total_pedidos_cliente as select id_cliente, count(*) as pedidos from pedido group by id_cliente;

create view vw_total_forma_pagamento as select id_formaPagamento, count(*) as pagamentos from pagamento group by id_formaPagamento;

create view vw_total_status_pedido as select id_statusped, count(*) as total from pedido group by id_statusped;

drop view if exists vw_pedido_pagamento_cliente_status;
create view vw_pedido_pagamento_cliente_status as
select
    pedido.id_pedido as "ID do Pedido",
    cliente.nome_cliente as "Nome do Cliente",
    status_pedido.status_pedido as "Status do Pedido",
    pagamento.status_pagamento as "Status do Pagamento",
    forma_pagamento.formaPagamento as "Forma de Pagamento"
from pedido, cliente, status_pedido, pagamento, forma_pagamento
where pedido.id_cliente = cliente.id_cliente
and pedido.id_statusped = status_pedido.id_statusped
and pedido.id_pedido = pagamento.id_pedido
and pagamento.id_formaPagamento = forma_pagamento.id_formaPagamento;

drop trigger if exists trg_pagamento_pago;
delimiter $$
create trigger trg_pagamento_pago
after insert on pagamento
for each row
begin
    -- Quando o pagamento entra como pago, o pedido vira "Pago".
    if new.status_pagamento = 'Pago' then
        update pedido
        set id_statusped = 2
        where id_pedido = new.id_pedido;
    end if;
end $$
delimiter ;

drop trigger if exists trg_pedido_data_padrao;
delimiter $$
create trigger trg_pedido_data_padrao
before insert on pedido
for each row
begin
    -- Se a data nao vier preenchida, usa a data de hoje.
    if new.data_pedido is null then
        set new.data_pedido = curdate();
    end if;
end $$
delimiter ;

drop trigger if exists trg_entrega_finalizada;
delimiter $$
create trigger trg_entrega_finalizada
after update on entrega
for each row
begin
    -- Quando a entrega termina, o pedido fica como entregue.
    if new.id_statusEtre = 4 then
        update pedido
        set id_statusped = 5
        where id_pedido = new.id_pedido;
    end if;
end $$
delimiter ;

drop procedure if exists proc_relatorio_cliente;
delimiter $$
create procedure proc_relatorio_cliente()
begin
    select
        cliente.id_cliente,
        cliente.nome_cliente,
        count(pedido.id_pedido) as total_pedidos

    from cliente, pedido

    where cliente.id_cliente = pedido.id_cliente

    group by cliente.id_cliente, cliente.nome_cliente

    order by total_pedidos desc;
end $$
delimiter ;

drop procedure if exists sp_registrar_pagamento;
delimiter $$
create procedure sp_registrar_pagamento(
in p_id_pedido int,
in p_status_pagamento varchar(50),
in p_id_forma_pagamento int
)
begin
    -- Gera o proximo id usando uma subquery derivada para evitar o erro 1093.
    insert into pagamento (
        id_pagamento,
        id_pedido,
        status_pagamento,
        id_formaPagamento
    )
    select
        dados.proximo_id,
        p_id_pedido,
        p_status_pagamento,
        p_id_forma_pagamento
    from (
        select coalesce(max(id_pagamento) + 1, 1) as proximo_id
        from pagamento
    ) as dados;

    -- Retorna o ultimo pagamento criado para aparecer no Tkinter.
    select *
    from pagamento
    order by id_pagamento desc
    limit 1;
end $$
delimiter ;

drop procedure if exists proc_pedidos_por_cliente;
delimiter $$
create procedure proc_pedidos_por_cliente(
in p_id_cliente int
)
begin
    -- Lista os pedidos de um cliente especifico.
    select
        pedido.id_pedido as "ID do Pedido",
        pedido.valor_pedido as "Valor do Pedido",
        pedido.data_pedido as "Data do Pedido",
        status_pedido.status_pedido as "Status do Pedido"

    from pedido, status_pedido

    where pedido.id_statusped = status_pedido.id_statusped
    and pedido.id_cliente = p_id_cliente

    order by pedido.data_pedido desc;
end $$
delimiter ;

drop procedure if exists proc_produtos_por_categoria;
delimiter $$
create procedure proc_produtos_por_categoria(
in p_id_categoria int
)
begin
    -- Lista os produtos de uma categoria especifica.
    select
        produto.id_produto as "ID do Produto",
        produto.nome_produto as "Nome do Produto",
        produto.valor_produto as "Valor do Produto"

    from produto

    where produto.id_categoria = p_id_categoria

    order by produto.nome_produto;
end $$
delimiter ;

drop procedure if exists proc_pagamentos_por_status;
delimiter $$
create procedure proc_pagamentos_por_status(
in p_status_pagamento varchar(50)
)
begin
    -- Lista os pagamentos por status informado.
    select
        pagamento.id_pagamento as "ID do Pagamento",
        pagamento.id_pedido as "ID do Pedido",
        pagamento.status_pagamento as "Status do Pagamento",
        forma_pagamento.formaPagamento as "Forma de Pagamento"

    from pagamento, forma_pagamento

    where pagamento.id_formaPagamento = forma_pagamento.id_formaPagamento
    and pagamento.status_pagamento = p_status_pagamento;
end $$
delimiter ;

select * from vw_qtd_produtos_categoria;
select * from vw_total_status_pagamento;
select * from vw_total_pedidos_cliente;
select * from vw_total_forma_pagamento;
select * from vw_total_status_pedido;

select * from vw_produtos_caros;
select * from vw_cliente_ana;
select * from vw_pedidos_recentes;
select * from vw_pagamentos_pagos;
select * from vw_avaliacoes_boas;


select * from vw_clientes_ordenados;
select * from vw_produtos_preco_desc;
select * from vw_pedidos_data;
select * from vw_avaliacoes_nota;
select * from vw_categoria_ordem;


select * from vw_qtd_produtos_categoria;
select * from vw_total_status_pagamento;
select * from vw_total_pedidos_cliente;
select * from vw_total_forma_pagamento;
select * from vw_total_status_pedido;
