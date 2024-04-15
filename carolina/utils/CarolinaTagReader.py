import xml.etree.ElementTree as ET
# testes
def get_root(xml_doc, namespace):
	#tree = ET.parse('SOCa.xml')
	tree = ET.parse(xml_doc)
	root = tree.getroot()
	ET.register_namespace('', namespace)
	return root


class DocXML:
	def __init__(self, xml_doc, namespace):
		self.root = get_root(xml_doc, namespace)
		# Adapt tags (remove initial part prepend)
		def get_prepend():
			root = self.root
			return root.tag[:(len(root.tag) - len('teiCorpus'))]
        
		self.prepend = get_prepend()
		

	def add_prepend(self, s):
		return self.prepend + s
	def remove_prepend(self, s):
		return s[len(self.prepend):]


class TextCuration:
	#1-------------Dados do trabalho feito pelo Carolina-------------
	def __init__(self,tei, add_prepend):
		self.tei = tei
		self.add_prepend = add_prepend 
		self.fileDesc = self.tei.find(self.add_prepend('teiHeader')).find(self.add_prepend('fileDesc'))
		
		# 1.1 titleStmt (dados de autoria)
		self.titleStmt = self.fileDesc.find(self.add_prepend('titleStmt'))
		# 1.1.3 publicationsStmt (dados de pulblicação Carolina)
		self.publicationStmt = self.fileDesc.find(self.add_prepend('publicationStmt'))

	#1.1 titleStmt (dados de autoria)
	def text_code(self):
		#1.1.1 title (codigo do texto ex: SOC000000001a) 
		text_code = self.titleStmt.find(self.add_prepend('title'))
		return text_code.text

	def organizers(self):
		# respStmt (par (responsabilidade, nome)) ex:('Download', 'Maria Clara') ('Metadata', 'Maria Ramos')
		respStmt = self.titleStmt.findall(self.add_prepend('respStmt'))
		resp_name = {child.find(self.add_prepend('resp')).text : ', '.join([str(name.text) for name in child.findall(self.add_prepend('name'))]) for child in respStmt}
	#	print(resp_name)
		return resp_name

	# 1.1.3 publicationsStmt (dados de pulblicação Carolina)
	def publication_authority(self):
		# publications authority (ex: 'LaViHD@C4AI')
		authority = self.publicationStmt.find(self.add_prepend('authority'))
		return authority.text

	def publication_date(self):
		# 1.1.4 publications dates (type and date) ex:'Download', '2022-09-02', 'Extraction', '2022-09-02')
		dates = self.publicationStmt.findall(self.add_prepend('date'))
		dates_of_publications = {d.attrib['type']:d.text for d in dates}
		#print(dates_publications)
		return dates_of_publications

	def license(self):
		# 1.1.5 license (url da licenca, licenca) ex: {'target': 'https://creativecommons.org/licenses/by-nc-sa/4.0/'}, 'CC BY-NC-SA 4.0'
		license = self.publicationStmt.find(self.add_prepend('availability')).find(self.add_prepend('license'))
		license_data = {'license_url': license.attrib['target'], 'license_name':license.text}
		#print(license_data)
		return license_data

	def availability(self):
		availability = self.publicationStmt.find(self.add_prepend('availability')).attrib['status']
		return availability

		


