# Propella Project

This Django application is configured to run using **production settings by
default** (see `config/settings/prod.py`).  The provided `manage.py` and
`run_prod.sh` helpers make it easy to start the project locally in the same
way Vercel will run it.

## Running in "production" locally

1.  **Copy or create a `.env` file.**
    ```bash
    cp .env.example .env
    # edit SECRET_KEY, database credentials, etc. as needed
    ```

2.  **Install dependencies & activate virtual env** (if you haven't already):
    ```bash
    python -m venv venv
    source venv/Scripts/activate    # Windows PowerShell/WSL; adjust for your shell
    pip install -r requirements.txt
    ```

3.  **Run the helper script** (this loads `.env`, applies migrations,
    collects static files and starts a WSGI server):

    ```bash
    chmod +x run_prod.sh          # first time only
    ./run_prod.sh                # defaults to port 8000
    # or: PORT=9000 ./run_prod.sh
    ```

    On Unix-like systems the script will invoke **gunicorn** (matching the
    Vercel runtime).  Windows doesn’t support the `fcntl` module which
    gunicorn requires, so on that platform the script automatically falls
    back to using `python manage.py runserver`, which is suitable for local
    testing.  You can install a different cross-platform WSGI server such as
    `waitress` and adjust the script if you prefer.

    Under the hood the same `config.settings.prod` settings are used when you
    execute `python manage.py` commands because `manage.py` already sets
    `DJANGO_SETTINGS_MODULE` to that module.

4.  **Alternatively**, you can run the Django development server directly:
    ```bash
    export DJANGO_SETTINGS_MODULE=config.settings.prod
    python manage.py migrate
    python manage.py collectstatic --noinput
    python manage.py runserver 0.0.0.0:8000
    ```

    This is useful if you want to attach a debugger or inspect error pages.  

5.  **Access the site** via `http://localhost:8000/` (or whatever port you chose).
    Static assets will be served by Whitenoise from `STATIC_ROOT` and the
    settings match what your Vercel deployment uses.

## Notes

*  `DEBUG` is controlled by the `DEBUG` variable in your `.env`.  When set to
   `False`, Django will not serve uploaded media or static files except via
   Whitenoise, and the error pages will not display debug information.

*  If you only want to spin up the development configuration instead, either
   change `DJANGO_SETTINGS_MODULE` to `config.settings.base`/`config.settings.dev`
   or modify `manage.py` accordingly.

*  The `run_prod.sh` script is a convenience; feel free to run Gunicorn or
   Daphne manually if you need a different WSGI/ASGI server.

*  Ensure `ALLOWED_HOSTS` in `.env` includes `localhost` or `127.0.0.1`.

*  To recreate a production-like database, set the appropriate Postgres
   variables (`HOST`, `NAME`, `USER`, etc.) or just let SQLite run by leaving
   them unset.  

Happy testing!  Feel free to tweak the script or settings to better mirror any
other hosting environment you use.