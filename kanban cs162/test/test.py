from app import Task
from app import db, app
import unittest
import os
import tempfile
TEST_DB = 'test.db'


class Tests(unittest.TestCase):

    # set up the test
    def setUp(self):
        self.db_test, app.config["DATABASE"] = tempfile.mkstemp()
        app.testing = True
        self.app = app.test_client()
        db.drop_all()
        with app.app_context():
            db.drop_all()
            db.create_all()

    # executed after each test
    def tearDown(self):
        pass

    def add(self, title, description, state):
        """
        Request to add a new task
        """
        return self.app.post('/add', data=dict(title=title,
                                               description=description,
                                               state=state),
                             follow_redirects=True)

    def changestate(self, id, state):

        # update the state of task using the ID
        # this takes into account the current state from the ID
        return self.app.post('/changestate/' + str(id) + '/' + str(state),
                             data=dict(id=id, state=state),
                             follow_redirects=True)

    def delete(self, id):
        # test the delete functionality

        return self.app.post('/delete/' + str(id), data=dict(id=id),
                             follow_redirects=True)

    def test_todo(self):
        # test the to do functionality

        self.add(title="CS114 Problem Set 1",
                 description="for sample", state="todo")
        task = Task.query.filter_by(title='CS114 Problem Set 1').first()
        self.assertEqual(task.description, 'for sample')
        self.assertEqual(task.state, 'todo')

        # test the doing functionality
        self.add(title="CS110 Scheduler",
                 description="for sample", state="doing")
        task = Task.query.filter_by(title="CS110 Scheduler").first()
        self.assertEqual(task.description, 'for sample')
        self.assertEqual(task.state, 'doing')

        # test the done functionality
        self.add(title="CS162 Kanban Board",
                 description="for sample", state="done")
        task = Task.query.filter_by(title='CS162 Kanban Board').first()
        self.assertEqual(task.description, 'for sample')
        self.assertEqual(task.state, 'done')

    def test_changestate(self):

        # test the update functionality

        # add a task
        self.add(title="CS110 Scheduler",
                 description="for sample", state="doing")
        task = Task.query.filter_by(title='CS110 Scheduler').first()

        # change task to todo
        old_id = task.id
        self.changestate(id=old_id, state='todo')
        task = Task.query.filter_by(title='CS110 Scheduler').first()
        self.assertEqual(task.id, old_id)
        self.assertEqual(task.state, 'todo')

        # change task to done
        old_id = task.id
        self.changestate(id=old_id, state='done')
        task = Task.query.filter_by(title='CS110 Scheduler').first()
        self.assertEqual(task.id, old_id)
        self.assertEqual(task.state, 'done')

    def test_delete(self):
        """
        Test if a task can be deleted
        """
        # add a task
        self.add(title="CS110 Scheduler",
                 description="for sample", state="doing")
        task = Task.query.filter_by(title='CS110 Scheduler').first()

        # delete
        self.delete(id=task.id)
        task = Task.query.filter_by(title='CS110 Scheduler').first()
        self.assertIsNone(task)


if __name__ == '__main__':
    unittest.main()
