from django.db.models import Case, When, Value

# Filters for db fields

PUBLICACAO = [
    ('artigo em revista','artigo em revista'),
    ('artigo em conferência','artigo em conferência'),
    ('livro','livro'),
    ('apresentação','apresentação'),
    ('seminário','seminário'),
    ('outro','outro')
]


publicacao_tipo_order = Case(*[
        When(tipo='artigo em revista', then=Value(1)),
        When(tipo='artigo em conferência', then=Value(2)),
        When(tipo='livro', then=Value(3)),
        When(tipo='apresentação', then=Value(4)),
        When(tipo='seminário', then=Value(5)),
        When(tipo='outro', then=Value(6)),
])


POSITION = [
    ('docente','docente'),
    ('pós-doc (completo)','pós-doc (completo)'),
    ('pós-doc (andamento)','pós-doc (andamento)'),
    ('doutorado (completo)','doutorado (completo)'),
    ('doutorado (andamento)','doutorado (andamento)'),
    ('mestrado (completo)','mestrado (completo)'),
    ('mestrado (andamento)','mestrado (andamento)'),
    ('graduação (completa)','graduação (completa)'),
    ('graduação (andamento)','graduação (andamento)'),
    ('outro','outro')
]


DISPLAY = [
    ('yes','yes'),
    ('no','no')
]


TIPO_FILTRO = [
    ('select', 'select'),
    ('text','text'),
    ('numeric', 'numeric (para valores de números inteiros)'),
]


TEXT_ID ={
    'name':'text_id',
    'frontname':'Código do texto',
    'namecss':'text_id',
    'options':[('DAT','DAT'),('PUB','PUB'),('LEG','LEG')]
}


VERSION ={
    'name':'corpus_version',
    'frontname':'Versão do Corpus',
    'namecss':'corpus_version',
    'options':[('1.2','1.2'),('1.1','1.1')]
}


SECTION = [
    ('1','Curadoria'),
    ('2','Texto'),
    ('3','Medidas'),
    ('4', 'Proveniência'),
]


FEATURES = {
    'Id': 'text_id', 
    'Versão do Carolina': 'corpus_version', 
    'Documento de alimentação dos dados': 'file_path', 
    'Responsabilidade pelo download': 'curation_organizers_download', 
    'Responsabilidade pela extração': 'curation_organizers_extraction', 
    'Responsabilidade pelos metadados': 'curation_organizers_metadata', 
    'Autoridade no Carolina': 'curation_publication_authority', 
    'Data de download': 'curation_date_download', 
    'Data de extração': 'curation_date_extraction', 
    'Licença no Carolina': 'curation_license_name', 
    'URL da licença no Carolina': 'curation_license_url', 
    'Acesso no Carolina': 'curation_availability', 
    'Título': 'origin_title', 
    'URL da fonte': 'origin_url', 
    'Autor': 'origin_author', 
    'Mantenedor': 'origin_sponsor', 
    'Autoridade da fonte': 'origin_authority', 
    'Data de publicação da fonte': 'origin_publication_date', 
    'Licença da fonte': 'origin_license_name', 
    'URL da licença da fonte': 'origin_license_url', 
    'Coleção': 'origin_series_title', 
    'Parte': 'origin_series_scope', 
    'Formato original': 'origin_file_type', 
    'Páginas da fonte': 'origin_pages', 
    'Arquivo fonte': 'origin_file_source', 
    'Tradutor': 'origin_translator', 
    'Editora': 'origin_publisher', 
    'Acesso da fonte': 'origin_access', 
    'Região da fonte': 'origin_region', 
    'Natureza da aquisição': 'origin_acquisition', 
    'Texto escrito ou transcrito': 'origin_text_mode', 
    'Integridade': 'origin_text_integrity', 
    'Tokens da fonte': 'origin_count_tokens', 
    'Bytes da fonte': 'origin_count_bytes', 
    'Tokens no Carolina': 'measure_tokens', 
    'Domínio': 'text_domain', 
    "Língua": 'text_language', 
    'Tipologia ampla': 'text_curation_typology', 
    'Tipologia da fonte': 'text_origin_typology', 
    'Grau de preparação': 'text_preparation_degree', 
    'Variedade linguística': 'text_linguistic_variation', 
    'Texto': 'text_content'
    }
