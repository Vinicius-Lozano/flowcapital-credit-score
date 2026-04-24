from django.contrib import admin
from django.urls import include, path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/analisar/', views.analisar_credito),
    path('api/pluggy/token/', views.pluggy_token),
    path('api/webhooks/pluggy/', views.pluggy_webhook),
    path('api/upload-extrato/', views.upload_extrato_pdf),
    path('api/autenticacao/', include('autenticacao.urls')),
]
