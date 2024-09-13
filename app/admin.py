from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from app import app, db, dao
from app.models import UserRoleEnum
from flask_login import logout_user, current_user
from flask import redirect, request


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(AuthenticatedUser):
    @expose("/")
    def index(self):
        kw = request.args.get("kw")
        return self.render('admin/stats.html', count_flights=dao.revenue_by_month_all_routes(kw=1))


class LogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


admin = Admin(app=app, name='QUẢN TRỊ CHUYẾN BAY', template_mode='bootstrap4')
admin.add_view(StatsView(name='Thông kê báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))
