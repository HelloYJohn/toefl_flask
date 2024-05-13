import csv

import click

from watchlist import app, db
from watchlist.models import User, Movie, TOEFL_IBT, TPO


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    name = 'john-y'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

@app.cli.command()
def toeflibt():
    """Generate fake data."""
    db.create_all()

    with open('./toefl_ibt.csv') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            toeflibt = TOEFL_IBT(name = row[0], reading = row[1], listening = row[2], writing = row[3],
                                 speaking = row[4])
            db.session().add(toeflibt)

    db.session.commit()
    click.echo('toefl_ibt done.')

@app.cli.command()
def tpo():
    """Generate fake data."""
    db.create_all()

    with open('./tpo.csv') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            tpo = TPO(name = row[0], reading = row[1], listening = row[2], speaking = row[3],
                                 writing = row[4])
            db.session().add(tpo)

    db.session.commit()
    click.echo('tpo done.')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name=username, role = 1)
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')