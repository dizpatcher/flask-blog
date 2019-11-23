from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Configuration

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask import render_template, request, redirect, url_for

from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security import current_user


app = Flask(__name__)
db = SQLAlchemy()
app.config.from_object(Configuration)
from posts.blueprint import posts
from models import *
app.register_blueprint(posts, url_prefix='/blog')
db.init_app(app)


with app.app_context():
    db.create_all()
app.app_context().push()


### MIGRATION INSTALLATION ###
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


### ADMIN ###
class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)


#class AdminView(AdminMixin, ModelView):
#   pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'body', 'tags']


class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ['name', 'posts']


admin = Admin(app, 'FlaskBlog', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))


### FLASK-SECURITY ###
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
     return render_template('404.html'), 404


if __name__ == "__main__":
    app.run()
    db.create_all()









