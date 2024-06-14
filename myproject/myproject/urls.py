from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from myapp.views import FileUploadView, saveColsTypesView, generateNewFileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('savecolstypes/', saveColsTypesView.as_view(), name='save-cols-types'),
    path('generateNewFile/<str:fileId>/', generateNewFileView.as_view(), name='generate_csv')
] 

