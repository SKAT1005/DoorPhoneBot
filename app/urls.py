from django.urls import path

from .views import login_view, main, set_visit_date, confirm_meeting, view_review

urlpatterns = [
    path("", login_view, name="login"),
    path('orders/', main, name='orders_page'),
    path('orders/<int:order_id>/set_visit_date/', set_visit_date, name='set_visit_date'),
    path('orders/<int:order_id>/confirm_meeting/', confirm_meeting, name='confirm_meeting'),
    path('orders/<int:order_id>/review/', view_review, name='view_review'),
]
