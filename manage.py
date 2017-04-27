# -*- coding: utf-8 -*-

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from planet import create_app, db

app = create_app('default')

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

