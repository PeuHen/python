-- NOME MARCA PREÇO

create database loja;

use loja;

create table produto(
	id_produto int primary key auto_increment not null,
	nome_produto varchar(50) not null,
	marca_produto varchar(40) not null,
	preco_produto decimal(8, 2) not null
);

/*
	a partir daqui eu começo falar de CRUD
	
	C = CREATE (insert)
    R = READ (select)
    U = UPDATE (update)
*/

select * from produto;

insert into produto(nome_produto, 
marca_produto, preco_produto)
values('Camisa', 'Nike', 250.00),
('Calça', 'Adidas', 99.90),
('Boné', 'Nike', 100.00),
('Fone', 'JBL', 130.99),
('Micro-fone', 'JBL', 300.99);

select nome_produto, preco_produto from produto;

select * from produto where preco_produto < 150.00;

select * from produto where marca_produto = 'Nike';

select * from produto where nome_produto like '%a%';

update produto set preco_produto = 110.00
where id_produto = 2;