class TextOrigin:
	# 2---------------Dados do corpus de origem---------------
	def __init__(self,tei, add_prepend):
		self.add_prepend = add_prepend
		self.fileDesc = tei.find(self.add_prepend('teiHeader')).find(self.add_prepend('fileDesc'))
		self.fileDesc1 = self.fileDesc.find(self.add_prepend('sourceDesc')).find(self.add_prepend('biblFull')).find(self.add_prepend('fileDesc'))
		
		#2.1 titleStmt (dados de autoria)
		self.titleStmt = self.fileDesc1.find(self.add_prepend('titleStmt'))
		self.text_title = self.titleStmt.find(self.add_prepend('title'))
		# 2.2 publicationStmt (dados da publicacao do texto)
		self.publicationStmt = self.fileDesc1.find(self.add_prepend('publicationStmt'))
		# 2.3 seriesStmt
		self.seriesStmt = self.fileDesc1.find(self.add_prepend('seriesStmt'))

	#2.1 titleStmt (dados de autoria do texto)
	def title(self):
		# 2.1.1 title (name, url do texto) 
        #ex:Empatia {'mimeType': 'text/csv', 'url': 'https://www.wattpad.com/800462253-algumas-palavras-empatia', 'source': 'chapters_content.csv'}
		text_title_name = self.text_title.find(self.add_prepend('name'))
		return text_title_name.text
	def origin_url(self):
		text_url = self.text_title.find(self.add_prepend('media')).attrib
		return {'text_origin_url':text_url['url'],'text_origin_file_source':text_url['source'], 'text_origin_file_type':text_url['mimeType']}
		
	def author(self):
		# 2.1.2 author
		authors = self.titleStmt.findall(self.add_prepend('author'))
		return ", ".join([str(author.text) for author in authors])

	def translator(self):
		# 2.1.3 editor
		translators = self.titleStmt.findall(self.add_prepend('editor'))
		return ", ".join([str(translator.text) for translator in translators])
		
	def sponsor(self):
		# 2.1.4 sponsor
		sponsors = self.titleStmt.findall(self.add_prepend('sponsor'))
		sponsors = ", ".join([str(sponsor.text) for sponsor in sponsors])
		return sponsors

	# 2.2 publicationStmt (dados da publicacao do texto)
	def publisher(self):
		publishers = self.publicationStmt.find(self.add_prepend('publisher'))
		return ", ".join([str(publisher.text) for publisher in publishers]) 

	def publication_authority(self):
		# 2.2.1 publications authority (ex: '')
		authorities = self.publicationStmt.findall(self.add_prepend('authority'))
		return ", ".join([str(authority.text) for authority in authorities])
		

	def publication_date(self):
		# 2.2.2 publications date (ex: '')
		date = self.publicationStmt.find(self.add_prepend('date'))
		return date.text

	def access(self): #Acesso da fonte 
		access = self.publicationStmt.find(self.add_prepend('availability')).attrib # falta o resto
		return access['status']

	def acquisition(self): #Acesso da fonte 
		acquisition = self.fileDesc1.find(self.add_prepend('sourceDesc')).find(self.add_prepend('p')) # falta o resto
		return acquisition.text
	
	def text_region(self): #Acesso da fonte 
		region = self.publicationStmt.find(self.add_prepend('address')).find(self.add_prepend('region')) # falta o resto
		return region.text

	def license(self):
		# 2.2.3 publications lincenca (url da licenca, licenca) ex: ({'target': 'https://www.wattpad.com/story/54284621-fatos-e-curiosidades-de-harry-potter'}, 'Public Domain')
		text_license = self.publicationStmt.find(self.add_prepend('availability')).find(self.add_prepend('license'))
		license_data = {'license_url':text_license.attrib['target'], 'license_name':text_license.text}
		return license_data
	
	# 2.3 seriesStmt
	def series(self):
		# 2.3.1 title
		series_title = self.seriesStmt.find(self.add_prepend('title'))
		# 2.3.2 bib scope
		biblScope = self.seriesStmt.find(self.add_prepend('biblScope'))
		#if n==1:print(title.text,' lalala ', biblScope.text)
		return {'series_title':series_title.text,'series_scope':biblScope.text}
	
	# 2.4 2.4.1 ---p?----
	def source_type(self):
		# 2.4 2.4.1 ---p?----
		p = self.fileDesc1.find(self.add_prepend('sourceDesc')).find(self.add_prepend('p'))
		return p.text

	def source_counts(self):#Tokens da fonte 
		# 2.1.4 sponsor
		measures = self.fileDesc1.find(self.add_prepend('extent')).findall(self.add_prepend('measure'))
		counts = {measure.attrib['unit']: measure.attrib['quantity'] for measure in measures}
		return counts



