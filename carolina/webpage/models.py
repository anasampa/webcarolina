import datetime
from .filters import *
from django.db import models
from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class Publicacao(models.Model):
    publicacao_id = models.AutoField(primary_key=True)
    data_adicao = models.DateTimeField(auto_now_add=True, blank=True)
    ano = models.PositiveIntegerField(validators=[MinValueValidator(2020), MaxValueValidator(current_year())], default=current_year())
    publicacao = models.TextField(max_length=700)
    link = models.CharField(max_length=200, default='', blank=True)
    bibtex = models.TextField(max_length=700, default='sem bib', blank=True)
    tipo = models.CharField(max_length=50,choices=PUBLICACAO, default='outro')

    def __str__(self):
        return str(self.publicacao)
    
    class Meta:
        verbose_name = 'Publicação'
        verbose_name_plural = 'Publicações'


class Equipe(models.Model):
    equipe_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    filiacao = models.CharField(max_length=200,blank=True)
    site = models.URLField(blank=True)
    lattes = models.URLField(blank=True)
    posicao = models.CharField(max_length=50 ,choices=POSITION, default='outro')
    display = models.CharField(max_length=10,choices=DISPLAY, default='yes')
    display_priority = models.IntegerField(default=100)
    foto = models.ImageField(upload_to="static/webpage_static/team_photos/", blank=True)

    def __str__(self):
        return str(self.nome)

    class Meta:
        verbose_name = 'Equipe'
        verbose_name_plural = 'Equipe' 


class Tema(models.Model):
    tema_id = models.AutoField(primary_key=True)
    tema_nome = models.CharField(max_length=200)
    n_textos = models.PositiveIntegerField(default=0)
    n_palavras = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.tema_nome)

    class Meta:
        verbose_name = 'Tipologia ampla'
        verbose_name_plural = 'Tipologia ampla'


class Subtema(models.Model):
    subtema_id = models.AutoField(primary_key=True)
    subtema_nome = models.CharField(max_length=200)
    subtema_tema = models.ForeignKey(Tema, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.subtema_nome)


class CorpusOrigem(models.Model):
    corpus_id = models.AutoField(primary_key=True)
    corpus_nome = models.CharField(max_length=300)
    tema = models.ForeignKey(Tema, on_delete=models.SET_DEFAULT, default="outros") 
    subtema = models.ForeignKey(Subtema, on_delete=models.SET_DEFAULT, default="outros") 
    autor = models.CharField(max_length=200, blank=True)
    autoridade = models.CharField(max_length=200, blank=True)
    instituicao_mantenedora = models.CharField(max_length=200, blank=True) 
    url = models.URLField(max_length=200, blank=True)
    licenca = models.CharField(max_length=350, blank=True)
    url_licenca = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return str(self.corpus_nome)
    
    class Meta():
        verbose_name = 'Coleção'
        verbose_name_plural = 'Coleção'


class CarolinaVersao(models.Model):
    versao_id = models.CharField(max_length=10,primary_key=True)
    versao_nome = models.CharField(max_length=20)
    tei_head = models.TextField()

    def __str__(self):
        return self.versao_id

    class Meta():
        verbose_name = "Versão"
        verbose_name_plural = "Versões do Carolina"


