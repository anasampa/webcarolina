from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, login, authenticate
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .filters import *
from .utils import *
from random import sample


# The 'corpus_current_version' must be equal to 'versao_id' of the current version in db 'CarolinaVersao' table.
corpus_current_version = '1_2_Ada'


@csrf_exempt
def sign_in(request):
    if request.user.is_authenticated:
        return render(request, 'carolina_home_option11.html')
    else:
        if request.method=="POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'carolina_home_option11.html')
        return render(request,'carolina_login.html')


@csrf_exempt
def sign_out(request):
    'Logout user if authenticated'
    if request.user.is_authenticated:
        logout(request)
    return redirect('sign_in')


def home(request):
    return render(request,'carolina_home_option11.html')


def about(request):
    return render(request,'carolina_about.html')


def docs(request):
    return render(request,'carolina_docs.html')


def schema(request, corpus_version):
    corpus_version_display = corpus_version[0]+'.'+ corpus_version[2]+' '+corpus_version[4:]
    return render(request,'carolina_corpus_schema.html', context={'corpus_version_display':corpus_version_display})


def corpus_collection(request, corpus_version):    
    if corpus_version =='1_1_Ada':
        return render(request,'carolina_corpus_collection_11ada.html')
    else:
        corpus_version_display = format_corpus_version(corpus_version)

        temas_trio = Subtema.objects.values_list('subtema_id', 'subtema_tema__tema_nome', 'subtema_nome')
        temas = Tema.objects.all().values()

        # Group objects by subtema
        corpus_tema_group = {}
        for trio in temas_trio:
            trio = list(trio)
            trio[1] = _(trio[1])
            corpus_group = CorpusOrigem.objects.filter(subtema__subtema_nome=trio[2])
            if corpus_group:
                corpus_tema_group[tuple(trio)] = corpus_group

        for tema in temas: tema['tema_nome'] = _(tema['tema_nome'])
        context = {
            'corpus_version_display':corpus_version_display, 
            'corpus_tema_group' : corpus_tema_group,
            'temas':temas
            } 
        return render(request,'carolina_corpus_collection.html', context=context)


def publications(request):
    publications = Publicacao.objects.all().order_by(publicacao_tipo_order, 'ano')
    context = {'publications' :publications}
    return render(request, 'carolina_publications.html',context)


def team(request):
    members_prof = Equipe.objects.filter(display='yes', posicao__contains='docente').order_by('display_priority','nome') 
    members_doctor = Equipe.objects.filter(display='yes', posicao__contains='doutorado').order_by('display_priority','nome')
    members_master = Equipe.objects.filter(display='yes', posicao__contains='mestrado').order_by('display_priority','nome')
    members_undergrad = Equipe.objects.filter(display='yes', posicao__contains='graduação').order_by('display_priority','nome')
    members_all = Equipe.objects.filter(display='yes').order_by('display_priority','nome')
    context={
        'members_prof':members_prof,
        'members_doctor':members_doctor,
        'members_master':members_master,
        'members_undergrad':members_undergrad,
        'members_all':members_all,
        }
    return render(request, 'carolina_team.html', context=context)


def text_info(request, text_id):
    text_n = Text.objects.get(pk=text_id).__dict__
    display_features = []
    for key, value in FEATURES.items():
        try:
            display_features.append((key,text_n[value]))
        except:
            pass      
    return render(request, 'carolina_text.html', {'text':display_features})

@csrf_exempt
def filter(request, corpus_version):
    get_model_fields(Text)
    corpus_version_display = format_corpus_version(corpus_version)

    # Attributes to be in filter and filter front preparation
    features = Atributo.objects.filter(filtro_display='yes')
    filters = make_filters(features) 
    filters_in_sections = split_in_sections(filters)

    texts_selection = [{'text_id':'DAT001034114eq'}]
    status = 200
    n_display = 10

    context={
        'corpus_version_display':corpus_version_display,
        'corpus_version':corpus_version,
        'filters_in_sections': filters_in_sections,
        'status': status,
        'text':[]
    }

    # Get filter values
    if request.method == 'POST':
        post = dict(request.POST.lists())
        post['origin_file_type'] = post['origin_file_type'][0].replace('/','$@$')
        context['initial'] = post        
        if 'textcode' in request.POST:
            try:
                context['texts'] = [Text.objects.get(pk=str(request.POST['textcode']))]
                counts = 1
                return render(request,'carolina_filter.html', context)
            except:
                context['status'] = _("Não foi encontrado texto com ID '")+ request.POST['textcode'] +"'."
                return render(request,'carolina_filter.html', context)
        else:
            texts_selection = filter_data(request,Text,filters)
            if texts_selection == False:
                context['status'] = _("Erro na busca.")+_(" Esperado valor inteiro numérico em campo min e max.")
                counts = 0
                return render(request,'carolina_filter.html', context)
            else:    
                counts = len(texts_selection)
                status = _("Sua busca retornou ")+'{:,}'.format(counts).replace(',','.')+ _(" textos")+"."
                if counts > n_display: status += _(" Segue abaixo uma amostra aleatória com ")+'{:,}'.format(n_display).replace(',','.')+"."
                context['status'] = status      
                context['stats'] = {'count': counts}
                context['texts'] = text_display(texts_selection, counts, n_display)

    return render(request,'carolina_filter.html', context)

