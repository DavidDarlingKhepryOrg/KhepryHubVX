import click
import pandas as pd
import sqlite3
import sys

from flask import current_app, g
from flask.cli import with_appcontext


def get_sqlite_db():
    if 'sqlite_db' not in g:
        g.sqlite_db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.sqlite_db.row_factory = sqlite3.Row

    return g.sqlite_db


def init_app(_app):
    _app.teardown_appcontext(close_sqlite_db)
    _app.cli.add_command(init_sqlite_db_command)


def init_sqlite_db():

    with current_app.open_resource(r'../dbase_routines/sqlite_schema.sql') as f:
        db = get_sqlite_db()
        cursor = db.cursor()
        cursor.executescript(f.read().decode('utf8'))
        close_sqlite_db()
        click.echo('Initialized the database schema.')

    with current_app.open_resource(r'../dbase_routines/sqlite_indexes.sql') as f:
        db = get_sqlite_db()
        cursor = db.cursor()
        cursor.executescript(f.read().decode('utf8'))
        cursor.close()
        close_sqlite_db()
        click.echo('Initialized the database indexes.')

    sys.exit(0)


def load_sqlite_db(action):
    load_state_counties_table(action)
    load_nc_voter_master_table(action)
    load_nc_voter_history_table(action)
    sys.exit(0)


def load_state_counties_table(action):
    with current_app.open_resource(r'../data/state_counties.csv') as csv_file:
        df_state_counties = pd.read_csv(csv_file)
        print(df_state_counties.head())
        db = get_sqlite_db()
        cursor = db.cursor()
        if action == 'replace':
            cursor.executescript('begin transaction; delete from state_counties; commit;')
        conn = cursor.connection
        try:
            df_state_counties.to_sql('state_counties', conn, if_exists='append', index=False)
            click.echo("Loaded the 'state_counties' table.")
        except sqlite3.IntegrityError as ex:
            print(ex)
            click.echo("FAILED to load the 'state_counties' table.")
        finally:
            cursor.close()
            conn.close()
            close_sqlite_db()


def load_nc_voter_master_table(action):
    with current_app.open_resource(r'../data/ncvoter48.txt') as tab_file:
        df_voter_master = pd.read_csv(tab_file, sep='\t', encoding='latin-1')
        print(df_voter_master.head())
        db = get_sqlite_db()
        cursor = db.cursor()
        if action == 'replace':
            cursor.executescript('begin transaction; delete from nc_voter_master; commit;')
        conn = cursor.connection
        try:
            df_voter_master.to_sql('nc_voter_master', conn, if_exists='append', index=False)
            click.echo("Loaded the 'nc_voter_master' table.")
        except sqlite3.IntegrityError as ex:
            print(ex)
            click.echo("FAILED to load the 'nc_voter_master' table.")
        finally:
            cursor.close()
            conn.close()
            close_sqlite_db()


def load_nc_voter_history_table(action):
    with current_app.open_resource(r'../data/ncvhis48.txt') as tab_file:
        df_voter_history = pd.read_csv(tab_file, sep='\t', encoding='latin-1')
        print(df_voter_history.head())
        db = get_sqlite_db()
        cursor = db.cursor()
        if action == 'replace':
            cursor.executescript('begin transaction; delete from nc_voter_history; commit;')
        conn = cursor.connection
        try:
            df_voter_history.to_sql('nc_voter_history', conn, if_exists='append', index=False)
            click.echo("Loaded the 'nc_voter_history' table.")
        except sqlite3.IntegrityError as ex:
            print(ex)
            click.echo("FAILED to load the 'nc_voter_history' table.")
        finally:
            cursor.close()
            conn.close()
            close_sqlite_db()


def vacuum_sqlite_db():
    db = get_sqlite_db()
    cursor = db.cursor()
    try:
        cursor.execute('vacuum;')
        click.echo("Vacuumed the SQLite database.")
    except sqlite3.IntegrityError as ex:
        print(ex)
        click.echo("FAILED to vacuum the SQLite database.")
    finally:
        cursor.close()
        close_sqlite_db()


@click.command('exec-sqlite-db')
@click.option('-a', '--action',
              default=None,
              prompt="Action to be executed on the SQLite database:",
              type=click.Choice(['init', 'replace', 'append', 'vacuum'], case_sensitive=False))
@with_appcontext
def init_sqlite_db_command(action):
    """Drop the existing tables and create new tables OR load the tables with data."""
    action = action.lower()
    if action == 'init':
        init_sqlite_db()
    elif action == 'vacuum':
        vacuum_sqlite_db()
        sys.exit(0)
    else:
        load_sqlite_db(action)
        sys.exit(0)


def close_sqlite_db(e=None):
    sqlite_db = g.pop('sqlite_db', None)
    if sqlite_db is not None:
        sqlite_db.close()