# obs: English names in order to align with tags from the tag reader script.
class Text(models.Model):
    text_id = models.CharField(max_length=300,primary_key=True) #"Id"
    corpus_version = models.ForeignKey(CarolinaVersao, on_delete=models.CASCADE) #"Versão do Carolina"
    file_path = models.CharField(max_length=300) #"Documento de alimentação dos dados"
    last_modified = models.DateTimeField(default=datetime.datetime.now) 

    # Curadoria
    curation_organizers_download = models.CharField(max_length=500) #"Responsabilidade pelo download" 
    curation_organizers_extraction = models.CharField(max_length=500) # "Responsabilidade pela extração"
    curation_organizers_metadata = models.CharField(max_length=500) #"Responsabilidade pelos metadados" 
    curation_publication_authority = models.CharField(max_length=500) # "Autoridade no Carolina"
    curation_date_download = models.DateField()# "Data de download"
    curation_date_extraction = models.DateField()# "Data de extração"
    curation_license_name = models.CharField(max_length=500) # "Licença no Carolina"
    curation_license_url = models.CharField(max_length=500) # "URL da licença no Carolina"
    curation_availability = models.CharField(max_length=500) # "Acesso no Carolina"#
   

    # Origem/Fonte      
    origin_title = models.CharField(max_length=500, blank=True, null=True)# "Título"
    origin_url = models.CharField(max_length=500)# "URL da fonte"
    origin_author = models.CharField(max_length=500, null=True) # "Autor"
    origin_sponsor = models.CharField(max_length=500, blank=True, null=True) # "Mantenedor"
    origin_authority = models.CharField(max_length=500, blank=True, null=True) # "Autoridade da fonte"
    origin_publication_date = models.CharField(max_length=500, blank=True, null=True)# "Data de publicação da fonte"
    origin_license_name = models.CharField(max_length=500) # "Licença da fonte"
    origin_license_url = models.CharField(max_length=500, blank=True, null=True) # "URL da licença da fonte"
    origin_series_title = models.CharField(max_length=500, blank=True, null=True) # "Coleção"
    origin_series_scope = models.CharField(max_length=500, blank=True, null=True) # "Parte"
    origin_file_type = models.CharField(max_length=500, blank=True, null=True) # "Formato original"
    origin_pages = models.CharField(max_length=500, blank=True, null=True) # Páginas da fonte
    origin_file_source = models.CharField(max_length=500, blank=True, null=True) # "Arquivo fonte
    origin_translator = models.CharField(max_length=500, blank=True, null=True) #  "Tradutor"
    origin_publisher = models.CharField(max_length=500, blank=True, null=True)# "Editora
    origin_access = models.CharField(max_length=500, blank=True, null=True) # Acesso da fonte  
    origin_region =  models.CharField(max_length=500, blank=True, null=True) # Região da fonte
    origin_acquisition = models.CharField(max_length=500, blank=True, null=True) # Natureza da aquisição
    origin_text_mode = models.CharField(max_length=500, blank=True, null=True)# Texto escrito ou transcrito 
    origin_text_integrity = models.CharField(max_length=500, blank=True, null=True) # Integridade
    origin_count_tokens = models.BigIntegerField(blank=True, null=True)# "Tokens da fonte"
    origin_count_bytes = models.BigIntegerField(blank=True, null=True)# "Bytes da fonte"

    # Medidas
    measure_tokens = models.BigIntegerField(blank=True, null=True) # Tokens no Carolina

    # Conteúdo do texto  
    text_domain = models.CharField(max_length=500, blank=True, null=True) # "Domínio"
    text_language = models.CharField(max_length=500, blank=True, null=True) #"Língua"
    text_curation_typology = models.CharField(max_length=500, blank=True, null=True) #"Tipologia ampla"
    text_origin_typology = models.CharField(max_length=500, blank=True, null=True)#Tipologia da fonte
    text_preparation_degree = models.CharField(max_length=500, blank=True, null=True) #Grau de preparação
    text_linguistic_variation = models.CharField(max_length=500, blank=True, null=True) #Variedade linguística 
    text_content = models.TextField()# "Texto"
    text_tei = models.TextField()#"tag <TEI>"


    
    file_path.verbose_name = "Documento de alimentação dos dados"
    corpus_version.verbose_name = "Versão do Carolina"
    text_id.verbose_name = "Id"

    curation_organizers_download.verbose_name = "Responsabilidade pelo download"
    curation_organizers_extraction.verbose_name = "Responsabilidade pela extração"
    curation_organizers_download.verbose_name = "Responsabilidade pelos metadados"
    curation_publication_authority.verbose_name = "Autoridade no Carolina"
    curation_date_download.verbose_name = "Data de download"
    curation_date_extraction.verbose_name = "Data de extração"
    curation_license_name.verbose_name = "Licença no Carolina" 
    curation_license_url.verbose_name = "URL da licença no Carolina" 
    curation_availability.verbose_name = "Acesso no Carolina"
    text_curation_typology.verbose_name = "Tipologia ampla"
    text_origin_typology.verbose_name = "Tipologia da fonte"

    origin_title.verbose_name = "Título"
    origin_url.verbose_name = "URL da fonte"
    origin_author.verbose_name = "Autor"
    origin_sponsor.verbose_name = "Mantenedor"
    origin_authority.verbose_name = "Autoridade da fonte"
    origin_publication_date.verbose_name = "Data de publicação da fonte"
    origin_license_name.verbose_name = "Licença da fonte"
    origin_license_url.verbose_name = "URL da licença da fonte"
    origin_series_title.verbose_name = "Coleção"
    origin_series_scope.verbose_name = "Parte"
    origin_file_type.verbose_name = "Formato original"
    text_preparation_degree.verbose_name = "Grau de preparação"


    origin_pages.verbose_name = "Páginas da fonte"
    origin_file_source.verbose_name = "Arquivo fonte" 
    origin_file_source.verbose_name = "Arquivo fonte" 
    origin_translator.verbose_name = "Tradutor" 
    origin_publisher.verbose_name = "Editora" 
    origin_access.verbose_name = "Acesso da fonte" 
    origin_region.verbose_name  = "Região da fonte" 
    origin_acquisition.verbose_name = "Natureza da aquisição"
    origin_text_mode.verbose_name = "Texto escrito ou transcrito" 
    origin_text_integrity.verbose_name = "Integridade" 
    origin_count_tokens.verbose_name = "Tokens da fonte"
    origin_count_bytes.verbose_name = "Bytes da fonte"
    text_linguistic_variation.verbose_name = "Variedade linguística" 

    text_domain.verbose_name = "Domínio" 
    text_language.verbose_name = "Língua"
    text_content.verbose_name = "Texto" 
    text_tei.verbose_name = "tag <TEI>" 

    measure_tokens.verbose_name = "Tokens no Carolina"

    class Meta():
        verbose_name = 'Texto'
        verbose_name_plural = 'Textos'


