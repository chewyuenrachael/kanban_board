from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'

db = SQLAlchemy(app)

# define a class for the task


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(200))
    state = db.Column(db.String(200))


@app.route('/')
def index():

    # query all the tasks that need to be done
    todo = Task.query.filter_by(state='todo').all()

    # query all the tasks that you are doing
    doing = Task.query.filter_by(
        state='doing').all()

    # query all the tasks that are done
    done = Task.query.filter_by(state='done').all()

    return render_template('index.html', todo=todo, doing=doing, done=done)


@app.route('/add', methods=['POST'])
def add():

    # to add a task, define the name, description and state of the task.
    task_to_add = Task(
        title=request.form['title'], description=request.form['description'], state=request.form['state'])

    # add the task to the database
    db.session.add(task_to_add)

    # commit to database
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<id>', methods=['POST'])
def delete(id):

    # delete task by task id
    Task.query.filter_by(id=int(id)).delete()

    # commit the change into the database
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/update_state/<id>/<state>', methods=['POST'])
# create function to update the state of the task
def update_state(id, state):

    # get task by task id
    task = Task.query.filter_by(id=int(id)).first()

    # update the task state
    task.state = str(state)

    # commit the update
    db.session.commit()
    return redirect(url_for('index'))


# to test out the app
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