class TextContent:
	# 2---------------Dados do texto---------------
	def __init__(self, tei, add_prepend):
		self.tei = tei
		self.add_prepend = add_prepend
		self.fileDesc = tei.find(self.add_prepend('teiHeader')).find(self.add_prepend('fileDesc'))
		
		# 2.5 ----profileDesc1----
		self.profileDesc1 = self.fileDesc.find(self.add_prepend('sourceDesc')).find(self.add_prepend('biblFull')).find(self.add_prepend('profileDesc'))
		# 2.6 ----profileDesc----
		self.profileDesc = self.tei.find(self.add_prepend('teiHeader')).find(self.add_prepend('profileDesc'))

	# 2.5 ----profileDesc----
	def text_domain(self): 
		# 2.5.1 (dominio) ex:'Literary'
		domain = self.profileDesc1.find(self.add_prepend('textDesc')).find(self.add_prepend('domain'))
		return domain.text
	
	def text_mode(self): 
		# 2.5.1 (dominio) ex:'Literary'
		mode = self.profileDesc1.find(self.add_prepend('textDesc')).find(self.add_prepend('channel')).attrib
		return mode['mode']

	def text_integrity(self):
		intergrity = self.profileDesc1.find(self.add_prepend('textDesc')).find(self.add_prepend('constitution')).attrib
		return intergrity['type']

	
	
	def typology(self):
		# 2.5.2 classe (scheme, target) ex:'{'scheme': '#Source_typology', 'target': '#ORIGINAL_STORY_LIT_W'}'
		typology_original = self.profileDesc1.find(self.add_prepend('textClass')).find(self.add_prepend('catRef')).attrib
		# 2.6 2.6.1 {'scheme': '#Source_typology', 'target': '#ORIGINAL_STORY_LIT_W'}

		typology_curation = self.profileDesc.find(self.add_prepend('textClass')).find(self.add_prepend('catRef')).attrib
		#print(typology)

		return {
			'source_typology':typology_original['target'][1:], 
			'curation_typology':typology_curation['target'][1:]
			}

	def language(self):
		# 2.5.3 language ex:'{'ident': 'pt-BR'}'
		text_language = self.profileDesc1.find(self.add_prepend('langUsage')).find(self.add_prepend('language')).attrib
		return text_language['ident']
		

	def text(self):
		# 2.7 2.7.1 TEXTO
		text_content = self.tei.find(self.add_prepend('text')).find(self.add_prepend('body')).findall(self.add_prepend('p'))
		text_paragraphs = '\n'.join([str(p.text) for p in text_content])
		return text_paragraphs
	
	def preparation_degree(self): 
		preparation_degree = self.profileDesc1.find(self.add_prepend('textDesc')).find(self.add_prepend('preparedness')).attrib
		return preparation_degree['type']
	
	def linguistic_variation(self): 
		linguistic_variation = self.profileDesc1.find(self.add_prepend('langUsage')).findall(self.add_prepend('language'))
		return ", ".join([str(variation.text) for variation in linguistic_variation])



class TextMeasurements:
	def __init__(self,tei, add_prepend):
		self.add_prepend = add_prepend
		self.fileDesc = tei.find(self.add_prepend('teiHeader')).find(self.add_prepend('fileDesc'))

	def tokens(self):
	    # 1.1.2 measure (medida em tokens) ex:{'unit': 'tokens', 'quantity': '7'}
		number_of_tokens = self.fileDesc.find(self.add_prepend('extent')).find(self.add_prepend('measure')).attrib
		#print(measure)
		return number_of_tokens #['quantity']


class Text(TextCuration,TextOrigin,TextContent):
	def __init__(self,tei, add_prepend):
		self.add_prepend = add_prepend
		self.TextCuration = TextCuration(tei, self.add_prepend)
		self.TextOrigin = TextOrigin(tei, self.add_prepend)
		self.TextMeasurements = TextMeasurements(tei, self.add_prepend)
		self.TextContent = TextContent(tei, self.add_prepend)

		#TextCuration - 5
		self.text_curation_textcode = self.TextCuration.text_code()
		self.text_curation_organizers = self.TextCuration.organizers()
		self.text_curation_publication_authority = self.TextCuration.publication_authority()
		self.text_curation_publication_date = self.TextCuration.publication_date()
		self.text_curation_license = self.TextCuration.license()
		self.text_curation_availability = self.TextCuration.availability()
		
		# TextOrigin - 10
		self.text_origin_title =self.TextOrigin.title()
		self.text_origin_url = self.TextOrigin.origin_url()
		self.text_origin_author = self.TextOrigin.author()
		self.text_origin_translator = self.TextOrigin.translator()
		self.text_origin_sponsor = self.TextOrigin.sponsor()
		self.text_origin_authority = self.TextOrigin.publication_authority()
		self.text_origin_publication_date = self.TextOrigin.publication_date()
		self.text_origin_license = self.TextOrigin.license()
		self.text_origin_series = self.TextOrigin.series()
		self.text_origin_source_type = self.TextOrigin.source_type()

		self.text_origin_access = self.TextOrigin.access()
		self.text_origin_publisher = self.TextOrigin.publisher()
		self.text_origin_integrity = self.TextContent.text_integrity()
		self.text_origin_acquisition = self.TextOrigin.acquisition() #Natureza da aquisição 
		self.text_mode = self.TextContent.text_mode()# Texto escrito ou transcrito
		#self.text_origin_pages = self.TextContent.origin_pages()
		self.text_origin_counts = self.TextOrigin.source_counts()
		self.text_origin_region = self.TextOrigin.text_region()

		# TextMeasurements - 1
		self.text_measure_tokens = self.TextMeasurements.tokens()

		# Text - 4
		self.text_domain = self.TextContent.text_domain()
		self.text_language = self.TextContent.language()
		self.text_typology = self.TextContent.typology()# "Tipologia ampla" e "Tipologia da fonte"
		self.text_content = self.TextContent.text()

		# Grau de preparação 
		self.text_preparation_degree = self.TextContent.preparation_degree() #Grau de preparação
		self.text_linguistic_variation = self.TextContent.linguistic_variation() #Variedade linguística


