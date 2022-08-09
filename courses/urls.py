from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('signup', views.user_signup, name='signup'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('contact-us', views.ContactUs.as_view(), name='contact-us'),
    path('thanks', views.thanks, name='thanks'),
    path('profile', views.profile_view, name='profile-view'),
    path('panel', views.panel, name='panel'),
    path('profile/<int:pk>/settings', views.ProfileSettings.as_view(), name='profile-settings'),
    path('panel/add_course', views.AddCourse.as_view(), name='add-course'),
    path('panel/courses', views.CourseList.as_view(), name='courses'),
    path('teacher_search/', views.TeacherSearch.as_view(), name='teacher_search'),
]
