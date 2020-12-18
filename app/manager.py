from flask import redirect, url_for
from flask_login import current_user
from app import db, app
from app.models import User, Post
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from flask_admin import Admin, AdminIndexView, expose


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.has_admin_previlages:
                return True

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        return redirect(url_for('login'))


class UserView(ModelView):
    column_exclude_list = ('password_hash')
    form_excluded_columns = ('posts', 'send_messages', 'received_messages', 'last_seen', 'has_unseen_messages')

    def on_model_change(self, form, model, is_created):
        model.password_hash = generate_password_hash(model.password_hash)


admin = Admin(app, template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(UserView(User, db.session))
admin.add_view(ModelView(Post, db.session))