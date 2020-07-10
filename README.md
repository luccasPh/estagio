<h3 align="center">
    <img alt="Logo" title="#logo" width="300px" src=".github/logo.png">
    <br><br>
    <b>Sistema de gerenciamento de eventos acadêmicos.</b>  
    <br>
</h3>
      
# Índice

- [Sobre](#sobre)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Como testar](#como-testar)

<a id="sobre"></a>

## :bookmark: Sobre

<strong>SIGEA</strong> é uma aplicação Web feita com intuito de ajuda comunidade acadêmicos no gerenciamento e divulgação de seus eventos a partir de uma plataforma on-line de fácil utilização.

Essa aplicação foi construída durante período de estagio obrigatório que eu cumpri no Departamento de Tecnologia da Informação e Comunicação - DTIC - UESPI. A necessidade do sistema se deve ao fato da deste departamento receber várias requisições da comunidade acadêmica para criação de uma página para divulgar os
seus eventos e fazer as inscrições dos participantes.

<a id="tecnologias-utilizadas"></a>

## :rocket: Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias

- [Django](https://www.djangoproject.com/)
- [Docker](https://www.docker.com/)
- [MySQL](https://www.mysql.com/)

<a id="como-testar"></a>
## :fire: Como Testar

- ### **Pré-requisitos**

  - É **necessário** possuir o **[Docker](https://www.docker.com/get-started)** instalado na máquina
  - Também, é **preciso** instalar o **[Docker Compose](https://docs.docker.com/compose/install/)**

1. Faça um clone :

```sh
  $ git clone https://github.com/luccasPh/estagio.git
```

2. Executando a Aplicação:

```sh
  $ cd estagio
  $ docker-compose build
  $ docker-compose up -d

  #Tende a da error na primeira veies.
  $ docker-compose stop
  $ docker-compose up -d

  $ docker-compose exec app python manage.py migrate

  #Cria um usuário.
  $ docker-compose exec app python manage.py createsuperuser

  Depois acesse http://localhost:3000/

```


<h4 align="center">
    Power by <a href="https://www.linkedin.com/in/lucas-pinheiro-462794152/" target="_blank">Lucas Pinheiro</a>
</h4>
