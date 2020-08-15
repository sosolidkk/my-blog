from flask import redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get("class"):
            kwargs["class"] += "ckeditor"
        else:
            kwargs.setdefault("class", "ckeditor")
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class AdminModelView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for("main.sign_in"))
        return super(AdminModelView, self).index()


class PostModelView(ModelView):
    can_create = True
    can_delete = True
    can_edit = True
    can_export = True
    can_view_details = True

    page_size = 25

    column_editable_list = ["title", "can_display"]

    extra_js = ["//cdn.ckeditor.com/4.14.0/full/ckeditor.js"]
    form_overrides = {"body": CKTextAreaField}

    def is_accessible(self):
        return current_user.is_authenticated
