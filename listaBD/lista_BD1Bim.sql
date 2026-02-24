CREATE DATABASE maratona;
USE maratona;

-- Criar tabela 'universidade' primeiro, pois é referenciada por outras
CREATE TABLE universidade (
  id_univ INT PRIMARY KEY,
  nome VARCHAR(150),
  cidade VARCHAR(120),
  uf CHAR(2)
);

-- Criar a tabela 'competidor', que depende de 'universidade'
CREATE TABLE competidor (
  id_comp INT PRIMARY KEY,
  nome VARCHAR(150),
  email VARCHAR(200),
  semestre INT,
  id_univ INT,
  FOREIGN KEY (id_univ) REFERENCES universidade(id_univ)
);

-- Criar a tabela 'equipe', que também depende de 'universidade'
CREATE TABLE equipe (
  id_equipe INT PRIMARY KEY,
  nome VARCHAR(120),
  id_univ INT,
  data_criacao DATE,
  FOREIGN KEY (id_univ) REFERENCES universidade(id_univ)
);

-- Criar a tabela 'membro_equipe', que depende de 'equipe' e 'competidor'
CREATE TABLE membro_equipe (
  id_equipe INT,
  id_comp INT,
  papel VARCHAR(40),
  PRIMARY KEY (id_equipe, id_comp),
  FOREIGN KEY (id_equipe) REFERENCES equipe(id_equipe),
  FOREIGN KEY (id_comp) REFERENCES competidor(id_comp)
);

-- Criar a tabela 'linguagem', que é independente
CREATE TABLE linguagem (
  id_ling INT PRIMARY KEY,
  nome VARCHAR(80),
  paradigma VARCHAR(80),
  ano_criacao INT
);

-- Criar a tabela 'problema', que é independente
CREATE TABLE problema (
  id_prob INT PRIMARY KEY,
  codigo VARCHAR(20),
  titulo VARCHAR(200),
  nivel VARCHAR(20),
  pontos INT,
  limite_tempo_ms INT
);

-- Criar a tabela 'submissao', que depende de 'equipe', 'problema' e 'linguagem'
CREATE TABLE submissao (
  id_sub INT PRIMARY KEY,
  id_equipe INT,
  id_prob INT,
  id_ling INT,
  data_hora DATETIME,
  resultado VARCHAR(30),
  tempo_exec_ms INT,
  memoria_kb INT,
  FOREIGN KEY (id_equipe) REFERENCES equipe(id_equipe),
  FOREIGN KEY (id_prob) REFERENCES problema(id_prob),
  FOREIGN KEY (id_ling) REFERENCES linguagem(id_ling)
);

-- Inserindo dados na tabela 'universidade'
INSERT INTO universidade VALUES 
(1, 'USP', 'São Paulo', 'SP'), 
(2, 'UNICAMP', 'Campinas', 'SP'), 
(3, 'UFMG', 'Belo Horizonte', 'MG');

-- Inserindo dados na tabela 'competidor'
INSERT INTO competidor VALUES 
(1, 'Ana Silva', 'ana@usp.br', 6, 1), 
(2, 'Bruno Lima', 'bruno@unicamp.br', 7, 2), 
(3, 'Carlos Souza', 'carlos@ufmg.br', 6, 3), 
(4, 'Daniel Rocha', 'daniel@usp.br', 8, 1);

-- Inserindo dados na tabela 'equipe'
INSERT INTO equipe VALUES 
(1, 'AlphaCoders', 1, '2024-01-10'), 
(2, 'BugHunters', 2, '2024-01-12');

-- Inserindo dados na tabela 'membro_equipe'
INSERT INTO membro_equipe VALUES 
(1, 1, 'Líder'), 
(1, 4, 'Membro'), 
(2, 2, 'Líder'), 
(2, 3, 'Membro');

-- Inserindo dados na tabela 'problema'
INSERT INTO problema VALUES 
(1, 'A', 'Soma Simples', 'Fácil', 100, 1000), 
(2, 'B', 'Busca em Grafo', 'Médio', 300, 2000), 
(3, 'C', 'Árvore Balanceada', 'Difícil', 500, 3000);


INSERT INTO linguagem VALUES
(1, 'Python', 'Imperativo', 1991),
(2, 'C', 'Procedural', 1972),
(3, 'Java', 'Orientado a Objetos', 1995);


-- Inserindo dados na tabela 'submissao'
INSERT INTO submissao VALUES 
(1, 1, 1, 1, '2024-02-01 10:00:00', 'AC', 120, 1024), 
(2, 1, 2, 2, '2024-02-01 10:20:00', 'WA', 2200, 2048), 
(3, 2, 1, 3, '2024-02-01 10:30:00', 'AC', 150, 1100), 
(4, 2, 3, 1, '2024-02-01 11:00:00', 'TLE', 3500, 4096);


#1.Liste o nome das equipes e suas respectivas universidades. 
select equipe.nome, universidade.nome from universidade,equipe;

#2.Liste os competidores com semestre maior ou igual a 6. 
select nome,semestre from competidor where semestre >= 6;

#3.Mostre os problemas classificados como “Fácil”.
select * from problema where nivel = 'facil';

#4.Conte o total de submissões por equipe. 
select count(*) from submissao;

#5. Liste todas as submissões com resultado “AC”.
select * from submissao where resultado = 'AC';

#6. Mostre quais equipes já submeteram o problema de código 
select equipe.nome from equipe,submissao,problema where problema.codigo ='A';

#7. Exiba o total de submissões por linguagem. 
select submissao.id_sub, linguagem.nome from submissao, linguagem where submissao.id_ling = linguagem.id_ling;

#8. Liste os problemas que nunca tiveram submissões.
select * from problema where id_prob <> 1 AND id_prob <> 2 AND id_prob <> 3;

#9.Mostre as equipes que possuem mais de uma submissão.
select id_equipe from submissao group by id_equipe having count(*) > 1;	

#10. Liste os competidores que são líderes de equipe.
SELECT competidor.nome FROM competidor, membro_equipe WHERE competidor.id_comp = membro_equipe.id_comp AND membro_equipe.papel = 'Líder';

#11. Atualize para “Médio” os problemas “Fácil” com pontos maiores que 200.
UPDATE problema
SET nivel = 'Medio'
WHERE nivel = 'Facil'
AND pontos > 200;

#12.Atualize para “AC” todas as submissões com resultado “Accepted”. 
update submissao
set resultado = 'AC'
where resultado = 'Accepted';

#13. Atualize o papel para “Membro” dos competidores do semestre 5.
UPDATE membro_equipe, competidor
SET membro_equipe.papel = 'Membro'
WHERE membro_equipe.id_comp = competidor.id_comp
AND competidor.semestre = 5;

# 14. Aumente em 10% os pontos dos problemas “Difícil”.
update problema
set pontos = pontos * 1.10
where nivel = 'Dificil';

#15. Atualize o email dos competidores que não possuem‘@’
UPDATE competidor
SET email = CONCAT(email, '@exemplo.com')
WHERE email NOT LIKE '%@%';

#16. Delete as submissões com resultado “TLE”.
delete from submissao where resultado = 'TLE';

#17. Delete os competidores que não pertencem a nenhuma equipe.
delete from equipe where competidor.id_univ = universidade.id_univ and universidade.id_univ = equipe.id_univ;
