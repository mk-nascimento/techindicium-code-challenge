# Indicium Tech Code Challenge

## Visão Geral

Este repositório contém a solução para o [Indicium Tech Code Challenge](CHALLENGE.md). O objetivo foi construir um pipeline de dados que extrai dados de duas fontes: um banco de dados PostgreSQL (northwind) e um arquivo CSV representando os detalhes de pedidos. O pipeline carrega os dados extraídos em um banco de dados PostgreSQL.

## Requisitos

- **Docker** e **Docker Compose** (ou o plugin Compose do Docker) para configuração de ambientes isolados e execução dos containers.

## Setup

### 1. Instale o Docker e Docker Compose

Certifique-se de que o **Docker** e o **Docker Compose** estão instalados em sua máquina. Se não tiver, siga as instruções de instalação:

- [Instalar Docker](https://docs.docker.com/get-docker/)
- [Instalar Docker Compose](https://docs.docker.com/compose/install/)

### 2. Clone o Repositório

```bash
git clone https://github.com/mk-nascimento/techindicium-code-challenge.git
cd indicium-tech-code-challenge
```

### 3. Configure o Ambiente Docker

Com o **Docker Compose**, podemos facilmente definir e orquestrar os containers necessários para rodar o pipeline. Execute o seguinte comando para iniciar os serviços:

#### **Opção 1: Comando clássico**
Caso o Docker Compose esteja instalado como uma ferramenta independente, execute:
```bash
docker-compose up --build
```

#### **Opção 2: Comando com o plugin do Docker Compose**
Se você utiliza o Docker Compose como um plugin do Docker CLI, o comando será:
```bash
docker compose up --build
```

Isso irá:

- Iniciar o **PostgreSQL** com o banco de dados `northwind` e output no`southwind`.
- Configurar o **Meltano** para extração e carregamento de dados.
- Iniciar o **Airflow** para orquestrar o pipeline.

### 4. Acesse a Interface do Airflow

Após os containers estarem rodando, você pode acessar a interface do Airflow através de:

```
http://localhost:8080
```
> **login**: `admin`
> **password**: `pass`

A partir daí, você pode monitorar o progresso do pipeline, se necessário.

### 5. Extração e o Carregamento de Dados

O pipeline é composto pelas seguintes etapas:

1. **Extração de Dados:**
   - Extrair tabelas do banco de dados PostgreSQL.
   - Extrair detalhes de pedidos do arquivo CSV.

2. **Carregamento de Dados:**
   - Escrever os dados extraídos no sistema de arquivos local, organizados por tabela e data.
   - Carregar os dados extraídos do sistema de arquivos para o PostgreSQL (`southwind`).

### 6. Execute o Pipeline

Você pode acionar o pipeline manualmente através da interface do Airflow. Por padrão, o pipeline será executado diariamente às 00:00 GMT.

### 7. Verifique os Resultados

Após a execução bem-sucedida do pipeline, a união dos dados no PostgreSQL foi exportada para [CSV](orders_with_details.csv) com a seguinte Query:

```sql
southwind=# \copy (SELECT * FROM orders o JOIN order_details od ON o.order_id = od.order_id) TO '/order_with_details.csv' DELIMITER ',' CSV HEADER;
```

Exporte os resultados para CSV ou JSON para demonstrar que o pipeline funciona como esperado.

## Nomeação e Organização de Arquivos

Conforme proposto para separação dos dados, a seguinte estrutura de diretórios é usada para armazenar os arquivos:

- **Arquivos [CSV](/data/csv/):**
  ```
  /data/csv/2025-01-01/file.csv
  /data/csv/2025-01-02/file.csv
  ```

- **Arquivos do [PostgreSQL](/data/postgres/):**
  ```
  /data/postgres/{table}/2025-01-01/orders.csv
  /data/postgres/{table}/2025-01-02/order_details.csv
  ```

## Solução de Problemas

### 1. Logs e Diagnóstico de Falhas

Em caso de falha, a interface do Airflow fornece logs detalhados para cada tarefa. Os logs das tarefas indicarão onde a falha ocorreu, seja durante a extração, gravação no disco ou carregamento no PostgreSQL.

## Conclusão

Esta solução demonstra um pipeline de dados que extrai dados de um banco de dados PostgreSQL e de um arquivo CSV, grava-os no sistema de arquivos local e carrega-os no PostgreSQL para análise. Foi utilizado **Airflow** para orquestração e **Meltano** para extração e carregamento de dados.