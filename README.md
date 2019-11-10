# DJANGO MONITOR

Projeto desenvolvido com Python/Django para monitorar o status de aplicações


## Requisitos
- Python 3.x
- Virtualenv

## Instalação
    ```sh
    mkvirtualenv monitor --python=python3
    ```

    ```sh
    $ (env) pip install -r requirements.txt
    ```

## Criando arquivo de configuração (.env)
    ```sh
    DATABASE_URL=
    DEBUG=True
    DEBUG_COLLECTSTATIC=True
    DISABLE_COLLECTSTATIC=True
    SENDER_EMAIL=tomonitor.noreply@gmail.com
    PASS_EMAIL=<pass>
    SECRET_KEY=<pass>
    SLEEP_TIME=300
    SLEEP_TIME_REQ=15
    ```

## Criando database (INSTALLED_APPS=module_monitor)
    ```sh
    $ (env) python manage.py makemigrations module_monitor
    ```

    ```sh
    $ (env) python manage.py migrate
    ```

## Criando superuser
    ```sh
    $ (env) python manage.py createsuperuser
    ```

## Rodando o projeto
   ### Iniciando serviço de monitoramento
    ```sh
    $ (env) python3 manage.py jobs
    ```

   ### Iniciando Aplicação Django
    ```sh
    $ (env) python3 manage.py runserver
    ```

   ### Acessando aplicação
    ```sh
    No browser, acesse a url: 127.0.0.1:8000
    ```
