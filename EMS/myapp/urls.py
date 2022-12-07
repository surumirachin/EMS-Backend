from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.conf import settings
from myapp import views

urlpatterns = [
    path('profile/', views.profileView.as_view()),
    path('api/auth/', views.CustomAuthToken.as_view()),
    path('employee/',views.employeeApi),
    path('employee/<int:id>/', views.employeeApi),
    path('save/',views.SaveFile),
    path('leave/',views.leaveApi),
    path('leave/<int:id>/', views.leaveApi),
    # path('files/',views.FileUploadView.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)