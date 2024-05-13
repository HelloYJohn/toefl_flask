import click
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.models import User, Movie, TOEFL_IBT, TPO


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('index'))

        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))

    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        users = db.session.query(User).filter(User.username == username).all()
        if len(users) != 0:
            for user in users:
                if username == user.username and user.validate_password(password):
                    login_user(user)
                    flash('Login success.')
                return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        mail = request.form['mail']
        password = request.form['password']

        if not username or not password or not mail:
            flash('Invalid input.')
            return redirect(url_for('register'))

        db.create_all()
        user = db.session.query(User).filter(User.username == username).all()
        if len(user) != 0:
            flash('username exists, please choose another one.')
            return redirect(url_for('register'))
        else:
            user = User(username=username, name=username, mail=mail, role=0)
            user.set_password(password)
            db.session.add(user)

        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))

@app.route('/toefl', methods=['GET', 'POST'])
def toefl():
    toefl_ibts = TOEFL_IBT.query.all()
    return render_template('toefl_list.html', toefl_ibts=toefl_ibts)

@app.route('/toefl/paper/<int:toefl_id>', methods=['GET', 'POST'])
@login_required
def toelf_ibt_paper(toefl_id):
    toeflibt = TOEFL_IBT.query.get_or_404(toefl_id)
    return render_template('toefl_paper.html', toeflibt=toeflibt)

@app.route('/tpo', methods=['GET', 'POST'])
def tpo():
    tpos = TPO.query.all()
    return render_template('tpo_list.html', tpos=tpos)

@app.route('/tpo/paper/<int:tpo_id>')
@login_required
def tpo_paper(tpo_id):
    tpo = TPO.query.get_or_404(tpo_id)
    return render_template('tpo_paper.html', tpo=tpo)