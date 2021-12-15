# jobz

## Informações importantes:

O deploy em [Docker](https://docker.com) desse projeto pode ser feito via [docker-compose](https://docs.docker.com/compose/). Caso seja preciso, siga
os seguintes passos para instalar o Docker e docker-compose.

* [Docker install](https://docs.docker.com/get-docker/)
* [docker-compose install](https://docs.docker.com/compose/install/)


## Iniciando o projeto:

```bash
# start docker-compose services
docker-compose up -d --build

# check services stati
docker-compose ps

# check web service log
docker-compose logs -f web
```

Feito isso, basta acessar a [página do admin](http://0.0.0.0:8000/admin) e informar as credenciais de acesso para acessar a aplicação.

**happy hacking!**
