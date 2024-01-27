from django.contrib import admin
from django.urls import path, include
from App_CourseTransaction import views as courseTransactionView

#images-media
from django.conf import settings 
from django.conf.urls.static import static
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
 
urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', include('App_Course.urls')),
    path('account/', include('App_Authentication.urls')),
    path('check-out/', include('App_CourseTransaction.urls')),
    path('verify_payment', courseTransactionView.verify_payment , name='verify_payment')
]

#urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  