#-*- coding: utf-8 -*-
from __future__ import unicode_literals
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_Rules_Brazilian_Specific(Plugin):

    only_for = ['BR']


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9018002] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'Brasil - Verificar')}
        self.errors[9018003] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'palavra abreviada em {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9018004] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'nome supérfluo/incompleto de local de lazer')}
        self.errors[9018005] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'nome supérfluo/incompleto de local de saúde')}
        self.errors[9018006] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'Brasil - Correções e melhorias')}
        self.errors[9018007] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'objeto com nomenclatura incorreta')}
        self.errors[9018008] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} não deve ser utilizado em nó; utilizar a restrição na via', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9018009] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} é uma chave utilizada apenas no Reino Unido', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9018010] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} sem pelo menos uma das tags: {1} ou {2}', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))}
        self.errors[9018012] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} sem nome', mapcss._tag_uncapture(capture_tags, u'{0.value}'))}
        self.errors[9018013] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} deve conter apenas o nome da cidade', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9018014] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} com valor = {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))}
        self.errors[9018016] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'SAMU classificado de forma errada')}
        self.errors[9018017] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'objeto não deve possuir {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))}
        self.errors[9018018] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'adicionar {0} ao {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}'))}
        self.errors[9018019] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} deve ser utilizado com {1}={0} ou {2}={0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))}
        self.errors[9018020] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} deve estar incluído em {1}, separado por \'\';\'\' caso necessário', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))}
        self.errors[9018021] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'especificar valor correto para {0} ao invés de \'\'{1}\'\'', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss.tag(tags, u'landuse'))}
        self.errors[9018022] = {'item': 9018, 'level': 2, 'tag': ["tag"], 'desc': mapcss.tr(u'chave inválida: {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9018023] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'não se deve utilizar {0} para demarcar áreas de cobertura de imagem', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9018026] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'possível ausência de tag {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))}
        self.errors[9018027] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'ausência do tempo de duração ({0}) da balsa', mapcss._tag_uncapture(capture_tags, u'{1.key}'))}
        self.errors[9018029] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'possível definição incorreta para praça: \'\'{0}\'\'', mapcss._tag_uncapture(capture_tags, u'{2.key}'))}
        self.errors[9018030] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'utilizar prefixo em português (pt:) para {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9018031] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'nome utilizado de forma incorreta')}
        self.errors[9018032] = {'item': 9018, 'level': 2, 'tag': ["tag"], 'desc': mapcss.tr(u'nó não deve possuir {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))}
        self.errors[9018033] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} deve possuir {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))}
        self.errors[9018034] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'valor incorreto para {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9018035] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'ausência de boundary=protected_area')}
        self.errors[9018036] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} deve ser usado apenas em ways', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9018037] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'utilize \'\'destination\'\' no caminho de saída ao invés de \'\'exit_to\'\'')}
        self.errors[9018039] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'o conteúdo de {0} deve fazer parte de ref, separado por ;', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9018041] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'objeto incompleto: possui apenas {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9018042] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'objeto incompleto: possui apenas {0} e {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))}
        self.errors[9018043] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', mapcss.tag(tags, u'addr:housenumber'))}
        self.errors[9018044] = {'item': 9018, 'level': 2, 'tag': ["tag"], 'desc': mapcss.tr(u'objeto contém Google como source')}
        self.errors[9018046] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'relação não deve possuir {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))}
        self.errors[9018047] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} deve ser utilizado apenas em nós', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))}
        self.errors[9018048] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} deve possuir \'\'type=boundary\'\'', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9018049] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} deve ser utilizado junto com {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))}
        self.errors[9018051] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'não classificar via como {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))}
        self.errors[9018052] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} com nome supérfluo/incompleto', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
        self.errors[9018053] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} não deve possuir {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))}
        self.errors[9018056] = {'item': 9018, 'level': 2, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} deve ser utilizado apenas no nó de saída da rodovia', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))}
        self.errors[9018063] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'uso incorreto de {0} com {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))}
        self.errors[9018064] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'uso incorreto de {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))}

        self.re_01454d46 = re.compile(r'(?i)\bmotel\b')
        self.re_044c8944 = re.compile(r'^(?i)(?u)(SENAC|SENAI|Serviço Nacional de Aprendizagem)')
        self.re_04873a60 = re.compile(r'^(river|stream)$')
        self.re_05a345c7 = re.compile(r'^(forest|grass|greenfield|meadow|orchard)$')
        self.re_066203d3 = re.compile(r'^[0-9]+$')
        self.re_073e5345 = re.compile(r'\b[A-Z]{2,3} (- )?[0-9]{2,3}\b')
        self.re_07f31a73 = re.compile(r'^(living_street|pedestrian|residential|road|service|track)$')
        self.re_0b27200b = re.compile(r'(?i)^s(\.|-| )?\/?n\.?º?$')
        self.re_0db5b64e = re.compile(r'village|town|city')
        self.re_1054eb5a = re.compile(r'bridleway|bus_stop|cycleway|crossing|footway|give_way|motorway_junction|path|raceway|rest_area|services|speed_camera|steps|stop')
        self.re_10f1c360 = re.compile(r'(,|( |-) ?[A-Z]{2})')
        self.re_126ba9a9 = re.compile(r'(?i)^Borrach(aria|eiro)')
        self.re_12b48afb = re.compile(r'^(grassland|heath|scrub|wood)$')
        self.re_131cc885 = re.compile(r' ou ')
        self.re_139e342b = re.compile(r'(?i)^Helipo(n|r)to.*')
        self.re_13f4c147 = re.compile(r'(?i)(?u)^paço\b')
        self.re_152c10ee = re.compile(r'hamlet|isolated_dwelling|town|village')
        self.re_15690541 = re.compile(r'^(?i)estrada de ferro')
        self.re_160d1bfc = re.compile(r'^(?i)creche\b')
        self.re_178f5446 = re.compile(r'(?i)(^|.* )(Cel|Cmte|Cond|Conj|Dª|Dr|Eng|Gov|Hab|Jd|Jr|Marg|Mun|p\/|Pde|Pe|Pq|Pst|Pref|Profa|Profª|Prof|Res|s\/|Sr(a|ª)?|Sta|Sto|Ver)\.? .*')
        self.re_17fd35b3 = re.compile(r'^pt:')
        self.re_1d232d4c = re.compile(r'^(?i)(?u)(Centro Universitário|Faculdades?|FATEC|Instituto Federal)\b')
        self.re_20188fb1 = re.compile(r'^[0-9]+( |-)*([A-Z])?$')
        self.re_20c7dd98 = re.compile(r'^(?i)(?u)(aldeia|borrach(aria|eiro)|bosque|capela|cemit(é|e)rio|c(ó|o)rrego|escola|estacionamento|fazenda|floresta|hospital|igreja|lago|lagoa|mata( nativa)?|praça|parque|parquinho|posto( de gasolina)?|riacho|rio|rodovi(á|a)ria|vila)$')
        self.re_20cf30ba = re.compile(r'^(?i)(?u)(alameda|avenida|beco|estrada|ladeira|rodovia|rotatória|rua|travessa|trevo|viela) .*')
        self.re_20fc5143 = re.compile(r'^(?i)Bairro\b')
        self.re_243f4993 = re.compile(r'^(\+55|0800)')
        self.re_280004fd = re.compile(r'^(Água|Arroio|Cabeceira|Córrego|Furo|Grota|Igarapé|Lajeado|Paraná|Restinga|Riacho|Ribeirão|Rio|Sanga)\b')
        self.re_292e0bb5 = re.compile(r'(?i)\b[0-9]+ ?m?\b')
        self.re_2cd1e949 = re.compile(r'^(?i)(?u)(Faz\.|Fazenda|Sítio|Chácara)')
        self.re_2dbaea13 = re.compile(r'^(?i)\bSAMU\b')
        self.re_2e8e4f2b = re.compile(r'(?i)google')
        self.re_2fcb6bab = re.compile(r'^(?i)ciclovia .*')
        self.re_2ffc377d = re.compile(r'.* D(a|e|o)s? .*')
        self.re_31732cd0 = re.compile(r'(?i)(?u)^(Brasilg(á|a)s|Consigaz|Copagaz|Liquig(á|a)s|Minasg(á|a)s|Nacional G(á|a)s|Supergasbras|Ultragaz)$')
        self.re_35bb0f2f = re.compile(r'^(?i)(?u)(auto(-| )?( moto )?escola|centro de formação de condutores|cfc|moto escola)\b')
        self.re_362f879f = re.compile(r'college|school')
        self.re_375e3de4 = re.compile(r'.*([A-Z]{2,3}-[0-9]{2,4}|SPM(-| )[0-9]{3} ?(D|E)?|SP(A|D|I)(-| )[0-9]{3}\/[0-9]{3}|[A-Z]{3}-[0-9]{3}\/[0-9]{3}).*')
        self.re_38a8f0ff = re.compile(r'^(?i)(?u)edifício.*')
        self.re_39d67968 = re.compile(r'^[a-z].*')
        self.re_3aeda39d = re.compile(r'hamlet|island|isolated_dwelling|neighbourhood|suburb|village')
        self.re_3b304b9b = re.compile(r'(?i)(?u)\b(Centro Paula Souza|Escola Técnica|ETEC)\b')
        self.re_3eb0ab44 = re.compile(r'clinic|doctors|hospital')
        self.re_408831d0 = re.compile(r'^(br|bR|Br)[0-9]{14}$')
        self.re_46ab4d8d = re.compile(r'^(?i)(?u)c(â|a)mara\b')
        self.re_4a8ca94e = re.compile(r'^(?i)(?u)praça.*')
        self.re_4bd3b925 = re.compile(r'^(?i)(?u)[a-z0-9]+_([a-z0-9]_?)+$')
        self.re_4cf86823 = re.compile(r'(?i)\bsaude\b')
        self.re_524288b6 = re.compile(r'^BR[0-9]{14}$')
        self.re_52ab3b8b = re.compile(r'^(?i)(?u)((Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF|hospital)$')
        self.re_53abc074 = re.compile(r'^(give_way|mini_roundabout|stop|turning_circle)$')
        self.re_568a42f4 = re.compile(r'\b[A-Z]{2,4} (- )?[0-9]{2,3}\b')
        self.re_57b8ef8e = re.compile(r'_[0-9]$')
        self.re_57bee688 = re.compile(r'^[0-9]{5}( |\.)[0-9]{3}$')
        self.re_5849be19 = re.compile(r'^(?i)(?u)(alameda|avenida|beco|estrada|ladeira|passarela|rodovia|rotatória|rua|travessa|trevo|viela|(anel|complexo|dispositivo) viário) .*')
        self.re_58f616c9 = re.compile(r'^(city_block|farm|hamlet|island|islet|isolated_dwelling|neighbourhood|square)$')
        self.re_591572a5 = re.compile(r'city|hamlet|isolated_dwelling|village')
        self.re_5ab76b11 = re.compile(r'^(clinic|doctors|hospital)$')
        self.re_5ac7053e = re.compile(r'^(1(a|b)?|[1-9][0-9]?)$')
        self.re_5cd37790 = re.compile(r'(?i)^motel\b')
        self.re_5d3348cb = re.compile(r'city|farm|neighbourhood|suburb|town|village')
        self.re_5ddbb7eb = re.compile(r'^[0-9]{2}\.[0-9]{3}\.[0-9]{3}\/[0-9]{4}-[0-9]{2}$')
        self.re_6024a566 = re.compile(r'(?i)^Aer(ódromo|oporto) de.*')
        self.re_604bb645 = re.compile(r'(?i)(?u)\b(Ale|BR|Esso|Ipiranga|Petrobr(á|a)s|Shell|Texaco)\b')
        self.re_60ad6838 = re.compile(r'^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Calçadão|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodoanel|Rodovia|Rotatória|Rótula|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*')
        self.re_6416be64 = re.compile(r'^(island|islet)$')
        self.re_64387998 = re.compile(r'^(?i)Bairro d(a|e|o)s?\b')
        self.re_6566db6a = re.compile(r'(?i).*heliport$')
        self.re_65710fdb = re.compile(r'(?i)(?u)((sem (denomina(ç|c)(ã|a)o|nome|sa(i|í)da))|desconhecido|n(ã|a)o conhecido)')
        self.re_667ce569 = re.compile(r'^(?i)(?u)((via de )?(acesso|ligação)(( (a|à))? propriedade)?|entrada|entroncamento|rampa|retorno|rotat(ó|o)ria|r(ó|o)tula|sa(í|i)da|trevo|estrada( municipal| de terra)?|rua|rodovia|via)( (de acesso|sem nome|projetad(a|o)))?$')
        self.re_67c67cf2 = re.compile(r'^[0-9]+0$')
        self.re_6b6e390d = re.compile(r'(Alameda|Avenida|Rua|Travessa|Viela) .*')
        self.re_6bf570a0 = re.compile(r'^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Calçadão|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodovia|Rotatória|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*')
        self.re_6c0d6e9e = re.compile(r'school|university')
        self.re_6e34cd0f = re.compile(r'(?i)\bcoreto\b')
        self.re_6efb8049 = re.compile(r'(?i).*airport$')
        self.re_72d45155 = re.compile(r'route|street')
        self.re_7633bf4e = re.compile(r'Rodovia ([A-Z]{2,3}-[0-9]{2,4})')
        self.re_793b22ec = re.compile(r'^(?i)(?u)c((â|a)me|ama)ra\b')
        self.re_7a246e93 = re.compile(r'^(100|18{0,1}|19[0-9])$')
        self.re_7a5b2736 = re.compile(r'\.')
        self.re_7afc6883 = re.compile(r'^[A-Z]{4}$')
        self.re_7b7c453d = re.compile(r'^(?i)(?u)(AM(A|E)|(Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF).*')
        self.re_7ec1fb9a = re.compile(r'(?i)^prefeitura\b')
        self.re_7f53e992 = re.compile(r'^(?i)(?u)(campo|est(á|a)dio|gin(á|a)sio|quadra)( de (futebol|esportes?))?$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *["addr:street"]["addr:street"!~/^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Calçadão|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodovia|Rotatória|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*/][inside("BR")]
        if (u'addr:street' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'addr:street') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_6bf570a0, u'^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Calçadão|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodovia|Rotatória|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*'), mapcss._tag_capture(capture_tags, 1, tags, u'addr:street')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} com logradouro ausente, errado ou abreviado","{0.key}")
                err.append({'class': 9018002, 'subclass': 279840772, 'text': mapcss.tr(u'{0} com logradouro ausente, errado ou abreviado', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[!highway][route!=road][!public_transport][type!~/route|street/][name][name=~/^(?i)(?u)(alameda|avenida|beco|estrada|ladeira|passarela|rodovia|rotatória|rua|travessa|trevo|viela|(anel|complexo|dispositivo) viário) .*/][name!~/^(?i)estrada de ferro/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'route') != mapcss._value_const_capture(capture_tags, 1, u'road', u'road') and not mapcss._tag_capture(capture_tags, 2, tags, u'public_transport') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_72d45155, u'route|street'), mapcss._tag_capture(capture_tags, 3, tags, u'type')) and mapcss._tag_capture(capture_tags, 4, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 5, self.re_5849be19), mapcss._tag_capture(capture_tags, 5, tags, u'name')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 6, self.re_15690541, u'^(?i)estrada de ferro'), mapcss._tag_capture(capture_tags, 6, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("objeto com nome de via mas sem tag de {0}","{0.key}")
                err.append({'class': 9018002, 'subclass': 535280341, 'text': mapcss.tr(u'objeto com nome de via mas sem tag de {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name=~/^(?i)(?u)[a-z0-9]+_([a-z0-9]_?)+$/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_4bd3b925), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("utilizar espaço ao invés de underscore")
                err.append({'class': 9018002, 'subclass': 1476954926, 'text': mapcss.tr(u'utilizar espaço ao invés de underscore')})

        # *[name=~/(?i)(^|.* )(Cel|Cmte|Cond|Conj|Dª|Dr|Eng|Gov|Hab|Jd|Jr|Marg|Mun|p\/|Pde|Pe|Pq|Pst|Pref|Profa|Profª|Prof|Res|s\/|Sr(a|ª)?|Sta|Sto|Ver)\.? .*/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_178f5446), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("palavra abreviada em {0}","{0.key}")
                err.append({'class': 9018003, 'subclass': 749019091, 'text': mapcss.tr(u'palavra abreviada em {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[leisure][name=~/^(?i)(?u)(campo|est(á|a)dio|gin(á|a)sio|quadra)( de (futebol|esportes?))?$/][inside("BR")]
        if (u'leisure' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7f53e992), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("nome supérfluo/incompleto de local de lazer")
                err.append({'class': 9018004, 'subclass': 1485441713, 'text': mapcss.tr(u'nome supérfluo/incompleto de local de lazer')})

        # *[name=~/^(?i)(?u)((Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF|hospital)$/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_52ab3b8b), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("nome supérfluo/incompleto de local de saúde")
                err.append({'class': 9018005, 'subclass': 1497769259, 'text': mapcss.tr(u'nome supérfluo/incompleto de local de saúde')})

        # *[amenity=~/^(clinic|doctors|hospital)$/][name=~/(?i)\bsaude\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5ab76b11), mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_4cf86823), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("erro de ortografia em ''saúde''")
                err.append({'class': 9018002, 'subclass': 1962359328, 'text': mapcss.tr(u'erro de ortografia em \'\'saúde\'\'')})

        # *[place=farm][name^="Sitio "][inside("BR")]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'farm') and mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, u'name'), mapcss._value_capture(capture_tags, 1, u'Sitio ')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("faltando acento em ''Sítio''")
                err.append({'class': 9018002, 'subclass': 653860263, 'text': mapcss.tr(u'faltando acento em \'\'Sítio\'\'')})

        # *[name=~/^(?i)(?u)(aldeia|borrach(aria|eiro)|bosque|capela|cemit(é|e)rio|c(ó|o)rrego|escola|estacionamento|fazenda|floresta|hospital|igreja|lago|lagoa|mata( nativa)?|praça|parque|parquinho|posto( de gasolina)?|riacho|rio|rodovi(á|a)ria|vila)$/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_20c7dd98), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("local com nome supérfluo, incompleto ou descritivo")
                err.append({'class': 9018002, 'subclass': 1104230922, 'text': mapcss.tr(u'local com nome supérfluo, incompleto ou descritivo')})

        # *[amenity=parking][name=~/(?i)^Estacionamento /][inside("BR")]
        # Rule Blacklisted

        # *[designation=*"addr:housename"][inside("BR")]
        # *[ref=*designation][inside("BR")]
        # *[ref=*old_ref][inside("BR")]
        # *[name=*"addr:housename"][inside("BR")]
        # *[name=*designation][inside("BR")]
        # *[name=*alt_name][inside("BR")]
        # *[name=*int_name][inside("BR")]
        # *[name=*loc_name][inside("BR")]
        # *[name=*nat_name][inside("BR")]
        # *[name=*official_name][inside("BR")]
        # *[name=*old_name][inside("BR")]
        # *[name=*reg_name][inside("BR")]
        # *[name=*short_name][inside("BR")]
        # *[name=*sorting_name][inside("BR")]
        if (u'designation' in keys) or (u'name' in keys) or (u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'designation') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'addr:housename')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'designation')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'old_ref')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'addr:housename')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'designation')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'alt_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'int_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'loc_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'nat_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'official_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'old_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'reg_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'short_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'sorting_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("{0} e {1} são iguais; remover chave {1} desnecessária","{0.key}","{0.value}")
                # fixRemove:"{0.value}"
                err.append({'class': 9018006, 'subclass': 2003922, 'text': mapcss.tr(u'{0} e {1} são iguais; remover chave {1} desnecessária', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.value}')])
                }})

        # *[source=*name][inside("BR")]
        if (u'source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} e {1} são iguais","{0.key}","{0.value}")
                err.append({'class': 9018002, 'subclass': 470146003, 'text': mapcss.tr(u'{0} e {1} são iguais', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[name=~/(?i)(?u)((sem (denomina(ç|c)(ã|a)o|nome|sa(i|í)da))|desconhecido|n(ã|a)o conhecido)/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_65710fdb), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto com nomenclatura incorreta")
                # suggestAlternative:"noname"
                err.append({'class': 9018007, 'subclass': 1272098213, 'text': mapcss.tr(u'objeto com nomenclatura incorreta')})

        # node[maxheight][barrier!=height_restrictor][!traffic_sign][inside("BR")]
        # node[maxspeed][highway!=speed_camera][!traffic_sign][inside("BR")]
        if (u'maxheight' in keys) or (u'maxspeed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxheight') and mapcss._tag_capture(capture_tags, 1, tags, u'barrier') != mapcss._value_const_capture(capture_tags, 1, u'height_restrictor', u'height_restrictor') and not mapcss._tag_capture(capture_tags, 2, tags, u'traffic_sign') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') != mapcss._value_const_capture(capture_tags, 1, u'speed_camera', u'speed_camera') and not mapcss._tag_capture(capture_tags, 2, tags, u'traffic_sign') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} não deve ser utilizado em nó; utilizar a restrição na via","{0.key}")
                err.append({'class': 9018008, 'subclass': 427326608, 'text': mapcss.tr(u'{0} não deve ser utilizado em nó; utilizar a restrição na via', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # node[noname?][inside("BR")]
        if (u'noname' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'noname') in ('yes', 'true', '1') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("uso suspeito de {0} em nó","{0.key}")
                err.append({'class': 9018002, 'subclass': 1940682714, 'text': mapcss.tr(u'uso suspeito de {0} em nó', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[designation][inside("BR")]
        if (u'designation' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'designation') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} é uma chave utilizada apenas no Reino Unido","{0.key}")
                # suggestAlternative:"description"
                # suggestAlternative:"name"
                err.append({'class': 9018009, 'subclass': 1818234763, 'text': mapcss.tr(u'{0} é uma chave utilizada apenas no Reino Unido', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # node[highway=motorway_junction][!name][!ref][inside("BR")]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'motorway_junction') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and not mapcss._tag_capture(capture_tags, 2, tags, u'ref') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} sem pelo menos uma das tags: {1} ou {2}","{0.value}","{1.key}","{2.key}")
                err.append({'class': 9018010, 'subclass': 1629006877, 'text': mapcss.tr(u'{0} sem pelo menos uma das tags: {1} ou {2}', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[place=~/hamlet|isolated_dwelling|town|village/][population>=100000][inside("BR")]
        if (u'place' in keys and u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_152c10ee), mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'population') >= mapcss._value_capture(capture_tags, 1, 100000) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("local com 100.000 habitantes ou mais deve ser classificado como city")
                # fixAdd:"place=city"
                err.append({'class': 9018006, 'subclass': 1009134521, 'text': mapcss.tr(u'local com 100.000 habitantes ou mais deve ser classificado como city'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'place',u'city']])
                }})

        # *[place=~/city|hamlet|isolated_dwelling|village/][population>=10000][population<100000][inside("BR")]
        if (u'place' in keys and u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_591572a5), mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'population') >= mapcss._value_capture(capture_tags, 1, 10000) and mapcss._tag_capture(capture_tags, 2, tags, u'population') < mapcss._value_capture(capture_tags, 2, 100000) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("local com população entre 10.000 e 100.000 deve ser classificado como town")
                # fixAdd:"place=town"
                err.append({'class': 9018006, 'subclass': 1343568198, 'text': mapcss.tr(u'local com população entre 10.000 e 100.000 deve ser classificado como town'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'place',u'town']])
                }})

        # *[place][place!~/hamlet|island|isolated_dwelling|neighbourhood|suburb|village/][population<10000][inside("BR")]
        if (u'place' in keys and u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_3aeda39d, u'hamlet|island|isolated_dwelling|neighbourhood|suburb|village'), mapcss._tag_capture(capture_tags, 1, tags, u'place')) and mapcss._tag_capture(capture_tags, 2, tags, u'population') < mapcss._value_capture(capture_tags, 2, 10000) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("local com menos de 10.000 habitantes deve ser classificado como village")
                # fixAdd:"place=village"
                err.append({'class': 9018006, 'subclass': 409005616, 'text': mapcss.tr(u'local com menos de 10.000 habitantes deve ser classificado como village'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'place',u'village']])
                }})

        # *[place=city][!population][inside("BR")]
        # *[place=town][!population][inside("BR")]
        # *[place=village][!population][inside("BR")]
        # Rule Blacklisted

        # *[place=city][!name][inside("BR")]
        # *[place=town][!name][inside("BR")]
        # *[place=village][!name][inside("BR")]
        if (u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'city') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'town') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'village') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} sem nome","{0.value}")
                err.append({'class': 9018012, 'subclass': 1473808194, 'text': mapcss.tr(u'{0} sem nome', mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # node[place=~/village|town|city/]["addr:city"=*name][inside("BR")]
        # node[place=suburb]["addr:suburb"=*name][inside("BR")]
        if (u'addr:city' in keys and u'place' in keys) or (u'addr:suburb' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_0db5b64e), mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'addr:city') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'suburb') and mapcss._tag_capture(capture_tags, 1, tags, u'addr:suburb') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwError:tr("não deve possuir {0}","{1.key}")
                # fixRemove:"{1.key}"
                err.append({'class': 9018006, 'subclass': 992485850, 'text': mapcss.tr(u'não deve possuir {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{1.key}')])
                }})

        # *["addr:city"=~/(,|( |-) ?[A-Z]{2})/][inside("BR")]
        if (u'addr:city' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_10f1c360), mapcss._tag_capture(capture_tags, 0, tags, u'addr:city')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve conter apenas o nome da cidade","{0.key}")
                err.append({'class': 9018013, 'subclass': 1479274467, 'text': mapcss.tr(u'{0} deve conter apenas o nome da cidade', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name=~/^(?i)(?u)(Faz\.|Fazenda|Sítio|Chácara)/][place][place!~/city|farm|neighbourhood|suburb|town|village/][inside("BR")]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2cd1e949), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'place') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_5d3348cb, u'city|farm|neighbourhood|suburb|town|village'), mapcss._tag_capture(capture_tags, 2, tags, u'place')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("objeto talvez deva ser {0}=farm","{1.key}")
                err.append({'class': 9018002, 'subclass': 337742963, 'text': mapcss.tr(u'objeto talvez deva ser {0}=farm', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[place][name=~/^(?i)Bairro\b/][name!~/^(?i)Bairro d(a|e|o)s?\b/][inside("BR")]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_20fc5143), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_64387998, u'^(?i)Bairro d(a|e|o)s?\b'), mapcss._tag_capture(capture_tags, 2, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("objeto talvez não deva ter ''Bairro'' no nome")
                err.append({'class': 9018002, 'subclass': 1441242115, 'text': mapcss.tr(u'objeto talvez não deva ter \'\'Bairro\'\' no nome')})

        # node[place=~/^(island|islet)$/][inside("BR")]
        if (u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_6416be64), mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("representar a ilha, se possível, como uma área")
                err.append({'class': 9018002, 'subclass': 820669758, 'text': mapcss.tr(u'representar a ilha, se possível, como uma área')})

        # *[iata="0"][inside("BR")]
        if (u'iata' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'iata') == mapcss._value_capture(capture_tags, 0, u'0') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} com valor = {1}","{0.key}","{0.value}")
                err.append({'class': 9018014, 'subclass': 1098244333, 'text': mapcss.tr(u'{0} com valor = {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[amenity=~/college|school/][name=~/^(?i)(?u)(Centro Universitário|Faculdades?|FATEC|Instituto Federal)\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_362f879f), mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1d232d4c), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("estabelecimento de ensino classificado incorretamente")
                # suggestAlternative:"amenity=university"
                # fixAdd:"{0.key}=university"
                err.append({'class': 9018006, 'subclass': 1605707172, 'text': mapcss.tr(u'estabelecimento de ensino classificado incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=university')).split('=', 1)])
                }})

        # *[amenity=school][name=~/^(?i)(?u)(SENAC|SENAI|Serviço Nacional de Aprendizagem)/][inside("BR")]
        # *[amenity=~/school|university/][name=~/(?i)(?u)\b(Centro Paula Souza|Escola Técnica|ETEC)\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'school') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_044c8944), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_6c0d6e9e), mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3b304b9b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("estabelecimento de ensino classificado incorretamente")
                # suggestAlternative:"amenity=college"
                # fixAdd:"{0.key}=college"
                err.append({'class': 9018006, 'subclass': 1282773099, 'text': mapcss.tr(u'estabelecimento de ensino classificado incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=college')).split('=', 1)])
                }})

        # *[amenity=school][name=~/^(?i)(?u)(auto(-| )?( moto )?escola|centro de formação de condutores|cfc|moto escola)\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'school') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_35bb0f2f), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("autoescola classificada incorretamente")
                # suggestAlternative:"amenity=driving_school"
                # fixAdd:"{0.key}=driving_school"
                err.append({'class': 9018006, 'subclass': 566309924, 'text': mapcss.tr(u'autoescola classificada incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=driving_school')).split('=', 1)])
                }})

        # *[amenity=school][name=~/^(?i)creche\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'school') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_160d1bfc), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("creche classificada incorretamente")
                # suggestAlternative:"amenity=kindergarten"
                # fixAdd:"{0.key}=kindergarten"
                err.append({'class': 9018006, 'subclass': 1847987722, 'text': mapcss.tr(u'creche classificada incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=kindergarten')).split('=', 1)])
                }})

        # *[name=~/^(?i)(?u)Subestação .*/][power][power!=substation][inside("BR")]
        # *[name=~/^(?i)(?u)Fórum .*/][amenity][amenity!=courthouse][inside("BR")]
        # *[name=~/^(?i)Hospital .*/][building][building!=hospital][inside("BR")]
        # *[name=~/^(?i)Universidade .*/][building][building!=university][inside("BR")]
        # *[name=~/^(?i)Escola .*/][building][building!=school][inside("BR")]
        # *[name=~/^(?i)Hotel .*/][building][building!=hotel][inside("BR")]
        # *[name=~/^(?i)Capela .*/][building][building!=chapel][inside("BR")]
        # *[name=~/^(?i)Igreja .*/][building][building!=church][inside("BR")]
        # *[name=~/^(?i)Catedral .*/][building][building!=cathedral][inside("BR")]
        # *[name=~/^(?i)Fazenda .*/][building][building!=farm][inside("BR")]
        # *[name=~/^(?i)Supermercado .*/][building][building!=supermarket][inside("BR")]
        # Rule Blacklisted

        # *[name=~/^(?i)(?u)(AM(A|E)|(Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF).*/][amenity=hospital][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7b7c453d), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') == mapcss._value_capture(capture_tags, 1, u'hospital') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("postos/unidades de saúde devem ser amenity=clinic")
                # fixAdd:"amenity=clinic"
                err.append({'class': 9018006, 'subclass': 74419437, 'text': mapcss.tr(u'postos/unidades de saúde devem ser amenity=clinic'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'clinic']])
                }})

        # *[name=~/^(?i)\bSAMU\b/][amenity=~/clinic|doctors|hospital/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2dbaea13), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3eb0ab44), mapcss._tag_capture(capture_tags, 1, tags, u'amenity')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("SAMU classificado de forma errada")
                # suggestAlternative:"emergency=ambulance_station"
                err.append({'class': 9018016, 'subclass': 392029310, 'text': mapcss.tr(u'SAMU classificado de forma errada')})

        # node[highway=~/^(give_way|mini_roundabout|stop|turning_circle)$/][name][inside("BR")]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_53abc074), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto não deve possuir {0}","{1.key}")
                err.append({'class': 9018017, 'subclass': 1025728334, 'text': mapcss.tr(u'objeto não deve possuir {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # node[highway=speed_camera][!maxspeed][inside("BR")]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'speed_camera') and not mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("adicionar {0} ao {1}","{1.key}","{0.tag}")
                err.append({'class': 9018018, 'subclass': 1228671542, 'text': mapcss.tr(u'adicionar {0} ao {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[crossing][!highway][!railway][inside("BR")]
        if (u'crossing' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'crossing') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve ser utilizado com {1}={0} ou {2}={0}","{0.key}","{1.key}","{2.key}")
                err.append({'class': 9018019, 'subclass': 2098306424, 'text': mapcss.tr(u'{0} deve ser utilizado com {1}={0} ou {2}={0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[aeroway][designation=~/^[A-Z]{4}$/][!icao][inside("BR")]
        # *[aeroway][ref=~/^[A-Z]{4}$/][!icao][inside("BR")]
        if (u'aeroway' in keys and u'designation' in keys) or (u'aeroway' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7afc6883), mapcss._tag_capture(capture_tags, 1, tags, u'designation')) and not mapcss._tag_capture(capture_tags, 2, tags, u'icao') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7afc6883), mapcss._tag_capture(capture_tags, 1, tags, u'ref')) and not mapcss._tag_capture(capture_tags, 2, tags, u'icao') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("{0} provavelmente deve ser utilizado como {1}","{1.key}","{2.key}")
                # fixChangeKey:"{1.key} => {2.key}"
                err.append({'class': 9018006, 'subclass': 619372172, 'text': mapcss.tr(u'{0} provavelmente deve ser utilizado como {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, u'{1.key} => {2.key}')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, u'{1.key} => {2.key}')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, u'{1.key} => {2.key}')).split('=>', 1)[0].strip()])
                }})

        # *[access=permissive][inside("BR")]
        if (u'access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'permissive') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} deve ser utilizado apenas em vias privadas com permissão de acesso e não em vias de acesso público","{0.tag}")
                err.append({'class': 9018002, 'subclass': 1240816112, 'text': mapcss.tr(u'{0} deve ser utilizado apenas em vias privadas com permissão de acesso e não em vias de acesso público', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[name=~/^(?U)(\p{Upper}| )+$/][inside("BR")]
        # *["addr:street"=~/^(?U)(\p{Upper}| )+$/][inside("BR")]
        # Rule Blacklisted

        # *["addr:postcode"=~/^[0-9]{8}$/][inside("BR")]
        # Rule Blacklisted

        # *[postal_code=~/^[0-9]{8}$/][inside("BR")]
        # Rule Blacklisted

        # *["addr:postcode"=~/^[0-9]{5}( |\.)[0-9]{3}$/][inside("BR")]
        if (u'addr:postcode' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_57bee688), mapcss._tag_capture(capture_tags, 0, tags, u'addr:postcode')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("formato do CEP pode ser melhorado")
                # fixAdd:concat("addr:postcode=",replace(replace(tag("addr:postcode")," ","-"),".","-"))
                err.append({'class': 9018006, 'subclass': 1667206075, 'text': mapcss.tr(u'formato do CEP pode ser melhorado'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'addr:postcode=', mapcss.replace(mapcss.replace(mapcss.tag(tags, u'addr:postcode'), u' ', u'-'), u'.', u'-'))).split('=', 1)])
                }})

        # *["postal_code"=~/^[0-9]{5}( |\.)[0-9]{3}$/][inside("BR")]
        if (u'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_57bee688), mapcss._tag_capture(capture_tags, 0, tags, u'postal_code')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("formato do CEP pode ser melhorado")
                # fixAdd:concat("postal_code=",replace(replace(tag("postal_code")," ","-"),".","-"))
                err.append({'class': 9018006, 'subclass': 1977906896, 'text': mapcss.tr(u'formato do CEP pode ser melhorado'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'postal_code=', mapcss.replace(mapcss.replace(mapcss.tag(tags, u'postal_code'), u' ', u'-'), u'.', u'-'))).split('=', 1)])
                }})

        # *["addr:postcode"]["addr:postcode"!~/^[0-9]{5}-[0-9]{3}$/][inside("BR")]
        # *[postal_code][postal_code!~/^[0-9]{5}-[0-9]{3}$/][inside("BR")]
        # Rule Blacklisted

        # *[alt_source][source][inside("BR")]
        if (u'alt_source' in keys and u'source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'alt_source') and mapcss._tag_capture(capture_tags, 1, tags, u'source') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve estar incluído em {1}, separado por '';'' caso necessário","{0.key}","{1.key}")
                err.append({'class': 9018020, 'subclass': 472956812, 'text': mapcss.tr(u'{0} deve estar incluído em {1}, separado por \'\';\'\' caso necessário', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[landuse?][inside("BR")]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') in ('yes', 'true', '1') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("especificar valor correto para {0} ao invés de ''{1}''","{0.key}",tag("landuse"))
                err.append({'class': 9018021, 'subclass': 6418462, 'text': mapcss.tr(u'especificar valor correto para {0} ao invés de \'\'{1}\'\'', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss.tag(tags, u'landuse'))})

        # *[long_name][inside("BR")]
        if (u'long_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'long_name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("chave inválida: {0}","{0.key}")
                # suggestAlternative:"alt_name"
                # suggestAlternative:"name"
                # suggestAlternative:"official_name"
                err.append({'class': 9018022, 'subclass': 1737555221, 'text': mapcss.tr(u'chave inválida: {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *["building:levels"<1][inside("BR")]
        if (u'building:levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:levels') < mapcss._value_capture(capture_tags, 0, 1) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} com valor inválido","{0.key}")
                err.append({'class': 9018002, 'subclass': 775859422, 'text': mapcss.tr(u'{0} com valor inválido', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[hires?][inside("BR")]
        if (u'hires' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'hires') in ('yes', 'true', '1') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("não se deve utilizar {0} para demarcar áreas de cobertura de imagem","{0.key}")
                err.append({'class': 9018023, 'subclass': 895278192, 'text': mapcss.tr(u'não se deve utilizar {0} para demarcar áreas de cobertura de imagem', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # node[man_made=tower]["tower:type"=lighting][inside("BR")]
        if (u'man_made' in keys and u'tower:type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == mapcss._value_capture(capture_tags, 0, u'tower') and mapcss._tag_capture(capture_tags, 1, tags, u'tower:type') == mapcss._value_capture(capture_tags, 1, u'lighting') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("uso incorreto de {0}","{0.tag}")
                # suggestAlternative:"man_made=mast"
                # fixAdd:"man_made=mast"
                err.append({'class': 9018064, 'subclass': 865785, 'text': mapcss.tr(u'uso incorreto de {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'man_made',u'mast']])
                }})

        # *[tourism=motel][amenity!=love_hotel][inside("BR")]
        # *[name=~/(?i)\bmotel\b/][amenity!=love_hotel][inside("BR")]
        if (u'name' in keys) or (u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == mapcss._value_capture(capture_tags, 0, u'motel') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'love_hotel', u'love_hotel') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_01454d46), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'love_hotel', u'love_hotel') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("ausência de tag ''{0}''","{1.value}")
                # fixAdd:"{1.key}={1.value}"
                err.append({'class': 9018006, 'subclass': 1987370859, 'text': mapcss.tr(u'ausência de tag \'\'{0}\'\'', mapcss._tag_uncapture(capture_tags, u'{1.value}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{1.key}={1.value}')).split('=', 1)])
                }})

        # *[amenity=love_hotel][tourism][tourism!=motel][inside("BR")]
        if (u'amenity' in keys and u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'love_hotel') and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') and mapcss._tag_capture(capture_tags, 2, tags, u'tourism') != mapcss._value_const_capture(capture_tags, 2, u'motel', u'motel') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("provavelmente deve ser ''{0}={1}''","{2.key}","{2.value}")
                err.append({'class': 9018002, 'subclass': 1760828878, 'text': mapcss.tr(u'provavelmente deve ser \'\'{0}={1}\'\'', mapcss._tag_uncapture(capture_tags, u'{2.key}'), mapcss._tag_uncapture(capture_tags, u'{2.value}'))})

        # *[name=~/(?i)^motel\b/][tourism!=motel][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5cd37790), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') != mapcss._value_const_capture(capture_tags, 1, u'motel', u'motel') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("motel classificado incorretamente")
                # suggestAlternative:"tourism=motel"
                err.append({'class': 9018002, 'subclass': 1456128106, 'text': mapcss.tr(u'motel classificado incorretamente')})

        # *[aeroway=aerodrome][name=~/(?i).*airport$/][inside("BR")]
        # *[aeroway=helipad][name=~/(?i).*heliport$/][inside("BR")]
        if (u'aeroway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'aerodrome') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6efb8049), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'helipad') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6566db6a), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} com nome em inglês","{0.tag}")
                err.append({'class': 9018002, 'subclass': 1743601177, 'text': mapcss.tr(u'{0} com nome em inglês', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[aeroway=aerodrome][name=~/(?i)^Aer(ódromo|oporto) de.*/][inside("BR")]
        # *[aeroway=helipad][name=~/(?i)^Helipo(n|r)to.*/][inside("BR")]
        if (u'aeroway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'aerodrome') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6024a566), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'helipad') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_139e342b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("conferir se existe nome oficial do {0}","{0.value}")
                err.append({'class': 9018002, 'subclass': 136467214, 'text': mapcss.tr(u'conferir se existe nome oficial do {0}', mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[aeroway=aerodrome][ref][inside("BR")]
        if (u'aeroway' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'aerodrome') and mapcss._tag_capture(capture_tags, 1, tags, u'ref') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("''{0}'' não faz sentido em aeroporto","{1.key}")
                err.append({'class': 9018002, 'subclass': 1633437696, 'text': mapcss.tr(u'\'\'{0}\'\' não faz sentido em aeroporto', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # node[surface][!traffic_calming][inside("BR")]
        # Rule Blacklisted

        # *[waterway][layer<0][!tunnel][inside("BR")]
        if (u'layer' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'layer') < mapcss._value_capture(capture_tags, 1, 0) and not mapcss._tag_capture(capture_tags, 2, tags, u'tunnel') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} negativo de {1} com ausência de {2}","{1.key}","{0.key}","{2.key}")
                err.append({'class': 9018002, 'subclass': 203420779, 'text': mapcss.tr(u'{0} negativo de {1} com ausência de {2}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[waterway][layer>0][!bridge][inside("BR")]
        if (u'layer' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'layer') > mapcss._value_capture(capture_tags, 1, 0) and not mapcss._tag_capture(capture_tags, 2, tags, u'bridge') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} positivo de {1} com ausência de {2}","{1.key}","{0.key}","{2.key}")
                err.append({'class': 9018002, 'subclass': 1870051659, 'text': mapcss.tr(u'{0} positivo de {1} com ausência de {2}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[layer][!building][!highway][man_made!=pipeline][!railway][!waterway][power!=line][inside("BR")]
        # Rule Blacklisted

        # *[name=~/^(?i)(?u)edifício.*/][!building][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_38a8f0ff), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("possível ausência de tag {0}","{1.key}")
                err.append({'class': 9018026, 'subclass': 1332986859, 'text': mapcss.tr(u'possível ausência de tag {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[route=ferry][!duration][inside("BR")]
        if (u'route' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'route') == mapcss._value_capture(capture_tags, 0, u'ferry') and not mapcss._tag_capture(capture_tags, 1, tags, u'duration') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("ausência do tempo de duração ({0}) da balsa","{1.key}")
                err.append({'class': 9018027, 'subclass': 1343391603, 'text': mapcss.tr(u'ausência do tempo de duração ({0}) da balsa', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[name=~/^(?i)(?u)praça.*/][!leisure][landuse=~/^(forest|grass|greenfield|meadow|orchard)$/][inside("BR")]
        # *[name=~/^(?i)(?u)praça.*/][!leisure][natural=~/^(grassland|heath|scrub|wood)$/][inside("BR")]
        if (u'landuse' in keys and u'name' in keys) or (u'name' in keys and u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_4a8ca94e), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'leisure') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_05a345c7), mapcss._tag_capture(capture_tags, 2, tags, u'landuse')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_4a8ca94e), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'leisure') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_12b48afb), mapcss._tag_capture(capture_tags, 2, tags, u'natural')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("possível definição incorreta para praça: ''{0}''","{2.key}")
                # suggestAlternative:"leisure=park"
                err.append({'class': 9018029, 'subclass': 181066872, 'text': mapcss.tr(u'possível definição incorreta para praça: \'\'{0}\'\'', mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[wikipedia][wikipedia!~/^pt:/][inside("BR")]
        if (u'wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_17fd35b3, u'^pt:'), mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("utilizar prefixo em português (pt:) para {0}","{0.key}")
                err.append({'class': 9018030, 'subclass': 1431112366, 'text': mapcss.tr(u'utilizar prefixo em português (pt:) para {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name=~/.*\(.*\).*/][inside("BR")]
        # Rule Blacklisted

        # *[name=~/ - /][inside("BR")]
        # Rule Blacklisted

        # *[name=~/, /][inside("BR")]
        # Rule Blacklisted

        # *[name=~/: /][inside("BR")]
        # Rule Blacklisted

        # *[name=~/ ou /][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_131cc885), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("nome utilizado de forma incorreta")
                # suggestAlternative:"name e alt_name"
                err.append({'class': 9018031, 'subclass': 115703372, 'text': mapcss.tr(u'nome utilizado de forma incorreta')})

        # node[admin_level][!capital][inside("BR")]
        # node[border_type][inside("BR")]
        # node[boundary][inside("BR")]
        # node[type=boundary][inside("BR")]
        if (u'admin_level' in keys) or (u'border_type' in keys) or (u'boundary' in keys) or (u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'admin_level') and not mapcss._tag_capture(capture_tags, 1, tags, u'capital') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'border_type') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'boundary') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("nó não deve possuir {0}","{0.tag}")
                err.append({'class': 9018032, 'subclass': 90903508, 'text': mapcss.tr(u'nó não deve possuir {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[boundary=national_park][!name][inside("BR")]
        # *[boundary=protected_area][!name][inside("BR")]
        # *[leisure=nature_reserve][!name][inside("BR")]
        if (u'boundary' in keys) or (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'national_park') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'protected_area') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'nature_reserve') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
                err.append({'class': 9018033, 'subclass': 1196875584, 'text': mapcss.tr(u'{0} deve possuir {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[boundary=protected_area][!protect_class][inside("BR")]
        if (u'boundary' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'protected_area') and not mapcss._tag_capture(capture_tags, 1, tags, u'protect_class') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
                err.append({'class': 9018033, 'subclass': 1593244126, 'text': mapcss.tr(u'{0} deve possuir {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[protect_class][protect_class!~/^(1(a|b)?|[1-9][0-9]?)$/][inside("BR")]
        if (u'protect_class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'protect_class') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_5ac7053e, u'^(1(a|b)?|[1-9][0-9]?)$'), mapcss._tag_capture(capture_tags, 1, tags, u'protect_class')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("valor incorreto para {0}","{0.key}")
                err.append({'class': 9018034, 'subclass': 1183781531, 'text': mapcss.tr(u'valor incorreto para {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[protect_class][boundary!=protected_area][inside("BR")]
        if (u'protect_class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'protect_class') and mapcss._tag_capture(capture_tags, 1, tags, u'boundary') != mapcss._value_const_capture(capture_tags, 1, u'protected_area', u'protected_area') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("ausência de boundary=protected_area")
                err.append({'class': 9018035, 'subclass': 1649283274, 'text': mapcss.tr(u'ausência de boundary=protected_area')})

        # node[destination][inside("BR")]
        if (u'destination' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'destination') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve ser usado apenas em ways","{0.key}")
                err.append({'class': 9018036, 'subclass': 878235238, 'text': mapcss.tr(u'{0} deve ser usado apenas em ways', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # node[exit_to][inside("BR")]
        if (u'exit_to' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'exit_to') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("utilize ''destination'' no caminho de saída ao invés de ''exit_to''")
                err.append({'class': 9018037, 'subclass': 1738747667, 'text': mapcss.tr(u'utilize \'\'destination\'\' no caminho de saída ao invés de \'\'exit_to\'\'')})

        # node[highway=motorway_junction][ref][ref!~/^[0-9]+( |-)*([A-Z])?$/][inside("BR")]
        if (u'highway' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'motorway_junction') and mapcss._tag_capture(capture_tags, 1, tags, u'ref') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_20188fb1, u'^[0-9]+( |-)*([A-Z])?$'), mapcss._tag_capture(capture_tags, 2, tags, u'ref')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("saída de rodovia ({0}) fora do padrão","{1.key}")
                err.append({'class': 9018002, 'subclass': 1001734093, 'text': mapcss.tr(u'saída de rodovia ({0}) fora do padrão', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # node[highway=motorway_junction][name][inside("BR")]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'motorway_junction') and mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} geralmente não possui nome; use ''destination'' no caminho de saída","{0.tag}")
                err.append({'class': 9018002, 'subclass': 625356625, 'text': mapcss.tr(u'{0} geralmente não possui nome; use \'\'destination\'\' no caminho de saída', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # node[junction][inside("BR")]
        if (u'junction' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'junction') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("junção ({0}) em um nó","{0.value}")
                # suggestAlternative:"highway=mini_roundabout"
                # suggestAlternative:"highway=turning_circle"
                err.append({'class': 9018002, 'subclass': 1621901547, 'text': mapcss.tr(u'junção ({0}) em um nó', mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[name=~/.* D(a|e|o)s? .*/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2ffc377d), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("''da'', ''de'' e ''do'' são minúsculos nos nomes em português")
                err.append({'class': 9018002, 'subclass': 874509528, 'text': mapcss.tr(u'\'\'da\'\', \'\'de\'\' e \'\'do\'\' são minúsculos nos nomes em português')})

        # *[name=~/^[a-z].*/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_39d67968), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("nome iniciando com letra minúscula")
                err.append({'class': 9018002, 'subclass': 2073274467, 'text': mapcss.tr(u'nome iniciando com letra minúscula')})

        # *[alt_ref][inside("BR")]
        if (u'alt_ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'alt_ref') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("o conteúdo de {0} deve fazer parte de ref, separado por ;","{0.key}")
                # suggestAlternative:"ref"
                err.append({'class': 9018039, 'subclass': 836388143, 'text': mapcss.tr(u'o conteúdo de {0} deve fazer parte de ref, separado por ;', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[surface][eval(number_of_tags())=1][inside("BR")]
        if (u'surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'surface') and len(tags) == 1 and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto incompleto: possui apenas {0}","{0.key}")
                err.append({'class': 9018041, 'subclass': 411244066, 'text': mapcss.tr(u'objeto incompleto: possui apenas {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name][surface][eval(number_of_tags())=2][inside("BR")]
        # *[name][website][eval(number_of_tags())=2][inside("BR")]
        if (u'name' in keys and u'surface' in keys) or (u'name' in keys and u'website' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'surface') and len(tags) == 2 and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'website') and len(tags) == 2 and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto incompleto: possui apenas {0} e {1}","{0.key}","{1.key}")
                err.append({'class': 9018042, 'subclass': 585137381, 'text': mapcss.tr(u'objeto incompleto: possui apenas {0} e {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # node[natural=peak][name=~/(?i)\b[0-9]+ ?m?\b/][inside("BR")]
        if (u'name' in keys and u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'natural') == mapcss._value_capture(capture_tags, 0, u'peak') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_292e0bb5), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("nome não deve conter a elevação do pico")
                # suggestAlternative:"ele"
                err.append({'class': 9018002, 'subclass': 907675189, 'text': mapcss.tr(u'nome não deve conter a elevação do pico')})

        # *[leisure=pitch][sport=tennis][surface=unpaved][inside("BR")]
        if (u'leisure' in keys and u'sport' in keys and u'surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'pitch') and mapcss._tag_capture(capture_tags, 1, tags, u'sport') == mapcss._value_capture(capture_tags, 1, u'tennis') and mapcss._tag_capture(capture_tags, 2, tags, u'surface') == mapcss._value_capture(capture_tags, 2, u'unpaved') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("{0} com superfície incorreta","{2.key}")
                # suggestAlternative:"surface=clay"
                # fixAdd:"surface=clay"
                err.append({'class': 9018006, 'subclass': 990400213, 'text': mapcss.tr(u'{0} com superfície incorreta', mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'surface',u'clay']])
                }})

        # *[amenity=fuel][name=~/(?i)(?u)\b(Ale|BR|Esso|Ipiranga|Petrobr(á|a)s|Shell|Texaco)\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'fuel') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_604bb645), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("o nome não deve conter a bandeira/marca do posto")
                # suggestAlternative:"brand"
                err.append({'class': 9018002, 'subclass': 1724035987, 'text': mapcss.tr(u'o nome não deve conter a bandeira/marca do posto')})

        # *[amenity=fuel][brand=BR][inside("BR")]
        if (u'amenity' in keys and u'brand' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'fuel') and mapcss._tag_capture(capture_tags, 1, tags, u'brand') == mapcss._value_capture(capture_tags, 1, u'BR') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("uso inconsistente de bandeira do posto")
                # suggestAlternative:"brand=Petrobras"
                # fixAdd:"brand=Petrobras"
                err.append({'class': 9018002, 'subclass': 435141543, 'text': mapcss.tr(u'uso inconsistente de bandeira do posto'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'brand',u'Petrobras']])
                }})

        # *[shop=gas][name=~/(?i)(?u)^(Brasilg(á|a)s|Consigaz|Copagaz|Liquig(á|a)s|Minasg(á|a)s|Nacional G(á|a)s|Supergasbras|Ultragaz)$/][inside("BR")]
        if (u'name' in keys and u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'gas') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_31732cd0), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("o nome não deve conter a bandeira/marca da loja")
                # suggestAlternative:"brand"
                err.append({'class': 9018002, 'subclass': 867102166, 'text': mapcss.tr(u'o nome não deve conter a bandeira/marca da loja')})

        # *[/_[0-9]$/][!"is_in:iso_3166_2"][inside("BR")]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_57b8ef8e) and not mapcss._tag_capture(capture_tags, 1, tags, u'is_in:iso_3166_2') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("chave inválida: {0}","{0.key}")
                err.append({'class': 9018022, 'subclass': 231229079, 'text': mapcss.tr(u'chave inválida: {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *["addr:housenumber"=~/(?i)^s(\.|-| )?\/?n\.?º?$/][!note][inside("BR")]
        if (u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_0b27200b), mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber')) and not mapcss._tag_capture(capture_tags, 1, tags, u'note') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("não utilizar ''{0}'' para locais sem número",tag("addr:housenumber"))
                # suggestAlternative:"note"
                # fixRemove:"addr:housenumber"
                # fixAdd:"note=Local sem número"
                err.append({'class': 9018006, 'subclass': 630415638, 'text': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', mapcss.tag(tags, u'addr:housenumber')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'note',u'Local sem número']]),
                    '-': ([
                    u'addr:housenumber'])
                }})

        # *["addr:housenumber"=~/(?i)^s(\.|-| )?\/?n\.?º?$/][note][inside("BR")]
        if (u'addr:housenumber' in keys and u'note' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_0b27200b), mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber')) and mapcss._tag_capture(capture_tags, 1, tags, u'note') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("não utilizar ''{0}'' para locais sem número",tag("addr:housenumber"))
                # suggestAlternative:"note"
                err.append({'class': 9018043, 'subclass': 1150070765, 'text': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', mapcss.tag(tags, u'addr:housenumber'))})

        # *[source=~/(?i)google/][inside("BR")]
        if (u'source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2e8e4f2b), mapcss._tag_capture(capture_tags, 0, tags, u'source')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("objeto contém Google como source")
                err.append({'class': 9018044, 'subclass': 1159310436, 'text': mapcss.tr(u'objeto contém Google como source')})

        # *[amenity=townhall][name=~/^(?i)(?u)c(â|a)mara\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'townhall') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_46ab4d8d), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("câmara de vereadores mapeada incorretamente")
                # suggestAlternative:"office=government + government=legislative"
                err.append({'class': 9018002, 'subclass': 532372413, 'text': mapcss.tr(u'câmara de vereadores mapeada incorretamente')})

        # *[office=government][government!=legislative][name=~/^(?i)(?u)c(â|a)mara\b/][inside("BR")]
        if (u'name' in keys and u'office' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'government') and mapcss._tag_capture(capture_tags, 1, tags, u'government') != mapcss._value_const_capture(capture_tags, 1, u'legislative', u'legislative') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_46ab4d8d), mapcss._tag_capture(capture_tags, 2, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("ausência de government=legislative")
                err.append({'class': 9018002, 'subclass': 2126685099, 'text': mapcss.tr(u'ausência de government=legislative')})

        # *[amenity=townhall][name=~/^(?i)(?u)c((â|a)me|ama)ra\b/][inside("BR")]
        # *[office=government][name=~/^(?i)(?u)c((â|a)me|ama)ra\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys) or (u'name' in keys and u'office' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'townhall') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_793b22ec), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'government') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_793b22ec), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("erro de ortografia em ''câmara''")
                err.append({'class': 9018002, 'subclass': 1277153079, 'text': mapcss.tr(u'erro de ortografia em \'\'câmara\'\'')})

        # *[name=~/(?i)^prefeitura\b/][amenity!=townhall][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7ec1fb9a), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'townhall', u'townhall') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("prefeitura possivelmente mapeada de forma incorreta")
                # suggestAlternative:"amenity=townhall"
                err.append({'class': 9018002, 'subclass': 1445137044, 'text': mapcss.tr(u'prefeitura possivelmente mapeada de forma incorreta')})

        # *[name=~/(?i)(?u)^paço\b/][amenity!=townhall][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_13f4c147), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'townhall', u'townhall') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("paço possivelmente mapeado de forma incorreta")
                # suggestAlternative:"amenity=townhall"
                err.append({'class': 9018002, 'subclass': 1169494638, 'text': mapcss.tr(u'paço possivelmente mapeado de forma incorreta')})

        # *[amenity=charging_station][inside("BR")]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'charging_station') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("possivelmente deve ser amenity=fuel")
                err.append({'class': 9018002, 'subclass': 2011797637, 'text': mapcss.tr(u'possivelmente deve ser amenity=fuel')})

        # *[name=~/(?i)^Borrach(aria|eiro)/][shop=tyres][!repair][inside("BR")]
        if (u'name' in keys and u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_126ba9a9), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'shop') == mapcss._value_capture(capture_tags, 1, u'tyres') and not mapcss._tag_capture(capture_tags, 2, tags, u'repair') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("borracharia sem ''repair=yes''")
                # suggestAlternative:"repair=yes"
                err.append({'class': 9018002, 'subclass': 1225518759, 'text': mapcss.tr(u'borracharia sem \'\'repair=yes\'\'')})

        # *[name=~/(?i)^Borrach(aria|eiro)/][shop!=tyres][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_126ba9a9), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'shop') != mapcss._value_const_capture(capture_tags, 1, u'tyres', u'tyres') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("borracharia sem ''shop=tyres''")
                # suggestAlternative:"shop=tyres"
                err.append({'class': 9018002, 'subclass': 755877630, 'text': mapcss.tr(u'borracharia sem \'\'shop=tyres\'\'')})

        # *[name=~/(?i)\bcoreto\b/][leisure!=bandstand][leisure!=park][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_6e34cd0f), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'leisure') != mapcss._value_const_capture(capture_tags, 1, u'bandstand', u'bandstand') and mapcss._tag_capture(capture_tags, 2, tags, u'leisure') != mapcss._value_const_capture(capture_tags, 2, u'park', u'park') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("coreto possivelmente classificado de forma incorreta")
                # suggestAlternative:"leisure=bandstand"
                err.append({'class': 9018002, 'subclass': 810497942, 'text': mapcss.tr(u'coreto possivelmente classificado de forma incorreta')})

        # *[leisure=recreation_ground][inside("BR")]
        if (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'recreation_ground') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} impreciso","{0.tag}")
                # suggestAlternative:"landuse=recreation_ground"
                # suggestAlternative:"leisure=park"
                err.append({'class': 9018002, 'subclass': 1594563801, 'text': mapcss.tr(u'{0} impreciso', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[leisure=recreation_ground][landuse=recreation_ground][inside("BR")]
        if (u'landuse' in keys and u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'recreation_ground') and mapcss._tag_capture(capture_tags, 1, tags, u'landuse') == mapcss._value_capture(capture_tags, 1, u'recreation_ground') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} supérfluo","{0.tag}")
                # fixRemove:"leisure"
                err.append({'class': 9018002, 'subclass': 627419845, 'text': mapcss.tr(u'{0} supérfluo', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'leisure'])
                }})

        # *["ref:vatin"]["ref:vatin"!~/^BR[0-9]{14}$/][inside("BR")]
        if (u'ref:vatin' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:vatin') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_524288b6, u'^BR[0-9]{14}$'), mapcss._tag_capture(capture_tags, 1, tags, u'ref:vatin')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("CNPJ diferente do formato BRxxxxxxxxxxxxxx")
                err.append({'class': 9018002, 'subclass': 1793026117, 'text': mapcss.tr(u'CNPJ diferente do formato BRxxxxxxxxxxxxxx')})

        # *["ref:vatin"=~/^[0-9]{2}\.[0-9]{3}\.[0-9]{3}\/[0-9]{4}-[0-9]{2}$/][inside("BR")]
        if (u'ref:vatin' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5ddbb7eb), mapcss._tag_capture(capture_tags, 0, tags, u'ref:vatin')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("formato do CNPJ pode ser melhorado em {0}","{0.key}")
                # fixAdd:concat("ref:vatin=BR",replace(replace(replace(tag("ref:vatin"),"/",""),".",""),"-",""))
                err.append({'class': 9018006, 'subclass': 1609978963, 'text': mapcss.tr(u'formato do CNPJ pode ser melhorado em {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'ref:vatin=BR', mapcss.replace(mapcss.replace(mapcss.replace(mapcss.tag(tags, u'ref:vatin'), u'/', u''), u'.', u''), u'-', u''))).split('=', 1)])
                }})

        # *["ref:vatin"=~/^(br|bR|Br)[0-9]{14}$/][inside("BR")]
        if (u'ref:vatin' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_408831d0), mapcss._tag_capture(capture_tags, 0, tags, u'ref:vatin')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("CNPJ deve iniciar maiúsculo: BRxxxxxxxxxxxxxx")
                # fixAdd:concat("ref:vatin=",upper(tag("ref:vatin")))
                err.append({'class': 9018006, 'subclass': 1616044431, 'text': mapcss.tr(u'CNPJ deve iniciar maiúsculo: BRxxxxxxxxxxxxxx'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'ref:vatin=', mapcss.upper(mapcss.tag(tags, u'ref:vatin')))).split('=', 1)])
                }})

        # *[phone][phone!~/^(\+55|0800)/][inside("BR")]
        # *["contact:phone"]["contact:phone"!~/^(\+55|0800)/][inside("BR")]
        if (u'contact:phone' in keys) or (u'phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'phone') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_243f4993, u'^(\+55|0800)'), mapcss._tag_capture(capture_tags, 1, tags, u'phone')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'contact:phone') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_243f4993, u'^(\+55|0800)'), mapcss._tag_capture(capture_tags, 1, tags, u'contact:phone')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} em formato diferente do internacional +55 XX YYYY-YYYY","{0.key}")
                err.append({'class': 9018002, 'subclass': 1438682200, 'text': mapcss.tr(u'{0} em formato diferente do internacional +55 XX YYYY-YYYY', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[phone=~/^(100|18{0,1}|19[0-9])$/][inside("BR")]
        # *["contact:phone"=~/^(100|18{0,1}|19[0-9])$/][inside("BR")]
        if (u'contact:phone' in keys) or (u'phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7a246e93), mapcss._tag_capture(capture_tags, 0, tags, u'phone')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7a246e93), mapcss._tag_capture(capture_tags, 0, tags, u'contact:phone')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("não usar número de emergência em {0}","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9018002, 'subclass': 371146161, 'text': mapcss.tr(u'não usar número de emergência em {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[name=*ref][highway][inside("BR")]
        # Rule Blacklisted

        # way[highway][name=~/\b[A-Z]{2,4} (- )?[0-9]{2,3}\b/][inside("BR")]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_568a42f4), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("rodovia com ref no nome")
                err.append({'class': 9018002, 'subclass': 457207682, 'text': mapcss.tr(u'rodovia com ref no nome')})

        # way[highway=cycleway][name][name!~/^(?i)ciclovia .*/][inside("BR")]
        # way[highway][highway!~/bridleway|bus_stop|cycleway|crossing|footway|give_way|motorway_junction|path|raceway|rest_area|services|speed_camera|steps|stop/][name][name!~/^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Calçadão|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodoanel|Rodovia|Rotatória|Rótula|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*/][inside("BR")]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'cycleway') and mapcss._tag_capture(capture_tags, 1, tags, u'name') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_2fcb6bab, u'^(?i)ciclovia .*'), mapcss._tag_capture(capture_tags, 2, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_1054eb5a, u'bridleway|bus_stop|cycleway|crossing|footway|give_way|motorway_junction|path|raceway|rest_area|services|speed_camera|steps|stop'), mapcss._tag_capture(capture_tags, 1, tags, u'highway')) and mapcss._tag_capture(capture_tags, 2, tags, u'name') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_60ad6838, u'^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Calçadão|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodoanel|Rodovia|Rotatória|Rótula|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*'), mapcss._tag_capture(capture_tags, 3, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} com logradouro ausente, errado ou abreviado","{0.key}")
                err.append({'class': 9018002, 'subclass': 20071126, 'text': mapcss.tr(u'{0} com logradouro ausente, errado ou abreviado', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *["addr:street"]["addr:street"!~/^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Calçadão|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodovia|Rotatória|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*/][inside("BR")]
        if (u'addr:street' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'addr:street') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_6bf570a0, u'^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Calçadão|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodovia|Rotatória|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*'), mapcss._tag_capture(capture_tags, 1, tags, u'addr:street')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} com logradouro ausente, errado ou abreviado","{0.key}")
                err.append({'class': 9018002, 'subclass': 279840772, 'text': mapcss.tr(u'{0} com logradouro ausente, errado ou abreviado', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way[highway][name][name=~/\./]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_7a5b2736), mapcss._tag_capture(capture_tags, 2, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("Rua com nome abreviado; procurar nome completo nas camadas de nomes")
                err.append({'class': 9018002, 'subclass': 2131010585, 'text': mapcss.tr(u'Rua com nome abreviado; procurar nome completo nas camadas de nomes')})

        # *[!highway][route!=road][!public_transport][type!~/route|street/][name][name=~/^(?i)(?u)(alameda|avenida|beco|estrada|ladeira|passarela|rodovia|rotatória|rua|travessa|trevo|viela|(anel|complexo|dispositivo) viário) .*/][name!~/^(?i)estrada de ferro/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'route') != mapcss._value_const_capture(capture_tags, 1, u'road', u'road') and not mapcss._tag_capture(capture_tags, 2, tags, u'public_transport') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_72d45155, u'route|street'), mapcss._tag_capture(capture_tags, 3, tags, u'type')) and mapcss._tag_capture(capture_tags, 4, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 5, self.re_5849be19), mapcss._tag_capture(capture_tags, 5, tags, u'name')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 6, self.re_15690541, u'^(?i)estrada de ferro'), mapcss._tag_capture(capture_tags, 6, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("objeto com nome de via mas sem tag de {0}","{0.key}")
                err.append({'class': 9018002, 'subclass': 535280341, 'text': mapcss.tr(u'objeto com nome de via mas sem tag de {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way[highway=track][name][name=~/^(?i)(?u)(alameda|avenida|beco|estrada|ladeira|rodovia|rotatória|rua|travessa|trevo|viela) .*/][inside("BR")]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'track') and mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_20cf30ba), mapcss._tag_capture(capture_tags, 2, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("não classificar via como {0}","{0.tag}")
                # suggestAlternative:"highway=residential"
                # suggestAlternative:"highway=unclassified"
                err.append({'class': 9018051, 'subclass': 1145810098, 'text': mapcss.tr(u'não classificar via como {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[name=~/^(?i)(?u)[a-z0-9]+_([a-z0-9]_?)+$/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_4bd3b925), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("utilizar espaço ao invés de underscore")
                err.append({'class': 9018002, 'subclass': 1476954926, 'text': mapcss.tr(u'utilizar espaço ao invés de underscore')})

        # *[name=~/(?i)(^|.* )(Cel|Cmte|Cond|Conj|Dª|Dr|Eng|Gov|Hab|Jd|Jr|Marg|Mun|p\/|Pde|Pe|Pq|Pst|Pref|Profa|Profª|Prof|Res|s\/|Sr(a|ª)?|Sta|Sto|Ver)\.? .*/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_178f5446), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("palavra abreviada em {0}","{0.key}")
                err.append({'class': 9018003, 'subclass': 749019091, 'text': mapcss.tr(u'palavra abreviada em {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way[highway][name=~/^(?i)(?u)((via de )?(acesso|ligação)(( (a|à))? propriedade)?|entrada|entroncamento|rampa|retorno|rotat(ó|o)ria|r(ó|o)tula|sa(í|i)da|trevo|estrada( municipal| de terra)?|rua|rodovia|via)( (de acesso|sem nome|projetad(a|o)))?$/][inside("BR")]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_667ce569), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} com nome supérfluo/incompleto","{0.key}")
                # suggestAlternative:"description"
                # suggestAlternative:"destination"
                err.append({'class': 9018052, 'subclass': 736885884, 'text': mapcss.tr(u'{0} com nome supérfluo/incompleto', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[leisure][name=~/^(?i)(?u)(campo|est(á|a)dio|gin(á|a)sio|quadra)( de (futebol|esportes?))?$/][inside("BR")]
        if (u'leisure' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7f53e992), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("nome supérfluo/incompleto de local de lazer")
                err.append({'class': 9018004, 'subclass': 1485441713, 'text': mapcss.tr(u'nome supérfluo/incompleto de local de lazer')})

        # *[name=~/^(?i)(?u)((Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF|hospital)$/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_52ab3b8b), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("nome supérfluo/incompleto de local de saúde")
                err.append({'class': 9018005, 'subclass': 1497769259, 'text': mapcss.tr(u'nome supérfluo/incompleto de local de saúde')})

        # *[amenity=~/^(clinic|doctors|hospital)$/][name=~/(?i)\bsaude\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5ab76b11), mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_4cf86823), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("erro de ortografia em ''saúde''")
                err.append({'class': 9018002, 'subclass': 1962359328, 'text': mapcss.tr(u'erro de ortografia em \'\'saúde\'\'')})

        # *[place=farm][name^="Sitio "][inside("BR")]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'farm') and mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, u'name'), mapcss._value_capture(capture_tags, 1, u'Sitio ')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("faltando acento em ''Sítio''")
                err.append({'class': 9018002, 'subclass': 653860263, 'text': mapcss.tr(u'faltando acento em \'\'Sítio\'\'')})

        # *[name=~/^(?i)(?u)(aldeia|borrach(aria|eiro)|bosque|capela|cemit(é|e)rio|c(ó|o)rrego|escola|estacionamento|fazenda|floresta|hospital|igreja|lago|lagoa|mata( nativa)?|praça|parque|parquinho|posto( de gasolina)?|riacho|rio|rodovi(á|a)ria|vila)$/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_20c7dd98), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("local com nome supérfluo, incompleto ou descritivo")
                err.append({'class': 9018002, 'subclass': 1104230922, 'text': mapcss.tr(u'local com nome supérfluo, incompleto ou descritivo')})

        # *[amenity=parking][name=~/(?i)^Estacionamento /][inside("BR")]
        # Rule Blacklisted

        # way[highway][type=route][inside("BR")]
        if (u'highway' in keys and u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'route') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} não deve possuir {1}","{0.key}","{1.tag}")
                err.append({'class': 9018053, 'subclass': 1158257088, 'text': mapcss.tr(u'{0} não deve possuir {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # way[highway][highway!~/bus_stop|milestone|motorway_junction|traffic_signals/][ref][ref!~/^(([A-Z]{2,3}-[0-9]{2,4}|SPM(-| )[0-9]{3} ?(D|E)?|SP(A|D|I)(-| )[0-9]{3}\/[0-9]{3}|[A-Z]{3}-[0-9]{3}\/[0-9]{3});?)+$/][inside("BR")]
        # Rule Blacklisted

        # way[highway][!ref][name=~/.*([A-Z]{2,3}-[0-9]{2,4}|SPM(-| )[0-9]{3} ?(D|E)?|SP(A|D|I)(-| )[0-9]{3}\/[0-9]{3}|[A-Z]{3}-[0-9]{3}\/[0-9]{3}).*/][inside("BR")]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and not mapcss._tag_capture(capture_tags, 1, tags, u'ref') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_375e3de4), mapcss._tag_capture(capture_tags, 2, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("utilizar o código/sigla da rodovia também na tag {0}","{1.key}")
                err.append({'class': 9018002, 'subclass': 2109205925, 'text': mapcss.tr(u'utilizar o código/sigla da rodovia também na tag {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # way[highway][name=~/Rodovia ([A-Z]{2,3}-[0-9]{2,4})/][inside("BR")]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7633bf4e), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("nome incorreto de rodovia; utilizar o nome oficial ou apenas ref")
                err.append({'class': 9018002, 'subclass': 718023291, 'text': mapcss.tr(u'nome incorreto de rodovia; utilizar o nome oficial ou apenas ref')})

        # way[name=*"addr:street"][highway][inside("BR")]
        # *[designation=*"addr:housename"][inside("BR")]
        # *[ref=*designation][inside("BR")]
        # *[ref=*old_ref][inside("BR")]
        # *[name=*"addr:housename"][inside("BR")]
        # *[name=*designation][inside("BR")]
        # *[name=*alt_name][inside("BR")]
        # *[name=*int_name][inside("BR")]
        # *[name=*loc_name][inside("BR")]
        # *[name=*nat_name][inside("BR")]
        # *[name=*official_name][inside("BR")]
        # *[name=*old_name][inside("BR")]
        # *[name=*reg_name][inside("BR")]
        # *[name=*short_name][inside("BR")]
        # *[name=*sorting_name][inside("BR")]
        # Rule Blacklisted

        # *[source=*name][inside("BR")]
        if (u'source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} e {1} são iguais","{0.key}","{0.value}")
                err.append({'class': 9018002, 'subclass': 470146003, 'text': mapcss.tr(u'{0} e {1} são iguais', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[name=~/(?i)(?u)((sem (denomina(ç|c)(ã|a)o|nome|sa(i|í)da))|desconhecido|n(ã|a)o conhecido)/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_65710fdb), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto com nomenclatura incorreta")
                # suggestAlternative:"noname"
                err.append({'class': 9018007, 'subclass': 1272098213, 'text': mapcss.tr(u'objeto com nomenclatura incorreta')})

        # *[designation][inside("BR")]
        if (u'designation' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'designation') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} é uma chave utilizada apenas no Reino Unido","{0.key}")
                # suggestAlternative:"description"
                # suggestAlternative:"name"
                err.append({'class': 9018009, 'subclass': 1818234763, 'text': mapcss.tr(u'{0} é uma chave utilizada apenas no Reino Unido', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way[highway=~/^(trunk|motorway)$/][!operator][inside("BR")]
        # Rule Blacklisted

        # way[highway$=_link][name=~/(Alameda|Avenida|Rua|Travessa|Viela) .*/][inside("BR")]
        # Rule Blacklisted

        # way[highway][name=~/(Alameda|Avenida|Rua|Travessa|Viela) .*/][ref][inside("BR")]
        if (u'highway' in keys and u'name' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6b6e390d), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'ref') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("possível uso desnecessário/errado de ref em {0}={1}","{0.key}",tag("highway"))
                err.append({'class': 9018002, 'subclass': 227495312, 'text': mapcss.tr(u'possível uso desnecessário/errado de ref em {0}={1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss.tag(tags, u'highway'))})

        # *[place=~/hamlet|isolated_dwelling|town|village/][population>=100000][inside("BR")]
        if (u'place' in keys and u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_152c10ee), mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'population') >= mapcss._value_capture(capture_tags, 1, 100000) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("local com 100.000 habitantes ou mais deve ser classificado como city")
                # fixAdd:"place=city"
                err.append({'class': 9018006, 'subclass': 1009134521, 'text': mapcss.tr(u'local com 100.000 habitantes ou mais deve ser classificado como city'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'place',u'city']])
                }})

        # *[place=~/city|hamlet|isolated_dwelling|village/][population>=10000][population<100000][inside("BR")]
        if (u'place' in keys and u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_591572a5), mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'population') >= mapcss._value_capture(capture_tags, 1, 10000) and mapcss._tag_capture(capture_tags, 2, tags, u'population') < mapcss._value_capture(capture_tags, 2, 100000) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("local com população entre 10.000 e 100.000 deve ser classificado como town")
                # fixAdd:"place=town"
                err.append({'class': 9018006, 'subclass': 1343568198, 'text': mapcss.tr(u'local com população entre 10.000 e 100.000 deve ser classificado como town'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'place',u'town']])
                }})

        # *[place][place!~/hamlet|island|isolated_dwelling|neighbourhood|suburb|village/][population<10000][inside("BR")]
        if (u'place' in keys and u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_3aeda39d, u'hamlet|island|isolated_dwelling|neighbourhood|suburb|village'), mapcss._tag_capture(capture_tags, 1, tags, u'place')) and mapcss._tag_capture(capture_tags, 2, tags, u'population') < mapcss._value_capture(capture_tags, 2, 10000) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("local com menos de 10.000 habitantes deve ser classificado como village")
                # fixAdd:"place=village"
                err.append({'class': 9018006, 'subclass': 409005616, 'text': mapcss.tr(u'local com menos de 10.000 habitantes deve ser classificado como village'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'place',u'village']])
                }})

        # *[place=city][!population][inside("BR")]
        # *[place=town][!population][inside("BR")]
        # *[place=village][!population][inside("BR")]
        # Rule Blacklisted

        # *[place=city][!name][inside("BR")]
        # *[place=town][!name][inside("BR")]
        # *[place=village][!name][inside("BR")]
        if (u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'city') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'town') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'village') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} sem nome","{0.value}")
                err.append({'class': 9018012, 'subclass': 1473808194, 'text': mapcss.tr(u'{0} sem nome', mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *["addr:city"=~/(,|( |-) ?[A-Z]{2})/][inside("BR")]
        if (u'addr:city' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_10f1c360), mapcss._tag_capture(capture_tags, 0, tags, u'addr:city')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve conter apenas o nome da cidade","{0.key}")
                err.append({'class': 9018013, 'subclass': 1479274467, 'text': mapcss.tr(u'{0} deve conter apenas o nome da cidade', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name=~/^(?i)(?u)(Faz\.|Fazenda|Sítio|Chácara)/][place][place!~/city|farm|neighbourhood|suburb|town|village/][inside("BR")]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2cd1e949), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'place') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_5d3348cb, u'city|farm|neighbourhood|suburb|town|village'), mapcss._tag_capture(capture_tags, 2, tags, u'place')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("objeto talvez deva ser {0}=farm","{1.key}")
                err.append({'class': 9018002, 'subclass': 337742963, 'text': mapcss.tr(u'objeto talvez deva ser {0}=farm', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[place][name=~/^(?i)Bairro\b/][name!~/^(?i)Bairro d(a|e|o)s?\b/][inside("BR")]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_20fc5143), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_64387998, u'^(?i)Bairro d(a|e|o)s?\b'), mapcss._tag_capture(capture_tags, 2, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("objeto talvez não deva ter ''Bairro'' no nome")
                err.append({'class': 9018002, 'subclass': 1441242115, 'text': mapcss.tr(u'objeto talvez não deva ter \'\'Bairro\'\' no nome')})

        # *[iata="0"][inside("BR")]
        if (u'iata' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'iata') == mapcss._value_capture(capture_tags, 0, u'0') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} com valor = {1}","{0.key}","{0.value}")
                err.append({'class': 9018014, 'subclass': 1098244333, 'text': mapcss.tr(u'{0} com valor = {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[amenity=~/college|school/][name=~/^(?i)(?u)(Centro Universitário|Faculdades?|FATEC|Instituto Federal)\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_362f879f), mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1d232d4c), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("estabelecimento de ensino classificado incorretamente")
                # suggestAlternative:"amenity=university"
                # fixAdd:"{0.key}=university"
                err.append({'class': 9018006, 'subclass': 1605707172, 'text': mapcss.tr(u'estabelecimento de ensino classificado incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=university')).split('=', 1)])
                }})

        # *[amenity=school][name=~/^(?i)(?u)(SENAC|SENAI|Serviço Nacional de Aprendizagem)/][inside("BR")]
        # *[amenity=~/school|university/][name=~/(?i)(?u)\b(Centro Paula Souza|Escola Técnica|ETEC)\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'school') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_044c8944), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_6c0d6e9e), mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3b304b9b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("estabelecimento de ensino classificado incorretamente")
                # suggestAlternative:"amenity=college"
                # fixAdd:"{0.key}=college"
                err.append({'class': 9018006, 'subclass': 1282773099, 'text': mapcss.tr(u'estabelecimento de ensino classificado incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=college')).split('=', 1)])
                }})

        # *[amenity=school][name=~/^(?i)(?u)(auto(-| )?( moto )?escola|centro de formação de condutores|cfc|moto escola)\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'school') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_35bb0f2f), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("autoescola classificada incorretamente")
                # suggestAlternative:"amenity=driving_school"
                # fixAdd:"{0.key}=driving_school"
                err.append({'class': 9018006, 'subclass': 566309924, 'text': mapcss.tr(u'autoescola classificada incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=driving_school')).split('=', 1)])
                }})

        # *[amenity=school][name=~/^(?i)creche\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'school') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_160d1bfc), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("creche classificada incorretamente")
                # suggestAlternative:"amenity=kindergarten"
                # fixAdd:"{0.key}=kindergarten"
                err.append({'class': 9018006, 'subclass': 1847987722, 'text': mapcss.tr(u'creche classificada incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=kindergarten')).split('=', 1)])
                }})

        # *[name=~/^(?i)(?u)Subestação .*/][power][power!=substation][inside("BR")]
        # *[name=~/^(?i)(?u)Fórum .*/][amenity][amenity!=courthouse][inside("BR")]
        # *[name=~/^(?i)Hospital .*/][building][building!=hospital][inside("BR")]
        # *[name=~/^(?i)Universidade .*/][building][building!=university][inside("BR")]
        # *[name=~/^(?i)Escola .*/][building][building!=school][inside("BR")]
        # *[name=~/^(?i)Hotel .*/][building][building!=hotel][inside("BR")]
        # *[name=~/^(?i)Capela .*/][building][building!=chapel][inside("BR")]
        # *[name=~/^(?i)Igreja .*/][building][building!=church][inside("BR")]
        # *[name=~/^(?i)Catedral .*/][building][building!=cathedral][inside("BR")]
        # *[name=~/^(?i)Fazenda .*/][building][building!=farm][inside("BR")]
        # *[name=~/^(?i)Supermercado .*/][building][building!=supermarket][inside("BR")]
        # Rule Blacklisted

        # *[name=~/^(?i)(?u)(AM(A|E)|(Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF).*/][amenity=hospital][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7b7c453d), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') == mapcss._value_capture(capture_tags, 1, u'hospital') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("postos/unidades de saúde devem ser amenity=clinic")
                # fixAdd:"amenity=clinic"
                err.append({'class': 9018006, 'subclass': 74419437, 'text': mapcss.tr(u'postos/unidades de saúde devem ser amenity=clinic'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'clinic']])
                }})

        # *[name=~/^(?i)\bSAMU\b/][amenity=~/clinic|doctors|hospital/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2dbaea13), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3eb0ab44), mapcss._tag_capture(capture_tags, 1, tags, u'amenity')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("SAMU classificado de forma errada")
                # suggestAlternative:"emergency=ambulance_station"
                err.append({'class': 9018016, 'subclass': 392029310, 'text': mapcss.tr(u'SAMU classificado de forma errada')})

        # way[highway=give_way][inside("BR")]
        # way[highway=mini_roundabout][inside("BR")]
        # way[highway=stop][inside("BR")]
        # way[highway=turning_circle][inside("BR")]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'give_way') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'mini_roundabout') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'stop') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'turning_circle') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve ser utilizado apenas em nós","{0.tag}")
                err.append({'class': 9018047, 'subclass': 1154213374, 'text': mapcss.tr(u'{0} deve ser utilizado apenas em nós', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # way[highway][junction=circular][!oneway?][inside("BR")]
        if (u'highway' in keys and u'junction' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'junction') == mapcss._value_capture(capture_tags, 1, u'circular') and not mapcss._tag_capture(capture_tags, 2, tags, u'oneway') in ('yes', 'true', '1') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("junção circular sem ''oneway''")
                # fixAdd:"oneway=yes"
                err.append({'class': 9018002, 'subclass': 1396859077, 'text': mapcss.tr(u'junção circular sem \'\'oneway\'\''), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'oneway',u'yes']])
                }})

        # *[crossing][!highway][!railway][inside("BR")]
        if (u'crossing' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'crossing') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve ser utilizado com {1}={0} ou {2}={0}","{0.key}","{1.key}","{2.key}")
                err.append({'class': 9018019, 'subclass': 2098306424, 'text': mapcss.tr(u'{0} deve ser utilizado com {1}={0} ou {2}={0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[aeroway][designation=~/^[A-Z]{4}$/][!icao][inside("BR")]
        # *[aeroway][ref=~/^[A-Z]{4}$/][!icao][inside("BR")]
        if (u'aeroway' in keys and u'designation' in keys) or (u'aeroway' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7afc6883), mapcss._tag_capture(capture_tags, 1, tags, u'designation')) and not mapcss._tag_capture(capture_tags, 2, tags, u'icao') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7afc6883), mapcss._tag_capture(capture_tags, 1, tags, u'ref')) and not mapcss._tag_capture(capture_tags, 2, tags, u'icao') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("{0} provavelmente deve ser utilizado como {1}","{1.key}","{2.key}")
                # fixChangeKey:"{1.key} => {2.key}"
                err.append({'class': 9018006, 'subclass': 619372172, 'text': mapcss.tr(u'{0} provavelmente deve ser utilizado como {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, u'{1.key} => {2.key}')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, u'{1.key} => {2.key}')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, u'{1.key} => {2.key}')).split('=>', 1)[0].strip()])
                }})

        # *[access=permissive][inside("BR")]
        if (u'access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'permissive') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} deve ser utilizado apenas em vias privadas com permissão de acesso e não em vias de acesso público","{0.tag}")
                err.append({'class': 9018002, 'subclass': 1240816112, 'text': mapcss.tr(u'{0} deve ser utilizado apenas em vias privadas com permissão de acesso e não em vias de acesso público', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[name=~/^(?U)(\p{Upper}| )+$/][inside("BR")]
        # *["addr:street"=~/^(?U)(\p{Upper}| )+$/][inside("BR")]
        # Rule Blacklisted

        # *["addr:postcode"=~/^[0-9]{8}$/][inside("BR")]
        # Rule Blacklisted

        # *[postal_code=~/^[0-9]{8}$/][inside("BR")]
        # Rule Blacklisted

        # *["addr:postcode"=~/^[0-9]{5}( |\.)[0-9]{3}$/][inside("BR")]
        if (u'addr:postcode' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_57bee688), mapcss._tag_capture(capture_tags, 0, tags, u'addr:postcode')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("formato do CEP pode ser melhorado")
                # fixAdd:concat("addr:postcode=",replace(replace(tag("addr:postcode")," ","-"),".","-"))
                err.append({'class': 9018006, 'subclass': 1667206075, 'text': mapcss.tr(u'formato do CEP pode ser melhorado'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'addr:postcode=', mapcss.replace(mapcss.replace(mapcss.tag(tags, u'addr:postcode'), u' ', u'-'), u'.', u'-'))).split('=', 1)])
                }})

        # *["postal_code"=~/^[0-9]{5}( |\.)[0-9]{3}$/][inside("BR")]
        if (u'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_57bee688), mapcss._tag_capture(capture_tags, 0, tags, u'postal_code')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("formato do CEP pode ser melhorado")
                # fixAdd:concat("postal_code=",replace(replace(tag("postal_code")," ","-"),".","-"))
                err.append({'class': 9018006, 'subclass': 1977906896, 'text': mapcss.tr(u'formato do CEP pode ser melhorado'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'postal_code=', mapcss.replace(mapcss.replace(mapcss.tag(tags, u'postal_code'), u' ', u'-'), u'.', u'-'))).split('=', 1)])
                }})

        # *["addr:postcode"]["addr:postcode"!~/^[0-9]{5}-[0-9]{3}$/][inside("BR")]
        # *[postal_code][postal_code!~/^[0-9]{5}-[0-9]{3}$/][inside("BR")]
        # Rule Blacklisted

        # way[highway]["addr:postcode"][highway!=services][inside("BR")]
        if (u'addr:postcode' in keys and u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'addr:postcode') and mapcss._tag_capture(capture_tags, 2, tags, u'highway') != mapcss._value_const_capture(capture_tags, 2, u'services', u'services') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("uso incorreto de {0}","{1.key}","{0.key}")
                # suggestAlternative:"postal_code"
                # fixChangeKey:"{1.key} => postal_code"
                err.append({'class': 9018006, 'subclass': 314748788, 'text': mapcss.tr(u'uso incorreto de {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, u'{1.key} => postal_code')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, u'{1.key} => postal_code')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, u'{1.key} => postal_code')).split('=>', 1)[0].strip()])
                }})

        # *[alt_source][source][inside("BR")]
        if (u'alt_source' in keys and u'source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'alt_source') and mapcss._tag_capture(capture_tags, 1, tags, u'source') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve estar incluído em {1}, separado por '';'' caso necessário","{0.key}","{1.key}")
                err.append({'class': 9018020, 'subclass': 472956812, 'text': mapcss.tr(u'{0} deve estar incluído em {1}, separado por \'\';\'\' caso necessário', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[landuse?][inside("BR")]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') in ('yes', 'true', '1') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("especificar valor correto para {0} ao invés de ''{1}''","{0.key}",tag("landuse"))
                err.append({'class': 9018021, 'subclass': 6418462, 'text': mapcss.tr(u'especificar valor correto para {0} ao invés de \'\'{1}\'\'', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss.tag(tags, u'landuse'))})

        # *[long_name][inside("BR")]
        if (u'long_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'long_name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("chave inválida: {0}","{0.key}")
                # suggestAlternative:"alt_name"
                # suggestAlternative:"name"
                # suggestAlternative:"official_name"
                err.append({'class': 9018022, 'subclass': 1737555221, 'text': mapcss.tr(u'chave inválida: {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *["building:levels"<1][inside("BR")]
        if (u'building:levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:levels') < mapcss._value_capture(capture_tags, 0, 1) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} com valor inválido","{0.key}")
                err.append({'class': 9018002, 'subclass': 775859422, 'text': mapcss.tr(u'{0} com valor inválido', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[hires?][inside("BR")]
        if (u'hires' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'hires') in ('yes', 'true', '1') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("não se deve utilizar {0} para demarcar áreas de cobertura de imagem","{0.key}")
                err.append({'class': 9018023, 'subclass': 895278192, 'text': mapcss.tr(u'não se deve utilizar {0} para demarcar áreas de cobertura de imagem', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[tourism=motel][amenity!=love_hotel][inside("BR")]
        # *[name=~/(?i)\bmotel\b/][amenity!=love_hotel][inside("BR")]
        if (u'name' in keys) or (u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == mapcss._value_capture(capture_tags, 0, u'motel') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'love_hotel', u'love_hotel') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_01454d46), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'love_hotel', u'love_hotel') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("ausência de tag ''{0}''","{1.value}")
                # fixAdd:"{1.key}={1.value}"
                err.append({'class': 9018006, 'subclass': 1987370859, 'text': mapcss.tr(u'ausência de tag \'\'{0}\'\'', mapcss._tag_uncapture(capture_tags, u'{1.value}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{1.key}={1.value}')).split('=', 1)])
                }})

        # *[amenity=love_hotel][tourism][tourism!=motel][inside("BR")]
        if (u'amenity' in keys and u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'love_hotel') and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') and mapcss._tag_capture(capture_tags, 2, tags, u'tourism') != mapcss._value_const_capture(capture_tags, 2, u'motel', u'motel') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("provavelmente deve ser ''{0}={1}''","{2.key}","{2.value}")
                err.append({'class': 9018002, 'subclass': 1760828878, 'text': mapcss.tr(u'provavelmente deve ser \'\'{0}={1}\'\'', mapcss._tag_uncapture(capture_tags, u'{2.key}'), mapcss._tag_uncapture(capture_tags, u'{2.value}'))})

        # *[name=~/(?i)^motel\b/][tourism!=motel][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5cd37790), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') != mapcss._value_const_capture(capture_tags, 1, u'motel', u'motel') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("motel classificado incorretamente")
                # suggestAlternative:"tourism=motel"
                err.append({'class': 9018002, 'subclass': 1456128106, 'text': mapcss.tr(u'motel classificado incorretamente')})

        # *[aeroway=aerodrome][name=~/(?i).*airport$/][inside("BR")]
        # *[aeroway=helipad][name=~/(?i).*heliport$/][inside("BR")]
        if (u'aeroway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'aerodrome') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6efb8049), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'helipad') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6566db6a), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} com nome em inglês","{0.tag}")
                err.append({'class': 9018002, 'subclass': 1743601177, 'text': mapcss.tr(u'{0} com nome em inglês', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[aeroway=aerodrome][name=~/(?i)^Aer(ódromo|oporto) de.*/][inside("BR")]
        # *[aeroway=helipad][name=~/(?i)^Helipo(n|r)to.*/][inside("BR")]
        if (u'aeroway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'aerodrome') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6024a566), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'helipad') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_139e342b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("conferir se existe nome oficial do {0}","{0.value}")
                err.append({'class': 9018002, 'subclass': 136467214, 'text': mapcss.tr(u'conferir se existe nome oficial do {0}', mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[aeroway=aerodrome][ref][inside("BR")]
        if (u'aeroway' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'aerodrome') and mapcss._tag_capture(capture_tags, 1, tags, u'ref') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("''{0}'' não faz sentido em aeroporto","{1.key}")
                err.append({'class': 9018002, 'subclass': 1633437696, 'text': mapcss.tr(u'\'\'{0}\'\' não faz sentido em aeroporto', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # way[waterway][tunnel=yes][inside("BR")]
        # Rule Blacklisted

        # way[highway][layer<0][!tunnel][inside("BR")]
        # *[waterway][layer<0][!tunnel][inside("BR")]
        # Rule Blacklisted

        # way[highway][layer>0][!bridge][highway!=bus_stop][inside("BR")]
        # *[waterway][layer>0][!bridge][inside("BR")]
        # Rule Blacklisted

        # *[layer][!building][!highway][man_made!=pipeline][!railway][!waterway][power!=line][inside("BR")]
        # Rule Blacklisted

        # way[highway=motorway_junction][inside("BR")]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'motorway_junction') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} deve ser utilizado apenas no nó de saída da rodovia","{0.tag}")
                # suggestAlternative:"highway=motorway_link"
                err.append({'class': 9018056, 'subclass': 687515179, 'text': mapcss.tr(u'{0} deve ser utilizado apenas no nó de saída da rodovia', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[name=~/^(?i)(?u)edifício.*/][!building][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_38a8f0ff), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("possível ausência de tag {0}","{1.key}")
                err.append({'class': 9018026, 'subclass': 1332986859, 'text': mapcss.tr(u'possível ausência de tag {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # way[highway][maxspeed][maxspeed!~/^[0-9]+$/][inside("BR")]
        if (u'highway' in keys and u'maxspeed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_066203d3, u'^[0-9]+$'), mapcss._tag_capture(capture_tags, 2, tags, u'maxspeed')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("velocidade máxima deve ser apenas o valor numérico, em km/h")
                err.append({'class': 9018002, 'subclass': 78890622, 'text': mapcss.tr(u'velocidade máxima deve ser apenas o valor numérico, em km/h')})

        # way[highway][maxspeed][maxspeed!~/^[0-9]+0$/][inside("BR")]
        if (u'highway' in keys and u'maxspeed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_67c67cf2, u'^[0-9]+0$'), mapcss._tag_capture(capture_tags, 2, tags, u'maxspeed')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("velocidade máxima deveria ser múltiplo de 10")
                err.append({'class': 9018002, 'subclass': 1298210435, 'text': mapcss.tr(u'velocidade máxima deveria ser múltiplo de 10')})

        # *[route=ferry][!duration][inside("BR")]
        if (u'route' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'route') == mapcss._value_capture(capture_tags, 0, u'ferry') and not mapcss._tag_capture(capture_tags, 1, tags, u'duration') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("ausência do tempo de duração ({0}) da balsa","{1.key}")
                err.append({'class': 9018027, 'subclass': 1343391603, 'text': mapcss.tr(u'ausência do tempo de duração ({0}) da balsa', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[name=~/^(?i)(?u)praça.*/][!leisure][landuse=~/^(forest|grass|greenfield|meadow|orchard)$/][inside("BR")]
        # *[name=~/^(?i)(?u)praça.*/][!leisure][natural=~/^(grassland|heath|scrub|wood)$/][inside("BR")]
        if (u'landuse' in keys and u'name' in keys) or (u'name' in keys and u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_4a8ca94e), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'leisure') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_05a345c7), mapcss._tag_capture(capture_tags, 2, tags, u'landuse')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_4a8ca94e), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'leisure') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_12b48afb), mapcss._tag_capture(capture_tags, 2, tags, u'natural')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("possível definição incorreta para praça: ''{0}''","{2.key}")
                # suggestAlternative:"leisure=park"
                err.append({'class': 9018029, 'subclass': 181066872, 'text': mapcss.tr(u'possível definição incorreta para praça: \'\'{0}\'\'', mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[wikipedia][wikipedia!~/^pt:/][inside("BR")]
        if (u'wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_17fd35b3, u'^pt:'), mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("utilizar prefixo em português (pt:) para {0}","{0.key}")
                err.append({'class': 9018030, 'subclass': 1431112366, 'text': mapcss.tr(u'utilizar prefixo em português (pt:) para {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way[highway][lanes=1][!oneway?][!junction][!narrow][inside("BR")]
        # Rule Blacklisted

        # way[cycleway=lane]["cycleway:left"=lane][inside("BR")]
        # way[cycleway=lane]["cycleway:right"=lane][inside("BR")]
        if (u'cycleway' in keys and u'cycleway:left' in keys) or (u'cycleway' in keys and u'cycleway:right' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'cycleway') == mapcss._value_capture(capture_tags, 0, u'lane') and mapcss._tag_capture(capture_tags, 1, tags, u'cycleway:left') == mapcss._value_capture(capture_tags, 1, u'lane') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'cycleway') == mapcss._value_capture(capture_tags, 0, u'lane') and mapcss._tag_capture(capture_tags, 1, tags, u'cycleway:right') == mapcss._value_capture(capture_tags, 1, u'lane') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("uso incorreto de {0} com {1}","{0.tag}","{1.tag}")
                # suggestAlternative:"{1.tag}"
                err.append({'class': 9018063, 'subclass': 1071847858, 'text': mapcss.tr(u'uso incorreto de {0} com {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # *[name=~/.*\(.*\).*/][inside("BR")]
        # Rule Blacklisted

        # *[name=~/ - /][inside("BR")]
        # Rule Blacklisted

        # *[name=~/, /][inside("BR")]
        # Rule Blacklisted

        # *[name=~/: /][inside("BR")]
        # Rule Blacklisted

        # *[name=~/ ou /][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_131cc885), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("nome utilizado de forma incorreta")
                # suggestAlternative:"name e alt_name"
                err.append({'class': 9018031, 'subclass': 115703372, 'text': mapcss.tr(u'nome utilizado de forma incorreta')})

        # way[boundary=administrative][!admin_level]!.way_in_relation
        # Use undeclared class way_in_relation

        # way[place][place!~/^(city_block|farm|hamlet|island|islet|isolated_dwelling|neighbourhood|square)$/][!admin_level][!boundary][inside("BR")]
        if (u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_58f616c9, u'^(city_block|farm|hamlet|island|islet|isolated_dwelling|neighbourhood|square)$'), mapcss._tag_capture(capture_tags, 1, tags, u'place')) and not mapcss._tag_capture(capture_tags, 2, tags, u'admin_level') and not mapcss._tag_capture(capture_tags, 3, tags, u'boundary') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("local com ausência/incoerência de limite administrativo")
                err.append({'class': 9018002, 'subclass': 1502787309, 'text': mapcss.tr(u'local com ausência/incoerência de limite administrativo')})

        # way[admin_level][!boundary]!.way_in_relation
        # way[admin_level][boundary][boundary!=administrative]!.way_in_relation
        # Use undeclared class way_in_relation

        # *[boundary=national_park][!name][inside("BR")]
        # *[boundary=protected_area][!name][inside("BR")]
        # *[leisure=nature_reserve][!name][inside("BR")]
        if (u'boundary' in keys) or (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'national_park') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'protected_area') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'nature_reserve') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
                err.append({'class': 9018033, 'subclass': 1196875584, 'text': mapcss.tr(u'{0} deve possuir {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[boundary=protected_area][!protect_class][inside("BR")]
        if (u'boundary' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'protected_area') and not mapcss._tag_capture(capture_tags, 1, tags, u'protect_class') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
                err.append({'class': 9018033, 'subclass': 1593244126, 'text': mapcss.tr(u'{0} deve possuir {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[protect_class][protect_class!~/^(1(a|b)?|[1-9][0-9]?)$/][inside("BR")]
        if (u'protect_class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'protect_class') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_5ac7053e, u'^(1(a|b)?|[1-9][0-9]?)$'), mapcss._tag_capture(capture_tags, 1, tags, u'protect_class')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("valor incorreto para {0}","{0.key}")
                err.append({'class': 9018034, 'subclass': 1183781531, 'text': mapcss.tr(u'valor incorreto para {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[protect_class][boundary!=protected_area][inside("BR")]
        if (u'protect_class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'protect_class') and mapcss._tag_capture(capture_tags, 1, tags, u'boundary') != mapcss._value_const_capture(capture_tags, 1, u'protected_area', u'protected_area') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("ausência de boundary=protected_area")
                err.append({'class': 9018035, 'subclass': 1649283274, 'text': mapcss.tr(u'ausência de boundary=protected_area')})

        # *[name=~/.* D(a|e|o)s? .*/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2ffc377d), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("''da'', ''de'' e ''do'' são minúsculos nos nomes em português")
                err.append({'class': 9018002, 'subclass': 874509528, 'text': mapcss.tr(u'\'\'da\'\', \'\'de\'\' e \'\'do\'\' são minúsculos nos nomes em português')})

        # *[name=~/^[a-z].*/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_39d67968), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("nome iniciando com letra minúscula")
                err.append({'class': 9018002, 'subclass': 2073274467, 'text': mapcss.tr(u'nome iniciando com letra minúscula')})

        # *[alt_ref][inside("BR")]
        if (u'alt_ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'alt_ref') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("o conteúdo de {0} deve fazer parte de ref, separado por ;","{0.key}")
                # suggestAlternative:"ref"
                err.append({'class': 9018039, 'subclass': 836388143, 'text': mapcss.tr(u'o conteúdo de {0} deve fazer parte de ref, separado por ;', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way[highway=path][tracktype][inside("BR")]
        if (u'highway' in keys and u'tracktype' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'path') and mapcss._tag_capture(capture_tags, 1, tags, u'tracktype') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("uso incorreto de {0}","{1.key}")
                # suggestAlternative:"trail_visibility"
                err.append({'class': 9018064, 'subclass': 1242889729, 'text': mapcss.tr(u'uso incorreto de {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # way[highway!=track][tracktype][inside("BR")]
        # Rule Blacklisted

        # *[surface][eval(number_of_tags())=1][inside("BR")]
        if (u'surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'surface') and len(tags) == 1 and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto incompleto: possui apenas {0}","{0.key}")
                err.append({'class': 9018041, 'subclass': 411244066, 'text': mapcss.tr(u'objeto incompleto: possui apenas {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name][surface][eval(number_of_tags())=2][inside("BR")]
        # *[name][website][eval(number_of_tags())=2][inside("BR")]
        if (u'name' in keys and u'surface' in keys) or (u'name' in keys and u'website' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'surface') and len(tags) == 2 and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'website') and len(tags) == 2 and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto incompleto: possui apenas {0} e {1}","{0.key}","{1.key}")
                err.append({'class': 9018042, 'subclass': 585137381, 'text': mapcss.tr(u'objeto incompleto: possui apenas {0} e {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # way[highway=~/^(living_street|pedestrian|residential|road|service|track)$/][ref][inside("BR")]
        if (u'highway' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_07f31a73), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'ref') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("a via deve ser ao menos tertiary")
                err.append({'class': 9018002, 'subclass': 728045324, 'text': mapcss.tr(u'a via deve ser ao menos tertiary')})

        # way[bridge][!layer][inside("BR")]
        # way[tunnel][!layer][inside("BR")]
        # Rule Blacklisted

        # *[leisure=pitch][sport=tennis][surface=unpaved][inside("BR")]
        if (u'leisure' in keys and u'sport' in keys and u'surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'pitch') and mapcss._tag_capture(capture_tags, 1, tags, u'sport') == mapcss._value_capture(capture_tags, 1, u'tennis') and mapcss._tag_capture(capture_tags, 2, tags, u'surface') == mapcss._value_capture(capture_tags, 2, u'unpaved') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("{0} com superfície incorreta","{2.key}")
                # suggestAlternative:"surface=clay"
                # fixAdd:"surface=clay"
                err.append({'class': 9018006, 'subclass': 990400213, 'text': mapcss.tr(u'{0} com superfície incorreta', mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'surface',u'clay']])
                }})

        # way[leisure=track][!area?][inside("BR")]:closed
        if (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'track') and not mapcss._tag_capture(capture_tags, 1, tags, u'area') in ('yes', 'true', '1') and mapcss.inside(self.father.config.options, u'BR') and nds[0] == nds[-1])
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("adicionar ''area=yes'' caso esteja representando uma área")
                err.append({'class': 9018002, 'subclass': 691633247, 'text': mapcss.tr(u'adicionar \'\'area=yes\'\' caso esteja representando uma área')})

        # *[amenity=fuel][name=~/(?i)(?u)\b(Ale|BR|Esso|Ipiranga|Petrobr(á|a)s|Shell|Texaco)\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'fuel') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_604bb645), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("o nome não deve conter a bandeira/marca do posto")
                # suggestAlternative:"brand"
                err.append({'class': 9018002, 'subclass': 1724035987, 'text': mapcss.tr(u'o nome não deve conter a bandeira/marca do posto')})

        # *[amenity=fuel][brand=BR][inside("BR")]
        if (u'amenity' in keys and u'brand' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'fuel') and mapcss._tag_capture(capture_tags, 1, tags, u'brand') == mapcss._value_capture(capture_tags, 1, u'BR') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("uso inconsistente de bandeira do posto")
                # suggestAlternative:"brand=Petrobras"
                # fixAdd:"brand=Petrobras"
                err.append({'class': 9018002, 'subclass': 435141543, 'text': mapcss.tr(u'uso inconsistente de bandeira do posto'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'brand',u'Petrobras']])
                }})

        # *[shop=gas][name=~/(?i)(?u)^(Brasilg(á|a)s|Consigaz|Copagaz|Liquig(á|a)s|Minasg(á|a)s|Nacional G(á|a)s|Supergasbras|Ultragaz)$/][inside("BR")]
        if (u'name' in keys and u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'gas') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_31732cd0), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("o nome não deve conter a bandeira/marca da loja")
                # suggestAlternative:"brand"
                err.append({'class': 9018002, 'subclass': 867102166, 'text': mapcss.tr(u'o nome não deve conter a bandeira/marca da loja')})

        # *[/_[0-9]$/][!"is_in:iso_3166_2"][inside("BR")]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_57b8ef8e) and not mapcss._tag_capture(capture_tags, 1, tags, u'is_in:iso_3166_2') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("chave inválida: {0}","{0.key}")
                err.append({'class': 9018022, 'subclass': 231229079, 'text': mapcss.tr(u'chave inválida: {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *["addr:housenumber"=~/(?i)^s(\.|-| )?\/?n\.?º?$/][!note][inside("BR")]
        if (u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_0b27200b), mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber')) and not mapcss._tag_capture(capture_tags, 1, tags, u'note') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("não utilizar ''{0}'' para locais sem número",tag("addr:housenumber"))
                # suggestAlternative:"note"
                # fixRemove:"addr:housenumber"
                # fixAdd:"note=Local sem número"
                err.append({'class': 9018006, 'subclass': 630415638, 'text': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', mapcss.tag(tags, u'addr:housenumber')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'note',u'Local sem número']]),
                    '-': ([
                    u'addr:housenumber'])
                }})

        # *["addr:housenumber"=~/(?i)^s(\.|-| )?\/?n\.?º?$/][note][inside("BR")]
        if (u'addr:housenumber' in keys and u'note' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_0b27200b), mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber')) and mapcss._tag_capture(capture_tags, 1, tags, u'note') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("não utilizar ''{0}'' para locais sem número",tag("addr:housenumber"))
                # suggestAlternative:"note"
                err.append({'class': 9018043, 'subclass': 1150070765, 'text': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', mapcss.tag(tags, u'addr:housenumber'))})

        # *[source=~/(?i)google/][inside("BR")]
        if (u'source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2e8e4f2b), mapcss._tag_capture(capture_tags, 0, tags, u'source')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("objeto contém Google como source")
                err.append({'class': 9018044, 'subclass': 1159310436, 'text': mapcss.tr(u'objeto contém Google como source')})

        # *[amenity=townhall][name=~/^(?i)(?u)c(â|a)mara\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'townhall') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_46ab4d8d), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("câmara de vereadores mapeada incorretamente")
                # suggestAlternative:"office=government + government=legislative"
                err.append({'class': 9018002, 'subclass': 532372413, 'text': mapcss.tr(u'câmara de vereadores mapeada incorretamente')})

        # *[office=government][government!=legislative][name=~/^(?i)(?u)c(â|a)mara\b/][inside("BR")]
        if (u'name' in keys and u'office' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'government') and mapcss._tag_capture(capture_tags, 1, tags, u'government') != mapcss._value_const_capture(capture_tags, 1, u'legislative', u'legislative') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_46ab4d8d), mapcss._tag_capture(capture_tags, 2, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("ausência de government=legislative")
                err.append({'class': 9018002, 'subclass': 2126685099, 'text': mapcss.tr(u'ausência de government=legislative')})

        # *[amenity=townhall][name=~/^(?i)(?u)c((â|a)me|ama)ra\b/][inside("BR")]
        # *[office=government][name=~/^(?i)(?u)c((â|a)me|ama)ra\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys) or (u'name' in keys and u'office' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'townhall') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_793b22ec), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'government') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_793b22ec), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("erro de ortografia em ''câmara''")
                err.append({'class': 9018002, 'subclass': 1277153079, 'text': mapcss.tr(u'erro de ortografia em \'\'câmara\'\'')})

        # *[name=~/(?i)^prefeitura\b/][amenity!=townhall][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7ec1fb9a), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'townhall', u'townhall') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("prefeitura possivelmente mapeada de forma incorreta")
                # suggestAlternative:"amenity=townhall"
                err.append({'class': 9018002, 'subclass': 1445137044, 'text': mapcss.tr(u'prefeitura possivelmente mapeada de forma incorreta')})

        # *[name=~/(?i)(?u)^paço\b/][amenity!=townhall][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_13f4c147), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'townhall', u'townhall') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("paço possivelmente mapeado de forma incorreta")
                # suggestAlternative:"amenity=townhall"
                err.append({'class': 9018002, 'subclass': 1169494638, 'text': mapcss.tr(u'paço possivelmente mapeado de forma incorreta')})

        # *[amenity=charging_station][inside("BR")]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'charging_station') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("possivelmente deve ser amenity=fuel")
                err.append({'class': 9018002, 'subclass': 2011797637, 'text': mapcss.tr(u'possivelmente deve ser amenity=fuel')})

        # *[name=~/(?i)^Borrach(aria|eiro)/][shop=tyres][!repair][inside("BR")]
        if (u'name' in keys and u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_126ba9a9), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'shop') == mapcss._value_capture(capture_tags, 1, u'tyres') and not mapcss._tag_capture(capture_tags, 2, tags, u'repair') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("borracharia sem ''repair=yes''")
                # suggestAlternative:"repair=yes"
                err.append({'class': 9018002, 'subclass': 1225518759, 'text': mapcss.tr(u'borracharia sem \'\'repair=yes\'\'')})

        # *[name=~/(?i)^Borrach(aria|eiro)/][shop!=tyres][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_126ba9a9), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'shop') != mapcss._value_const_capture(capture_tags, 1, u'tyres', u'tyres') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("borracharia sem ''shop=tyres''")
                # suggestAlternative:"shop=tyres"
                err.append({'class': 9018002, 'subclass': 755877630, 'text': mapcss.tr(u'borracharia sem \'\'shop=tyres\'\'')})

        # way[waterway=~/^(river|stream)$/][name][name!~/^(?U)(Água|Arroio|Cabeceira|Córrego|Furo|Grota|Igarapé|Lajeado|Paraná|Restinga|Riacho|Ribeirão|Rio|Sanga)\b/][inside("BR")]
        # way[waterway=~/^(river|stream)$/][alt_name][alt_name!~/^(?U)(Água|Arroio|Cabeceira|Córrego|Furo|Grota|Igarapé|Lajeado|Paraná|Restinga|Riacho|Ribeirão|Rio|Sanga)\b/][inside("BR")]
        if (u'alt_name' in keys and u'waterway' in keys) or (u'name' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_04873a60), mapcss._tag_capture(capture_tags, 0, tags, u'waterway')) and mapcss._tag_capture(capture_tags, 1, tags, u'name') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_280004fd, u'^(?U)(Água|Arroio|Cabeceira|Córrego|Furo|Grota|Igarapé|Lajeado|Paraná|Restinga|Riacho|Ribeirão|Rio|Sanga)\b'), mapcss._tag_capture(capture_tags, 2, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_04873a60), mapcss._tag_capture(capture_tags, 0, tags, u'waterway')) and mapcss._tag_capture(capture_tags, 1, tags, u'alt_name') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_280004fd, u'^(?U)(Água|Arroio|Cabeceira|Córrego|Furo|Grota|Igarapé|Lajeado|Paraná|Restinga|Riacho|Ribeirão|Rio|Sanga)\b'), mapcss._tag_capture(capture_tags, 2, tags, u'alt_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} com possível nome errado/incompleto",tag(waterway))
                err.append({'class': 9018002, 'subclass': 139982797, 'text': mapcss.tr(u'{0} com possível nome errado/incompleto', mapcss.tag(tags, u'waterway'))})

        # *[name=~/(?i)\bcoreto\b/][leisure!=bandstand][leisure!=park][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_6e34cd0f), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'leisure') != mapcss._value_const_capture(capture_tags, 1, u'bandstand', u'bandstand') and mapcss._tag_capture(capture_tags, 2, tags, u'leisure') != mapcss._value_const_capture(capture_tags, 2, u'park', u'park') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("coreto possivelmente classificado de forma incorreta")
                # suggestAlternative:"leisure=bandstand"
                err.append({'class': 9018002, 'subclass': 810497942, 'text': mapcss.tr(u'coreto possivelmente classificado de forma incorreta')})

        # *[leisure=recreation_ground][inside("BR")]
        if (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'recreation_ground') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} impreciso","{0.tag}")
                # suggestAlternative:"landuse=recreation_ground"
                # suggestAlternative:"leisure=park"
                err.append({'class': 9018002, 'subclass': 1594563801, 'text': mapcss.tr(u'{0} impreciso', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[leisure=recreation_ground][landuse=recreation_ground][inside("BR")]
        if (u'landuse' in keys and u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'recreation_ground') and mapcss._tag_capture(capture_tags, 1, tags, u'landuse') == mapcss._value_capture(capture_tags, 1, u'recreation_ground') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} supérfluo","{0.tag}")
                # fixRemove:"leisure"
                err.append({'class': 9018002, 'subclass': 627419845, 'text': mapcss.tr(u'{0} supérfluo', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'leisure'])
                }})

        # *["ref:vatin"]["ref:vatin"!~/^BR[0-9]{14}$/][inside("BR")]
        if (u'ref:vatin' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:vatin') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_524288b6, u'^BR[0-9]{14}$'), mapcss._tag_capture(capture_tags, 1, tags, u'ref:vatin')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("CNPJ diferente do formato BRxxxxxxxxxxxxxx")
                err.append({'class': 9018002, 'subclass': 1793026117, 'text': mapcss.tr(u'CNPJ diferente do formato BRxxxxxxxxxxxxxx')})

        # *["ref:vatin"=~/^[0-9]{2}\.[0-9]{3}\.[0-9]{3}\/[0-9]{4}-[0-9]{2}$/][inside("BR")]
        if (u'ref:vatin' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5ddbb7eb), mapcss._tag_capture(capture_tags, 0, tags, u'ref:vatin')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("formato do CNPJ pode ser melhorado em {0}","{0.key}")
                # fixAdd:concat("ref:vatin=BR",replace(replace(replace(tag("ref:vatin"),"/",""),".",""),"-",""))
                err.append({'class': 9018006, 'subclass': 1609978963, 'text': mapcss.tr(u'formato do CNPJ pode ser melhorado em {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'ref:vatin=BR', mapcss.replace(mapcss.replace(mapcss.replace(mapcss.tag(tags, u'ref:vatin'), u'/', u''), u'.', u''), u'-', u''))).split('=', 1)])
                }})

        # *["ref:vatin"=~/^(br|bR|Br)[0-9]{14}$/][inside("BR")]
        if (u'ref:vatin' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_408831d0), mapcss._tag_capture(capture_tags, 0, tags, u'ref:vatin')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("CNPJ deve iniciar maiúsculo: BRxxxxxxxxxxxxxx")
                # fixAdd:concat("ref:vatin=",upper(tag("ref:vatin")))
                err.append({'class': 9018006, 'subclass': 1616044431, 'text': mapcss.tr(u'CNPJ deve iniciar maiúsculo: BRxxxxxxxxxxxxxx'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'ref:vatin=', mapcss.upper(mapcss.tag(tags, u'ref:vatin')))).split('=', 1)])
                }})

        # *[phone][phone!~/^(\+55|0800)/][inside("BR")]
        # *["contact:phone"]["contact:phone"!~/^(\+55|0800)/][inside("BR")]
        if (u'contact:phone' in keys) or (u'phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'phone') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_243f4993, u'^(\+55|0800)'), mapcss._tag_capture(capture_tags, 1, tags, u'phone')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'contact:phone') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_243f4993, u'^(\+55|0800)'), mapcss._tag_capture(capture_tags, 1, tags, u'contact:phone')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} em formato diferente do internacional +55 XX YYYY-YYYY","{0.key}")
                err.append({'class': 9018002, 'subclass': 1438682200, 'text': mapcss.tr(u'{0} em formato diferente do internacional +55 XX YYYY-YYYY', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[phone=~/^(100|18{0,1}|19[0-9])$/][inside("BR")]
        # *["contact:phone"=~/^(100|18{0,1}|19[0-9])$/][inside("BR")]
        if (u'contact:phone' in keys) or (u'phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7a246e93), mapcss._tag_capture(capture_tags, 0, tags, u'phone')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7a246e93), mapcss._tag_capture(capture_tags, 0, tags, u'contact:phone')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("não usar número de emergência em {0}","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9018002, 'subclass': 371146161, 'text': mapcss.tr(u'não usar número de emergência em {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # relation[highway][name=~/\b[A-Z]{2,3} (- )?[0-9]{2,3}\b/][inside("BR")]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_073e5345), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("rodovia com ref no nome")
                err.append({'class': 9018002, 'subclass': 1625358529, 'text': mapcss.tr(u'rodovia com ref no nome')})

        # *["addr:street"]["addr:street"!~/^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Calçadão|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodovia|Rotatória|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*/][inside("BR")]
        if (u'addr:street' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'addr:street') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_6bf570a0, u'^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Calçadão|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodovia|Rotatória|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*'), mapcss._tag_capture(capture_tags, 1, tags, u'addr:street')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} com logradouro ausente, errado ou abreviado","{0.key}")
                err.append({'class': 9018002, 'subclass': 279840772, 'text': mapcss.tr(u'{0} com logradouro ausente, errado ou abreviado', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[!highway][route!=road][!public_transport][type!~/route|street/][name][name=~/^(?i)(?u)(alameda|avenida|beco|estrada|ladeira|passarela|rodovia|rotatória|rua|travessa|trevo|viela|(anel|complexo|dispositivo) viário) .*/][name!~/^(?i)estrada de ferro/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'route') != mapcss._value_const_capture(capture_tags, 1, u'road', u'road') and not mapcss._tag_capture(capture_tags, 2, tags, u'public_transport') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 3, self.re_72d45155, u'route|street'), mapcss._tag_capture(capture_tags, 3, tags, u'type')) and mapcss._tag_capture(capture_tags, 4, tags, u'name') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 5, self.re_5849be19), mapcss._tag_capture(capture_tags, 5, tags, u'name')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 6, self.re_15690541, u'^(?i)estrada de ferro'), mapcss._tag_capture(capture_tags, 6, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("objeto com nome de via mas sem tag de {0}","{0.key}")
                err.append({'class': 9018002, 'subclass': 535280341, 'text': mapcss.tr(u'objeto com nome de via mas sem tag de {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name=~/^(?i)(?u)[a-z0-9]+_([a-z0-9]_?)+$/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_4bd3b925), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("utilizar espaço ao invés de underscore")
                err.append({'class': 9018002, 'subclass': 1476954926, 'text': mapcss.tr(u'utilizar espaço ao invés de underscore')})

        # *[name=~/(?i)(^|.* )(Cel|Cmte|Cond|Conj|Dª|Dr|Eng|Gov|Hab|Jd|Jr|Marg|Mun|p\/|Pde|Pe|Pq|Pst|Pref|Profa|Profª|Prof|Res|s\/|Sr(a|ª)?|Sta|Sto|Ver)\.? .*/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_178f5446), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("palavra abreviada em {0}","{0.key}")
                err.append({'class': 9018003, 'subclass': 749019091, 'text': mapcss.tr(u'palavra abreviada em {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[leisure][name=~/^(?i)(?u)(campo|est(á|a)dio|gin(á|a)sio|quadra)( de (futebol|esportes?))?$/][inside("BR")]
        if (u'leisure' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7f53e992), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("nome supérfluo/incompleto de local de lazer")
                err.append({'class': 9018004, 'subclass': 1485441713, 'text': mapcss.tr(u'nome supérfluo/incompleto de local de lazer')})

        # *[name=~/^(?i)(?u)((Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF|hospital)$/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_52ab3b8b), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("nome supérfluo/incompleto de local de saúde")
                err.append({'class': 9018005, 'subclass': 1497769259, 'text': mapcss.tr(u'nome supérfluo/incompleto de local de saúde')})

        # *[amenity=~/^(clinic|doctors|hospital)$/][name=~/(?i)\bsaude\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5ab76b11), mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_4cf86823), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("erro de ortografia em ''saúde''")
                err.append({'class': 9018002, 'subclass': 1962359328, 'text': mapcss.tr(u'erro de ortografia em \'\'saúde\'\'')})

        # *[place=farm][name^="Sitio "][inside("BR")]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'farm') and mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, u'name'), mapcss._value_capture(capture_tags, 1, u'Sitio ')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("faltando acento em ''Sítio''")
                err.append({'class': 9018002, 'subclass': 653860263, 'text': mapcss.tr(u'faltando acento em \'\'Sítio\'\'')})

        # *[name=~/^(?i)(?u)(aldeia|borrach(aria|eiro)|bosque|capela|cemit(é|e)rio|c(ó|o)rrego|escola|estacionamento|fazenda|floresta|hospital|igreja|lago|lagoa|mata( nativa)?|praça|parque|parquinho|posto( de gasolina)?|riacho|rio|rodovi(á|a)ria|vila)$/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_20c7dd98), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("local com nome supérfluo, incompleto ou descritivo")
                err.append({'class': 9018002, 'subclass': 1104230922, 'text': mapcss.tr(u'local com nome supérfluo, incompleto ou descritivo')})

        # *[amenity=parking][name=~/(?i)^Estacionamento /][inside("BR")]
        # Rule Blacklisted

        # relation[type=route][highway][inside("BR")]
        if (u'highway' in keys and u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'route') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("relação não deve possuir {0}","{1.key}")
                err.append({'class': 9018046, 'subclass': 954714547, 'text': mapcss.tr(u'relação não deve possuir {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[designation=*"addr:housename"][inside("BR")]
        # *[ref=*designation][inside("BR")]
        # *[ref=*old_ref][inside("BR")]
        # *[name=*"addr:housename"][inside("BR")]
        # *[name=*designation][inside("BR")]
        # *[name=*alt_name][inside("BR")]
        # *[name=*int_name][inside("BR")]
        # *[name=*loc_name][inside("BR")]
        # *[name=*nat_name][inside("BR")]
        # *[name=*official_name][inside("BR")]
        # *[name=*old_name][inside("BR")]
        # *[name=*reg_name][inside("BR")]
        # *[name=*short_name][inside("BR")]
        # *[name=*sorting_name][inside("BR")]
        if (u'designation' in keys) or (u'name' in keys) or (u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'designation') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'addr:housename')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'designation')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'old_ref')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'addr:housename')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'designation')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'alt_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'int_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'loc_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'nat_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'official_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'old_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'reg_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'short_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'sorting_name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("{0} e {1} são iguais; remover chave {1} desnecessária","{0.key}","{0.value}")
                # fixRemove:"{0.value}"
                err.append({'class': 9018006, 'subclass': 2003922, 'text': mapcss.tr(u'{0} e {1} são iguais; remover chave {1} desnecessária', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.value}')])
                }})

        # *[source=*name][inside("BR")]
        if (u'source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} e {1} são iguais","{0.key}","{0.value}")
                err.append({'class': 9018002, 'subclass': 470146003, 'text': mapcss.tr(u'{0} e {1} são iguais', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[name=~/(?i)(?u)((sem (denomina(ç|c)(ã|a)o|nome|sa(i|í)da))|desconhecido|n(ã|a)o conhecido)/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_65710fdb), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto com nomenclatura incorreta")
                # suggestAlternative:"noname"
                err.append({'class': 9018007, 'subclass': 1272098213, 'text': mapcss.tr(u'objeto com nomenclatura incorreta')})

        # *[designation][inside("BR")]
        if (u'designation' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'designation') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} é uma chave utilizada apenas no Reino Unido","{0.key}")
                # suggestAlternative:"description"
                # suggestAlternative:"name"
                err.append({'class': 9018009, 'subclass': 1818234763, 'text': mapcss.tr(u'{0} é uma chave utilizada apenas no Reino Unido', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[place=~/hamlet|isolated_dwelling|town|village/][population>=100000][inside("BR")]
        if (u'place' in keys and u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_152c10ee), mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'population') >= mapcss._value_capture(capture_tags, 1, 100000) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("local com 100.000 habitantes ou mais deve ser classificado como city")
                # fixAdd:"place=city"
                err.append({'class': 9018006, 'subclass': 1009134521, 'text': mapcss.tr(u'local com 100.000 habitantes ou mais deve ser classificado como city'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'place',u'city']])
                }})

        # *[place=~/city|hamlet|isolated_dwelling|village/][population>=10000][population<100000][inside("BR")]
        if (u'place' in keys and u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_591572a5), mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'population') >= mapcss._value_capture(capture_tags, 1, 10000) and mapcss._tag_capture(capture_tags, 2, tags, u'population') < mapcss._value_capture(capture_tags, 2, 100000) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("local com população entre 10.000 e 100.000 deve ser classificado como town")
                # fixAdd:"place=town"
                err.append({'class': 9018006, 'subclass': 1343568198, 'text': mapcss.tr(u'local com população entre 10.000 e 100.000 deve ser classificado como town'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'place',u'town']])
                }})

        # *[place][place!~/hamlet|island|isolated_dwelling|neighbourhood|suburb|village/][population<10000][inside("BR")]
        if (u'place' in keys and u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_3aeda39d, u'hamlet|island|isolated_dwelling|neighbourhood|suburb|village'), mapcss._tag_capture(capture_tags, 1, tags, u'place')) and mapcss._tag_capture(capture_tags, 2, tags, u'population') < mapcss._value_capture(capture_tags, 2, 10000) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("local com menos de 10.000 habitantes deve ser classificado como village")
                # fixAdd:"place=village"
                err.append({'class': 9018006, 'subclass': 409005616, 'text': mapcss.tr(u'local com menos de 10.000 habitantes deve ser classificado como village'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'place',u'village']])
                }})

        # *[place=city][!population][inside("BR")]
        # *[place=town][!population][inside("BR")]
        # *[place=village][!population][inside("BR")]
        # Rule Blacklisted

        # *[place=city][!name][inside("BR")]
        # *[place=town][!name][inside("BR")]
        # *[place=village][!name][inside("BR")]
        if (u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'city') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'town') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'village') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} sem nome","{0.value}")
                err.append({'class': 9018012, 'subclass': 1473808194, 'text': mapcss.tr(u'{0} sem nome', mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *["addr:city"=~/(,|( |-) ?[A-Z]{2})/][inside("BR")]
        if (u'addr:city' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_10f1c360), mapcss._tag_capture(capture_tags, 0, tags, u'addr:city')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve conter apenas o nome da cidade","{0.key}")
                err.append({'class': 9018013, 'subclass': 1479274467, 'text': mapcss.tr(u'{0} deve conter apenas o nome da cidade', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name=~/^(?i)(?u)(Faz\.|Fazenda|Sítio|Chácara)/][place][place!~/city|farm|neighbourhood|suburb|town|village/][inside("BR")]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2cd1e949), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'place') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_5d3348cb, u'city|farm|neighbourhood|suburb|town|village'), mapcss._tag_capture(capture_tags, 2, tags, u'place')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("objeto talvez deva ser {0}=farm","{1.key}")
                err.append({'class': 9018002, 'subclass': 337742963, 'text': mapcss.tr(u'objeto talvez deva ser {0}=farm', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[place][name=~/^(?i)Bairro\b/][name!~/^(?i)Bairro d(a|e|o)s?\b/][inside("BR")]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_20fc5143), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 2, self.re_64387998, u'^(?i)Bairro d(a|e|o)s?\b'), mapcss._tag_capture(capture_tags, 2, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("objeto talvez não deva ter ''Bairro'' no nome")
                err.append({'class': 9018002, 'subclass': 1441242115, 'text': mapcss.tr(u'objeto talvez não deva ter \'\'Bairro\'\' no nome')})

        # *[iata="0"][inside("BR")]
        if (u'iata' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'iata') == mapcss._value_capture(capture_tags, 0, u'0') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} com valor = {1}","{0.key}","{0.value}")
                err.append({'class': 9018014, 'subclass': 1098244333, 'text': mapcss.tr(u'{0} com valor = {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[amenity=~/college|school/][name=~/^(?i)(?u)(Centro Universitário|Faculdades?|FATEC|Instituto Federal)\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_362f879f), mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_1d232d4c), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("estabelecimento de ensino classificado incorretamente")
                # suggestAlternative:"amenity=university"
                # fixAdd:"{0.key}=university"
                err.append({'class': 9018006, 'subclass': 1605707172, 'text': mapcss.tr(u'estabelecimento de ensino classificado incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=university')).split('=', 1)])
                }})

        # *[amenity=school][name=~/^(?i)(?u)(SENAC|SENAI|Serviço Nacional de Aprendizagem)/][inside("BR")]
        # *[amenity=~/school|university/][name=~/(?i)(?u)\b(Centro Paula Souza|Escola Técnica|ETEC)\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'school') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_044c8944), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_6c0d6e9e), mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3b304b9b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("estabelecimento de ensino classificado incorretamente")
                # suggestAlternative:"amenity=college"
                # fixAdd:"{0.key}=college"
                err.append({'class': 9018006, 'subclass': 1282773099, 'text': mapcss.tr(u'estabelecimento de ensino classificado incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=college')).split('=', 1)])
                }})

        # *[amenity=school][name=~/^(?i)(?u)(auto(-| )?( moto )?escola|centro de formação de condutores|cfc|moto escola)\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'school') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_35bb0f2f), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("autoescola classificada incorretamente")
                # suggestAlternative:"amenity=driving_school"
                # fixAdd:"{0.key}=driving_school"
                err.append({'class': 9018006, 'subclass': 566309924, 'text': mapcss.tr(u'autoescola classificada incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=driving_school')).split('=', 1)])
                }})

        # *[amenity=school][name=~/^(?i)creche\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'school') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_160d1bfc), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("creche classificada incorretamente")
                # suggestAlternative:"amenity=kindergarten"
                # fixAdd:"{0.key}=kindergarten"
                err.append({'class': 9018006, 'subclass': 1847987722, 'text': mapcss.tr(u'creche classificada incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=kindergarten')).split('=', 1)])
                }})

        # *[name=~/^(?i)(?u)Subestação .*/][power][power!=substation][inside("BR")]
        # *[name=~/^(?i)(?u)Fórum .*/][amenity][amenity!=courthouse][inside("BR")]
        # *[name=~/^(?i)Hospital .*/][building][building!=hospital][inside("BR")]
        # *[name=~/^(?i)Universidade .*/][building][building!=university][inside("BR")]
        # *[name=~/^(?i)Escola .*/][building][building!=school][inside("BR")]
        # *[name=~/^(?i)Hotel .*/][building][building!=hotel][inside("BR")]
        # *[name=~/^(?i)Capela .*/][building][building!=chapel][inside("BR")]
        # *[name=~/^(?i)Igreja .*/][building][building!=church][inside("BR")]
        # *[name=~/^(?i)Catedral .*/][building][building!=cathedral][inside("BR")]
        # *[name=~/^(?i)Fazenda .*/][building][building!=farm][inside("BR")]
        # *[name=~/^(?i)Supermercado .*/][building][building!=supermarket][inside("BR")]
        # Rule Blacklisted

        # *[name=~/^(?i)(?u)(AM(A|E)|(Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF).*/][amenity=hospital][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7b7c453d), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') == mapcss._value_capture(capture_tags, 1, u'hospital') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("postos/unidades de saúde devem ser amenity=clinic")
                # fixAdd:"amenity=clinic"
                err.append({'class': 9018006, 'subclass': 74419437, 'text': mapcss.tr(u'postos/unidades de saúde devem ser amenity=clinic'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'amenity',u'clinic']])
                }})

        # *[name=~/^(?i)\bSAMU\b/][amenity=~/clinic|doctors|hospital/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2dbaea13), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_3eb0ab44), mapcss._tag_capture(capture_tags, 1, tags, u'amenity')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("SAMU classificado de forma errada")
                # suggestAlternative:"emergency=ambulance_station"
                err.append({'class': 9018016, 'subclass': 392029310, 'text': mapcss.tr(u'SAMU classificado de forma errada')})

        # relation[highway=give_way][inside("BR")]
        # relation[highway=mini_roundabout][inside("BR")]
        # relation[highway=stop][inside("BR")]
        # relation[highway=turning_circle][inside("BR")]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'give_way') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'mini_roundabout') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'stop') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'turning_circle') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve ser utilizado apenas em nós","{0.tag}")
                err.append({'class': 9018047, 'subclass': 484299691, 'text': mapcss.tr(u'{0} deve ser utilizado apenas em nós', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # relation[enforcement=maxspeed][!maxspeed][inside("BR")]
        # relation[enforcement=maxheight][!maxheight][inside("BR")]
        # relation[enforcement=maxweight][!maxweight][inside("BR")]
        if (u'enforcement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'enforcement') == mapcss._value_capture(capture_tags, 0, u'maxspeed') and not mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'enforcement') == mapcss._value_capture(capture_tags, 0, u'maxheight') and not mapcss._tag_capture(capture_tags, 1, tags, u'maxheight') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'enforcement') == mapcss._value_capture(capture_tags, 0, u'maxweight') and not mapcss._tag_capture(capture_tags, 1, tags, u'maxweight') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("adicionar {0} ao {1}","{1.key}","{0.tag}")
                err.append({'class': 9018018, 'subclass': 24087693, 'text': mapcss.tr(u'adicionar {0} ao {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[crossing][!highway][!railway][inside("BR")]
        if (u'crossing' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'crossing') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve ser utilizado com {1}={0} ou {2}={0}","{0.key}","{1.key}","{2.key}")
                err.append({'class': 9018019, 'subclass': 2098306424, 'text': mapcss.tr(u'{0} deve ser utilizado com {1}={0} ou {2}={0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[aeroway][designation=~/^[A-Z]{4}$/][!icao][inside("BR")]
        # *[aeroway][ref=~/^[A-Z]{4}$/][!icao][inside("BR")]
        if (u'aeroway' in keys and u'designation' in keys) or (u'aeroway' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7afc6883), mapcss._tag_capture(capture_tags, 1, tags, u'designation')) and not mapcss._tag_capture(capture_tags, 2, tags, u'icao') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_7afc6883), mapcss._tag_capture(capture_tags, 1, tags, u'ref')) and not mapcss._tag_capture(capture_tags, 2, tags, u'icao') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("{0} provavelmente deve ser utilizado como {1}","{1.key}","{2.key}")
                # fixChangeKey:"{1.key} => {2.key}"
                err.append({'class': 9018006, 'subclass': 619372172, 'text': mapcss.tr(u'{0} provavelmente deve ser utilizado como {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, u'{1.key} => {2.key}')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, u'{1.key} => {2.key}')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, u'{1.key} => {2.key}')).split('=>', 1)[0].strip()])
                }})

        # *[access=permissive][inside("BR")]
        if (u'access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'permissive') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} deve ser utilizado apenas em vias privadas com permissão de acesso e não em vias de acesso público","{0.tag}")
                err.append({'class': 9018002, 'subclass': 1240816112, 'text': mapcss.tr(u'{0} deve ser utilizado apenas em vias privadas com permissão de acesso e não em vias de acesso público', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[name=~/^(?U)(\p{Upper}| )+$/][inside("BR")]
        # *["addr:street"=~/^(?U)(\p{Upper}| )+$/][inside("BR")]
        # Rule Blacklisted

        # *["addr:postcode"=~/^[0-9]{8}$/][inside("BR")]
        # Rule Blacklisted

        # *[postal_code=~/^[0-9]{8}$/][inside("BR")]
        # Rule Blacklisted

        # *["addr:postcode"=~/^[0-9]{5}( |\.)[0-9]{3}$/][inside("BR")]
        if (u'addr:postcode' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_57bee688), mapcss._tag_capture(capture_tags, 0, tags, u'addr:postcode')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("formato do CEP pode ser melhorado")
                # fixAdd:concat("addr:postcode=",replace(replace(tag("addr:postcode")," ","-"),".","-"))
                err.append({'class': 9018006, 'subclass': 1667206075, 'text': mapcss.tr(u'formato do CEP pode ser melhorado'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'addr:postcode=', mapcss.replace(mapcss.replace(mapcss.tag(tags, u'addr:postcode'), u' ', u'-'), u'.', u'-'))).split('=', 1)])
                }})

        # *["postal_code"=~/^[0-9]{5}( |\.)[0-9]{3}$/][inside("BR")]
        if (u'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_57bee688), mapcss._tag_capture(capture_tags, 0, tags, u'postal_code')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("formato do CEP pode ser melhorado")
                # fixAdd:concat("postal_code=",replace(replace(tag("postal_code")," ","-"),".","-"))
                err.append({'class': 9018006, 'subclass': 1977906896, 'text': mapcss.tr(u'formato do CEP pode ser melhorado'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'postal_code=', mapcss.replace(mapcss.replace(mapcss.tag(tags, u'postal_code'), u' ', u'-'), u'.', u'-'))).split('=', 1)])
                }})

        # *["addr:postcode"]["addr:postcode"!~/^[0-9]{5}-[0-9]{3}$/][inside("BR")]
        # *[postal_code][postal_code!~/^[0-9]{5}-[0-9]{3}$/][inside("BR")]
        # Rule Blacklisted

        # *[alt_source][source][inside("BR")]
        if (u'alt_source' in keys and u'source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'alt_source') and mapcss._tag_capture(capture_tags, 1, tags, u'source') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve estar incluído em {1}, separado por '';'' caso necessário","{0.key}","{1.key}")
                err.append({'class': 9018020, 'subclass': 472956812, 'text': mapcss.tr(u'{0} deve estar incluído em {1}, separado por \'\';\'\' caso necessário', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[landuse?][inside("BR")]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') in ('yes', 'true', '1') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("especificar valor correto para {0} ao invés de ''{1}''","{0.key}",tag("landuse"))
                err.append({'class': 9018021, 'subclass': 6418462, 'text': mapcss.tr(u'especificar valor correto para {0} ao invés de \'\'{1}\'\'', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss.tag(tags, u'landuse'))})

        # *[long_name][inside("BR")]
        if (u'long_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'long_name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("chave inválida: {0}","{0.key}")
                # suggestAlternative:"alt_name"
                # suggestAlternative:"name"
                # suggestAlternative:"official_name"
                err.append({'class': 9018022, 'subclass': 1737555221, 'text': mapcss.tr(u'chave inválida: {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *["building:levels"<1][inside("BR")]
        if (u'building:levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:levels') < mapcss._value_capture(capture_tags, 0, 1) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} com valor inválido","{0.key}")
                err.append({'class': 9018002, 'subclass': 775859422, 'text': mapcss.tr(u'{0} com valor inválido', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[hires?][inside("BR")]
        if (u'hires' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'hires') in ('yes', 'true', '1') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("não se deve utilizar {0} para demarcar áreas de cobertura de imagem","{0.key}")
                err.append({'class': 9018023, 'subclass': 895278192, 'text': mapcss.tr(u'não se deve utilizar {0} para demarcar áreas de cobertura de imagem', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[tourism=motel][amenity!=love_hotel][inside("BR")]
        # *[name=~/(?i)\bmotel\b/][amenity!=love_hotel][inside("BR")]
        if (u'name' in keys) or (u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == mapcss._value_capture(capture_tags, 0, u'motel') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'love_hotel', u'love_hotel') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_01454d46), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'love_hotel', u'love_hotel') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("ausência de tag ''{0}''","{1.value}")
                # fixAdd:"{1.key}={1.value}"
                err.append({'class': 9018006, 'subclass': 1987370859, 'text': mapcss.tr(u'ausência de tag \'\'{0}\'\'', mapcss._tag_uncapture(capture_tags, u'{1.value}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{1.key}={1.value}')).split('=', 1)])
                }})

        # *[amenity=love_hotel][tourism][tourism!=motel][inside("BR")]
        if (u'amenity' in keys and u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'love_hotel') and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') and mapcss._tag_capture(capture_tags, 2, tags, u'tourism') != mapcss._value_const_capture(capture_tags, 2, u'motel', u'motel') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("provavelmente deve ser ''{0}={1}''","{2.key}","{2.value}")
                err.append({'class': 9018002, 'subclass': 1760828878, 'text': mapcss.tr(u'provavelmente deve ser \'\'{0}={1}\'\'', mapcss._tag_uncapture(capture_tags, u'{2.key}'), mapcss._tag_uncapture(capture_tags, u'{2.value}'))})

        # *[name=~/(?i)^motel\b/][tourism!=motel][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5cd37790), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') != mapcss._value_const_capture(capture_tags, 1, u'motel', u'motel') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("motel classificado incorretamente")
                # suggestAlternative:"tourism=motel"
                err.append({'class': 9018002, 'subclass': 1456128106, 'text': mapcss.tr(u'motel classificado incorretamente')})

        # *[aeroway=aerodrome][name=~/(?i).*airport$/][inside("BR")]
        # *[aeroway=helipad][name=~/(?i).*heliport$/][inside("BR")]
        if (u'aeroway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'aerodrome') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6efb8049), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'helipad') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6566db6a), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} com nome em inglês","{0.tag}")
                err.append({'class': 9018002, 'subclass': 1743601177, 'text': mapcss.tr(u'{0} com nome em inglês', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[aeroway=aerodrome][name=~/(?i)^Aer(ódromo|oporto) de.*/][inside("BR")]
        # *[aeroway=helipad][name=~/(?i)^Helipo(n|r)to.*/][inside("BR")]
        if (u'aeroway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'aerodrome') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_6024a566), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'helipad') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_139e342b), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("conferir se existe nome oficial do {0}","{0.value}")
                err.append({'class': 9018002, 'subclass': 136467214, 'text': mapcss.tr(u'conferir se existe nome oficial do {0}', mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[aeroway=aerodrome][ref][inside("BR")]
        if (u'aeroway' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'aerodrome') and mapcss._tag_capture(capture_tags, 1, tags, u'ref') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("''{0}'' não faz sentido em aeroporto","{1.key}")
                err.append({'class': 9018002, 'subclass': 1633437696, 'text': mapcss.tr(u'\'\'{0}\'\' não faz sentido em aeroporto', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[waterway][layer<0][!tunnel][inside("BR")]
        if (u'layer' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'layer') < mapcss._value_capture(capture_tags, 1, 0) and not mapcss._tag_capture(capture_tags, 2, tags, u'tunnel') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} negativo de {1} com ausência de {2}","{1.key}","{0.key}","{2.key}")
                err.append({'class': 9018002, 'subclass': 203420779, 'text': mapcss.tr(u'{0} negativo de {1} com ausência de {2}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[waterway][layer>0][!bridge][inside("BR")]
        if (u'layer' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'layer') > mapcss._value_capture(capture_tags, 1, 0) and not mapcss._tag_capture(capture_tags, 2, tags, u'bridge') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} positivo de {1} com ausência de {2}","{1.key}","{0.key}","{2.key}")
                err.append({'class': 9018002, 'subclass': 1870051659, 'text': mapcss.tr(u'{0} positivo de {1} com ausência de {2}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[layer][!building][!highway][man_made!=pipeline][!railway][!waterway][power!=line][inside("BR")]
        # Rule Blacklisted

        # *[name=~/^(?i)(?u)edifício.*/][!building][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_38a8f0ff), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("possível ausência de tag {0}","{1.key}")
                err.append({'class': 9018026, 'subclass': 1332986859, 'text': mapcss.tr(u'possível ausência de tag {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[route=ferry][!duration][inside("BR")]
        if (u'route' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'route') == mapcss._value_capture(capture_tags, 0, u'ferry') and not mapcss._tag_capture(capture_tags, 1, tags, u'duration') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("ausência do tempo de duração ({0}) da balsa","{1.key}")
                err.append({'class': 9018027, 'subclass': 1343391603, 'text': mapcss.tr(u'ausência do tempo de duração ({0}) da balsa', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[name=~/^(?i)(?u)praça.*/][!leisure][landuse=~/^(forest|grass|greenfield|meadow|orchard)$/][inside("BR")]
        # *[name=~/^(?i)(?u)praça.*/][!leisure][natural=~/^(grassland|heath|scrub|wood)$/][inside("BR")]
        if (u'landuse' in keys and u'name' in keys) or (u'name' in keys and u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_4a8ca94e), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'leisure') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_05a345c7), mapcss._tag_capture(capture_tags, 2, tags, u'landuse')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_4a8ca94e), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'leisure') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_12b48afb), mapcss._tag_capture(capture_tags, 2, tags, u'natural')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("possível definição incorreta para praça: ''{0}''","{2.key}")
                # suggestAlternative:"leisure=park"
                err.append({'class': 9018029, 'subclass': 181066872, 'text': mapcss.tr(u'possível definição incorreta para praça: \'\'{0}\'\'', mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[wikipedia][wikipedia!~/^pt:/][inside("BR")]
        if (u'wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_17fd35b3, u'^pt:'), mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("utilizar prefixo em português (pt:) para {0}","{0.key}")
                err.append({'class': 9018030, 'subclass': 1431112366, 'text': mapcss.tr(u'utilizar prefixo em português (pt:) para {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name=~/.*\(.*\).*/][inside("BR")]
        # Rule Blacklisted

        # *[name=~/ - /][inside("BR")]
        # Rule Blacklisted

        # *[name=~/, /][inside("BR")]
        # Rule Blacklisted

        # *[name=~/: /][inside("BR")]
        # Rule Blacklisted

        # *[name=~/ ou /][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_131cc885), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("nome utilizado de forma incorreta")
                # suggestAlternative:"name e alt_name"
                err.append({'class': 9018031, 'subclass': 115703372, 'text': mapcss.tr(u'nome utilizado de forma incorreta')})

        # relation[boundary][type!=boundary][inside("BR")]
        if (u'boundary' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') and mapcss._tag_capture(capture_tags, 1, tags, u'type') != mapcss._value_const_capture(capture_tags, 1, u'boundary', u'boundary') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve possuir ''type=boundary''","{0.key}")
                err.append({'class': 9018048, 'subclass': 1926430386, 'text': mapcss.tr(u'{0} deve possuir \'\'type=boundary\'\'', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # relation[type=boundary][!boundary][inside("BR")]
        if (u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'boundary') and not mapcss._tag_capture(capture_tags, 1, tags, u'boundary') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve ser utilizado junto com {1}","{0.tag}","{1.key}")
                err.append({'class': 9018049, 'subclass': 1270177491, 'text': mapcss.tr(u'{0} deve ser utilizado junto com {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # relation[admin_level][boundary!=administrative][inside("BR")]
        if (u'admin_level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'admin_level') and mapcss._tag_capture(capture_tags, 1, tags, u'boundary') != mapcss._value_const_capture(capture_tags, 1, u'administrative', u'administrative') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwError:tr("ausência de boundary=administrative")
                # fixAdd:"boundary=administrative"
                err.append({'class': 9018006, 'subclass': 1136060061, 'text': mapcss.tr(u'ausência de boundary=administrative'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'boundary',u'administrative']])
                }})

        # relation[boundary=administrative][!admin_level][inside("BR")]
        if (u'boundary' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'administrative') and not mapcss._tag_capture(capture_tags, 1, tags, u'admin_level') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
                err.append({'class': 9018033, 'subclass': 802276360, 'text': mapcss.tr(u'{0} deve possuir {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # relation[place][place!~/^(city_block|farm|hamlet|island|islet|isolated_dwelling|neighbourhood|square)$/][!admin_level][!boundary][inside("BR")]
        if (u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_58f616c9, u'^(city_block|farm|hamlet|island|islet|isolated_dwelling|neighbourhood|square)$'), mapcss._tag_capture(capture_tags, 1, tags, u'place')) and not mapcss._tag_capture(capture_tags, 2, tags, u'admin_level') and not mapcss._tag_capture(capture_tags, 3, tags, u'boundary') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("local com ausência/incoerência de limite administrativo")
                err.append({'class': 9018002, 'subclass': 1689081650, 'text': mapcss.tr(u'local com ausência/incoerência de limite administrativo')})

        # relation[boundary=administrative][type=multipolygon][inside("BR")]
        if (u'boundary' in keys and u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'administrative') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'multipolygon') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwError:tr("relação deve ser do tipo ''type=boundary''")
                # fixAdd:"type=boundary"
                err.append({'class': 9018006, 'subclass': 238210452, 'text': mapcss.tr(u'relação deve ser do tipo \'\'type=boundary\'\''), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'type',u'boundary']])
                }})

        # *[boundary=national_park][!name][inside("BR")]
        # *[boundary=protected_area][!name][inside("BR")]
        # *[leisure=nature_reserve][!name][inside("BR")]
        if (u'boundary' in keys) or (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'national_park') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'protected_area') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'nature_reserve') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
                err.append({'class': 9018033, 'subclass': 1196875584, 'text': mapcss.tr(u'{0} deve possuir {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[boundary=protected_area][!protect_class][inside("BR")]
        if (u'boundary' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'protected_area') and not mapcss._tag_capture(capture_tags, 1, tags, u'protect_class') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
                err.append({'class': 9018033, 'subclass': 1593244126, 'text': mapcss.tr(u'{0} deve possuir {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[protect_class][protect_class!~/^(1(a|b)?|[1-9][0-9]?)$/][inside("BR")]
        if (u'protect_class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'protect_class') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_5ac7053e, u'^(1(a|b)?|[1-9][0-9]?)$'), mapcss._tag_capture(capture_tags, 1, tags, u'protect_class')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("valor incorreto para {0}","{0.key}")
                err.append({'class': 9018034, 'subclass': 1183781531, 'text': mapcss.tr(u'valor incorreto para {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[protect_class][boundary!=protected_area][inside("BR")]
        if (u'protect_class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'protect_class') and mapcss._tag_capture(capture_tags, 1, tags, u'boundary') != mapcss._value_const_capture(capture_tags, 1, u'protected_area', u'protected_area') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("ausência de boundary=protected_area")
                err.append({'class': 9018035, 'subclass': 1649283274, 'text': mapcss.tr(u'ausência de boundary=protected_area')})

        # relation[destination][type!=waterway][inside("BR")]
        if (u'destination' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'destination') and mapcss._tag_capture(capture_tags, 1, tags, u'type') != mapcss._value_const_capture(capture_tags, 1, u'waterway', u'waterway') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve ser usado apenas em ways","{0.key}")
                err.append({'class': 9018036, 'subclass': 1899110172, 'text': mapcss.tr(u'{0} deve ser usado apenas em ways', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name=~/.* D(a|e|o)s? .*/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2ffc377d), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("''da'', ''de'' e ''do'' são minúsculos nos nomes em português")
                err.append({'class': 9018002, 'subclass': 874509528, 'text': mapcss.tr(u'\'\'da\'\', \'\'de\'\' e \'\'do\'\' são minúsculos nos nomes em português')})

        # *[name=~/^[a-z].*/][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_39d67968), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("nome iniciando com letra minúscula")
                err.append({'class': 9018002, 'subclass': 2073274467, 'text': mapcss.tr(u'nome iniciando com letra minúscula')})

        # *[alt_ref][inside("BR")]
        if (u'alt_ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'alt_ref') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("o conteúdo de {0} deve fazer parte de ref, separado por ;","{0.key}")
                # suggestAlternative:"ref"
                err.append({'class': 9018039, 'subclass': 836388143, 'text': mapcss.tr(u'o conteúdo de {0} deve fazer parte de ref, separado por ;', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[surface][eval(number_of_tags())=1][inside("BR")]
        if (u'surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'surface') and len(tags) == 1 and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto incompleto: possui apenas {0}","{0.key}")
                err.append({'class': 9018041, 'subclass': 411244066, 'text': mapcss.tr(u'objeto incompleto: possui apenas {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name][surface][eval(number_of_tags())=2][inside("BR")]
        # *[name][website][eval(number_of_tags())=2][inside("BR")]
        if (u'name' in keys and u'surface' in keys) or (u'name' in keys and u'website' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'surface') and len(tags) == 2 and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'website') and len(tags) == 2 and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto incompleto: possui apenas {0} e {1}","{0.key}","{1.key}")
                err.append({'class': 9018042, 'subclass': 585137381, 'text': mapcss.tr(u'objeto incompleto: possui apenas {0} e {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[leisure=pitch][sport=tennis][surface=unpaved][inside("BR")]
        if (u'leisure' in keys and u'sport' in keys and u'surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'pitch') and mapcss._tag_capture(capture_tags, 1, tags, u'sport') == mapcss._value_capture(capture_tags, 1, u'tennis') and mapcss._tag_capture(capture_tags, 2, tags, u'surface') == mapcss._value_capture(capture_tags, 2, u'unpaved') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("{0} com superfície incorreta","{2.key}")
                # suggestAlternative:"surface=clay"
                # fixAdd:"surface=clay"
                err.append({'class': 9018006, 'subclass': 990400213, 'text': mapcss.tr(u'{0} com superfície incorreta', mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'surface',u'clay']])
                }})

        # *[amenity=fuel][name=~/(?i)(?u)\b(Ale|BR|Esso|Ipiranga|Petrobr(á|a)s|Shell|Texaco)\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'fuel') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_604bb645), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("o nome não deve conter a bandeira/marca do posto")
                # suggestAlternative:"brand"
                err.append({'class': 9018002, 'subclass': 1724035987, 'text': mapcss.tr(u'o nome não deve conter a bandeira/marca do posto')})

        # *[amenity=fuel][brand=BR][inside("BR")]
        if (u'amenity' in keys and u'brand' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'fuel') and mapcss._tag_capture(capture_tags, 1, tags, u'brand') == mapcss._value_capture(capture_tags, 1, u'BR') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("uso inconsistente de bandeira do posto")
                # suggestAlternative:"brand=Petrobras"
                # fixAdd:"brand=Petrobras"
                err.append({'class': 9018002, 'subclass': 435141543, 'text': mapcss.tr(u'uso inconsistente de bandeira do posto'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'brand',u'Petrobras']])
                }})

        # *[shop=gas][name=~/(?i)(?u)^(Brasilg(á|a)s|Consigaz|Copagaz|Liquig(á|a)s|Minasg(á|a)s|Nacional G(á|a)s|Supergasbras|Ultragaz)$/][inside("BR")]
        if (u'name' in keys and u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'shop') == mapcss._value_capture(capture_tags, 0, u'gas') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_31732cd0), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("o nome não deve conter a bandeira/marca da loja")
                # suggestAlternative:"brand"
                err.append({'class': 9018002, 'subclass': 867102166, 'text': mapcss.tr(u'o nome não deve conter a bandeira/marca da loja')})

        # *[/_[0-9]$/][!"is_in:iso_3166_2"][inside("BR")]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_57b8ef8e) and not mapcss._tag_capture(capture_tags, 1, tags, u'is_in:iso_3166_2') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("chave inválida: {0}","{0.key}")
                err.append({'class': 9018022, 'subclass': 231229079, 'text': mapcss.tr(u'chave inválida: {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *["addr:housenumber"=~/(?i)^s(\.|-| )?\/?n\.?º?$/][!note][inside("BR")]
        if (u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_0b27200b), mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber')) and not mapcss._tag_capture(capture_tags, 1, tags, u'note') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("não utilizar ''{0}'' para locais sem número",tag("addr:housenumber"))
                # suggestAlternative:"note"
                # fixRemove:"addr:housenumber"
                # fixAdd:"note=Local sem número"
                err.append({'class': 9018006, 'subclass': 630415638, 'text': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', mapcss.tag(tags, u'addr:housenumber')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'note',u'Local sem número']]),
                    '-': ([
                    u'addr:housenumber'])
                }})

        # *["addr:housenumber"=~/(?i)^s(\.|-| )?\/?n\.?º?$/][note][inside("BR")]
        if (u'addr:housenumber' in keys and u'note' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_0b27200b), mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber')) and mapcss._tag_capture(capture_tags, 1, tags, u'note') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("não utilizar ''{0}'' para locais sem número",tag("addr:housenumber"))
                # suggestAlternative:"note"
                err.append({'class': 9018043, 'subclass': 1150070765, 'text': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', mapcss.tag(tags, u'addr:housenumber'))})

        # *[source=~/(?i)google/][inside("BR")]
        if (u'source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_2e8e4f2b), mapcss._tag_capture(capture_tags, 0, tags, u'source')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("objeto contém Google como source")
                err.append({'class': 9018044, 'subclass': 1159310436, 'text': mapcss.tr(u'objeto contém Google como source')})

        # *[amenity=townhall][name=~/^(?i)(?u)c(â|a)mara\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'townhall') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_46ab4d8d), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("câmara de vereadores mapeada incorretamente")
                # suggestAlternative:"office=government + government=legislative"
                err.append({'class': 9018002, 'subclass': 532372413, 'text': mapcss.tr(u'câmara de vereadores mapeada incorretamente')})

        # *[office=government][government!=legislative][name=~/^(?i)(?u)c(â|a)mara\b/][inside("BR")]
        if (u'name' in keys and u'office' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'government') and mapcss._tag_capture(capture_tags, 1, tags, u'government') != mapcss._value_const_capture(capture_tags, 1, u'legislative', u'legislative') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 2, self.re_46ab4d8d), mapcss._tag_capture(capture_tags, 2, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("ausência de government=legislative")
                err.append({'class': 9018002, 'subclass': 2126685099, 'text': mapcss.tr(u'ausência de government=legislative')})

        # *[amenity=townhall][name=~/^(?i)(?u)c((â|a)me|ama)ra\b/][inside("BR")]
        # *[office=government][name=~/^(?i)(?u)c((â|a)me|ama)ra\b/][inside("BR")]
        if (u'amenity' in keys and u'name' in keys) or (u'name' in keys and u'office' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'townhall') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_793b22ec), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'government') and mapcss.regexp_test(mapcss._value_capture(capture_tags, 1, self.re_793b22ec), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("erro de ortografia em ''câmara''")
                err.append({'class': 9018002, 'subclass': 1277153079, 'text': mapcss.tr(u'erro de ortografia em \'\'câmara\'\'')})

        # *[name=~/(?i)^prefeitura\b/][amenity!=townhall][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7ec1fb9a), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'townhall', u'townhall') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("prefeitura possivelmente mapeada de forma incorreta")
                # suggestAlternative:"amenity=townhall"
                err.append({'class': 9018002, 'subclass': 1445137044, 'text': mapcss.tr(u'prefeitura possivelmente mapeada de forma incorreta')})

        # *[name=~/(?i)(?u)^paço\b/][amenity!=townhall][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_13f4c147), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_const_capture(capture_tags, 1, u'townhall', u'townhall') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("paço possivelmente mapeado de forma incorreta")
                # suggestAlternative:"amenity=townhall"
                err.append({'class': 9018002, 'subclass': 1169494638, 'text': mapcss.tr(u'paço possivelmente mapeado de forma incorreta')})

        # *[amenity=charging_station][inside("BR")]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'charging_station') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("possivelmente deve ser amenity=fuel")
                err.append({'class': 9018002, 'subclass': 2011797637, 'text': mapcss.tr(u'possivelmente deve ser amenity=fuel')})

        # *[name=~/(?i)^Borrach(aria|eiro)/][shop=tyres][!repair][inside("BR")]
        if (u'name' in keys and u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_126ba9a9), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'shop') == mapcss._value_capture(capture_tags, 1, u'tyres') and not mapcss._tag_capture(capture_tags, 2, tags, u'repair') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("borracharia sem ''repair=yes''")
                # suggestAlternative:"repair=yes"
                err.append({'class': 9018002, 'subclass': 1225518759, 'text': mapcss.tr(u'borracharia sem \'\'repair=yes\'\'')})

        # *[name=~/(?i)^Borrach(aria|eiro)/][shop!=tyres][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_126ba9a9), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'shop') != mapcss._value_const_capture(capture_tags, 1, u'tyres', u'tyres') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("borracharia sem ''shop=tyres''")
                # suggestAlternative:"shop=tyres"
                err.append({'class': 9018002, 'subclass': 755877630, 'text': mapcss.tr(u'borracharia sem \'\'shop=tyres\'\'')})

        # *[name=~/(?i)\bcoreto\b/][leisure!=bandstand][leisure!=park][inside("BR")]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_6e34cd0f), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'leisure') != mapcss._value_const_capture(capture_tags, 1, u'bandstand', u'bandstand') and mapcss._tag_capture(capture_tags, 2, tags, u'leisure') != mapcss._value_const_capture(capture_tags, 2, u'park', u'park') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("coreto possivelmente classificado de forma incorreta")
                # suggestAlternative:"leisure=bandstand"
                err.append({'class': 9018002, 'subclass': 810497942, 'text': mapcss.tr(u'coreto possivelmente classificado de forma incorreta')})

        # *[leisure=recreation_ground][inside("BR")]
        if (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'recreation_ground') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} impreciso","{0.tag}")
                # suggestAlternative:"landuse=recreation_ground"
                # suggestAlternative:"leisure=park"
                err.append({'class': 9018002, 'subclass': 1594563801, 'text': mapcss.tr(u'{0} impreciso', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[leisure=recreation_ground][landuse=recreation_ground][inside("BR")]
        if (u'landuse' in keys and u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'recreation_ground') and mapcss._tag_capture(capture_tags, 1, tags, u'landuse') == mapcss._value_capture(capture_tags, 1, u'recreation_ground') and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} supérfluo","{0.tag}")
                # fixRemove:"leisure"
                err.append({'class': 9018002, 'subclass': 627419845, 'text': mapcss.tr(u'{0} supérfluo', mapcss._tag_uncapture(capture_tags, u'{0.tag}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    u'leisure'])
                }})

        # *["ref:vatin"]["ref:vatin"!~/^BR[0-9]{14}$/][inside("BR")]
        if (u'ref:vatin' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref:vatin') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_524288b6, u'^BR[0-9]{14}$'), mapcss._tag_capture(capture_tags, 1, tags, u'ref:vatin')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("CNPJ diferente do formato BRxxxxxxxxxxxxxx")
                err.append({'class': 9018002, 'subclass': 1793026117, 'text': mapcss.tr(u'CNPJ diferente do formato BRxxxxxxxxxxxxxx')})

        # *["ref:vatin"=~/^[0-9]{2}\.[0-9]{3}\.[0-9]{3}\/[0-9]{4}-[0-9]{2}$/][inside("BR")]
        if (u'ref:vatin' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_5ddbb7eb), mapcss._tag_capture(capture_tags, 0, tags, u'ref:vatin')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("formato do CNPJ pode ser melhorado em {0}","{0.key}")
                # fixAdd:concat("ref:vatin=BR",replace(replace(replace(tag("ref:vatin"),"/",""),".",""),"-",""))
                err.append({'class': 9018006, 'subclass': 1609978963, 'text': mapcss.tr(u'formato do CNPJ pode ser melhorado em {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'ref:vatin=BR', mapcss.replace(mapcss.replace(mapcss.replace(mapcss.tag(tags, u'ref:vatin'), u'/', u''), u'.', u''), u'-', u''))).split('=', 1)])
                }})

        # *["ref:vatin"=~/^(br|bR|Br)[0-9]{14}$/][inside("BR")]
        if (u'ref:vatin' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_408831d0), mapcss._tag_capture(capture_tags, 0, tags, u'ref:vatin')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("CNPJ deve iniciar maiúsculo: BRxxxxxxxxxxxxxx")
                # fixAdd:concat("ref:vatin=",upper(tag("ref:vatin")))
                err.append({'class': 9018006, 'subclass': 1616044431, 'text': mapcss.tr(u'CNPJ deve iniciar maiúsculo: BRxxxxxxxxxxxxxx'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'ref:vatin=', mapcss.upper(mapcss.tag(tags, u'ref:vatin')))).split('=', 1)])
                }})

        # *[phone][phone!~/^(\+55|0800)/][inside("BR")]
        # *["contact:phone"]["contact:phone"!~/^(\+55|0800)/][inside("BR")]
        if (u'contact:phone' in keys) or (u'phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'phone') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_243f4993, u'^(\+55|0800)'), mapcss._tag_capture(capture_tags, 1, tags, u'phone')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'contact:phone') and not mapcss.regexp_test(mapcss._value_const_capture(capture_tags, 1, self.re_243f4993, u'^(\+55|0800)'), mapcss._tag_capture(capture_tags, 1, tags, u'contact:phone')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} em formato diferente do internacional +55 XX YYYY-YYYY","{0.key}")
                err.append({'class': 9018002, 'subclass': 1438682200, 'text': mapcss.tr(u'{0} em formato diferente do internacional +55 XX YYYY-YYYY', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[phone=~/^(100|18{0,1}|19[0-9])$/][inside("BR")]
        # *["contact:phone"=~/^(100|18{0,1}|19[0-9])$/][inside("BR")]
        if (u'contact:phone' in keys) or (u'phone' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7a246e93), mapcss._tag_capture(capture_tags, 0, tags, u'phone')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test(mapcss._value_capture(capture_tags, 0, self.re_7a246e93), mapcss._tag_capture(capture_tags, 0, tags, u'contact:phone')) and mapcss.inside(self.father.config.options, u'BR'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("não usar número de emergência em {0}","{0.key}")
                # fixRemove:"{0.key}"
                err.append({'class': 9018002, 'subclass': 371146161, 'text': mapcss.tr(u'não usar número de emergência em {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.key}')])
                }})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = Josm_Rules_Brazilian_Specific(None)
        class _config:
            options = {"country": None, "language": None}
        class father:
            config = _config()
        n.father = father()
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}


