# Desafio

# Database

A modelagem do banco foi feita e colocada no arquivo [init](./init-scripts/init.sql), foi um pouco complexo devido ao caso de haver a sobreposição de problemas de engenharia de dados(DE) e software(SE), busquei atender a demanda de SE, com uma tabela para clientes e outra para funcionarios, e uma de eventos.

A tabela de franquia e item, tentei traduzir mas confundi os conceitos.

Busquei uma modelagem com starchema.

# Serviços

No contexto dos serviços para mensageria utilizei rabbitmq, banco postgresql e api usei o flask .

## RabbitMQ

Basicamente temos o consumer que faz a leitura do evento e persiste na pasta /consumar/data para ser processado 
posteriori por uma aplicação de dados.
Validar o evento, de modo a entender se ele vai entrar para o banco de dado se torna um horizonte de responsabilidades,
existe a responsabilidade de SE, de validar a informação e persistir no banco, e existe a responsabilidade de DE, de coletar o evento e persistir no lake. A troca de responsabilidades se vem ao caso de que DE não cria dados, apenas coleta, já SE, recebe os dados.

## Flask

Com o flaks foi criado um endpoint para servir de publisher para o rabbitmq.

## Postgresql

O banco postgresql foi feito de modo a iniciar com as tabelas e alguns dados para testar.

## Executando o Projeto

Há o docker-compose na raiz do projeto, utilize ubuntu para testar o projeto, e instale docker e docker-compose.

```sh
docker compose up
```

Será iniciado o serviço do rabbitmq, o flask e o postgresql para ser utilizado.

Após isso inicie o consumer, instale o ambiente virtual python:

```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Inicie o consumer

```sh
# execute o consumer
python3 consumer/consumer_db.py
```

Este consumer faz a leitura dos eventos e persiste na pasta /data

## Testando consumer

Execute no terminal este curl, basicamente será enviado um evento ao flask, que redirecionara para
o consumer do rabbitmq que irá processar o evento persistindo na pasta /data.

```sh
curl -X POST -H "Content-Type: application/json" -d '{"id_cliente": 1, "id_funcionario": 1, "id_item": 1, "data_aluguel": "2023-06-23", "data_devolucao": "2023-06-30", "id_evento":"Aluguel"}' http://localhost:5000/send_event
```

Há algumas regras de limpeza, para verificar se o dado é bom ou ruim, que a posteriori poderiam ser feitas pelo time de DE.
Coletando todos json da pasta /data, onde estão segmentados em fail e msg

```
data/
├── 02-processed
│   ├── event
│   │   └── msg
│   │       ├── 2f92eb9b-9665-47bc-a6df-03d91ed3edea_2023-06-26_.json
│   │       ├── 52ccabde-65ce-4cd0-a398-b2a5174339bb_2023-06-26_.json
│   │       ├── 5d031b25-8dc1-4e66-a5ee-eefcf1ab1f71_2023-06-26_.json
│   │       └── f1f774c2-95e9-4525-bb5c-ffbdcfdee98e_2023-06-26_.json
│   └── fail
│       └── msg
│           ├── acea0b62-c501-4898-a667-8b5a4a21d4e4_2023-06-26_.json
│           └── c974d7e3-4b32-44e9-b39b-d7722cad132e_2023-06-26_.json
├── 03-enhanced
│   └── year=2023
│       └── month=03
│           └── file.parquet
└── 01-raw
    └── event
        └── msg
            ├── 0541bf40-3dcc-471e-b698-0d8073fb4432_2023-06-26_.json
            ├── 3fcd1080-4fc3-4cf9-bee6-152db9605327_2023-06-26_.json
            ├── 7df29815-ef1f-4886-b1eb-077fa0a49fa2_2023-06-26_.json
            ├── 8dc3b684-9fcf-42a1-9418-ba7e6be46b5e_2023-06-26_.json
            ├── c710e2c5-92bf-4df4-841f-f17cb0737191_2023-06-26_.json
            └── ce6644a5-1d2a-4209-bd25-2d05fc8d1ebc_2023-06-26_.json

```

A priori coloquei apenas um uuid para o nome do arquivo, e algum enriquecimento no json, baseado se existe: usuario, funcionario ou item.
Faltando a posteriori validacoes de:
- cartao de credito

Para o time de DE, os eventos persistidos no /data, são os dados raw, com enriquecimento basico dos eventos.

Criei a estrutura medalhao dos dados, com a seguinte proposta

01-raw
msg do evento sem tratamento
02-processed
msg do evento com tratamento se o usuario, funcionario e item existe.

A partir da camada 03 os processos serão feitos utilizando pipelines, como databricks, utilizando notebooks

03-enhanced
aqui sera feito o tratamento para transformar os dados para csv mergeando todos os json
e depois verificado a consistencia dos conteudos
04-refined
aqui temos os dados prontos para serem utilizados pelas plataformas de BI, alem dos dados
estarem em formatos mais compactados como parquet.

# Todo

Não foi feito uma validação do cartão de credito no evento de envio