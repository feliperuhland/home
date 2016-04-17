# Home

Work in progress ...

```sh
git clone git@github.com:feliperuhland/home.git
cd home
```

Create a key=value ``.env`` file with ``DATABASE_RUL`` and ``SECRET_KEY``.

For docker-compose, you can use ``DATABASE_URL=postgres://postgres@db:5432/postgres``.

```sh
docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser
docker-compose up
```
