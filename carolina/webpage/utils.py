import sys, os, django, shutil, datetime, random, json
from pathlib import Path
from tempfile import TemporaryDirectory
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
from django.utils.translation import gettext_lazy as _
from django.http import FileResponse
from django.shortcuts import redirect
from carolina.settings import BASE_DIR 
from .filters import *
from .models import *
from django.http import HttpResponse


def format_corpus_version(corpus_version):
    corpus_version_display = corpus_version[0]+'.'+ corpus_version[2]+' '+corpus_version[4:]
    return corpus_version_display


# Filter type: select
def make_filter_select(filter_db, feature):
    filters = filter_db.objects.filter(atributo=feature)
    filter_options = list(set([(f.opcao,f.opcao) for f in filters]))
    FILTER = {
        'name': feature.nome,
        'frontname': _(feature.get_nome_display()),
        'namecss':'',
        'options':sorted(filter_options, key=lambda x: x[0]),
        'type':'select',
        'section':feature.get_secao_display(),
        'msg': feature.mensagem,
    }
    return FILTER


# Filter type : text
def make_filter_text(feature):
    FILTER = {
        'name': feature.nome,
        'frontname': _(feature.get_nome_display()),
        'namecss':'',
        'options':'',
        'type':'text',
        'section':feature.get_secao_display(),
        'msg': feature.mensagem
    }
    return FILTER


# Filter type : text
def make_filter_numeric(feature):
    FILTER = {
        'name': feature.nome,
        'frontname': _(feature.get_nome_display()),
        'namecss':'',
        'options':'',
        'type':'numeric',
        'section':feature.get_secao_display(),
        'msg':feature.mensagem
    }
    return FILTER


# Filter sections
def split_in_sections(filters):
    filters_in_sections = {}
    for FILTER in filters:
        try:
            filters_in_sections[_(FILTER['section'])].append(FILTER)
        except:
            filters_in_sections[_(FILTER['section'])] = [FILTER]
    order = [_(section[1]) for section in SECTION]
    return sorted(list(filters_in_sections.items()), key=lambda i: order.index(i[0])) 


def get_tei(tei,i, step):
    for i in range(i, len(tei), step):
        yield tei[i: i+step]


def save_files(tmp_dir, tei, head, code, i):
    step = 50
    cut_size = 25000000
    size = 0
    n=1
    top = len(tei)
    while i < top:
        f = open(os.path.join(tmp_dir,f'carolina{code}_part{n}.xml'), 'w', encoding='utf-8')
        f.write(head+'\n') 
        for part in get_tei(tei,i,step):
            f.write(''.join(part))
            i+=step
            if f.tell() > cut_size:
                n+=1
                f.write('</teiCorpus>')
                break
            else:
                if i >= top:
                    f.write('</teiCorpus>')
        f.close()


def corpus_download(request, corpus_folder, corpus_version, corpus_selection, initial):
    initial = json.loads(initial.replace('[','').replace(']','').replace("'",'"').replace('min','__gte').replace('max','__lte'))
    query = {key:value for key,value in initial.items() if value not in ('','all')}
    #query['origin_file_type'] = query['origin_file_type'].replace('$@$','/')

    tei = Text.objects.filter(**query).values_list('text_tei', flat=True)
    head = CarolinaVersao.objects.get(pk=corpus_version).tei_head

    # folder names
    selection_code = f'_{datetime.datetime.now().strftime("%d%m%Y_%H%M%S%f")+str(random.randint(0, 9))}'
   
    with TemporaryDirectory() as tmp_dir:
        save_files(tmp_dir,tei,head, selection_code, 0)
        folder_path,corpus_selection = os.path.split(tmp_dir)
        shutil.make_archive(tmp_dir, 'zip', folder_path, corpus_selection)
        response = HttpResponse(open(os.path.join(folder_path,corpus_selection+'.zip'),'rb').read(), content_type="application/zip")
        response['Content-Disposition'] = f'inline; filename=carolina_selection_{selection_code}.zip'
    return response


#Get fields name and verbose name from a specific model
def get_model_fields(model):
    fields =  model._meta.get_fields()
    fields_names = []
    for f in fields:
        if hasattr(f, 'verbose_name'):
            fields_names.append((f.name,f.verbose_name))
        else:
            fields_names.append((f.name, f.name))
    return fields_names


def doc_download(request, doc_folder, doc_file):
    filename= os.path.join(BASE_DIR,'static',doc_folder,doc_file)
    f = open(filename, 'rb')
    return FileResponse(f)


def text_display(texts_selection, counts, n_sample):
    if counts > n_sample:
        texts_selection = [texts_selection[i] for i in random.sample(range(1, counts-1), n_sample)]
    return Text.objects.filter(pk__in = texts_selection)
        
# Prepare filter to display
def make_filters(features):
    filters = []
    for feature in features:
        if str(feature.tipo_filtro) == 'select':
            try:
                filters.append(make_filter_select(Filtro, feature))
            except:
                pass
        elif str(feature.tipo_filtro) == 'text':
            filters.append(make_filter_text(feature))
        elif str(feature.tipo_filtro) == 'numeric':
            filters.append(make_filter_numeric(feature))
        else:
            # possible to introduce more types of filter
            pass  
    return filters


# Prepare filter for db query
def filter_data(request, corpus, filters):
    options = request.POST
    make_filter = {}
    for filter in filters:
        try:
            if filter['type'] == 'numeric':
                try:
                    if options[filter['name']+'min']: 
                        make_filter[filter['name']+'__gte'] = int(options[filter['name']+'min'])
                    if options[filter['name']+'max']: 
                        make_filter[filter['name']+'__lte'] = int(options[filter['name']+'max'])
                except:
                    return False
            elif options[filter['name']] not in ('all'):
                if options[filter['name']] in ('','-') and filter['type'] == 'select':
                    make_filter[filter['name']+'__isnull'] = True
                else:
                    make_filter[filter['name']] = options[filter['name']]
            else:
                pass
        except:
            pass
    if len(make_filter)!=0: 
        return Text.objects.filter(**make_filter).values_list('text_id', flat=True) 
    return []
