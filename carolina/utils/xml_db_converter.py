# Rode este programa para inserir os dados dos arquivos xml que estiverem na pasta corpuscarolina no banco de dados

import sys, os, django, json
from pathlib import Path
import CarolinaTagReader as ctag
import xml.etree.ElementTree as ET
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carolina.settings")
django.setup()
from webpage.models import *


namespace = "http://www.tei-c.org/ns/1.0"
versao_id = "1.2 Ada"


def extract_xmltei_to_db(root, file_name, control):
	i=1
	for text in root.findall(doc.add_prepend('TEI')):
		tei = ctag.Text(text, doc.add_prepend)

		text_code = tei.text_curation_textcode
		corpus_version = CarolinaVersao.objects.get(versao_id=versao_id)
		try:
			a = {}
			print(a['chavenaoexiste'])
			text = Text.objects.get(text_id=text_code)
		except:
			control.append(tei.text_curation_textcode)
			tei_string = ET.tostring(text, encoding="unicode")
			tei_string = '\t<TEI'+tei_string[len(namespace)+13:]

			t = Text(
				# info
				text_id = text_code,  #Id
				corpus_version = corpus_version, #"Versão do Carolina"
				file_path = file_name, #"Documento de alimentação dos dados"
				# text
				text_domain = tei.text_domain, #Domínio
				text_language = tei.text_language, #"Língua"
				text_curation_typology = tei.text_typology['curation_typology'], #"Tipologia ampla"
				text_origin_typology = tei.text_typology['source_typology'], #Tipologia da fonte
				text_linguistic_variation = tei.text_linguistic_variation, #Variedade linguística 
				text_preparation_degree = tei.text_preparation_degree, #Grau de preparação
				text_content = tei.text_content, # "Texto"
				text_tei = tei_string, #"tag <TEI>"
				# curation
				curation_organizers_download = tei.text_curation_organizers['Download'],#"Responsabilidade pelo download" 
				curation_organizers_extraction = tei.text_curation_organizers['Extraction'], # "Responsabilidade pela extração"
				curation_organizers_metadata = tei.text_curation_organizers['Metadata'],#"Responsabilidade pelos metadados"
				curation_publication_authority = tei.text_curation_publication_authority, #Autoridade no Carolina
				curation_date_download = tei.text_curation_publication_date['Download'],#"Data de download"
				curation_date_extraction = tei.text_curation_publication_date['Extraction'],# "Data de extração"
				curation_license_name = tei.text_curation_license['license_name'],#"Licença no Carolina"
				curation_license_url = tei.text_curation_license['license_url'],#"URL da licença no Carolina"
				curation_availability = tei.text_curation_availability, #"Acesso no Carolina"   
			    # origin
				origin_title = tei.text_origin_title, #"Título"
				origin_url = tei.text_origin_url['text_origin_url'], #"URL da fonte"
				origin_author = tei.text_origin_author, # "Autor"
				origin_sponsor = tei.text_origin_sponsor,#"Mantenedor"
				origin_authority = tei.text_origin_authority,  #"Autoridade da fonte"
				origin_publication_date = tei.text_origin_publication_date, #"Data de publicação da fonte"
				origin_file_type = tei.text_origin_url['text_origin_file_type'], # Formato original
				origin_pages = tei.text_origin_counts['pages'],  #Páginas da fonte 
				origin_license_name = tei.text_origin_license['license_name'], #"Licença da fonte"
				origin_file_source = tei.text_origin_url['text_origin_file_source'], # Arquivo fonte
				origin_translator = tei.text_origin_translator, # "Tradutor" = adiionar 
				origin_publisher = tei.text_origin_publisher, #"Editora 
				origin_access = tei.text_origin_access, #Acesso da fonte 
				origin_region = tei.text_origin_region, #Região da fonte  
				origin_acquisition = tei.text_origin_acquisition, #Natureza da aquisição adiionar
				origin_text_mode = tei.text_mode, #Texto escrito ou transcrito adiionar 
				origin_text_integrity = tei.text_origin_integrity,#Integridade adiionar 
				origin_count_tokens = int(tei.text_origin_counts['tokens']), #"Tokens da fonte" 
				origin_count_bytes = int(tei.text_origin_counts['bytes']), #"Bytes da fonte" 
				origin_license_url = tei.text_origin_license['license_url'], # "URL da licença da fonte"
				origin_series_title = tei.text_origin_series['series_title'], #"Coleção"
				origin_series_scope = tei.text_origin_series['series_scope'], # "Parte"
				measure_tokens = int(tei.text_measure_tokens['quantity']) # Tokens no Carolina
			)

			a = TextoArmazenamento(
				text_id = text_code,
    			file_path = file_name
			)

			t.save()
			a.save()
		i+=1
	return i, control



path_corpus = os.path.join(BASE_DIR,'corpuscarolina')
print(path_corpus)
doc_paths = []
for dirs,subdirs,files in os.walk(path_corpus):
	for file in files:
		if file.endswith('.xml'):
			doc_paths.append(os.path.join(dirs,file))


count_tei = 0
control = []
for doc_path in doc_paths:
	xml_doc = doc_path
	file = os.path.relpath(doc_path, path_corpus)
	doc = ctag.DocXML(xml_doc,namespace)
	root = doc.root
	i, control = extract_xmltei_to_db(root, file, control)
	count_tei+=i
	
	# arquivo de controle dos textos inseridos
	with open('control_xml_db_insert.json', 'w') as f:
		json.dump(control, f)
	
	print('quantidade de textos inseridos: ',count_tei)