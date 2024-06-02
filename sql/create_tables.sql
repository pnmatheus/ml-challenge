CREATE TABLE cliente (
    id_cliente int CONSTRAINT pk_cliente PRIMARY KEY,
    nome varchar(50) NOT NULL,
    sobrenome varchar(50) NOT NULL,
    genero varchar(15) NOT NULL,
    data_nascimento date NOT NULL
    cpf varchar(11) NOT NULL,
    email varchar(50) NOT NULL,
    telefone varchar(15) NOT NULL,
    logradouro varchar(100) NOT NULL,
    complemento varchar(20) NOT NULL,
    bairro varchar(50) NOT NULL,
    cep varchar(8) NOT NULL,
    cidade varchar(30) NOT NULL,
    estado varchar(30) NOT NULL,
    tipo_cliente varchar(20) NOT NULL
);

CREATE TABLE item (
    id_item bigint CONSTRAINT pk_item PRIMARY KEY,
    nome_item varchar(50) NOT NULL,
    marca varchar(50) NOT NULL,
    descricao varchar(200) NOT NULL,
    quantidade int NOT NULL,
    valor float NOT NULL,
    status_item varchar(10) NOT NULL,
    data_retirada timestamp NOT NULL,
    categoria_id int NOT NULL,
    data_hora_atualizacao timestamp NOT NULL,
    CONSTRAINT fk_categoria FOREIGN KEY(id_categoria) REFERENCES categoria(id_categoria)
);

CREATE TABLE categoria (
    id_categoria int CONSTRAINT pk_categoria PRIMARY KEY,
    parente_categoria int NOT NULL,
    nome_categoria varchar NOT NULL,
    path_categoria varchar NOT NULL
);

CREATE TABLE pedido (
    id_pedido int CONSTRAINT pk_pedido PRIMARY KEY,
    id_item int NOT NULL,
    id_cliente int NOT NULL,
    id_vendedor int NOT NULL,
    data_pedido timestamp NOT NULL,
    data_envio timestamp NOT NULL,
    status_pedido varchar NOT NULL,
    data_cancelamento timestamp NOT NULL,
    CONSTRAINT fk_item FOREIGN KEY(id_item) REFERENCES item(id_item),
    CONSTRAINT fk_cliente FOREIGN KEY(id_cliente) REFERENCES id_cliente(id_cliente),
    CONSTRAINT fk_vendedor FOREIGN KEY(id_vendedor) REFERENCES id_cliente(id_vendedor)
);

CREATE TABLE item_atual (
    id_item bigint CONSTRAINT pk_item PRIMARY KEY,
    nome_item varchar(50) NOT NULL,
    marca varchar(50) NOT NULL,
    descricao varchar(200) NOT NULL,
    quantidade int NOT NULL,
    valor float NOT NULL,
    status_item varchar(10) NOT NULL,
    data_retirada timestamp NOT NULL,
    categoria_id int NOT NULL
    CONSTRAINT fk_categoria FOREIGN KEY(id_categoria) REFERENCES categoria(id_categoria)
);