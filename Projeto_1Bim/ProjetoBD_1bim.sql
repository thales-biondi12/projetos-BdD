create database projeto5;
use projeto5;

create table unidades(
id_unidade int primary key,
status_unidade varchar(15) #ocupada ou vazia
);

create table moradores(
id_morador int primary key,
nome varchar(55) not null,
ocupacao varchar(20) #proprietario ou inquilino
);

create table his_moradores(
id_historico int primary key,
id_unidade int,
id_morador int,
data_inicio date, #(Ano-Mês-Dia)
data_fim date,
foreign key(id_unidade) references unidades(id_unidade),
foreign key(id_morador) references moradores(id_morador)
);

create table cobrancas(
id_cobranca int primary key,
id_unidade int,
mes_referencia date,
valor decimal(10, 2),
foreign key(id_unidade) references unidades(id_unidade)
);

create table pagamentos(
id_pagamento int primary key,
id_cobranca int,
data_pagamento date,
valor_pago decimal(10, 2),
status varchar(20),
foreign key(id_cobranca) references cobrancas(id_cobranca)
);

create table funcionarios(
id_funcionario int primary key,
nome varchar(55) not null
);

create table ocorrencias(
id_ocorrencia int primary key,
id_unidade int,
id_funcionario int,
motivo varchar(100),
data_ocorrencia date,
foreign key(id_unidade) references unidades(id_unidade),
foreign key(id_funcionario) references funcionarios(id_funcionario)
);

create table reservas(
id_reserva int primary key,
id_unidade int,
area varchar(30),
data_reserva date,
horario_inicio time,
horario_fim time,
foreign key(id_unidade) references unidades(id_unidade)
);

insert into unidades values
(1, 'vazia'),
(2, 'ocupada'),
(3, 'ocupada'),
(4, 'ocupada'),
(5, 'ocupada');

insert into moradores values
(1, 'Pedro', 'proprietario'),
(2, 'Thales', 'proprietario'),
(3, 'Bruno', 'inquilino'),
(4, 'Italo', 'inquilino'),
(5, 'Daniel', 'proprietario');

insert into his_moradores values
(1, 5, 4, '2018-08-26', '2022-12-01'),
(2, 1, 5, '2014-02-06', '2025-06-22'),
(3, 2, 1, '2023-01-01', null),
(4, 3, 2, '2022-05-10', null),
(5, 4, 3, '2024-03-15', null);

insert into cobrancas values
(1, 2, '2026-01-01', 500.00),
(2, 3, '2026-01-01', 500.00),
(3, 4, '2026-01-01', 500.00),
(4, 5, '2026-01-01', 500.00),
(5, 2, '2026-02-01', 500.00);

insert into pagamentos values
(1, 1, '2026-01-10', 500.00, 'pago'),
(2, 2, '2026-01-15', 500.00, 'pago'),
(3, 3, NULL, 0.00, 'pendente'),
(4, 4, '2026-01-20', 500.00, 'pago'),
(5, 5, NULL, 0.00, 'pendente');

insert into funcionarios values
(1, 'Carlos'),
(2, 'Marcos'),
(3, 'Fernanda');

insert into ocorrencias values
(1, 2, 1, 'Barulho alto', '2026-01-05'),
(2, 3, 2, 'Vaga ocupada indevidamente', '2026-01-10'),
(3, 2, 3, 'Discussão entre moradores', '2026-02-01'),
(4, 4, 1, 'Som alto à noite', '2026-02-10'),
(5, 2, 2, 'Lixo em local inadequado', '2026-03-01');

insert into reservas values
(1, 2, 'churrasqueira', '2026-03-20', '18:00:00', '22:00:00'),
(2, 3, 'salão de festas', '2026-03-20', '19:00:00', '23:00:00'),
(3, 2, 'churrasqueira', '2026-03-20', '18:00:00', '22:00:00'), 
(4, 4, 'quadra', '2026-03-21', '10:00:00', '12:00:00');

#D1. Listar todas as unidades cadastradas e seu status (ocupada/vazia, se aplic ́avel).

select id_unidade, status_unidade from unidades;

#D2. Exibir o historico de moradores de uma unidade informada (por identificador da unidade).

select id_morador, data_inicio, data_fim from his_moradores where id_unidade = 1;

#D3. Listar moradores ativos no condomınio em ordem alfabetica.

select nome from moradores where id_morador in (select id_morador from his_moradores where data_fim is null) order by nome; 

#D4. Listar reservas de uma  ́area comum em uma data informada.

select area, data_reserva, horario_inicio, horario_fim, id_unidade from reservas where data_reserva = '2026-03-20';

#D5. Verificar conflitos: reservas duplicadas para a mesma  ́area, data e hor ́ario (auditoria).

SELECT area, data_reserva, horario_inicio, horario_fim, COUNT(*) AS total_reservas FROM reservas GROUP BY area, data_reserva, horario_inicio, horario_fim HAVING COUNT(*) > 1;

#D6. Exibir ocorrencias registradas em um intervalo de datas.

select id_ocorrencia from ocorrencias where data_ocorrencia >='2026-01-05' and data_ocorrencia <= '2026-02-01';

#D7. Exibir total arrecadado em um mes (pagamentos confirmados no perıodo). 

select valor_pago from pagamentos where  data_pagamento >= '2026-1-1' and data_pagamento <= '2026-1-31';#preciso fazer somar

#D8. Listar unidades inadimplentes no mes (sem pagamento da cobranca do perıodo).

select id_unidade from cobrancas where id_cobranca in(select id_cobranca from pagamentos where status = 'pendente');

#D9. Exibir as 3 unidades com maior numero de ocorrencias no trimestre.

select id_unidade, count(*) as total from ocorrencias where data_ocorrencia >= '2026-1-1' and data_ocorrencia <= '2026-3-31' group by id_unidade;

#D10. Listar unidades que tiveram mudanca de responsavel no semestre (com base no historico).

select id_unidade from his_moradores where data_inicio >= '2026-1-1' and data_inicio <= '2026-6-1';