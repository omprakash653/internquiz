from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name='home'),
    path('account/register', views.register, name='register'),
    path('categories', views.categories, name='categories'),
    path('category_questions/<int:cat_id>',
         views.category_questions, name='category_questions'),
    path('submit-answer/<int:cat_id>/<int:quest_id>',
         views.submit_answer, name='submit_answer'),
    path('attempt-limit/', views.attempt_limit, name='attempt-limit'),
    url(r'^media/(?P<path>.*)$', serve,
        {'document_root':       settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
