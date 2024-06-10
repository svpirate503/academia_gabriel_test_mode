from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('xxxx',views.index),
    path('dashboard/',views.user_dashboard,name='dashboard'),
    path('api/capitulos/', views.CapituloView.as_view(), name='capitulo-list-create'),
    path('api/capitulos/<int:id>/', views.CapituloRetrieveUpdateDestroy.as_view(), name='capitulo-retrieve-update-destroy'),
    path('plans/',views.plans,name='plans'),
    path('testimonios/',views.testimonios,name='testimonios'),
    path('category-detail/<int:post_id>/',views.category_detail,name='cat_detail'),
    path('contact/',views.contact,name='contact'),
    path('register/',views.register,name='register'),
    path('playlist/',views.videoplaylist,name='playlist'),
    path('sigin/',views.log_in,name='sigin'),
    path('logout/',views.log_out,name='logout'),
    path('home/',views.home,name='home'),
    path('success/',views.success,name='success'),
    path('cancelar-membresia/', views.cancelar_membresia, name='cancelar-membresia'),
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('webhook/', views.stripe_webhook,name='stripe-webhook'),  # new
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='custom/password_reset_form.html',
        email_template_name='custom/password_reset_email.html',
        subject_template_name='custom/password_reset_subject.txt',
        success_url='/password_reset_done/'
    ), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='custom/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='custom/password_reset_confirm.html',
        success_url='/password_reset_complete/'
    ), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='custom/password_reset_complete.html'
    ), name='password_reset_complete'),


]