from django.urls import path 
from django.contrib import admin
from django.contrib.auth import views as auth_views

from account import views as account_views
from boards import views


urlpatterns = [
    path('', views.BoardListView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('signup/',account_views.signup,name='signup'),
    path('boards/<str:board_name>/',views.TopicListView.as_view(),name='board_topics'),
    path('boards/<str:board_name>/new/',views.new_topic,name='new_topic'),
    path('reset/',
    auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt'
    ),
    name='password_reset'),
    path('reset/done/',
    auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
    name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
    name='password_reset_confirm'),
    path('reset/complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
    name='password_reset_complete'),
    path('settings/password/',         auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
    name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
    name='password_change_done'),
    path('boards/<str:board_name>/topics/<int:topic_pk>/',views.PostListView.as_view(), name='topic_posts'),
    path('boards/<str:board_name>/topics/<int:topic_pk>/reply/',views.reply_topic,
      name='reply_topic'),
    path('boards/<str:board_name>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/',views.PostUpdateView.as_view(), name='edit_post') , 
    path('settings/account/',account_views.UserUpdateView.as_view(),name='my_account'),    
    path('account/<str:user_name>/'  ,account_views.my_details.as_view(),name='my_details'),
]
