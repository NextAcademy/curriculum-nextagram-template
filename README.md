## Flask Nextagram Template

version 0.0.1 (alpha)

### Development

**Install dependencies**

- Python 3.7.2 was tested
- Postgresql 10.3 was tested

```
pip install -r requirements.txt
```

Remove `certifi==2018.11.29` if you're having trouble installing dependencies.

**Create a `.env` file at the root of the directory**

```
FLASK_APP='start'
FLASK_ENV='development'
APP_SETTINGS="config.DevelopmentConfig"
DATABASE_URL="postgres://localhost:5432/nextagram_dev"
```

Since this app uses Pooled Connections, you may also want to set: _(see `database.py`)_

```
DB_TIMEOUT=300 # 5 minutes
DB_POOL=5
```

**Create a Database**

- this application is configured to use Postgresql

```
createdb nextagram_dev
```

**Ignoring Files from Git**

Before git commiting, remember to ignore key files. Here's an example of `.gitignore`

```
.vscode
*.DS_Store
*__pycache__
*.env
```

### Database Migrations

```
python migrate.py
```

\*_this template is configured to use Peewee's PooledConnection, however, migrations using Peewee-DB-Evolve doesn't work well. A hack was used to not use PooledConnection when running migration. Pending investigation. There are no known side effects to run this template in production._

### Starting Server

```
flask run
```

### Staring Shell

```
flask shell
```

### Deploying to Production

- ensure environment variables are configured appropriately
- migrations will not run in interactive mode when FLASK_ENV is set to 'production'

### Architecture

This template separates out API and Web to separate packages. Both API and Web are configured to use Flask's Blueprints.

All new models should go into it's own file/script within the models directory.

The entry point for a Flask server to start is located at `start.py`

### Dependencies

This template was created against `Python 3.7`

`Peewee` is used as ORM along with a database migration library `peewee-db-evolve`.

A copy of requirements.txt is included with this project.

```
autopep8==1.4.3
certifi==2018.11.29
Click==7.0
colorama==0.4.1
Flask==1.0.2
Flask-Cors==3.0.7
itsdangerous==1.1.0
Jinja2==2.10
MarkupSafe==1.1.0
peewee==3.8.2
peewee-db-evolve==3.7.0
psycopg2-binary==2.7.7
pycodestyle==2.5.0
python-dotenv==0.10.1
six==1.12.0
Werkzeug==0.14.1
```

Remove `certifi==2018.11.29` if you're having trouble installing dependencies.
