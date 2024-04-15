from django.urls import path, include
from webpage import views

urlpatterns = [
    path('about', views.about, name='about'),
    path('home', views.home, name='home'),
    path('corpus/<str:text_id>', views.text_info, name='text_info'),
    path('corpus/<str:corpus_version>/filter', views.filter, name='filter'),
    path('corpus/<str:corpus_version>/schema', views.schema, name='schema'),
    path('docs', views.docs, name='docs'),
    path('publications', views.publications, name='publications'),
    path('team', views.team, name='team'),
    path('corpus/<str:corpus_version>/collection', views.corpus_collection, name='corpus_collection'),
    path('', include("django.contrib.auth.urls")),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('corpus/<str:corpus_version>/filter/<str:corpus_folder>/<str:corpus_selection>/<str:initial>', views.corpus_download, name='corpus_download'),
    path('docs/<str:doc_folder>/<str:doc_file>', views.doc_download, name='doc_download'),   
]
