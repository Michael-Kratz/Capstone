from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="root"),
    path("home/", views.home_view, name="home"),
    path("about/", views.about_view, name="about"),
    
    # Authentication
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    # Events
    path("events/", views.events_list, name="events_list"),
    path("events/<int:pk>/", views.event_detail, name="event_detail"),
    path("events/<int:pk>/register/", views.register_for_event, name="register_for_event"),
    path("events/<int:pk>/cancel/", views.cancel_event_registration, name="cancel_event_registration"),
    path("my-registrations/", views.my_event_registrations, name="my_event_registrations"),
    
    # Services
    path("services/", views.services_list, name="services_list"),
    path("services/<int:pk>/", views.service_detail, name="service_detail"),
    path("services/<int:pk>/book/", views.request_service_booking, name="request_service_booking"),
    path("bookings/<int:booking_id>/confirmation/", views.booking_confirmation, name="booking_confirmation"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    
    # Trading Posts
    path("trading/", views.trading_list, name="trading_list"),
    path("trading/<int:pk>/", views.trading_detail, name="trading_detail"),
    path("trading/<int:pk>/message/", views.send_message_to_post, name="send_message_to_post"),
    path("trading/message/<int:message_id>/reply/", views.reply_to_message, name="reply_to_message"),
    path("trading/create/", views.trading_create, name="trading_create"),
    path("trading/<int:pk>/edit/", views.trading_edit, name="trading_edit"),
    path("trading/<int:pk>/delete/", views.trading_delete, name="trading_delete"),
    
    # Staff Management
    path("staff/", views.staff_dashboard, name="staff_dashboard"),
    path("staff/events/", views.staff_events_list, name="staff_events_list"),
    path("staff/events/add/", views.staff_add_event, name="staff_add_event"),
    path("staff/events/<int:pk>/delete/", views.staff_delete_event, name="staff_delete_event"),
    path("staff/services/", views.staff_services_list, name="staff_services_list"),
    path("staff/services/add/", views.staff_add_service, name="staff_add_service"),
    path("staff/services/<int:pk>/delete/", views.staff_delete_service, name="staff_delete_service"),
    path("staff/trading/", views.staff_trading_posts, name="staff_trading_posts"),
    path("staff/trading/<int:pk>/delete/", views.staff_delete_trading_post, name="staff_delete_trading_post"),
    path("staff/bookings/", views.staff_bookings, name="staff_bookings"),
    path("staff/bookings/<int:booking_id>/status/", views.staff_update_booking_status, name="staff_update_booking_status"),
    path("staff/registrations/", views.staff_event_registrations, name="staff_event_registrations"),
    path("staff/registrations/<int:registration_id>/", views.staff_event_registration_detail, name="staff_event_registration_detail"),
    path("staff/users/", views.staff_users, name="staff_users"),
    path("staff/users/<int:pk>/rank/", views.staff_update_user_rank, name="staff_update_user_rank"),
]