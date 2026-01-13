from django.urls import path
from .views import upload_csv, get_applicants, update_applicant, status_chart, login_api

urlpatterns = [
    path("upload/", upload_csv),
    path("list/", get_applicants),
    path("update/<int:id>/", update_applicant),
    path("chart/", status_chart),
    path("login/", login_api),
]