class Atributo(models.Model):
    atributo_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100,choices=zip(FEATURES.values(),FEATURES.keys()), default='select')
    secao = models.CharField(max_length=300, choices=SECTION, default=1)
    tipo_filtro = models.CharField(max_length=40,choices=TIPO_FILTRO, default='select')
    mensagem = models.CharField(max_length=300, blank=True)
    filtro_display = models.CharField(max_length=10,choices=DISPLAY, default='no')
    
    secao.verbose_name = "Seção no filtro"

    class Meta():
        verbose_name = "Atributo"
        verbose_name_plural = "Atributos"
    def __str__(self):
        return str(self.atributo_id) + ' - ' + self.nome

class Filtro(models.Model):
    filtro_id = models.AutoField(primary_key=True)
    atributo = models.ForeignKey(Atributo, on_delete=models.CASCADE)
    opcao = models.CharField(max_length=500,  blank=True, null=True)

    class Meta():
        verbose_name = "Opções de filtro seleção"
        verbose_name_plural = "Opções de filtro seleção"

class TextoArmazenamento(models.Model):
    text_id = models.CharField(max_length=300,primary_key=True) #"Id"
    file_path = models.CharField(max_length=500)
    date_db = models.DateTimeField(default=datetime.datetime.now) 
   
    class Meta:
        verbose_name = "Data de inclusão (xml)"
        verbose_name_plural = "Data de inclusão (xml)"
    
class TextoConteudoAdmin(admin.ModelAdmin):
    list_display = ("text_id", "corpus_version","text_domain","text_typology","text_language")

class TextoCuradoriaAdmin(admin.ModelAdmin):
    list_display = ("curation_id", "corpus_version","curation_date_download","curation_license_name")

class FiltroAdmin(admin.ModelAdmin):
    list_display = ("atributo", "opcao")
    ordering = ["atributo","opcao"]
   
class TextAdmin(admin.ModelAdmin):
    list_display = ("text_id", "corpus_version","text_curation_typology","text_language", "curation_date_download","curation_license_name","origin_license_name")
    search_fields = ["text_id"]
    
class TextoMedidasAdmin(admin.ModelAdmin):
    list_display = ("measure_id", "corpus_version","measure_tokens")

class AtributoAdmin(admin.ModelAdmin):
    def nome_display(self, nome):
        return get_nome_display()

    list_display = ("atributo_id","nome", "secao","tipo_filtro","filtro_display")
    search_fields = ["nome"]
    ordering = ["atributo_id","nome", "filtro_display"]

class TextoOrigemAdmin(admin.ModelAdmin):
    list_display = ("origin_id", "corpus_version","origin_publication_date","origin_license_name")

class EquipeAdmin(admin.ModelAdmin):
    list_display = ("nome","filiacao","posicao")
    search_fields = ["nome","filiacao","posicao"]
    ordering = ["nome","filiacao","posicao"]

class CorpusOrigemAdmin(admin.ModelAdmin):
    list_display = ('corpus_nome', 'autor', 'autoridade', 'tema', 'subtema', 'instituicao_mantenedora', 'licenca')
    search_fields = ['corpus_nome', 'autor','autoridade']

class SubtemaAdmin(admin.ModelAdmin):
    list_display = ('subtema_nome', 'subtema_tema')

class TextoArmazenamentoAdmin(admin.ModelAdmin):
    list_display = ('text_id', 'date_db')
    search_fields = ["text_id"]
    ordering = ["date_db"]





   




