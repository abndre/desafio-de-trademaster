-- Tabela: Cliente
CREATE TABLE Cliente (
  id_cliente SERIAL PRIMARY KEY,
  nome VARCHAR(100),
  email VARCHAR(100),
  telefone VARCHAR(20),
  endereco VARCHAR(200),
  cpf VARCHAR(14),
  cartao_credito VARCHAR(16)
);

-- Tabela: Funcionario
CREATE TABLE Funcionario (
  id_funcionario SERIAL PRIMARY KEY,
  nome VARCHAR(100),
  email VARCHAR(100),
  telefone VARCHAR(20),
  endereco VARCHAR(200),
  cpf VARCHAR(14),
  cargo VARCHAR(100),
  expediente VARCHAR(20)
);

-- Tabela: Franquia
CREATE TABLE Franquia (
  id_franquia SERIAL PRIMARY KEY,
  nome VARCHAR(100)
);

-- Tabela: Item
CREATE TABLE Item (
  id_item SERIAL PRIMARY KEY,
  nome VARCHAR(100),
  tipo VARCHAR(20),
  id_franquia INT,
  FOREIGN KEY (id_franquia) REFERENCES Franquia(id_franquia)
);



-- Tabela: Cartao
CREATE TABLE Cartao (
  id_cartao SERIAL PRIMARY KEY,
  numero_cartao VARCHAR(16),
  data_validade DATE,
  nome_cartao VARCHAR(100),
  bandeira VARCHAR(50)
);

-- Tabela: Cliente_cc
CREATE TABLE Cliente_cc (
  id_cliente_cc SERIAL PRIMARY KEY,
  id_cliente INT,
  id_cartao INT,
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
  FOREIGN KEY (id_cartao) REFERENCES Cartao(id_cartao)
);


-- Tabela: Venda
CREATE TABLE Venda (
  id_venda SERIAL PRIMARY KEY,
  id_cliente INT,
  id_funcionario INT,
  id_item INT,
  data_venda DATE,
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
  FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario),
  FOREIGN KEY (id_item) REFERENCES Item(id_item)
);

-- Tabela: Aluguel
CREATE TABLE Aluguel (
  id_aluguel SERIAL PRIMARY KEY,
  id_cliente INT,
  id_funcionario INT,
  id_item INT,
  data_aluguel DATE,
  data_devolucao DATE,
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
  FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario),
  FOREIGN KEY (id_item) REFERENCES Item(id_item)
);

-- Tabela: Aluguel_Venda
CREATE TABLE Aluguel_Venda (
  id_evento SERIAL PRIMARY KEY,
  id_cliente INT,
  id_funcionario INT,
  id_item INT,
  data_evento DATE,
  data_devolucao DATE,
  evento VARCHAR(10),
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
  FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario),
  FOREIGN KEY (id_item) REFERENCES Item(id_item)
);

-- Tabela: Estoque
CREATE TABLE Estoque (
  id_estoque SERIAL PRIMARY KEY,
  id_item INT,
  quantidade INT,
  FOREIGN KEY (id_item) REFERENCES Item(id_item)
);

-- Tabela: Estoque_Franquia
CREATE TABLE Estoque_Franquia (
  id_estoque_franquia SERIAL PRIMARY KEY,
  id_franquia INT,
  id_item INT,
  quantidade INT,
  FOREIGN KEY (id_franquia) REFERENCES Franquia(id_franquia),
  FOREIGN KEY (id_item) REFERENCES Item(id_item)
);

-- Exemplo de inserts para a tabela Cliente
INSERT INTO Cliente (nome, email, telefone, endereco, cpf, cartao_credito)
VALUES ('João Silva', 'joao@example.com', '987654321', 'Rua A, 123', '123.456.789-00', '1111222233334444');

INSERT INTO Cliente (nome, email, telefone, endereco, cpf, cartao_credito)
VALUES ('Maria Souza', 'maria@example.com', '987654322', 'Rua B, 456', '987.654.321-00', '2222333344445555');


-- Exemplo de inserts para a tabela Funcionario
INSERT INTO Funcionario (nome, email, telefone, endereco, cpf, cargo, expediente)
VALUES ('Pedro Santos', 'pedro@example.com', '987654323', 'Rua C, 789', '654.321.987-00', 'Vendedor', 'Manhã');

INSERT INTO Funcionario (nome, email, telefone, endereco, cpf, cargo, expediente)
VALUES ('Ana Oliveira', 'ana@example.com', '987654324', 'Rua D, 987', '321.987.654-00', 'Atendente', 'Tarde');

-- Exemplo de inserts para a tabela Cartao
INSERT INTO Cartao (numero_cartao, data_validade, nome_cartao, bandeira)
VALUES ('1111222233334444', '2025-12-31', 'João Silva', 'Visa');

INSERT INTO Cartao (numero_cartao, data_validade, nome_cartao, bandeira)
VALUES ('2222333344445555', '2024-10-31', 'Maria Souza', 'MasterCard');


-- Exemplo de inserts para a tabela Cliente_cc
INSERT INTO Cliente_cc (id_cliente, id_cartao)
VALUES (1, 1);

INSERT INTO Cliente_cc (id_cliente, id_cartao)
VALUES (2, 2);



INSERT INTO Item (id_item, nome, tipo)
VALUES (1, 'Livro A', 'Livro'),
       (2, 'Filme B', 'Filme'),
       (3, 'Série C', 'Série');

INSERT INTO Franquia (id_franquia, nome)
VALUES (1, 'Franquia A'),
       (2, 'Franquia B'),
       (3, 'Franquia C');
