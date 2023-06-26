# Desafio

# Database

A modelagem do banco foi feita e colocada no arquivo [init](./init-scripts/init.sql), foi um pouco complexo devido ao caso de haver a sobreposição de problemas de engenharia de dados(DE) e software(SE), busquei atender a demanda de SE, com uma tabela para clientes e outra para funcionarios, e uma de eventos.

A tabela de franquia e item, tentei traduzir mas confundi os conceitos.

Busquei uma modelagem com starchema.

# Serviços

No contexto dos serviços para mensageria utilizei rabbitmq, banco postgresql e api usei um flask ou fastapi.

## RabbitMQ

Basicamente temos o consumer que faz a leitura do evento e persiste na pasta /consumar/data para ser processado 
posteriori por uma aplicação de dados.
Validar o evento, de modo a entender se ele vai entrar para o banco de dado se torna um horizonte de responsabilidades,
existe a responsabilidade de SE, de validar a informação e persistir no banco, e existe a responsabilidade de DE, de coletar o evento e persistir no lake. A troca de responsabilidades se vem ao caso de que DE não cria dados, apenas coleta, já SE, recebe os dados.

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

```sh
# execute o consumer
python3 consumer/consumer_db.py
```

Este consumer faz a leitura dos eventos e persiste na pasta /data/events

## Testando consumer

Execute no terminal este curl, basicamente será enviado um evento ao flask, que redirecionara para
o consumer do rabbitmq que irá processar o evento persistindo na pasta /data.

```sh
curl -X POST -H "Content-Type: application/json" -d '{"id_cliente": 1, "id_funcionario": 1, "id_item": 1, "data_aluguel": "2023-06-23", "data_devolucao": "2023-06-30", "id_evento":"Aluguel"}' http://localhost:5000/send_event
```

Há algumas regras de limpeza, para verificar se o dado é bom ou ruim, que a posteriori poderiam ser feitas pelo time de DE.
Coletando todos json da pasta /data, onde estão segmentados em fail e msg

```
data
├── fail
│   └── msg
│       ├── 0e8e8360-430b-4c1e-bb13-3893e41171a4.json
└── msg
    ├── 5a0ca630-652a-4a91-a335-8ee4dd2346ad.json
    └── 85d8d689-6a2a-4c0d-b51d-f633035a7db7.json
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
03-enhanced
aqui sera feito o tratamento para transformar os dados para csv mergeando todos os json
e depois verificado a consistencia dos conteudos
04-refined
aqui temos os dados prontos para serem utilizados pelas plataformas de BI, alem dos dados
estarem em formatos mais compactados como parquet.

# Todo