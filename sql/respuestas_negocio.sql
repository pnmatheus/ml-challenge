-- Sintaxe baseada no PostgreSQL
/*
Listar os usuários que fazem aniversário hoje e que realizaram mais de 1500 vendas em janeiro de 2020.
*/
SELECT 
    b.id_cliente, 
    b.nome, 
    b.sobrenome, 
    b.data_nascimento, 
    COUNT(a.id_pedido) AS qtd_vendas
FROM pedido AS a
INNER JOIN cliente AS b
    ON a.id_vendedor = b.id_cliente
WHERE b.data_nascimento = CURRENT_DATE
AND MONTH(a.data_pedido) = 1
AND YEAR(a.data_pedido) = 2020
GROUP BY b.id_cliente, b.nome, b.sobrenome, b.data_nascimento
HAVING COUNT(a.id_pedido) > 1500

/*
Para cada mês de 2020, solicitar o top 5 usuários que mais venderam ($) na categoria Celulares. 
Requer-se o mês e ano de análise, nome e sobrenome do vendedor, quantidade de vendas realizadas, 
quantidade de produtos vendidos e o montante total transacionado.
*/

WITH vendasMes AS (
    SELECT
        d.nome_categoria,
        YEAR(a.data_pedido) AS ano_pedido,
        MONTH(a.data_pedido) AS mes_pedido,
        b.id_cliente,
        b.nome,
        b.sobrenome,
        COUNT(a.id_pedido) AS qtd_vendas,
        COUNT(DISTINCT a.id_item) AS qtd_itens_distintos,
        SUM(c.valor) AS total_transacionado,
        ROW_NUMBER() OVER (PARTITION BY YEAR(a.data_venda), MONTH(a.data_venda) ORDER BY SUM(c.valor_total) DESC) AS posicao
    FROM pedido AS a
    INNER JOIN cliente AS b
        ON a.id_vendedor = b.id_cliente
    INNER JOIN item AS c
        ON a.id_item = c.id_item
    INNER JOIN categoria AS d
        ON c.id_categoria = d.id_categoria
    WHERE YEAR(a.data_pedido) = 2020
    and d.nome_categoria = 'Celulares'
    GROUP BY d.nome_categoria,
    YEAR(a.data_pedido),
    MONTH(a.data_pedido),
    b.id_cliente,
    b.nome,
    b.sobrenome
)
SELECT 
    nome_categoria,
    ano_pedido,
    mes_pedido,
    id_cliente,
    nome,
    sobrenome,
    qtd_vendas,
    qtd_itens_distintos,
    total_transacionado
FROM vendasMes
WHERE posicao <= 5;


/*
Solicita-se popular uma nova tabela com o preço e estado dos itens no final do dia. 
Deve ser reprocesável e ter apenas o último estado informado com a chave primária definida.
*/

CREATE PROCEDURE estado_itens_atual AS
BEGIN
    -- limpa tabela atual de itens
    TRUNCATE TABLE item_atual;

    -- insere o ultimo estado dos itens
    INSERT INTO item_atual 
    (
        id_item,
        nome_item,
        marca,
        descricao,
        quantidade,
        valor,
        status_item,
        data_retirada,
        categoria_id
        )
    SELECT
        i.id_item,
        i.nome_item,
        i.marca,
        i.descricao,
        i.quantidade,
        i.valor,
        i.status_item,
        i.data_retirada,
        i.categoria_id
    FROM (
        SELECT 
            id_item,
            MAX(data_hora_atualizacao) AS data_hora_atualizacao
        FROM item
        GROUP BY id_item
    ) AS ultima_att
    INNER JOIN item AS i
        ON i.item_id = ultima_att.id_item
        AND i.data_hora_atualizacao = ultima_att.data_hora_atualizacao;

END;
