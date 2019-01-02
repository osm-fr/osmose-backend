#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin, with_options

class Josm_Rules_Brazilian_Specific(Plugin):

    only_for = ['BR']


    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9018001] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'{0} com logradouro ausente, errado ou abreviado', mapcss._tag_uncapture(capture_tags, u'{0.key}'))}
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
        self.errors[9018015] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'postos/unidades de saúde devem ser amenity=clinic')}
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
        self.errors[9018045] = {'item': 9018, 'level': 3, 'tag': ["tag"], 'desc': mapcss.tr(u'rodovia com ref no nome')}
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

        self.re_01454d46 = re.compile(ur'(?i)\bmotel\b')
        self.re_044c8944 = re.compile(ur'^(?i)(?u)(SENAC|SENAI|Serviço Nacional de Aprendizagem)')
        self.re_04873a60 = re.compile(ur'^(river|stream)$')
        self.re_05a345c7 = re.compile(ur'^(forest|grass|greenfield|meadow|orchard)$')
        self.re_073e5345 = re.compile(ur'\b[A-Z]{2,3} (- )?[0-9]{2,3}\b')
        self.re_07f31a73 = re.compile(ur'^(living_street|pedestrian|residential|road|service|track)$')
        self.re_0b27200b = re.compile(ur'(?i)^s(\.|-| )?\/?n\.?º?$')
        self.re_0db5b64e = re.compile(ur'village|town|city')
        self.re_1054eb5a = re.compile(ur'bridleway|bus_stop|cycleway|crossing|footway|give_way|motorway_junction|path|raceway|rest_area|services|speed_camera|steps|stop')
        self.re_10f1c360 = re.compile(ur'(,|( |-) ?[A-Z]{2})')
        self.re_126ba9a9 = re.compile(ur'(?i)^Borrach(aria|eiro)')
        self.re_12b48afb = re.compile(ur'^(grassland|heath|scrub|wood)$')
        self.re_131cc885 = re.compile(ur' ou ')
        self.re_139e342b = re.compile(ur'(?i)^Helipo(n|r)to.*')
        self.re_152c10ee = re.compile(ur'hamlet|isolated_dwelling|town|village')
        self.re_15690541 = re.compile(ur'^(?i)estrada de ferro')
        self.re_160d1bfc = re.compile(ur'^(?i)creche\b')
        self.re_178f5446 = re.compile(ur'(?i)(^|.* )(Cel|Cmte|Cond|Conj|Dª|Dr|Eng|Gov|Hab|Jd|Jr|Marg|Mun|p\/|Pde|Pe|Pq|Pst|Pref|Profa|Profª|Prof|Res|s\/|Sr(a|ª)?|Sta|Sto|Ver)\.? .*')
        self.re_17fd35b3 = re.compile(ur'^pt:')
        self.re_1d232d4c = re.compile(ur'^(?i)(?u)(Centro Universitário|Faculdades?|FATEC|Instituto Federal)\b')
        self.re_20188fb1 = re.compile(ur'^[0-9]+( |-)*([A-Z])?$')
        self.re_20c7dd98 = re.compile(ur'^(?i)(?u)(aldeia|borrach(aria|eiro)|bosque|capela|cemit(é|e)rio|c(ó|o)rrego|escola|estacionamento|fazenda|floresta|hospital|igreja|lago|lagoa|mata( nativa)?|praça|parque|parquinho|posto( de gasolina)?|riacho|rio|rodovi(á|a)ria|vila)$')
        self.re_20cf30ba = re.compile(ur'^(?i)(?u)(alameda|avenida|beco|estrada|ladeira|rodovia|rotatória|rua|travessa|trevo|viela) .*')
        self.re_20fc5143 = re.compile(ur'^(?i)Bairro\b')
        self.re_280004fd = re.compile(ur'^(Água|Arroio|Cabeceira|Córrego|Furo|Grota|Igarapé|Lajeado|Paraná|Restinga|Riacho|Ribeirão|Rio|Sanga)\b')
        self.re_2cd1e949 = re.compile(ur'^(?i)(?u)(Faz\.|Fazenda|Sítio|Chácara)')
        self.re_2dbaea13 = re.compile(ur'^(?i)\bSAMU\b')
        self.re_2e8e4f2b = re.compile(ur'(?i)google')
        self.re_2fcb6bab = re.compile(ur'^(?i)ciclovia .*')
        self.re_2ffc377d = re.compile(ur'.* D(a|e|o)s? .*')
        self.re_35bb0f2f = re.compile(ur'^(?i)(?u)(auto(-| )?( moto )?escola|centro de formação de condutores|cfc|moto escola)\b')
        self.re_362f879f = re.compile(ur'college|school')
        self.re_375e3de4 = re.compile(ur'.*([A-Z]{2,3}-[0-9]{2,4}|SPM(-| )[0-9]{3} ?(D|E)?|SP(A|D|I)(-| )[0-9]{3}\/[0-9]{3}|[A-Z]{3}-[0-9]{3}\/[0-9]{3}).*')
        self.re_38a8f0ff = re.compile(ur'^(?i)(?u)edifício.*')
        self.re_39d67968 = re.compile(ur'^[a-z].*')
        self.re_3aeda39d = re.compile(ur'hamlet|island|isolated_dwelling|neighbourhood|suburb|village')
        self.re_3b304b9b = re.compile(ur'(?i)(?u)\b(Centro Paula Souza|Escola Técnica|ETEC)\b')
        self.re_3b777b9d = re.compile(ur'^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodovia|Rotatória|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*')
        self.re_3eb0ab44 = re.compile(ur'clinic|doctors|hospital')
        self.re_46ab4d8d = re.compile(ur'^(?i)(?u)c(â|a)mara\b')
        self.re_4a8ca94e = re.compile(ur'^(?i)(?u)praça.*')
        self.re_4bd3b925 = re.compile(ur'^(?i)(?u)[a-z0-9]+_([a-z0-9]_?)+$')
        self.re_4cf86823 = re.compile(ur'(?i)\bsaude\b')
        self.re_52ab3b8b = re.compile(ur'^(?i)(?u)((Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF|hospital)$')
        self.re_53abc074 = re.compile(ur'^(give_way|mini_roundabout|stop|turning_circle)$')
        self.re_568a42f4 = re.compile(ur'\b[A-Z]{2,4} (- )?[0-9]{2,3}\b')
        self.re_57b8ef8e = re.compile(ur'_[0-9]$')
        self.re_57bee688 = re.compile(ur'^[0-9]{5}( |\.)[0-9]{3}$')
        self.re_57eb9fe5 = re.compile(ur'^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodoanel|Rodovia|Rotatória|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*')
        self.re_5849be19 = re.compile(ur'^(?i)(?u)(alameda|avenida|beco|estrada|ladeira|passarela|rodovia|rotatória|rua|travessa|trevo|viela|(anel|complexo|dispositivo) viário) .*')
        self.re_58f616c9 = re.compile(ur'^(city_block|farm|hamlet|island|islet|isolated_dwelling|neighbourhood|square)$')
        self.re_591572a5 = re.compile(ur'city|hamlet|isolated_dwelling|village')
        self.re_5ab76b11 = re.compile(ur'^(clinic|doctors|hospital)$')
        self.re_5ac7053e = re.compile(ur'^(1(a|b)?|[1-9][0-9]?)$')
        self.re_5cd37790 = re.compile(ur'(?i)^motel\b')
        self.re_5d3348cb = re.compile(ur'city|farm|neighbourhood|suburb|town|village')
        self.re_6024a566 = re.compile(ur'(?i)^Aer(ódromo|oporto) de.*')
        self.re_604bb645 = re.compile(ur'(?i)(?u)\b(Ale|BR|Esso|Ipiranga|Petrobr(á|a)s|Shell|Texaco)\b')
        self.re_6416be64 = re.compile(ur'^(island|islet)$')
        self.re_64387998 = re.compile(ur'^(?i)Bairro d(a|e|o)s?\b')
        self.re_6566db6a = re.compile(ur'(?i).*heliport$')
        self.re_65710fdb = re.compile(ur'(?i)(?u)((sem (denomina(ç|c)(ã|a)o|nome|sa(i|í)da))|desconhecido|n(ã|a)o conhecido)')
        self.re_667ce569 = re.compile(ur'^(?i)(?u)((via de )?(acesso|ligação)(( (a|à))? propriedade)?|entrada|entroncamento|rampa|retorno|rotat(ó|o)ria|r(ó|o)tula|sa(í|i)da|trevo|estrada( municipal| de terra)?|rua|rodovia|via)( (de acesso|sem nome|projetad(a|o)))?$')
        self.re_6b6e390d = re.compile(ur'(Alameda|Avenida|Rua|Travessa|Viela) .*')
        self.re_6c0d6e9e = re.compile(ur'school|university')
        self.re_6efb8049 = re.compile(ur'(?i).*airport$')
        self.re_72d45155 = re.compile(ur'route|street')
        self.re_7633bf4e = re.compile(ur'Rodovia ([A-Z]{2,3}-[0-9]{2,4})')
        self.re_793b22ec = re.compile(ur'^(?i)(?u)c((â|a)me|ama)ra\b')
        self.re_7afc6883 = re.compile(ur'^[A-Z]{4}$')
        self.re_7b7c453d = re.compile(ur'^(?i)(?u)(AM(A|E)|(Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF).*')
        self.re_7f53e992 = re.compile(ur'^(?i)(?u)(campo|est(á|a)dio|gin(á|a)sio|quadra)( de (futebol|esportes?))?$')


    def node(self, data, tags):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *["addr:street"]["addr:street"!~/^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodovia|Rotatória|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*/]
        if (u'addr:street' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'addr:street') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_3b777b9d), mapcss._tag_capture(capture_tags, 1, tags, u'addr:street')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} com logradouro ausente, errado ou abreviado","{0.key}")
                err.append({'class': 9018001, 'subclass': 588331445, 'text': mapcss.tr(u'{0} com logradouro ausente, errado ou abreviado', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[!highway][route!=road][!public_transport][type!~/route|street/][name][name=~/^(?i)(?u)(alameda|avenida|beco|estrada|ladeira|passarela|rodovia|rotatória|rua|travessa|trevo|viela|(anel|complexo|dispositivo) viário) .*/][name!~/^(?i)estrada de ferro/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'route') != mapcss._value_capture(capture_tags, 1, u'road') and not mapcss._tag_capture(capture_tags, 2, tags, u'public_transport') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_72d45155), mapcss._tag_capture(capture_tags, 3, tags, u'type')) and mapcss._tag_capture(capture_tags, 4, tags, u'name') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 5, self.re_5849be19), mapcss._tag_capture(capture_tags, 5, tags, u'name')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 6, self.re_15690541), mapcss._tag_capture(capture_tags, 6, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("objeto com nome de via mas sem tag de {0}","{0.key}")
                err.append({'class': 9018002, 'subclass': 874993957, 'text': mapcss.tr(u'objeto com nome de via mas sem tag de {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name=~/^(?i)(?u)[a-z0-9]+_([a-z0-9]_?)+$/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_4bd3b925), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("utilizar espaço ao invés de underscore")
                err.append({'class': 9018002, 'subclass': 378801374, 'text': mapcss.tr(u'utilizar espaço ao invés de underscore')})

        # *[name=~/(?i)(^|.* )(Cel|Cmte|Cond|Conj|Dª|Dr|Eng|Gov|Hab|Jd|Jr|Marg|Mun|p\/|Pde|Pe|Pq|Pst|Pref|Profa|Profª|Prof|Res|s\/|Sr(a|ª)?|Sta|Sto|Ver)\.? .*/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_178f5446), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("palavra abreviada em {0}","{0.key}")
                err.append({'class': 9018003, 'subclass': 1784756763, 'text': mapcss.tr(u'palavra abreviada em {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[leisure][name=~/^(?i)(?u)(campo|est(á|a)dio|gin(á|a)sio|quadra)( de (futebol|esportes?))?$/]
        if (u'leisure' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7f53e992), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("nome supérfluo/incompleto de local de lazer")
                err.append({'class': 9018004, 'subclass': 790401825, 'text': mapcss.tr(u'nome supérfluo/incompleto de local de lazer')})

        # *[name=~/^(?i)(?u)((Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF|hospital)$/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_52ab3b8b), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("nome supérfluo/incompleto de local de saúde")
                err.append({'class': 9018005, 'subclass': 1792576894, 'text': mapcss.tr(u'nome supérfluo/incompleto de local de saúde')})

        # *[amenity=~/^(clinic|doctors|hospital)$/][name=~/(?i)\bsaude\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_5ab76b11), mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_4cf86823), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("erro de ortografia em ''saúde''")
                err.append({'class': 9018002, 'subclass': 1455303428, 'text': mapcss.tr(u'erro de ortografia em \'\'saúde\'\'')})

        # *[place=farm][name^="Sitio "]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'farm') and mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, u'name'), mapcss._value_capture(capture_tags, 1, u'Sitio ')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("faltando acento em ''Sítio''")
                err.append({'class': 9018002, 'subclass': 962677162, 'text': mapcss.tr(u'faltando acento em \'\'Sítio\'\'')})

        # *[name=~/^(?i)(?u)(aldeia|borrach(aria|eiro)|bosque|capela|cemit(é|e)rio|c(ó|o)rrego|escola|estacionamento|fazenda|floresta|hospital|igreja|lago|lagoa|mata( nativa)?|praça|parque|parquinho|posto( de gasolina)?|riacho|rio|rodovi(á|a)ria|vila)$/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_20c7dd98), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("local com nome supérfluo, incompleto ou descritivo")
                err.append({'class': 9018002, 'subclass': 501162763, 'text': mapcss.tr(u'local com nome supérfluo, incompleto ou descritivo')})

        # *[amenity=parking][name=~/(?i)^Estacionamento /]
        # Rule Blacklisted

        # *[designation=*"addr:housename"]
        # *[ref=*designation]
        # *[ref=*old_ref]
        # *[name=*"addr:housename"]
        # *[name=*designation]
        # *[name=*alt_name]
        # *[name=*int_name]
        # *[name=*loc_name]
        # *[name=*nat_name]
        # *[name=*official_name]
        # *[name=*old_name]
        # *[name=*reg_name]
        # *[name=*short_name]
        # *[name=*sorting_name]
        if (u'designation' in keys) or (u'name' in keys) or (u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'designation') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'addr:housename')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'designation')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'old_ref')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'addr:housename')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'designation')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'alt_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'int_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'loc_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'nat_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'official_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'old_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'reg_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'short_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'sorting_name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("{0} e {1} são iguais; remover chave {1} desnecessária","{0.key}","{0.value}")
                # fixRemove:"{0.value}"
                err.append({'class': 9018006, 'subclass': 1882388489, 'text': mapcss.tr(u'{0} e {1} são iguais; remover chave {1} desnecessária', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.value}')])
                }})

        # *[source=*name]
        if (u'source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} e {1} são iguais","{0.key}","{0.value}")
                err.append({'class': 9018002, 'subclass': 1403015964, 'text': mapcss.tr(u'{0} e {1} são iguais', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[name=~/(?i)(?u)((sem (denomina(ç|c)(ã|a)o|nome|sa(i|í)da))|desconhecido|n(ã|a)o conhecido)/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_65710fdb), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto com nomenclatura incorreta")
                # suggestAlternative:"noname"
                err.append({'class': 9018007, 'subclass': 506924923, 'text': mapcss.tr(u'objeto com nomenclatura incorreta')})

        # node[maxheight][barrier!=height_restrictor][!traffic_sign]
        # node[maxspeed][highway!=speed_camera][!traffic_sign]
        if (u'maxheight' in keys) or (u'maxspeed' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxheight') and mapcss._tag_capture(capture_tags, 1, tags, u'barrier') != mapcss._value_capture(capture_tags, 1, u'height_restrictor') and not mapcss._tag_capture(capture_tags, 2, tags, u'traffic_sign'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') != mapcss._value_capture(capture_tags, 1, u'speed_camera') and not mapcss._tag_capture(capture_tags, 2, tags, u'traffic_sign'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} não deve ser utilizado em nó; utilizar a restrição na via","{0.key}")
                err.append({'class': 9018008, 'subclass': 1663448238, 'text': mapcss.tr(u'{0} não deve ser utilizado em nó; utilizar a restrição na via', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # node[noname?]
        if (u'noname' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'noname') in ('yes', 'true', '1'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("uso suspeito de {0} em nó","{0.key}")
                err.append({'class': 9018002, 'subclass': 1281771763, 'text': mapcss.tr(u'uso suspeito de {0} em nó', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[designation]
        if (u'designation' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'designation'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} é uma chave utilizada apenas no Reino Unido","{0.key}")
                # suggestAlternative:"description"
                # suggestAlternative:"name"
                err.append({'class': 9018009, 'subclass': 1259259930, 'text': mapcss.tr(u'{0} é uma chave utilizada apenas no Reino Unido', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # node[highway=motorway_junction][!name][!ref]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'motorway_junction') and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and not mapcss._tag_capture(capture_tags, 2, tags, u'ref'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} sem pelo menos uma das tags: {1} ou {2}","{0.value}","{1.key}","{2.key}")
                err.append({'class': 9018010, 'subclass': 1402053593, 'text': mapcss.tr(u'{0} sem pelo menos uma das tags: {1} ou {2}', mapcss._tag_uncapture(capture_tags, u'{0.value}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[place=~/hamlet|isolated_dwelling|town|village/][population>=100000]
        if (u'place' in keys and u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_152c10ee), mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'population') >= mapcss._value_capture(capture_tags, 1, 100000))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("local com 100.000 habitantes ou mais deve ser classificado como city")
                # fixAdd:"place=city"
                err.append({'class': 9018006, 'subclass': 149235075, 'text': mapcss.tr(u'local com 100.000 habitantes ou mais deve ser classificado como city'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'place',u'city']])
                }})

        # *[place=~/city|hamlet|isolated_dwelling|village/][population>=10000][population<100000]
        if (u'place' in keys and u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_591572a5), mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'population') >= mapcss._value_capture(capture_tags, 1, 10000) and mapcss._tag_capture(capture_tags, 2, tags, u'population') < mapcss._value_capture(capture_tags, 2, 100000))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("local com população entre 10.000 e 100.000 deve ser classificado como town")
                # fixAdd:"place=town"
                err.append({'class': 9018006, 'subclass': 1174321645, 'text': mapcss.tr(u'local com população entre 10.000 e 100.000 deve ser classificado como town'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'place',u'town']])
                }})

        # *[place][place!~/hamlet|island|isolated_dwelling|neighbourhood|suburb|village/][population<10000]
        if (u'place' in keys and u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_3aeda39d), mapcss._tag_capture(capture_tags, 1, tags, u'place')) and mapcss._tag_capture(capture_tags, 2, tags, u'population') < mapcss._value_capture(capture_tags, 2, 10000))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("local com menos de 10.000 habitantes deve ser classificado como village")
                # fixAdd:"place=village"
                err.append({'class': 9018006, 'subclass': 719699918, 'text': mapcss.tr(u'local com menos de 10.000 habitantes deve ser classificado como village'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'place',u'village']])
                }})

        # *[place=city][!population]
        # *[place=town][!population]
        # *[place=village][!population]
        # Rule Blacklisted

        # *[place=city][!name]
        # *[place=town][!name]
        # *[place=village][!name]
        if (u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'city') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'town') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'village') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} sem nome","{0.value}")
                err.append({'class': 9018012, 'subclass': 828568305, 'text': mapcss.tr(u'{0} sem nome', mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # node[place=~/village|town|city/]["addr:city"=*name]
        # node[place=suburb]["addr:suburb"=*name]
        if (u'addr:city' in keys and u'place' in keys) or (u'addr:suburb' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_0db5b64e), mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'addr:city') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, u'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'suburb') and mapcss._tag_capture(capture_tags, 1, tags, u'addr:suburb') == mapcss._value_capture(capture_tags, 1, mapcss.tag(tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwError:tr("não deve possuir {0}","{1.key}")
                # fixRemove:"{1.key}"
                err.append({'class': 9018006, 'subclass': 1782871982, 'text': mapcss.tr(u'não deve possuir {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{1.key}')])
                }})

        # *["addr:city"=~/(,|( |-) ?[A-Z]{2})/]
        if (u'addr:city' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_10f1c360), mapcss._tag_capture(capture_tags, 0, tags, u'addr:city')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve conter apenas o nome da cidade","{0.key}")
                err.append({'class': 9018013, 'subclass': 223700239, 'text': mapcss.tr(u'{0} deve conter apenas o nome da cidade', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name=~/^(?i)(?u)(Faz\.|Fazenda|Sítio|Chácara)/][place][place!~/city|farm|neighbourhood|suburb|town|village/]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_2cd1e949), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'place') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_5d3348cb), mapcss._tag_capture(capture_tags, 2, tags, u'place')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("objeto talvez deva ser {0}=farm","{1.key}")
                err.append({'class': 9018002, 'subclass': 414255329, 'text': mapcss.tr(u'objeto talvez deva ser {0}=farm', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[place][name=~/^(?i)Bairro\b/][name!~/^(?i)Bairro d(a|e|o)s?\b/]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_20fc5143), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_64387998), mapcss._tag_capture(capture_tags, 2, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("objeto talvez não deva ter ''Bairro'' no nome")
                err.append({'class': 9018002, 'subclass': 457937105, 'text': mapcss.tr(u'objeto talvez não deva ter \'\'Bairro\'\' no nome')})

        # node[place=~/^(island|islet)$/]
        if (u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_6416be64), mapcss._tag_capture(capture_tags, 0, tags, u'place')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("representar a ilha, se possível, como uma área")
                err.append({'class': 9018002, 'subclass': 903906160, 'text': mapcss.tr(u'representar a ilha, se possível, como uma área')})

        # *[iata="0"]
        if (u'iata' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'iata') == mapcss._value_capture(capture_tags, 0, u'0'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} com valor = {1}","{0.key}","{0.value}")
                err.append({'class': 9018014, 'subclass': 1389202412, 'text': mapcss.tr(u'{0} com valor = {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[amenity=~/college|school/][name=~/^(?i)(?u)(Centro Universitário|Faculdades?|FATEC|Instituto Federal)\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_362f879f), mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_1d232d4c), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("estabelecimento de ensino classificado incorretamente")
                # suggestAlternative:"amenity=university"
                # fixAdd:"{0.key}=university"
                err.append({'class': 9018006, 'subclass': 221523813, 'text': mapcss.tr(u'estabelecimento de ensino classificado incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=university')).split('=', 1)])
                }})

        # *[amenity=school][name=~/^(?i)(?u)(SENAC|SENAI|Serviço Nacional de Aprendizagem)/]
        # *[amenity=~/school|university/][name=~/(?i)(?u)\b(Centro Paula Souza|Escola Técnica|ETEC)\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'school') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_044c8944), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_6c0d6e9e), mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_3b304b9b), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("estabelecimento de ensino classificado incorretamente")
                # suggestAlternative:"amenity=college"
                # fixAdd:"{0.key}=college"
                err.append({'class': 9018006, 'subclass': 897019825, 'text': mapcss.tr(u'estabelecimento de ensino classificado incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=college')).split('=', 1)])
                }})

        # *[amenity=school][name=~/^(?i)(?u)(auto(-| )?( moto )?escola|centro de formação de condutores|cfc|moto escola)\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'school') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_35bb0f2f), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("autoescola classificada incorretamente")
                # suggestAlternative:"amenity=driving_school"
                # fixAdd:"{0.key}=driving_school"
                err.append({'class': 9018006, 'subclass': 1796023580, 'text': mapcss.tr(u'autoescola classificada incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=driving_school')).split('=', 1)])
                }})

        # *[amenity=school][name=~/^(?i)creche\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'school') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_160d1bfc), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("creche classificada incorretamente")
                # suggestAlternative:"amenity=kindergarten"
                # fixAdd:"{0.key}=kindergarten"
                err.append({'class': 9018006, 'subclass': 121701344, 'text': mapcss.tr(u'creche classificada incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=kindergarten')).split('=', 1)])
                }})

        # *[name=~/^(?i)(?u)Subestação .*/][power][power!=substation]
        # *[name=~/^(?i)(?u)Fórum .*/][amenity][amenity!=courthouse]
        # *[name=~/^(?i)Hospital .*/][building][building!=hospital]
        # *[name=~/^(?i)Universidade .*/][building][building!=university]
        # *[name=~/^(?i)Escola .*/][building][building!=school]
        # *[name=~/^(?i)Hotel .*/][building][building!=hotel]
        # *[name=~/^(?i)Capela .*/][building][building!=chapel]
        # *[name=~/^(?i)Igreja .*/][building][building!=church]
        # *[name=~/^(?i)Catedral .*/][building][building!=cathedral]
        # *[name=~/^(?i)Fazenda .*/][building][building!=farm]
        # *[name=~/^(?i)Supermercado .*/][building][building!=supermarket]
        # Rule Blacklisted

        # *[name=~/^(?i)(?u)(AM(A|E)|(Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF).*/][amenity=hospital]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_7b7c453d), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') == mapcss._value_capture(capture_tags, 1, u'hospital'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("postos/unidades de saúde devem ser amenity=clinic")
                err.append({'class': 9018015, 'subclass': 2108543140, 'text': mapcss.tr(u'postos/unidades de saúde devem ser amenity=clinic')})

        # *[name=~/^(?i)\bSAMU\b/][amenity=~/clinic|doctors|hospital/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_2dbaea13), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_3eb0ab44), mapcss._tag_capture(capture_tags, 1, tags, u'amenity')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("SAMU classificado de forma errada")
                # suggestAlternative:"emergency=ambulance_station"
                err.append({'class': 9018016, 'subclass': 2090365947, 'text': mapcss.tr(u'SAMU classificado de forma errada')})

        # node[highway=~/^(give_way|mini_roundabout|stop|turning_circle)$/][name]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_53abc074), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto não deve possuir {0}","{1.key}")
                err.append({'class': 9018017, 'subclass': 306235762, 'text': mapcss.tr(u'objeto não deve possuir {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # node[highway=speed_camera][!maxspeed]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'speed_camera') and not mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("adicionar {0} ao {1}","{1.key}","{0.tag}")
                err.append({'class': 9018018, 'subclass': 1369285067, 'text': mapcss.tr(u'adicionar {0} ao {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[crossing][!highway][!railway]
        if (u'crossing' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'crossing') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve ser utilizado com {1}={0} ou {2}={0}","{0.key}","{1.key}","{2.key}")
                err.append({'class': 9018019, 'subclass': 139983185, 'text': mapcss.tr(u'{0} deve ser utilizado com {1}={0} ou {2}={0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[aeroway][designation=~/^[A-Z]{4}$/][!icao]
        # *[aeroway][ref=~/^[A-Z]{4}$/][!icao]
        if (u'aeroway' in keys and u'ref' in keys) or (u'aeroway' in keys and u'designation' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7afc6883), mapcss._tag_capture(capture_tags, 1, tags, u'designation')) and not mapcss._tag_capture(capture_tags, 2, tags, u'icao'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7afc6883), mapcss._tag_capture(capture_tags, 1, tags, u'ref')) and not mapcss._tag_capture(capture_tags, 2, tags, u'icao'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("{0} provavelmente deve ser utilizado como {1}","{1.key}","{2.key}")
                # fixChangeKey:"{1.key} => {2.key}"
                err.append({'class': 9018006, 'subclass': 662001655, 'text': mapcss.tr(u'{0} provavelmente deve ser utilizado como {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, u'{1.key} => {2.key}')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, u'{1.key} => {2.key}')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, u'{1.key} => {2.key}')).split('=>', 1)[0].strip()])
                }})

        # *[access=permissive]
        if (u'access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'permissive'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} deve ser utilizado apenas em vias privadas com permissão de acesso e não em vias de acesso público","{0.tag}")
                err.append({'class': 9018002, 'subclass': 1918455197, 'text': mapcss.tr(u'{0} deve ser utilizado apenas em vias privadas com permissão de acesso e não em vias de acesso público', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[name=~/^(?U)(\p{Upper}| )+$/]
        # *["addr:street"=~/^(?U)(\p{Upper}| )+$/]
        # Rule Blacklisted

        # *["addr:postcode"=~/^[0-9]{8}$/]
        # Rule Blacklisted

        # *[postal_code=~/^[0-9]{8}$/]
        # Rule Blacklisted

        # *["addr:postcode"=~/^[0-9]{5}( |\.)[0-9]{3}$/]
        if (u'addr:postcode' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_57bee688), mapcss._tag_capture(capture_tags, 0, tags, u'addr:postcode')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("formato do CEP pode ser melhorado")
                # fixAdd:concat("addr:postcode=",replace(replace(tag("addr:postcode")," ","-"),".","-"))
                err.append({'class': 9018006, 'subclass': 308348773, 'text': mapcss.tr(u'formato do CEP pode ser melhorado'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'addr:postcode=', mapcss.replace(mapcss.replace(mapcss.tag(tags, u'addr:postcode'), u' ', u'-'), u'.', u'-'))).split('=', 1)])
                }})

        # *["postal_code"=~/^[0-9]{5}( |\.)[0-9]{3}$/]
        if (u'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_57bee688), mapcss._tag_capture(capture_tags, 0, tags, u'postal_code')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("formato do CEP pode ser melhorado")
                # fixAdd:concat("postal_code=",replace(replace(tag("postal_code")," ","-"),".","-"))
                err.append({'class': 9018006, 'subclass': 1211220107, 'text': mapcss.tr(u'formato do CEP pode ser melhorado'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'postal_code=', mapcss.replace(mapcss.replace(mapcss.tag(tags, u'postal_code'), u' ', u'-'), u'.', u'-'))).split('=', 1)])
                }})

        # *["addr:postcode"]["addr:postcode"!~/^[0-9]{5}-[0-9]{3}$/]
        # *[postal_code][postal_code!~/^[0-9]{5}-[0-9]{3}$/]
        # Rule Blacklisted

        # *[alt_source][source]
        if (u'alt_source' in keys and u'source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'alt_source') and mapcss._tag_capture(capture_tags, 1, tags, u'source'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve estar incluído em {1}, separado por '';'' caso necessário","{0.key}","{1.key}")
                err.append({'class': 9018020, 'subclass': 512568644, 'text': mapcss.tr(u'{0} deve estar incluído em {1}, separado por \'\';\'\' caso necessário', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[landuse?]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') in ('yes', 'true', '1'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("especificar valor correto para {0} ao invés de ''{1}''","{0.key}",tag("landuse"))
                err.append({'class': 9018021, 'subclass': 2004192493, 'text': mapcss.tr(u'especificar valor correto para {0} ao invés de \'\'{1}\'\'', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss.tag(tags, u'landuse'))})

        # *[long_name]
        if (u'long_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'long_name'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("chave inválida: {0}","{0.key}")
                # suggestAlternative:"alt_name"
                # suggestAlternative:"name"
                # suggestAlternative:"official_name"
                err.append({'class': 9018022, 'subclass': 1648910015, 'text': mapcss.tr(u'chave inválida: {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *["building:levels"<1]
        if (u'building:levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:levels') < mapcss._value_capture(capture_tags, 0, 1))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} com valor inválido","{0.key}")
                err.append({'class': 9018002, 'subclass': 154478605, 'text': mapcss.tr(u'{0} com valor inválido', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[hires?]
        if (u'hires' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'hires') in ('yes', 'true', '1'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("não se deve utilizar {0} para demarcar áreas de cobertura de imagem","{0.key}")
                err.append({'class': 9018023, 'subclass': 1394305840, 'text': mapcss.tr(u'não se deve utilizar {0} para demarcar áreas de cobertura de imagem', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[tourism=motel][amenity!=love_hotel]
        # *[name=~/(?i)\bmotel\b/][amenity!=love_hotel]
        if (u'name' in keys) or (u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == mapcss._value_capture(capture_tags, 0, u'motel') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_capture(capture_tags, 1, u'love_hotel'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_01454d46), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_capture(capture_tags, 1, u'love_hotel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("ausência de tag ''{0}''","{1.value}")
                # fixAdd:"{1.key}={1.value}"
                err.append({'class': 9018006, 'subclass': 444111908, 'text': mapcss.tr(u'ausência de tag \'\'{0}\'\'', mapcss._tag_uncapture(capture_tags, u'{1.value}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{1.key}={1.value}')).split('=', 1)])
                }})

        # *[amenity=love_hotel][tourism][tourism!=motel]
        if (u'amenity' in keys and u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'love_hotel') and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') and mapcss._tag_capture(capture_tags, 2, tags, u'tourism') != mapcss._value_capture(capture_tags, 2, u'motel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("provavelmente deve ser ''{0}={1}''","{2.key}","{2.value}")
                err.append({'class': 9018002, 'subclass': 2021262051, 'text': mapcss.tr(u'provavelmente deve ser \'\'{0}={1}\'\'', mapcss._tag_uncapture(capture_tags, u'{2.key}'), mapcss._tag_uncapture(capture_tags, u'{2.value}'))})

        # *[name=~/(?i)^motel\b/][tourism!=motel]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_5cd37790), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') != mapcss._value_capture(capture_tags, 1, u'motel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("motel classificado incorretamente")
                # suggestAlternative:"tourism=motel"
                err.append({'class': 9018002, 'subclass': 2096064741, 'text': mapcss.tr(u'motel classificado incorretamente')})

        # *[aeroway=aerodrome][name=~/(?i).*airport$/]
        # *[aeroway=helipad][name=~/(?i).*heliport$/]
        if (u'aeroway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'aerodrome') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_6efb8049), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'helipad') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_6566db6a), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} com nome em inglês","{0.tag}")
                err.append({'class': 9018002, 'subclass': 134725283, 'text': mapcss.tr(u'{0} com nome em inglês', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[aeroway=aerodrome][name=~/(?i)^Aer(ódromo|oporto) de.*/]
        # *[aeroway=helipad][name=~/(?i)^Helipo(n|r)to.*/]
        if (u'aeroway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'aerodrome') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_6024a566), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'helipad') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_139e342b), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("conferir se existe nome oficial do {0}","{0.value}")
                err.append({'class': 9018002, 'subclass': 2002284471, 'text': mapcss.tr(u'conferir se existe nome oficial do {0}', mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[aeroway=aerodrome][ref]
        if (u'aeroway' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'aerodrome') and mapcss._tag_capture(capture_tags, 1, tags, u'ref'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("''{0}'' não faz sentido em aeroporto","{1.key}")
                err.append({'class': 9018002, 'subclass': 339634841, 'text': mapcss.tr(u'\'\'{0}\'\' não faz sentido em aeroporto', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # node[surface][!traffic_calming]
        # Rule Blacklisted

        # *[waterway][layer<0][!tunnel]
        if (u'layer' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'layer') < mapcss._value_capture(capture_tags, 1, 0) and not mapcss._tag_capture(capture_tags, 2, tags, u'tunnel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} negativo de {1} com ausência de {2}","{1.key}","{0.key}","{2.key}")
                err.append({'class': 9018002, 'subclass': 1476002587, 'text': mapcss.tr(u'{0} negativo de {1} com ausência de {2}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[waterway][layer>0][!bridge]
        if (u'layer' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'layer') > mapcss._value_capture(capture_tags, 1, 0) and not mapcss._tag_capture(capture_tags, 2, tags, u'bridge'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} positivo de {1} com ausência de {2}","{1.key}","{0.key}","{2.key}")
                err.append({'class': 9018002, 'subclass': 1137415389, 'text': mapcss.tr(u'{0} positivo de {1} com ausência de {2}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[layer][!building][!highway][man_made!=pipeline][!railway][!waterway]
        # Rule Blacklisted

        # *[name=~/^(?i)(?u)edifício.*/][!building]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_38a8f0ff), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'building'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("possível ausência de tag {0}","{1.key}")
                err.append({'class': 9018026, 'subclass': 1417041710, 'text': mapcss.tr(u'possível ausência de tag {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[route=ferry][!duration]
        if (u'route' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'route') == mapcss._value_capture(capture_tags, 0, u'ferry') and not mapcss._tag_capture(capture_tags, 1, tags, u'duration'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("ausência do tempo de duração ({0}) da balsa","{1.key}")
                err.append({'class': 9018027, 'subclass': 1289884816, 'text': mapcss.tr(u'ausência do tempo de duração ({0}) da balsa', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[name=~/^(?i)(?u)praça.*/][!leisure][landuse=~/^(forest|grass|greenfield|meadow|orchard)$/]
        # *[name=~/^(?i)(?u)praça.*/][!leisure][natural=~/^(grassland|heath|scrub|wood)$/]
        if (u'landuse' in keys and u'name' in keys) or (u'name' in keys and u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_4a8ca94e), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'leisure') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_05a345c7), mapcss._tag_capture(capture_tags, 2, tags, u'landuse')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_4a8ca94e), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'leisure') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_12b48afb), mapcss._tag_capture(capture_tags, 2, tags, u'natural')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("possível definição incorreta para praça: ''{0}''","{2.key}")
                # suggestAlternative:"leisure=park"
                err.append({'class': 9018029, 'subclass': 80498829, 'text': mapcss.tr(u'possível definição incorreta para praça: \'\'{0}\'\'', mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[wikipedia][wikipedia!~/^pt:/]
        if (u'wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_17fd35b3), mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("utilizar prefixo em português (pt:) para {0}","{0.key}")
                err.append({'class': 9018030, 'subclass': 1219382195, 'text': mapcss.tr(u'utilizar prefixo em português (pt:) para {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name=~/.*\(.*\).*/]
        # Rule Blacklisted

        # *[name=~/ - /]
        # Rule Blacklisted

        # *[name=~/, /]
        # Rule Blacklisted

        # *[name=~/: /]
        # Rule Blacklisted

        # *[name=~/ ou /]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_131cc885), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("nome utilizado de forma incorreta")
                # suggestAlternative:"name e alt_name"
                err.append({'class': 9018031, 'subclass': 23034604, 'text': mapcss.tr(u'nome utilizado de forma incorreta')})

        # node[admin_level][!capital]
        # node[border_type]
        # node[boundary]
        # node[type=boundary]
        if (u'admin_level' in keys) or (u'border_type' in keys) or (u'boundary' in keys) or (u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'admin_level') and not mapcss._tag_capture(capture_tags, 1, tags, u'capital'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'border_type'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'boundary'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("nó não deve possuir {0}","{0.tag}")
                err.append({'class': 9018032, 'subclass': 573228766, 'text': mapcss.tr(u'nó não deve possuir {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[boundary=national_park][!name]
        # *[boundary=protected_area][!name]
        # *[leisure=nature_reserve][!name]
        if (u'boundary' in keys) or (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'national_park') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'protected_area') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'nature_reserve') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
                err.append({'class': 9018033, 'subclass': 1492609299, 'text': mapcss.tr(u'{0} deve possuir {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[boundary=protected_area][!protect_class]
        if (u'boundary' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'protected_area') and not mapcss._tag_capture(capture_tags, 1, tags, u'protect_class'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
                err.append({'class': 9018033, 'subclass': 822952800, 'text': mapcss.tr(u'{0} deve possuir {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[protect_class][protect_class!~/^(1(a|b)?|[1-9][0-9]?)$/]
        if (u'protect_class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'protect_class') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_5ac7053e), mapcss._tag_capture(capture_tags, 1, tags, u'protect_class')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("valor incorreto para {0}","{0.key}")
                err.append({'class': 9018034, 'subclass': 1459161459, 'text': mapcss.tr(u'valor incorreto para {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[protect_class][boundary!=protected_area]
        if (u'protect_class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'protect_class') and mapcss._tag_capture(capture_tags, 1, tags, u'boundary') != mapcss._value_capture(capture_tags, 1, u'protected_area'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("ausência de boundary=protected_area")
                err.append({'class': 9018035, 'subclass': 1208814760, 'text': mapcss.tr(u'ausência de boundary=protected_area')})

        # node[destination]
        if (u'destination' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'destination'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve ser usado apenas em ways","{0.key}")
                err.append({'class': 9018036, 'subclass': 1394019686, 'text': mapcss.tr(u'{0} deve ser usado apenas em ways', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # node[exit_to]
        if (u'exit_to' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'exit_to'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("utilize ''destination'' no caminho de saída ao invés de ''exit_to''")
                err.append({'class': 9018037, 'subclass': 2117439762, 'text': mapcss.tr(u'utilize \'\'destination\'\' no caminho de saída ao invés de \'\'exit_to\'\'')})

        # node[highway=motorway_junction][ref][ref!~/^[0-9]+( |-)*([A-Z])?$/]
        if (u'highway' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'motorway_junction') and mapcss._tag_capture(capture_tags, 1, tags, u'ref') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_20188fb1), mapcss._tag_capture(capture_tags, 2, tags, u'ref')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("saída de rodovia ({0}) fora do padrão","{1.key}")
                err.append({'class': 9018002, 'subclass': 2069822365, 'text': mapcss.tr(u'saída de rodovia ({0}) fora do padrão', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # node[highway=motorway_junction][name]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'motorway_junction') and mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} geralmente não possui nome; use ''destination'' no caminho de saída","{0.tag}")
                err.append({'class': 9018002, 'subclass': 1930778720, 'text': mapcss.tr(u'{0} geralmente não possui nome; use \'\'destination\'\' no caminho de saída', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # node[junction]
        if (u'junction' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'junction'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("junção ({0}) em um nó","{0.value}")
                # suggestAlternative:"highway=mini_roundabout"
                # suggestAlternative:"highway=turning_circle"
                err.append({'class': 9018002, 'subclass': 1193804268, 'text': mapcss.tr(u'junção ({0}) em um nó', mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[name=~/.* D(a|e|o)s? .*/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_2ffc377d), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("''da'', ''de'' e ''do'' são minúsculos nos nomes em português")
                err.append({'class': 9018002, 'subclass': 1986668346, 'text': mapcss.tr(u'\'\'da\'\', \'\'de\'\' e \'\'do\'\' são minúsculos nos nomes em português')})

        # *[name=~/^[a-z].*/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_39d67968), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("nome iniciando com letra minúscula")
                err.append({'class': 9018002, 'subclass': 167462302, 'text': mapcss.tr(u'nome iniciando com letra minúscula')})

        # *[alt_ref]
        if (u'alt_ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'alt_ref'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("o conteúdo de {0} deve fazer parte de ref, separado por ;","{0.key}")
                # suggestAlternative:"ref"
                err.append({'class': 9018039, 'subclass': 722411109, 'text': mapcss.tr(u'o conteúdo de {0} deve fazer parte de ref, separado por ;', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[surface][eval(number_of_tags())=1]
        if (u'surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'surface') and len(tags) == 1)
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto incompleto: possui apenas {0}","{0.key}")
                err.append({'class': 9018041, 'subclass': 1776991136, 'text': mapcss.tr(u'objeto incompleto: possui apenas {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name][surface][eval(number_of_tags())=2]
        # *[name][website][eval(number_of_tags())=2]
        if (u'name' in keys and u'surface' in keys) or (u'name' in keys and u'website' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'surface') and len(tags) == 2)
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'website') and len(tags) == 2)
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto incompleto: possui apenas {0} e {1}","{0.key}","{1.key}")
                err.append({'class': 9018042, 'subclass': 626126700, 'text': mapcss.tr(u'objeto incompleto: possui apenas {0} e {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[leisure=pitch][sport=tennis][surface=unpaved]
        if (u'leisure' in keys and u'sport' in keys and u'surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'pitch') and mapcss._tag_capture(capture_tags, 1, tags, u'sport') == mapcss._value_capture(capture_tags, 1, u'tennis') and mapcss._tag_capture(capture_tags, 2, tags, u'surface') == mapcss._value_capture(capture_tags, 2, u'unpaved'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("{0} com superfície incorreta","{2.key}")
                # suggestAlternative:"surface=clay"
                # fixAdd:"surface=clay"
                err.append({'class': 9018006, 'subclass': 1659179489, 'text': mapcss.tr(u'{0} com superfície incorreta', mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'surface',u'clay']])
                }})

        # *[amenity=fuel][name=~/(?i)(?u)\b(Ale|BR|Esso|Ipiranga|Petrobr(á|a)s|Shell|Texaco)\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'fuel') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_604bb645), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("uso incorreto da bandeira do posto")
                # suggestAlternative:"brand"
                err.append({'class': 9018002, 'subclass': 935774110, 'text': mapcss.tr(u'uso incorreto da bandeira do posto')})

        # *[/_[0-9]$/][!"is_in:iso_3166_2"]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_57b8ef8e) and not mapcss._tag_capture(capture_tags, 1, tags, u'is_in:iso_3166_2'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("chave inválida: {0}","{0.key}")
                err.append({'class': 9018022, 'subclass': 331369569, 'text': mapcss.tr(u'chave inválida: {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *["addr:housenumber"=~/(?i)^s(\.|-| )?\/?n\.?º?$/][!note]
        if (u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_0b27200b), mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber')) and not mapcss._tag_capture(capture_tags, 1, tags, u'note'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("não utilizar ''{0}'' para locais sem número",tag("addr:housenumber"))
                # suggestAlternative:"note"
                # fixRemove:"addr:housenumber"
                # fixAdd:"note=Local sem número"
                err.append({'class': 9018006, 'subclass': 931902546, 'text': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', mapcss.tag(tags, u'addr:housenumber')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'note',u'Local sem número']]),
                    '-': ([
                    u'addr:housenumber'])
                }})

        # *["addr:housenumber"=~/(?i)^s(\.|-| )?\/?n\.?º?$/][note]
        if (u'addr:housenumber' in keys and u'note' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_0b27200b), mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber')) and mapcss._tag_capture(capture_tags, 1, tags, u'note'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("não utilizar ''{0}'' para locais sem número",tag("addr:housenumber"))
                # suggestAlternative:"note"
                err.append({'class': 9018043, 'subclass': 1717284811, 'text': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', mapcss.tag(tags, u'addr:housenumber'))})

        # *[source=~/(?i)google/]
        if (u'source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_2e8e4f2b), mapcss._tag_capture(capture_tags, 0, tags, u'source')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("objeto contém Google como source")
                err.append({'class': 9018044, 'subclass': 1313403884, 'text': mapcss.tr(u'objeto contém Google como source')})

        # *[amenity=townhall][name=~/^(?i)(?u)c(â|a)mara\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'townhall') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_46ab4d8d), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("câmara de vereadores mapeada incorretamente")
                # suggestAlternative:"office=government + government=legislative"
                err.append({'class': 9018002, 'subclass': 129695507, 'text': mapcss.tr(u'câmara de vereadores mapeada incorretamente')})

        # *[office=government][government!=legislative][name=~/^(?i)(?u)c(â|a)mara\b/]
        if (u'name' in keys and u'office' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'government') and mapcss._tag_capture(capture_tags, 1, tags, u'government') != mapcss._value_capture(capture_tags, 1, u'legislative') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_46ab4d8d), mapcss._tag_capture(capture_tags, 2, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("ausência de government=legislative")
                err.append({'class': 9018002, 'subclass': 869412796, 'text': mapcss.tr(u'ausência de government=legislative')})

        # *[amenity=townhall][name=~/^(?i)(?u)c((â|a)me|ama)ra\b/]
        # *[office=government][name=~/^(?i)(?u)c((â|a)me|ama)ra\b/]
        if (u'amenity' in keys and u'name' in keys) or (u'name' in keys and u'office' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'townhall') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_793b22ec), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'government') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_793b22ec), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("erro de ortografia em ''câmara''")
                err.append({'class': 9018002, 'subclass': 212328084, 'text': mapcss.tr(u'erro de ortografia em \'\'câmara\'\'')})

        # *[amenity=charging_station]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'charging_station'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("possivelmente deve ser amenity=fuel")
                err.append({'class': 9018002, 'subclass': 128902291, 'text': mapcss.tr(u'possivelmente deve ser amenity=fuel')})

        # *[name=~/(?i)^Borrach(aria|eiro)/][shop=tyres][!repair]
        if (u'name' in keys and u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_126ba9a9), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'shop') == mapcss._value_capture(capture_tags, 1, u'tyres') and not mapcss._tag_capture(capture_tags, 2, tags, u'repair'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("borracharia sem ''repair=yes''")
                # suggestAlternative:"repair=yes"
                err.append({'class': 9018002, 'subclass': 817061630, 'text': mapcss.tr(u'borracharia sem \'\'repair=yes\'\'')})

        # *[name=~/(?i)^Borrach(aria|eiro)/][shop!=tyres]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_126ba9a9), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'shop') != mapcss._value_capture(capture_tags, 1, u'tyres'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("borracharia sem ''shop=tyres''")
                # suggestAlternative:"shop=tyres"
                err.append({'class': 9018002, 'subclass': 1324999258, 'text': mapcss.tr(u'borracharia sem \'\'shop=tyres\'\'')})

        return err

    def way(self, data, tags, nds):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[name=*ref][highway]
        # Rule Blacklisted

        # way[highway][name=~/\b[A-Z]{2,4} (- )?[0-9]{2,3}\b/]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_568a42f4), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("rodovia com ref no nome")
                err.append({'class': 9018045, 'subclass': 63246253, 'text': mapcss.tr(u'rodovia com ref no nome')})

        # way[highway=cycleway][name][name!~/^(?i)ciclovia .*/]
        # way[highway][highway!~/bridleway|bus_stop|cycleway|crossing|footway|give_way|motorway_junction|path|raceway|rest_area|services|speed_camera|steps|stop/][name][name!~/^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodoanel|Rodovia|Rotatória|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*/]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'cycleway') and mapcss._tag_capture(capture_tags, 1, tags, u'name') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_2fcb6bab), mapcss._tag_capture(capture_tags, 2, tags, u'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_1054eb5a), mapcss._tag_capture(capture_tags, 1, tags, u'highway')) and mapcss._tag_capture(capture_tags, 2, tags, u'name') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_57eb9fe5), mapcss._tag_capture(capture_tags, 3, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} com logradouro ausente, errado ou abreviado","{0.key}")
                err.append({'class': 9018001, 'subclass': 1231643071, 'text': mapcss.tr(u'{0} com logradouro ausente, errado ou abreviado', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *["addr:street"]["addr:street"!~/^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodovia|Rotatória|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*/]
        if (u'addr:street' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'addr:street') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_3b777b9d), mapcss._tag_capture(capture_tags, 1, tags, u'addr:street')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} com logradouro ausente, errado ou abreviado","{0.key}")
                err.append({'class': 9018001, 'subclass': 588331445, 'text': mapcss.tr(u'{0} com logradouro ausente, errado ou abreviado', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[!highway][route!=road][!public_transport][type!~/route|street/][name][name=~/^(?i)(?u)(alameda|avenida|beco|estrada|ladeira|passarela|rodovia|rotatória|rua|travessa|trevo|viela|(anel|complexo|dispositivo) viário) .*/][name!~/^(?i)estrada de ferro/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'route') != mapcss._value_capture(capture_tags, 1, u'road') and not mapcss._tag_capture(capture_tags, 2, tags, u'public_transport') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_72d45155), mapcss._tag_capture(capture_tags, 3, tags, u'type')) and mapcss._tag_capture(capture_tags, 4, tags, u'name') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 5, self.re_5849be19), mapcss._tag_capture(capture_tags, 5, tags, u'name')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 6, self.re_15690541), mapcss._tag_capture(capture_tags, 6, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("objeto com nome de via mas sem tag de {0}","{0.key}")
                err.append({'class': 9018002, 'subclass': 874993957, 'text': mapcss.tr(u'objeto com nome de via mas sem tag de {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way[highway=track][name][name=~/^(?i)(?u)(alameda|avenida|beco|estrada|ladeira|rodovia|rotatória|rua|travessa|trevo|viela) .*/]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'track') and mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_20cf30ba), mapcss._tag_capture(capture_tags, 2, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("não classificar via como {0}","{0.tag}")
                # suggestAlternative:"highway=residential"
                # suggestAlternative:"highway=unclassified"
                err.append({'class': 9018051, 'subclass': 450185002, 'text': mapcss.tr(u'não classificar via como {0}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[name=~/^(?i)(?u)[a-z0-9]+_([a-z0-9]_?)+$/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_4bd3b925), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("utilizar espaço ao invés de underscore")
                err.append({'class': 9018002, 'subclass': 378801374, 'text': mapcss.tr(u'utilizar espaço ao invés de underscore')})

        # *[name=~/(?i)(^|.* )(Cel|Cmte|Cond|Conj|Dª|Dr|Eng|Gov|Hab|Jd|Jr|Marg|Mun|p\/|Pde|Pe|Pq|Pst|Pref|Profa|Profª|Prof|Res|s\/|Sr(a|ª)?|Sta|Sto|Ver)\.? .*/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_178f5446), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("palavra abreviada em {0}","{0.key}")
                err.append({'class': 9018003, 'subclass': 1784756763, 'text': mapcss.tr(u'palavra abreviada em {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way[highway][name=~/^(?i)(?u)((via de )?(acesso|ligação)(( (a|à))? propriedade)?|entrada|entroncamento|rampa|retorno|rotat(ó|o)ria|r(ó|o)tula|sa(í|i)da|trevo|estrada( municipal| de terra)?|rua|rodovia|via)( (de acesso|sem nome|projetad(a|o)))?$/]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_667ce569), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} com nome supérfluo/incompleto","{0.key}")
                # suggestAlternative:"description"
                # suggestAlternative:"destination"
                err.append({'class': 9018052, 'subclass': 729248989, 'text': mapcss.tr(u'{0} com nome supérfluo/incompleto', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[leisure][name=~/^(?i)(?u)(campo|est(á|a)dio|gin(á|a)sio|quadra)( de (futebol|esportes?))?$/]
        if (u'leisure' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7f53e992), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("nome supérfluo/incompleto de local de lazer")
                err.append({'class': 9018004, 'subclass': 790401825, 'text': mapcss.tr(u'nome supérfluo/incompleto de local de lazer')})

        # *[name=~/^(?i)(?u)((Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF|hospital)$/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_52ab3b8b), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("nome supérfluo/incompleto de local de saúde")
                err.append({'class': 9018005, 'subclass': 1792576894, 'text': mapcss.tr(u'nome supérfluo/incompleto de local de saúde')})

        # *[amenity=~/^(clinic|doctors|hospital)$/][name=~/(?i)\bsaude\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_5ab76b11), mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_4cf86823), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("erro de ortografia em ''saúde''")
                err.append({'class': 9018002, 'subclass': 1455303428, 'text': mapcss.tr(u'erro de ortografia em \'\'saúde\'\'')})

        # *[place=farm][name^="Sitio "]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'farm') and mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, u'name'), mapcss._value_capture(capture_tags, 1, u'Sitio ')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("faltando acento em ''Sítio''")
                err.append({'class': 9018002, 'subclass': 962677162, 'text': mapcss.tr(u'faltando acento em \'\'Sítio\'\'')})

        # *[name=~/^(?i)(?u)(aldeia|borrach(aria|eiro)|bosque|capela|cemit(é|e)rio|c(ó|o)rrego|escola|estacionamento|fazenda|floresta|hospital|igreja|lago|lagoa|mata( nativa)?|praça|parque|parquinho|posto( de gasolina)?|riacho|rio|rodovi(á|a)ria|vila)$/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_20c7dd98), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("local com nome supérfluo, incompleto ou descritivo")
                err.append({'class': 9018002, 'subclass': 501162763, 'text': mapcss.tr(u'local com nome supérfluo, incompleto ou descritivo')})

        # *[amenity=parking][name=~/(?i)^Estacionamento /]
        # Rule Blacklisted

        # way[highway][type=route]
        if (u'highway' in keys and u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'route'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} não deve possuir {1}","{0.key}","{1.tag}")
                err.append({'class': 9018053, 'subclass': 1357959449, 'text': mapcss.tr(u'{0} não deve possuir {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # way[highway][highway!~/bus_stop|milestone|motorway_junction|traffic_signals/][ref][ref!~/^(([A-Z]{2,3}-[0-9]{2,4}|SPM(-| )[0-9]{3} ?(D|E)?|SP(A|D|I)(-| )[0-9]{3}\/[0-9]{3}|[A-Z]{3}-[0-9]{3}\/[0-9]{3});?)+$/]
        # Rule Blacklisted

        # way[highway][!ref][name=~/.*([A-Z]{2,3}-[0-9]{2,4}|SPM(-| )[0-9]{3} ?(D|E)?|SP(A|D|I)(-| )[0-9]{3}\/[0-9]{3}|[A-Z]{3}-[0-9]{3}\/[0-9]{3}).*/]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and not mapcss._tag_capture(capture_tags, 1, tags, u'ref') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_375e3de4), mapcss._tag_capture(capture_tags, 2, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("utilizar o código/sigla da rodovia também na tag {0}","{1.key}")
                err.append({'class': 9018002, 'subclass': 1854606955, 'text': mapcss.tr(u'utilizar o código/sigla da rodovia também na tag {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # way[highway][name=~/Rodovia ([A-Z]{2,3}-[0-9]{2,4})/]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7633bf4e), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("nome incorreto de rodovia; utilizar o nome oficial ou apenas ref")
                err.append({'class': 9018002, 'subclass': 955724850, 'text': mapcss.tr(u'nome incorreto de rodovia; utilizar o nome oficial ou apenas ref')})

        # way[name=*"addr:street"][highway]
        # *[designation=*"addr:housename"]
        # *[ref=*designation]
        # *[ref=*old_ref]
        # *[name=*"addr:housename"]
        # *[name=*designation]
        # *[name=*alt_name]
        # *[name=*int_name]
        # *[name=*loc_name]
        # *[name=*nat_name]
        # *[name=*official_name]
        # *[name=*old_name]
        # *[name=*reg_name]
        # *[name=*short_name]
        # *[name=*sorting_name]
        # Rule Blacklisted

        # *[source=*name]
        if (u'source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} e {1} são iguais","{0.key}","{0.value}")
                err.append({'class': 9018002, 'subclass': 1403015964, 'text': mapcss.tr(u'{0} e {1} são iguais', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[name=~/(?i)(?u)((sem (denomina(ç|c)(ã|a)o|nome|sa(i|í)da))|desconhecido|n(ã|a)o conhecido)/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_65710fdb), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto com nomenclatura incorreta")
                # suggestAlternative:"noname"
                err.append({'class': 9018007, 'subclass': 506924923, 'text': mapcss.tr(u'objeto com nomenclatura incorreta')})

        # *[designation]
        if (u'designation' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'designation'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} é uma chave utilizada apenas no Reino Unido","{0.key}")
                # suggestAlternative:"description"
                # suggestAlternative:"name"
                err.append({'class': 9018009, 'subclass': 1259259930, 'text': mapcss.tr(u'{0} é uma chave utilizada apenas no Reino Unido', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way[highway=~/^(trunk|motorway)$/][!operator]
        # Rule Blacklisted

        # way[highway$=_link][name=~/(Alameda|Avenida|Rua|Travessa|Viela) .*/]
        # Rule Blacklisted

        # way[highway][name=~/(Alameda|Avenida|Rua|Travessa|Viela) .*/][ref]
        if (u'highway' in keys and u'name' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_6b6e390d), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'ref'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("possível uso desnecessário/errado de ref em {0}={1}","{0.key}",tag("highway"))
                err.append({'class': 9018002, 'subclass': 1325624158, 'text': mapcss.tr(u'possível uso desnecessário/errado de ref em {0}={1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss.tag(tags, u'highway'))})

        # *[place=~/hamlet|isolated_dwelling|town|village/][population>=100000]
        if (u'place' in keys and u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_152c10ee), mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'population') >= mapcss._value_capture(capture_tags, 1, 100000))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("local com 100.000 habitantes ou mais deve ser classificado como city")
                # fixAdd:"place=city"
                err.append({'class': 9018006, 'subclass': 149235075, 'text': mapcss.tr(u'local com 100.000 habitantes ou mais deve ser classificado como city'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'place',u'city']])
                }})

        # *[place=~/city|hamlet|isolated_dwelling|village/][population>=10000][population<100000]
        if (u'place' in keys and u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_591572a5), mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'population') >= mapcss._value_capture(capture_tags, 1, 10000) and mapcss._tag_capture(capture_tags, 2, tags, u'population') < mapcss._value_capture(capture_tags, 2, 100000))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("local com população entre 10.000 e 100.000 deve ser classificado como town")
                # fixAdd:"place=town"
                err.append({'class': 9018006, 'subclass': 1174321645, 'text': mapcss.tr(u'local com população entre 10.000 e 100.000 deve ser classificado como town'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'place',u'town']])
                }})

        # *[place][place!~/hamlet|island|isolated_dwelling|neighbourhood|suburb|village/][population<10000]
        if (u'place' in keys and u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_3aeda39d), mapcss._tag_capture(capture_tags, 1, tags, u'place')) and mapcss._tag_capture(capture_tags, 2, tags, u'population') < mapcss._value_capture(capture_tags, 2, 10000))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("local com menos de 10.000 habitantes deve ser classificado como village")
                # fixAdd:"place=village"
                err.append({'class': 9018006, 'subclass': 719699918, 'text': mapcss.tr(u'local com menos de 10.000 habitantes deve ser classificado como village'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'place',u'village']])
                }})

        # *[place=city][!population]
        # *[place=town][!population]
        # *[place=village][!population]
        # Rule Blacklisted

        # *[place=city][!name]
        # *[place=town][!name]
        # *[place=village][!name]
        if (u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'city') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'town') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'village') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} sem nome","{0.value}")
                err.append({'class': 9018012, 'subclass': 828568305, 'text': mapcss.tr(u'{0} sem nome', mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *["addr:city"=~/(,|( |-) ?[A-Z]{2})/]
        if (u'addr:city' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_10f1c360), mapcss._tag_capture(capture_tags, 0, tags, u'addr:city')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve conter apenas o nome da cidade","{0.key}")
                err.append({'class': 9018013, 'subclass': 223700239, 'text': mapcss.tr(u'{0} deve conter apenas o nome da cidade', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name=~/^(?i)(?u)(Faz\.|Fazenda|Sítio|Chácara)/][place][place!~/city|farm|neighbourhood|suburb|town|village/]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_2cd1e949), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'place') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_5d3348cb), mapcss._tag_capture(capture_tags, 2, tags, u'place')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("objeto talvez deva ser {0}=farm","{1.key}")
                err.append({'class': 9018002, 'subclass': 414255329, 'text': mapcss.tr(u'objeto talvez deva ser {0}=farm', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[place][name=~/^(?i)Bairro\b/][name!~/^(?i)Bairro d(a|e|o)s?\b/]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_20fc5143), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_64387998), mapcss._tag_capture(capture_tags, 2, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("objeto talvez não deva ter ''Bairro'' no nome")
                err.append({'class': 9018002, 'subclass': 457937105, 'text': mapcss.tr(u'objeto talvez não deva ter \'\'Bairro\'\' no nome')})

        # *[iata="0"]
        if (u'iata' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'iata') == mapcss._value_capture(capture_tags, 0, u'0'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} com valor = {1}","{0.key}","{0.value}")
                err.append({'class': 9018014, 'subclass': 1389202412, 'text': mapcss.tr(u'{0} com valor = {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[amenity=~/college|school/][name=~/^(?i)(?u)(Centro Universitário|Faculdades?|FATEC|Instituto Federal)\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_362f879f), mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_1d232d4c), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("estabelecimento de ensino classificado incorretamente")
                # suggestAlternative:"amenity=university"
                # fixAdd:"{0.key}=university"
                err.append({'class': 9018006, 'subclass': 221523813, 'text': mapcss.tr(u'estabelecimento de ensino classificado incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=university')).split('=', 1)])
                }})

        # *[amenity=school][name=~/^(?i)(?u)(SENAC|SENAI|Serviço Nacional de Aprendizagem)/]
        # *[amenity=~/school|university/][name=~/(?i)(?u)\b(Centro Paula Souza|Escola Técnica|ETEC)\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'school') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_044c8944), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_6c0d6e9e), mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_3b304b9b), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("estabelecimento de ensino classificado incorretamente")
                # suggestAlternative:"amenity=college"
                # fixAdd:"{0.key}=college"
                err.append({'class': 9018006, 'subclass': 897019825, 'text': mapcss.tr(u'estabelecimento de ensino classificado incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=college')).split('=', 1)])
                }})

        # *[amenity=school][name=~/^(?i)(?u)(auto(-| )?( moto )?escola|centro de formação de condutores|cfc|moto escola)\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'school') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_35bb0f2f), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("autoescola classificada incorretamente")
                # suggestAlternative:"amenity=driving_school"
                # fixAdd:"{0.key}=driving_school"
                err.append({'class': 9018006, 'subclass': 1796023580, 'text': mapcss.tr(u'autoescola classificada incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=driving_school')).split('=', 1)])
                }})

        # *[amenity=school][name=~/^(?i)creche\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'school') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_160d1bfc), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("creche classificada incorretamente")
                # suggestAlternative:"amenity=kindergarten"
                # fixAdd:"{0.key}=kindergarten"
                err.append({'class': 9018006, 'subclass': 121701344, 'text': mapcss.tr(u'creche classificada incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=kindergarten')).split('=', 1)])
                }})

        # *[name=~/^(?i)(?u)Subestação .*/][power][power!=substation]
        # *[name=~/^(?i)(?u)Fórum .*/][amenity][amenity!=courthouse]
        # *[name=~/^(?i)Hospital .*/][building][building!=hospital]
        # *[name=~/^(?i)Universidade .*/][building][building!=university]
        # *[name=~/^(?i)Escola .*/][building][building!=school]
        # *[name=~/^(?i)Hotel .*/][building][building!=hotel]
        # *[name=~/^(?i)Capela .*/][building][building!=chapel]
        # *[name=~/^(?i)Igreja .*/][building][building!=church]
        # *[name=~/^(?i)Catedral .*/][building][building!=cathedral]
        # *[name=~/^(?i)Fazenda .*/][building][building!=farm]
        # *[name=~/^(?i)Supermercado .*/][building][building!=supermarket]
        # Rule Blacklisted

        # *[name=~/^(?i)(?u)(AM(A|E)|(Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF).*/][amenity=hospital]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_7b7c453d), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') == mapcss._value_capture(capture_tags, 1, u'hospital'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("postos/unidades de saúde devem ser amenity=clinic")
                err.append({'class': 9018015, 'subclass': 2108543140, 'text': mapcss.tr(u'postos/unidades de saúde devem ser amenity=clinic')})

        # *[name=~/^(?i)\bSAMU\b/][amenity=~/clinic|doctors|hospital/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_2dbaea13), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_3eb0ab44), mapcss._tag_capture(capture_tags, 1, tags, u'amenity')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("SAMU classificado de forma errada")
                # suggestAlternative:"emergency=ambulance_station"
                err.append({'class': 9018016, 'subclass': 2090365947, 'text': mapcss.tr(u'SAMU classificado de forma errada')})

        # way[highway=give_way]
        # way[highway=mini_roundabout]
        # way[highway=stop]
        # way[highway=turning_circle]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'give_way'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'mini_roundabout'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'stop'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'turning_circle'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve ser utilizado apenas em nós","{0.tag}")
                err.append({'class': 9018047, 'subclass': 2084016255, 'text': mapcss.tr(u'{0} deve ser utilizado apenas em nós', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[crossing][!highway][!railway]
        if (u'crossing' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'crossing') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve ser utilizado com {1}={0} ou {2}={0}","{0.key}","{1.key}","{2.key}")
                err.append({'class': 9018019, 'subclass': 139983185, 'text': mapcss.tr(u'{0} deve ser utilizado com {1}={0} ou {2}={0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[aeroway][designation=~/^[A-Z]{4}$/][!icao]
        # *[aeroway][ref=~/^[A-Z]{4}$/][!icao]
        if (u'aeroway' in keys and u'ref' in keys) or (u'aeroway' in keys and u'designation' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7afc6883), mapcss._tag_capture(capture_tags, 1, tags, u'designation')) and not mapcss._tag_capture(capture_tags, 2, tags, u'icao'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7afc6883), mapcss._tag_capture(capture_tags, 1, tags, u'ref')) and not mapcss._tag_capture(capture_tags, 2, tags, u'icao'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("{0} provavelmente deve ser utilizado como {1}","{1.key}","{2.key}")
                # fixChangeKey:"{1.key} => {2.key}"
                err.append({'class': 9018006, 'subclass': 662001655, 'text': mapcss.tr(u'{0} provavelmente deve ser utilizado como {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, u'{1.key} => {2.key}')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, u'{1.key} => {2.key}')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, u'{1.key} => {2.key}')).split('=>', 1)[0].strip()])
                }})

        # *[access=permissive]
        if (u'access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'permissive'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} deve ser utilizado apenas em vias privadas com permissão de acesso e não em vias de acesso público","{0.tag}")
                err.append({'class': 9018002, 'subclass': 1918455197, 'text': mapcss.tr(u'{0} deve ser utilizado apenas em vias privadas com permissão de acesso e não em vias de acesso público', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[name=~/^(?U)(\p{Upper}| )+$/]
        # *["addr:street"=~/^(?U)(\p{Upper}| )+$/]
        # Rule Blacklisted

        # *["addr:postcode"=~/^[0-9]{8}$/]
        # Rule Blacklisted

        # *[postal_code=~/^[0-9]{8}$/]
        # Rule Blacklisted

        # *["addr:postcode"=~/^[0-9]{5}( |\.)[0-9]{3}$/]
        if (u'addr:postcode' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_57bee688), mapcss._tag_capture(capture_tags, 0, tags, u'addr:postcode')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("formato do CEP pode ser melhorado")
                # fixAdd:concat("addr:postcode=",replace(replace(tag("addr:postcode")," ","-"),".","-"))
                err.append({'class': 9018006, 'subclass': 308348773, 'text': mapcss.tr(u'formato do CEP pode ser melhorado'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'addr:postcode=', mapcss.replace(mapcss.replace(mapcss.tag(tags, u'addr:postcode'), u' ', u'-'), u'.', u'-'))).split('=', 1)])
                }})

        # *["postal_code"=~/^[0-9]{5}( |\.)[0-9]{3}$/]
        if (u'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_57bee688), mapcss._tag_capture(capture_tags, 0, tags, u'postal_code')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("formato do CEP pode ser melhorado")
                # fixAdd:concat("postal_code=",replace(replace(tag("postal_code")," ","-"),".","-"))
                err.append({'class': 9018006, 'subclass': 1211220107, 'text': mapcss.tr(u'formato do CEP pode ser melhorado'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'postal_code=', mapcss.replace(mapcss.replace(mapcss.tag(tags, u'postal_code'), u' ', u'-'), u'.', u'-'))).split('=', 1)])
                }})

        # *["addr:postcode"]["addr:postcode"!~/^[0-9]{5}-[0-9]{3}$/]
        # *[postal_code][postal_code!~/^[0-9]{5}-[0-9]{3}$/]
        # Rule Blacklisted

        # way[highway]["addr:postcode"][highway!=services]
        if (u'addr:postcode' in keys and u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'addr:postcode') and mapcss._tag_capture(capture_tags, 2, tags, u'highway') != mapcss._value_capture(capture_tags, 2, u'services'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("uso incorreto de {0}","{1.key}","{0.key}")
                # suggestAlternative:"postal_code"
                # fixChangeKey:"{1.key} => postal_code"
                err.append({'class': 9018006, 'subclass': 1893232368, 'text': mapcss.tr(u'uso incorreto de {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, u'{1.key} => postal_code')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, u'{1.key} => postal_code')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, u'{1.key} => postal_code')).split('=>', 1)[0].strip()])
                }})

        # *[alt_source][source]
        if (u'alt_source' in keys and u'source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'alt_source') and mapcss._tag_capture(capture_tags, 1, tags, u'source'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve estar incluído em {1}, separado por '';'' caso necessário","{0.key}","{1.key}")
                err.append({'class': 9018020, 'subclass': 512568644, 'text': mapcss.tr(u'{0} deve estar incluído em {1}, separado por \'\';\'\' caso necessário', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[landuse?]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') in ('yes', 'true', '1'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("especificar valor correto para {0} ao invés de ''{1}''","{0.key}",tag("landuse"))
                err.append({'class': 9018021, 'subclass': 2004192493, 'text': mapcss.tr(u'especificar valor correto para {0} ao invés de \'\'{1}\'\'', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss.tag(tags, u'landuse'))})

        # *[long_name]
        if (u'long_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'long_name'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("chave inválida: {0}","{0.key}")
                # suggestAlternative:"alt_name"
                # suggestAlternative:"name"
                # suggestAlternative:"official_name"
                err.append({'class': 9018022, 'subclass': 1648910015, 'text': mapcss.tr(u'chave inválida: {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *["building:levels"<1]
        if (u'building:levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:levels') < mapcss._value_capture(capture_tags, 0, 1))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} com valor inválido","{0.key}")
                err.append({'class': 9018002, 'subclass': 154478605, 'text': mapcss.tr(u'{0} com valor inválido', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[hires?]
        if (u'hires' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'hires') in ('yes', 'true', '1'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("não se deve utilizar {0} para demarcar áreas de cobertura de imagem","{0.key}")
                err.append({'class': 9018023, 'subclass': 1394305840, 'text': mapcss.tr(u'não se deve utilizar {0} para demarcar áreas de cobertura de imagem', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[tourism=motel][amenity!=love_hotel]
        # *[name=~/(?i)\bmotel\b/][amenity!=love_hotel]
        if (u'name' in keys) or (u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == mapcss._value_capture(capture_tags, 0, u'motel') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_capture(capture_tags, 1, u'love_hotel'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_01454d46), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_capture(capture_tags, 1, u'love_hotel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("ausência de tag ''{0}''","{1.value}")
                # fixAdd:"{1.key}={1.value}"
                err.append({'class': 9018006, 'subclass': 444111908, 'text': mapcss.tr(u'ausência de tag \'\'{0}\'\'', mapcss._tag_uncapture(capture_tags, u'{1.value}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{1.key}={1.value}')).split('=', 1)])
                }})

        # *[amenity=love_hotel][tourism][tourism!=motel]
        if (u'amenity' in keys and u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'love_hotel') and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') and mapcss._tag_capture(capture_tags, 2, tags, u'tourism') != mapcss._value_capture(capture_tags, 2, u'motel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("provavelmente deve ser ''{0}={1}''","{2.key}","{2.value}")
                err.append({'class': 9018002, 'subclass': 2021262051, 'text': mapcss.tr(u'provavelmente deve ser \'\'{0}={1}\'\'', mapcss._tag_uncapture(capture_tags, u'{2.key}'), mapcss._tag_uncapture(capture_tags, u'{2.value}'))})

        # *[name=~/(?i)^motel\b/][tourism!=motel]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_5cd37790), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') != mapcss._value_capture(capture_tags, 1, u'motel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("motel classificado incorretamente")
                # suggestAlternative:"tourism=motel"
                err.append({'class': 9018002, 'subclass': 2096064741, 'text': mapcss.tr(u'motel classificado incorretamente')})

        # *[aeroway=aerodrome][name=~/(?i).*airport$/]
        # *[aeroway=helipad][name=~/(?i).*heliport$/]
        if (u'aeroway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'aerodrome') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_6efb8049), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'helipad') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_6566db6a), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} com nome em inglês","{0.tag}")
                err.append({'class': 9018002, 'subclass': 134725283, 'text': mapcss.tr(u'{0} com nome em inglês', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[aeroway=aerodrome][name=~/(?i)^Aer(ódromo|oporto) de.*/]
        # *[aeroway=helipad][name=~/(?i)^Helipo(n|r)to.*/]
        if (u'aeroway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'aerodrome') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_6024a566), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'helipad') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_139e342b), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("conferir se existe nome oficial do {0}","{0.value}")
                err.append({'class': 9018002, 'subclass': 2002284471, 'text': mapcss.tr(u'conferir se existe nome oficial do {0}', mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[aeroway=aerodrome][ref]
        if (u'aeroway' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'aerodrome') and mapcss._tag_capture(capture_tags, 1, tags, u'ref'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("''{0}'' não faz sentido em aeroporto","{1.key}")
                err.append({'class': 9018002, 'subclass': 339634841, 'text': mapcss.tr(u'\'\'{0}\'\' não faz sentido em aeroporto', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # way[waterway][tunnel=yes]
        # Rule Blacklisted

        # way[highway][layer<0][!tunnel]
        # *[waterway][layer<0][!tunnel]
        # Rule Blacklisted

        # way[highway][layer>0][!bridge][highway!=bus_stop]
        # *[waterway][layer>0][!bridge]
        # Rule Blacklisted

        # *[layer][!building][!highway][man_made!=pipeline][!railway][!waterway]
        # Rule Blacklisted

        # way[highway=motorway_junction]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'motorway_junction'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} deve ser utilizado apenas no nó de saída da rodovia","{0.tag}")
                # suggestAlternative:"highway=motorway_link"
                err.append({'class': 9018056, 'subclass': 260528564, 'text': mapcss.tr(u'{0} deve ser utilizado apenas no nó de saída da rodovia', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[name=~/^(?i)(?u)edifício.*/][!building]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_38a8f0ff), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'building'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("possível ausência de tag {0}","{1.key}")
                err.append({'class': 9018026, 'subclass': 1417041710, 'text': mapcss.tr(u'possível ausência de tag {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[route=ferry][!duration]
        if (u'route' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'route') == mapcss._value_capture(capture_tags, 0, u'ferry') and not mapcss._tag_capture(capture_tags, 1, tags, u'duration'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("ausência do tempo de duração ({0}) da balsa","{1.key}")
                err.append({'class': 9018027, 'subclass': 1289884816, 'text': mapcss.tr(u'ausência do tempo de duração ({0}) da balsa', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[name=~/^(?i)(?u)praça.*/][!leisure][landuse=~/^(forest|grass|greenfield|meadow|orchard)$/]
        # *[name=~/^(?i)(?u)praça.*/][!leisure][natural=~/^(grassland|heath|scrub|wood)$/]
        if (u'landuse' in keys and u'name' in keys) or (u'name' in keys and u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_4a8ca94e), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'leisure') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_05a345c7), mapcss._tag_capture(capture_tags, 2, tags, u'landuse')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_4a8ca94e), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'leisure') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_12b48afb), mapcss._tag_capture(capture_tags, 2, tags, u'natural')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("possível definição incorreta para praça: ''{0}''","{2.key}")
                # suggestAlternative:"leisure=park"
                err.append({'class': 9018029, 'subclass': 80498829, 'text': mapcss.tr(u'possível definição incorreta para praça: \'\'{0}\'\'', mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[wikipedia][wikipedia!~/^pt:/]
        if (u'wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_17fd35b3), mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("utilizar prefixo em português (pt:) para {0}","{0.key}")
                err.append({'class': 9018030, 'subclass': 1219382195, 'text': mapcss.tr(u'utilizar prefixo em português (pt:) para {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way[highway][lanes=1][!oneway?][!junction][!narrow]
        # Rule Blacklisted

        # way[cycleway=lane]["cycleway:left"=lane]
        # way[cycleway=lane]["cycleway:right"=lane]
        if (u'cycleway' in keys and u'cycleway:left' in keys) or (u'cycleway' in keys and u'cycleway:right' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'cycleway') == mapcss._value_capture(capture_tags, 0, u'lane') and mapcss._tag_capture(capture_tags, 1, tags, u'cycleway:left') == mapcss._value_capture(capture_tags, 1, u'lane'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'cycleway') == mapcss._value_capture(capture_tags, 0, u'lane') and mapcss._tag_capture(capture_tags, 1, tags, u'cycleway:right') == mapcss._value_capture(capture_tags, 1, u'lane'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("uso incorreto de {0} com {1}","{0.tag}","{1.tag}")
                # suggestAlternative:"{1.tag}"
                err.append({'class': 9018063, 'subclass': 528363416, 'text': mapcss.tr(u'uso incorreto de {0} com {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.tag}'))})

        # *[name=~/.*\(.*\).*/]
        # Rule Blacklisted

        # *[name=~/ - /]
        # Rule Blacklisted

        # *[name=~/, /]
        # Rule Blacklisted

        # *[name=~/: /]
        # Rule Blacklisted

        # *[name=~/ ou /]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_131cc885), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("nome utilizado de forma incorreta")
                # suggestAlternative:"name e alt_name"
                err.append({'class': 9018031, 'subclass': 23034604, 'text': mapcss.tr(u'nome utilizado de forma incorreta')})

        # way[boundary=administrative][!admin_level]!.way_in_relation
        # Use undeclared class way_in_relation

        # way[place][place!~/^(city_block|farm|hamlet|island|islet|isolated_dwelling|neighbourhood|square)$/][!admin_level][!boundary]
        if (u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_58f616c9), mapcss._tag_capture(capture_tags, 1, tags, u'place')) and not mapcss._tag_capture(capture_tags, 2, tags, u'admin_level') and not mapcss._tag_capture(capture_tags, 3, tags, u'boundary'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("local com ausência/incoerência de limite administrativo")
                err.append({'class': 9018002, 'subclass': 372086249, 'text': mapcss.tr(u'local com ausência/incoerência de limite administrativo')})

        # way[admin_level][!boundary]!.way_in_relation
        # way[admin_level][boundary][boundary!=administrative]!.way_in_relation
        # Use undeclared class way_in_relation

        # *[boundary=national_park][!name]
        # *[boundary=protected_area][!name]
        # *[leisure=nature_reserve][!name]
        if (u'boundary' in keys) or (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'national_park') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'protected_area') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'nature_reserve') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
                err.append({'class': 9018033, 'subclass': 1492609299, 'text': mapcss.tr(u'{0} deve possuir {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[boundary=protected_area][!protect_class]
        if (u'boundary' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'protected_area') and not mapcss._tag_capture(capture_tags, 1, tags, u'protect_class'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
                err.append({'class': 9018033, 'subclass': 822952800, 'text': mapcss.tr(u'{0} deve possuir {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[protect_class][protect_class!~/^(1(a|b)?|[1-9][0-9]?)$/]
        if (u'protect_class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'protect_class') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_5ac7053e), mapcss._tag_capture(capture_tags, 1, tags, u'protect_class')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("valor incorreto para {0}","{0.key}")
                err.append({'class': 9018034, 'subclass': 1459161459, 'text': mapcss.tr(u'valor incorreto para {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[protect_class][boundary!=protected_area]
        if (u'protect_class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'protect_class') and mapcss._tag_capture(capture_tags, 1, tags, u'boundary') != mapcss._value_capture(capture_tags, 1, u'protected_area'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("ausência de boundary=protected_area")
                err.append({'class': 9018035, 'subclass': 1208814760, 'text': mapcss.tr(u'ausência de boundary=protected_area')})

        # *[name=~/.* D(a|e|o)s? .*/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_2ffc377d), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("''da'', ''de'' e ''do'' são minúsculos nos nomes em português")
                err.append({'class': 9018002, 'subclass': 1986668346, 'text': mapcss.tr(u'\'\'da\'\', \'\'de\'\' e \'\'do\'\' são minúsculos nos nomes em português')})

        # *[name=~/^[a-z].*/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_39d67968), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("nome iniciando com letra minúscula")
                err.append({'class': 9018002, 'subclass': 167462302, 'text': mapcss.tr(u'nome iniciando com letra minúscula')})

        # *[alt_ref]
        if (u'alt_ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'alt_ref'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("o conteúdo de {0} deve fazer parte de ref, separado por ;","{0.key}")
                # suggestAlternative:"ref"
                err.append({'class': 9018039, 'subclass': 722411109, 'text': mapcss.tr(u'o conteúdo de {0} deve fazer parte de ref, separado por ;', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # way[highway=path][tracktype]
        if (u'highway' in keys and u'tracktype' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'path') and mapcss._tag_capture(capture_tags, 1, tags, u'tracktype'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("uso incorreto de {0}","{1.key}")
                # suggestAlternative:"trail_visibility"
                err.append({'class': 9018064, 'subclass': 2113951549, 'text': mapcss.tr(u'uso incorreto de {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # way[highway!=track][tracktype]
        # Rule Blacklisted

        # *[surface][eval(number_of_tags())=1]
        if (u'surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'surface') and len(tags) == 1)
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto incompleto: possui apenas {0}","{0.key}")
                err.append({'class': 9018041, 'subclass': 1776991136, 'text': mapcss.tr(u'objeto incompleto: possui apenas {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name][surface][eval(number_of_tags())=2]
        # *[name][website][eval(number_of_tags())=2]
        if (u'name' in keys and u'surface' in keys) or (u'name' in keys and u'website' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'surface') and len(tags) == 2)
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'website') and len(tags) == 2)
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto incompleto: possui apenas {0} e {1}","{0.key}","{1.key}")
                err.append({'class': 9018042, 'subclass': 626126700, 'text': mapcss.tr(u'objeto incompleto: possui apenas {0} e {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # way[highway=~/^(living_street|pedestrian|residential|road|service|track)$/][ref]
        if (u'highway' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_07f31a73), mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'ref'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("a via deve ser ao menos tertiary")
                err.append({'class': 9018002, 'subclass': 1461580029, 'text': mapcss.tr(u'a via deve ser ao menos tertiary')})

        # way[bridge][!layer]
        # way[tunnel][!layer]
        # Rule Blacklisted

        # *[leisure=pitch][sport=tennis][surface=unpaved]
        if (u'leisure' in keys and u'sport' in keys and u'surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'pitch') and mapcss._tag_capture(capture_tags, 1, tags, u'sport') == mapcss._value_capture(capture_tags, 1, u'tennis') and mapcss._tag_capture(capture_tags, 2, tags, u'surface') == mapcss._value_capture(capture_tags, 2, u'unpaved'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("{0} com superfície incorreta","{2.key}")
                # suggestAlternative:"surface=clay"
                # fixAdd:"surface=clay"
                err.append({'class': 9018006, 'subclass': 1659179489, 'text': mapcss.tr(u'{0} com superfície incorreta', mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'surface',u'clay']])
                }})

        # *[amenity=fuel][name=~/(?i)(?u)\b(Ale|BR|Esso|Ipiranga|Petrobr(á|a)s|Shell|Texaco)\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'fuel') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_604bb645), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("uso incorreto da bandeira do posto")
                # suggestAlternative:"brand"
                err.append({'class': 9018002, 'subclass': 935774110, 'text': mapcss.tr(u'uso incorreto da bandeira do posto')})

        # *[/_[0-9]$/][!"is_in:iso_3166_2"]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_57b8ef8e) and not mapcss._tag_capture(capture_tags, 1, tags, u'is_in:iso_3166_2'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("chave inválida: {0}","{0.key}")
                err.append({'class': 9018022, 'subclass': 331369569, 'text': mapcss.tr(u'chave inválida: {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *["addr:housenumber"=~/(?i)^s(\.|-| )?\/?n\.?º?$/][!note]
        if (u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_0b27200b), mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber')) and not mapcss._tag_capture(capture_tags, 1, tags, u'note'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("não utilizar ''{0}'' para locais sem número",tag("addr:housenumber"))
                # suggestAlternative:"note"
                # fixRemove:"addr:housenumber"
                # fixAdd:"note=Local sem número"
                err.append({'class': 9018006, 'subclass': 931902546, 'text': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', mapcss.tag(tags, u'addr:housenumber')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'note',u'Local sem número']]),
                    '-': ([
                    u'addr:housenumber'])
                }})

        # *["addr:housenumber"=~/(?i)^s(\.|-| )?\/?n\.?º?$/][note]
        if (u'addr:housenumber' in keys and u'note' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_0b27200b), mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber')) and mapcss._tag_capture(capture_tags, 1, tags, u'note'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("não utilizar ''{0}'' para locais sem número",tag("addr:housenumber"))
                # suggestAlternative:"note"
                err.append({'class': 9018043, 'subclass': 1717284811, 'text': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', mapcss.tag(tags, u'addr:housenumber'))})

        # *[source=~/(?i)google/]
        if (u'source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_2e8e4f2b), mapcss._tag_capture(capture_tags, 0, tags, u'source')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("objeto contém Google como source")
                err.append({'class': 9018044, 'subclass': 1313403884, 'text': mapcss.tr(u'objeto contém Google como source')})

        # *[amenity=townhall][name=~/^(?i)(?u)c(â|a)mara\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'townhall') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_46ab4d8d), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("câmara de vereadores mapeada incorretamente")
                # suggestAlternative:"office=government + government=legislative"
                err.append({'class': 9018002, 'subclass': 129695507, 'text': mapcss.tr(u'câmara de vereadores mapeada incorretamente')})

        # *[office=government][government!=legislative][name=~/^(?i)(?u)c(â|a)mara\b/]
        if (u'name' in keys and u'office' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'government') and mapcss._tag_capture(capture_tags, 1, tags, u'government') != mapcss._value_capture(capture_tags, 1, u'legislative') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_46ab4d8d), mapcss._tag_capture(capture_tags, 2, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("ausência de government=legislative")
                err.append({'class': 9018002, 'subclass': 869412796, 'text': mapcss.tr(u'ausência de government=legislative')})

        # *[amenity=townhall][name=~/^(?i)(?u)c((â|a)me|ama)ra\b/]
        # *[office=government][name=~/^(?i)(?u)c((â|a)me|ama)ra\b/]
        if (u'amenity' in keys and u'name' in keys) or (u'name' in keys and u'office' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'townhall') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_793b22ec), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'government') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_793b22ec), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("erro de ortografia em ''câmara''")
                err.append({'class': 9018002, 'subclass': 212328084, 'text': mapcss.tr(u'erro de ortografia em \'\'câmara\'\'')})

        # *[amenity=charging_station]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'charging_station'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("possivelmente deve ser amenity=fuel")
                err.append({'class': 9018002, 'subclass': 128902291, 'text': mapcss.tr(u'possivelmente deve ser amenity=fuel')})

        # *[name=~/(?i)^Borrach(aria|eiro)/][shop=tyres][!repair]
        if (u'name' in keys and u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_126ba9a9), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'shop') == mapcss._value_capture(capture_tags, 1, u'tyres') and not mapcss._tag_capture(capture_tags, 2, tags, u'repair'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("borracharia sem ''repair=yes''")
                # suggestAlternative:"repair=yes"
                err.append({'class': 9018002, 'subclass': 817061630, 'text': mapcss.tr(u'borracharia sem \'\'repair=yes\'\'')})

        # *[name=~/(?i)^Borrach(aria|eiro)/][shop!=tyres]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_126ba9a9), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'shop') != mapcss._value_capture(capture_tags, 1, u'tyres'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("borracharia sem ''shop=tyres''")
                # suggestAlternative:"shop=tyres"
                err.append({'class': 9018002, 'subclass': 1324999258, 'text': mapcss.tr(u'borracharia sem \'\'shop=tyres\'\'')})

        # way[waterway=~/^(river|stream)$/][name][name!~/^(?U)(Água|Arroio|Cabeceira|Córrego|Furo|Grota|Igarapé|Lajeado|Paraná|Restinga|Riacho|Ribeirão|Rio|Sanga)\b/]
        # way[waterway=~/^(river|stream)$/][alt_name][alt_name!~/^(?U)(Água|Arroio|Cabeceira|Córrego|Furo|Grota|Igarapé|Lajeado|Paraná|Restinga|Riacho|Ribeirão|Rio|Sanga)\b/]
        if (u'name' in keys and u'waterway' in keys) or (u'alt_name' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_04873a60), mapcss._tag_capture(capture_tags, 0, tags, u'waterway')) and mapcss._tag_capture(capture_tags, 1, tags, u'name') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_280004fd), mapcss._tag_capture(capture_tags, 2, tags, u'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_04873a60), mapcss._tag_capture(capture_tags, 0, tags, u'waterway')) and mapcss._tag_capture(capture_tags, 1, tags, u'alt_name') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_280004fd), mapcss._tag_capture(capture_tags, 2, tags, u'alt_name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} com possível nome errado/incompleto",tag(waterway))
                err.append({'class': 9018002, 'subclass': 1906904535, 'text': mapcss.tr(u'{0} com possível nome errado/incompleto', mapcss.tag(tags, u'waterway'))})

        return err

    def relation(self, data, tags, members):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # relation[highway][name=~/\b[A-Z]{2,3} (- )?[0-9]{2,3}\b/]
        if (u'highway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_073e5345), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("rodovia com ref no nome")
                err.append({'class': 9018045, 'subclass': 523480189, 'text': mapcss.tr(u'rodovia com ref no nome')})

        # *["addr:street"]["addr:street"!~/^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodovia|Rotatória|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*/]
        if (u'addr:street' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'addr:street') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_3b777b9d), mapcss._tag_capture(capture_tags, 1, tags, u'addr:street')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} com logradouro ausente, errado ou abreviado","{0.key}")
                err.append({'class': 9018001, 'subclass': 588331445, 'text': mapcss.tr(u'{0} com logradouro ausente, errado ou abreviado', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[!highway][route!=road][!public_transport][type!~/route|street/][name][name=~/^(?i)(?u)(alameda|avenida|beco|estrada|ladeira|passarela|rodovia|rotatória|rua|travessa|trevo|viela|(anel|complexo|dispositivo) viário) .*/][name!~/^(?i)estrada de ferro/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (not mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'route') != mapcss._value_capture(capture_tags, 1, u'road') and not mapcss._tag_capture(capture_tags, 2, tags, u'public_transport') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 3, self.re_72d45155), mapcss._tag_capture(capture_tags, 3, tags, u'type')) and mapcss._tag_capture(capture_tags, 4, tags, u'name') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 5, self.re_5849be19), mapcss._tag_capture(capture_tags, 5, tags, u'name')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 6, self.re_15690541), mapcss._tag_capture(capture_tags, 6, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("objeto com nome de via mas sem tag de {0}","{0.key}")
                err.append({'class': 9018002, 'subclass': 874993957, 'text': mapcss.tr(u'objeto com nome de via mas sem tag de {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name=~/^(?i)(?u)[a-z0-9]+_([a-z0-9]_?)+$/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_4bd3b925), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("utilizar espaço ao invés de underscore")
                err.append({'class': 9018002, 'subclass': 378801374, 'text': mapcss.tr(u'utilizar espaço ao invés de underscore')})

        # *[name=~/(?i)(^|.* )(Cel|Cmte|Cond|Conj|Dª|Dr|Eng|Gov|Hab|Jd|Jr|Marg|Mun|p\/|Pde|Pe|Pq|Pst|Pref|Profa|Profª|Prof|Res|s\/|Sr(a|ª)?|Sta|Sto|Ver)\.? .*/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_178f5446), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("palavra abreviada em {0}","{0.key}")
                err.append({'class': 9018003, 'subclass': 1784756763, 'text': mapcss.tr(u'palavra abreviada em {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[leisure][name=~/^(?i)(?u)(campo|est(á|a)dio|gin(á|a)sio|quadra)( de (futebol|esportes?))?$/]
        if (u'leisure' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7f53e992), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("nome supérfluo/incompleto de local de lazer")
                err.append({'class': 9018004, 'subclass': 790401825, 'text': mapcss.tr(u'nome supérfluo/incompleto de local de lazer')})

        # *[name=~/^(?i)(?u)((Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF|hospital)$/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_52ab3b8b), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("nome supérfluo/incompleto de local de saúde")
                err.append({'class': 9018005, 'subclass': 1792576894, 'text': mapcss.tr(u'nome supérfluo/incompleto de local de saúde')})

        # *[amenity=~/^(clinic|doctors|hospital)$/][name=~/(?i)\bsaude\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_5ab76b11), mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_4cf86823), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("erro de ortografia em ''saúde''")
                err.append({'class': 9018002, 'subclass': 1455303428, 'text': mapcss.tr(u'erro de ortografia em \'\'saúde\'\'')})

        # *[place=farm][name^="Sitio "]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'farm') and mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, u'name'), mapcss._value_capture(capture_tags, 1, u'Sitio ')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("faltando acento em ''Sítio''")
                err.append({'class': 9018002, 'subclass': 962677162, 'text': mapcss.tr(u'faltando acento em \'\'Sítio\'\'')})

        # *[name=~/^(?i)(?u)(aldeia|borrach(aria|eiro)|bosque|capela|cemit(é|e)rio|c(ó|o)rrego|escola|estacionamento|fazenda|floresta|hospital|igreja|lago|lagoa|mata( nativa)?|praça|parque|parquinho|posto( de gasolina)?|riacho|rio|rodovi(á|a)ria|vila)$/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_20c7dd98), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("local com nome supérfluo, incompleto ou descritivo")
                err.append({'class': 9018002, 'subclass': 501162763, 'text': mapcss.tr(u'local com nome supérfluo, incompleto ou descritivo')})

        # *[amenity=parking][name=~/(?i)^Estacionamento /]
        # Rule Blacklisted

        # relation[type=route][highway]
        if (u'highway' in keys and u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'route') and mapcss._tag_capture(capture_tags, 1, tags, u'highway'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("relação não deve possuir {0}","{1.key}")
                err.append({'class': 9018046, 'subclass': 890277462, 'text': mapcss.tr(u'relação não deve possuir {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[designation=*"addr:housename"]
        # *[ref=*designation]
        # *[ref=*old_ref]
        # *[name=*"addr:housename"]
        # *[name=*designation]
        # *[name=*alt_name]
        # *[name=*int_name]
        # *[name=*loc_name]
        # *[name=*nat_name]
        # *[name=*official_name]
        # *[name=*old_name]
        # *[name=*reg_name]
        # *[name=*short_name]
        # *[name=*sorting_name]
        if (u'designation' in keys) or (u'name' in keys) or (u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'designation') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'addr:housename')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'designation')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'ref') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'old_ref')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'addr:housename')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'designation')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'alt_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'int_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'loc_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'nat_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'official_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'old_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'reg_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'short_name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'sorting_name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("{0} e {1} são iguais; remover chave {1} desnecessária","{0.key}","{0.value}")
                # fixRemove:"{0.value}"
                err.append({'class': 9018006, 'subclass': 1882388489, 'text': mapcss.tr(u'{0} e {1} são iguais; remover chave {1} desnecessária', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}')), 'allow_fix_override': True, 'fix': {
                    '-': ([
                    mapcss._tag_uncapture(capture_tags, u'{0.value}')])
                }})

        # *[source=*name]
        if (u'source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'source') == mapcss._value_capture(capture_tags, 0, mapcss.tag(tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} e {1} são iguais","{0.key}","{0.value}")
                err.append({'class': 9018002, 'subclass': 1403015964, 'text': mapcss.tr(u'{0} e {1} são iguais', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[name=~/(?i)(?u)((sem (denomina(ç|c)(ã|a)o|nome|sa(i|í)da))|desconhecido|n(ã|a)o conhecido)/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_65710fdb), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto com nomenclatura incorreta")
                # suggestAlternative:"noname"
                err.append({'class': 9018007, 'subclass': 506924923, 'text': mapcss.tr(u'objeto com nomenclatura incorreta')})

        # *[designation]
        if (u'designation' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'designation'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} é uma chave utilizada apenas no Reino Unido","{0.key}")
                # suggestAlternative:"description"
                # suggestAlternative:"name"
                err.append({'class': 9018009, 'subclass': 1259259930, 'text': mapcss.tr(u'{0} é uma chave utilizada apenas no Reino Unido', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[place=~/hamlet|isolated_dwelling|town|village/][population>=100000]
        if (u'place' in keys and u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_152c10ee), mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'population') >= mapcss._value_capture(capture_tags, 1, 100000))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("local com 100.000 habitantes ou mais deve ser classificado como city")
                # fixAdd:"place=city"
                err.append({'class': 9018006, 'subclass': 149235075, 'text': mapcss.tr(u'local com 100.000 habitantes ou mais deve ser classificado como city'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'place',u'city']])
                }})

        # *[place=~/city|hamlet|isolated_dwelling|village/][population>=10000][population<100000]
        if (u'place' in keys and u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_591572a5), mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'population') >= mapcss._value_capture(capture_tags, 1, 10000) and mapcss._tag_capture(capture_tags, 2, tags, u'population') < mapcss._value_capture(capture_tags, 2, 100000))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("local com população entre 10.000 e 100.000 deve ser classificado como town")
                # fixAdd:"place=town"
                err.append({'class': 9018006, 'subclass': 1174321645, 'text': mapcss.tr(u'local com população entre 10.000 e 100.000 deve ser classificado como town'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'place',u'town']])
                }})

        # *[place][place!~/hamlet|island|isolated_dwelling|neighbourhood|suburb|village/][population<10000]
        if (u'place' in keys and u'population' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_3aeda39d), mapcss._tag_capture(capture_tags, 1, tags, u'place')) and mapcss._tag_capture(capture_tags, 2, tags, u'population') < mapcss._value_capture(capture_tags, 2, 10000))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("local com menos de 10.000 habitantes deve ser classificado como village")
                # fixAdd:"place=village"
                err.append({'class': 9018006, 'subclass': 719699918, 'text': mapcss.tr(u'local com menos de 10.000 habitantes deve ser classificado como village'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'place',u'village']])
                }})

        # *[place=city][!population]
        # *[place=town][!population]
        # *[place=village][!population]
        # Rule Blacklisted

        # *[place=city][!name]
        # *[place=town][!name]
        # *[place=village][!name]
        if (u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'city') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'town') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') == mapcss._value_capture(capture_tags, 0, u'village') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} sem nome","{0.value}")
                err.append({'class': 9018012, 'subclass': 828568305, 'text': mapcss.tr(u'{0} sem nome', mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *["addr:city"=~/(,|( |-) ?[A-Z]{2})/]
        if (u'addr:city' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_10f1c360), mapcss._tag_capture(capture_tags, 0, tags, u'addr:city')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve conter apenas o nome da cidade","{0.key}")
                err.append({'class': 9018013, 'subclass': 223700239, 'text': mapcss.tr(u'{0} deve conter apenas o nome da cidade', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name=~/^(?i)(?u)(Faz\.|Fazenda|Sítio|Chácara)/][place][place!~/city|farm|neighbourhood|suburb|town|village/]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_2cd1e949), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'place') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_5d3348cb), mapcss._tag_capture(capture_tags, 2, tags, u'place')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("objeto talvez deva ser {0}=farm","{1.key}")
                err.append({'class': 9018002, 'subclass': 414255329, 'text': mapcss.tr(u'objeto talvez deva ser {0}=farm', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[place][name=~/^(?i)Bairro\b/][name!~/^(?i)Bairro d(a|e|o)s?\b/]
        if (u'name' in keys and u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_20fc5143), mapcss._tag_capture(capture_tags, 1, tags, u'name')) and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_64387998), mapcss._tag_capture(capture_tags, 2, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("objeto talvez não deva ter ''Bairro'' no nome")
                err.append({'class': 9018002, 'subclass': 457937105, 'text': mapcss.tr(u'objeto talvez não deva ter \'\'Bairro\'\' no nome')})

        # *[iata="0"]
        if (u'iata' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'iata') == mapcss._value_capture(capture_tags, 0, u'0'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} com valor = {1}","{0.key}","{0.value}")
                err.append({'class': 9018014, 'subclass': 1389202412, 'text': mapcss.tr(u'{0} com valor = {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[amenity=~/college|school/][name=~/^(?i)(?u)(Centro Universitário|Faculdades?|FATEC|Instituto Federal)\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_362f879f), mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_1d232d4c), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("estabelecimento de ensino classificado incorretamente")
                # suggestAlternative:"amenity=university"
                # fixAdd:"{0.key}=university"
                err.append({'class': 9018006, 'subclass': 221523813, 'text': mapcss.tr(u'estabelecimento de ensino classificado incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=university')).split('=', 1)])
                }})

        # *[amenity=school][name=~/^(?i)(?u)(SENAC|SENAI|Serviço Nacional de Aprendizagem)/]
        # *[amenity=~/school|university/][name=~/(?i)(?u)\b(Centro Paula Souza|Escola Técnica|ETEC)\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'school') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_044c8944), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_6c0d6e9e), mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_3b304b9b), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("estabelecimento de ensino classificado incorretamente")
                # suggestAlternative:"amenity=college"
                # fixAdd:"{0.key}=college"
                err.append({'class': 9018006, 'subclass': 897019825, 'text': mapcss.tr(u'estabelecimento de ensino classificado incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=college')).split('=', 1)])
                }})

        # *[amenity=school][name=~/^(?i)(?u)(auto(-| )?( moto )?escola|centro de formação de condutores|cfc|moto escola)\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'school') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_35bb0f2f), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("autoescola classificada incorretamente")
                # suggestAlternative:"amenity=driving_school"
                # fixAdd:"{0.key}=driving_school"
                err.append({'class': 9018006, 'subclass': 1796023580, 'text': mapcss.tr(u'autoescola classificada incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=driving_school')).split('=', 1)])
                }})

        # *[amenity=school][name=~/^(?i)creche\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'school') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_160d1bfc), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("creche classificada incorretamente")
                # suggestAlternative:"amenity=kindergarten"
                # fixAdd:"{0.key}=kindergarten"
                err.append({'class': 9018006, 'subclass': 121701344, 'text': mapcss.tr(u'creche classificada incorretamente'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{0.key}=kindergarten')).split('=', 1)])
                }})

        # *[name=~/^(?i)(?u)Subestação .*/][power][power!=substation]
        # *[name=~/^(?i)(?u)Fórum .*/][amenity][amenity!=courthouse]
        # *[name=~/^(?i)Hospital .*/][building][building!=hospital]
        # *[name=~/^(?i)Universidade .*/][building][building!=university]
        # *[name=~/^(?i)Escola .*/][building][building!=school]
        # *[name=~/^(?i)Hotel .*/][building][building!=hotel]
        # *[name=~/^(?i)Capela .*/][building][building!=chapel]
        # *[name=~/^(?i)Igreja .*/][building][building!=church]
        # *[name=~/^(?i)Catedral .*/][building][building!=cathedral]
        # *[name=~/^(?i)Fazenda .*/][building][building!=farm]
        # *[name=~/^(?i)Supermercado .*/][building][building!=supermarket]
        # Rule Blacklisted

        # *[name=~/^(?i)(?u)(AM(A|E)|(Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF).*/][amenity=hospital]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_7b7c453d), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') == mapcss._value_capture(capture_tags, 1, u'hospital'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("postos/unidades de saúde devem ser amenity=clinic")
                err.append({'class': 9018015, 'subclass': 2108543140, 'text': mapcss.tr(u'postos/unidades de saúde devem ser amenity=clinic')})

        # *[name=~/^(?i)\bSAMU\b/][amenity=~/clinic|doctors|hospital/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_2dbaea13), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_3eb0ab44), mapcss._tag_capture(capture_tags, 1, tags, u'amenity')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("SAMU classificado de forma errada")
                # suggestAlternative:"emergency=ambulance_station"
                err.append({'class': 9018016, 'subclass': 2090365947, 'text': mapcss.tr(u'SAMU classificado de forma errada')})

        # relation[highway=give_way]
        # relation[highway=mini_roundabout]
        # relation[highway=stop]
        # relation[highway=turning_circle]
        if (u'highway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'give_way'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'mini_roundabout'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'stop'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == mapcss._value_capture(capture_tags, 0, u'turning_circle'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve ser utilizado apenas em nós","{0.tag}")
                err.append({'class': 9018047, 'subclass': 1663665792, 'text': mapcss.tr(u'{0} deve ser utilizado apenas em nós', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # relation[enforcement=maxspeed][!maxspeed]
        # relation[enforcement=maxheight][!maxheight]
        # relation[enforcement=maxweight][!maxweight]
        if (u'enforcement' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'enforcement') == mapcss._value_capture(capture_tags, 0, u'maxspeed') and not mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'enforcement') == mapcss._value_capture(capture_tags, 0, u'maxheight') and not mapcss._tag_capture(capture_tags, 1, tags, u'maxheight'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'enforcement') == mapcss._value_capture(capture_tags, 0, u'maxweight') and not mapcss._tag_capture(capture_tags, 1, tags, u'maxweight'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("adicionar {0} ao {1}","{1.key}","{0.tag}")
                err.append({'class': 9018018, 'subclass': 73808614, 'text': mapcss.tr(u'adicionar {0} ao {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[crossing][!highway][!railway]
        if (u'crossing' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'crossing') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve ser utilizado com {1}={0} ou {2}={0}","{0.key}","{1.key}","{2.key}")
                err.append({'class': 9018019, 'subclass': 139983185, 'text': mapcss.tr(u'{0} deve ser utilizado com {1}={0} ou {2}={0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[aeroway][designation=~/^[A-Z]{4}$/][!icao]
        # *[aeroway][ref=~/^[A-Z]{4}$/][!icao]
        if (u'aeroway' in keys and u'ref' in keys) or (u'aeroway' in keys and u'designation' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7afc6883), mapcss._tag_capture(capture_tags, 1, tags, u'designation')) and not mapcss._tag_capture(capture_tags, 2, tags, u'icao'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_7afc6883), mapcss._tag_capture(capture_tags, 1, tags, u'ref')) and not mapcss._tag_capture(capture_tags, 2, tags, u'icao'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("{0} provavelmente deve ser utilizado como {1}","{1.key}","{2.key}")
                # fixChangeKey:"{1.key} => {2.key}"
                err.append({'class': 9018006, 'subclass': 662001655, 'text': mapcss.tr(u'{0} provavelmente deve ser utilizado como {1}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [(mapcss._tag_uncapture(capture_tags, u'{1.key} => {2.key}')).split('=>', 1)[1].strip(), mapcss.tag(tags, (mapcss._tag_uncapture(capture_tags, u'{1.key} => {2.key}')).split('=>', 1)[0].strip())]]),
                    '-': ([
                    (mapcss._tag_uncapture(capture_tags, u'{1.key} => {2.key}')).split('=>', 1)[0].strip()])
                }})

        # *[access=permissive]
        if (u'access' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'access') == mapcss._value_capture(capture_tags, 0, u'permissive'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} deve ser utilizado apenas em vias privadas com permissão de acesso e não em vias de acesso público","{0.tag}")
                err.append({'class': 9018002, 'subclass': 1918455197, 'text': mapcss.tr(u'{0} deve ser utilizado apenas em vias privadas com permissão de acesso e não em vias de acesso público', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[name=~/^(?U)(\p{Upper}| )+$/]
        # *["addr:street"=~/^(?U)(\p{Upper}| )+$/]
        # Rule Blacklisted

        # *["addr:postcode"=~/^[0-9]{8}$/]
        # Rule Blacklisted

        # *[postal_code=~/^[0-9]{8}$/]
        # Rule Blacklisted

        # *["addr:postcode"=~/^[0-9]{5}( |\.)[0-9]{3}$/]
        if (u'addr:postcode' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_57bee688), mapcss._tag_capture(capture_tags, 0, tags, u'addr:postcode')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("formato do CEP pode ser melhorado")
                # fixAdd:concat("addr:postcode=",replace(replace(tag("addr:postcode")," ","-"),".","-"))
                err.append({'class': 9018006, 'subclass': 308348773, 'text': mapcss.tr(u'formato do CEP pode ser melhorado'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'addr:postcode=', mapcss.replace(mapcss.replace(mapcss.tag(tags, u'addr:postcode'), u' ', u'-'), u'.', u'-'))).split('=', 1)])
                }})

        # *["postal_code"=~/^[0-9]{5}( |\.)[0-9]{3}$/]
        if (u'postal_code' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_57bee688), mapcss._tag_capture(capture_tags, 0, tags, u'postal_code')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("formato do CEP pode ser melhorado")
                # fixAdd:concat("postal_code=",replace(replace(tag("postal_code")," ","-"),".","-"))
                err.append({'class': 9018006, 'subclass': 1211220107, 'text': mapcss.tr(u'formato do CEP pode ser melhorado'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss.concat(u'postal_code=', mapcss.replace(mapcss.replace(mapcss.tag(tags, u'postal_code'), u' ', u'-'), u'.', u'-'))).split('=', 1)])
                }})

        # *["addr:postcode"]["addr:postcode"!~/^[0-9]{5}-[0-9]{3}$/]
        # *[postal_code][postal_code!~/^[0-9]{5}-[0-9]{3}$/]
        # Rule Blacklisted

        # *[alt_source][source]
        if (u'alt_source' in keys and u'source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'alt_source') and mapcss._tag_capture(capture_tags, 1, tags, u'source'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve estar incluído em {1}, separado por '';'' caso necessário","{0.key}","{1.key}")
                err.append({'class': 9018020, 'subclass': 512568644, 'text': mapcss.tr(u'{0} deve estar incluído em {1}, separado por \'\';\'\' caso necessário', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[landuse?]
        if (u'landuse' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'landuse') in ('yes', 'true', '1'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("especificar valor correto para {0} ao invés de ''{1}''","{0.key}",tag("landuse"))
                err.append({'class': 9018021, 'subclass': 2004192493, 'text': mapcss.tr(u'especificar valor correto para {0} ao invés de \'\'{1}\'\'', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss.tag(tags, u'landuse'))})

        # *[long_name]
        if (u'long_name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'long_name'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("chave inválida: {0}","{0.key}")
                # suggestAlternative:"alt_name"
                # suggestAlternative:"name"
                # suggestAlternative:"official_name"
                err.append({'class': 9018022, 'subclass': 1648910015, 'text': mapcss.tr(u'chave inválida: {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *["building:levels"<1]
        if (u'building:levels' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'building:levels') < mapcss._value_capture(capture_tags, 0, 1))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} com valor inválido","{0.key}")
                err.append({'class': 9018002, 'subclass': 154478605, 'text': mapcss.tr(u'{0} com valor inválido', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[hires?]
        if (u'hires' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'hires') in ('yes', 'true', '1'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("não se deve utilizar {0} para demarcar áreas de cobertura de imagem","{0.key}")
                err.append({'class': 9018023, 'subclass': 1394305840, 'text': mapcss.tr(u'não se deve utilizar {0} para demarcar áreas de cobertura de imagem', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[tourism=motel][amenity!=love_hotel]
        # *[name=~/(?i)\bmotel\b/][amenity!=love_hotel]
        if (u'name' in keys) or (u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == mapcss._value_capture(capture_tags, 0, u'motel') and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_capture(capture_tags, 1, u'love_hotel'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_01454d46), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != mapcss._value_capture(capture_tags, 1, u'love_hotel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("ausência de tag ''{0}''","{1.value}")
                # fixAdd:"{1.key}={1.value}"
                err.append({'class': 9018006, 'subclass': 444111908, 'text': mapcss.tr(u'ausência de tag \'\'{0}\'\'', mapcss._tag_uncapture(capture_tags, u'{1.value}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    (mapcss._tag_uncapture(capture_tags, u'{1.key}={1.value}')).split('=', 1)])
                }})

        # *[amenity=love_hotel][tourism][tourism!=motel]
        if (u'amenity' in keys and u'tourism' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'love_hotel') and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') and mapcss._tag_capture(capture_tags, 2, tags, u'tourism') != mapcss._value_capture(capture_tags, 2, u'motel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("provavelmente deve ser ''{0}={1}''","{2.key}","{2.value}")
                err.append({'class': 9018002, 'subclass': 2021262051, 'text': mapcss.tr(u'provavelmente deve ser \'\'{0}={1}\'\'', mapcss._tag_uncapture(capture_tags, u'{2.key}'), mapcss._tag_uncapture(capture_tags, u'{2.value}'))})

        # *[name=~/(?i)^motel\b/][tourism!=motel]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_5cd37790), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') != mapcss._value_capture(capture_tags, 1, u'motel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("motel classificado incorretamente")
                # suggestAlternative:"tourism=motel"
                err.append({'class': 9018002, 'subclass': 2096064741, 'text': mapcss.tr(u'motel classificado incorretamente')})

        # *[aeroway=aerodrome][name=~/(?i).*airport$/]
        # *[aeroway=helipad][name=~/(?i).*heliport$/]
        if (u'aeroway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'aerodrome') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_6efb8049), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'helipad') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_6566db6a), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} com nome em inglês","{0.tag}")
                err.append({'class': 9018002, 'subclass': 134725283, 'text': mapcss.tr(u'{0} com nome em inglês', mapcss._tag_uncapture(capture_tags, u'{0.tag}'))})

        # *[aeroway=aerodrome][name=~/(?i)^Aer(ódromo|oporto) de.*/]
        # *[aeroway=helipad][name=~/(?i)^Helipo(n|r)to.*/]
        if (u'aeroway' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'aerodrome') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_6024a566), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'helipad') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_139e342b), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("conferir se existe nome oficial do {0}","{0.value}")
                err.append({'class': 9018002, 'subclass': 2002284471, 'text': mapcss.tr(u'conferir se existe nome oficial do {0}', mapcss._tag_uncapture(capture_tags, u'{0.value}'))})

        # *[aeroway=aerodrome][ref]
        if (u'aeroway' in keys and u'ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == mapcss._value_capture(capture_tags, 0, u'aerodrome') and mapcss._tag_capture(capture_tags, 1, tags, u'ref'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("''{0}'' não faz sentido em aeroporto","{1.key}")
                err.append({'class': 9018002, 'subclass': 339634841, 'text': mapcss.tr(u'\'\'{0}\'\' não faz sentido em aeroporto', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[waterway][layer<0][!tunnel]
        if (u'layer' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'layer') < mapcss._value_capture(capture_tags, 1, 0) and not mapcss._tag_capture(capture_tags, 2, tags, u'tunnel'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} negativo de {1} com ausência de {2}","{1.key}","{0.key}","{2.key}")
                err.append({'class': 9018002, 'subclass': 1476002587, 'text': mapcss.tr(u'{0} negativo de {1} com ausência de {2}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[waterway][layer>0][!bridge]
        if (u'layer' in keys and u'waterway' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'layer') > mapcss._value_capture(capture_tags, 1, 0) and not mapcss._tag_capture(capture_tags, 2, tags, u'bridge'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("{0} positivo de {1} com ausência de {2}","{1.key}","{0.key}","{2.key}")
                err.append({'class': 9018002, 'subclass': 1137415389, 'text': mapcss.tr(u'{0} positivo de {1} com ausência de {2}', mapcss._tag_uncapture(capture_tags, u'{1.key}'), mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[layer][!building][!highway][man_made!=pipeline][!railway][!waterway]
        # Rule Blacklisted

        # *[name=~/^(?i)(?u)edifício.*/][!building]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_38a8f0ff), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'building'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("possível ausência de tag {0}","{1.key}")
                err.append({'class': 9018026, 'subclass': 1417041710, 'text': mapcss.tr(u'possível ausência de tag {0}', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[route=ferry][!duration]
        if (u'route' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'route') == mapcss._value_capture(capture_tags, 0, u'ferry') and not mapcss._tag_capture(capture_tags, 1, tags, u'duration'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("ausência do tempo de duração ({0}) da balsa","{1.key}")
                err.append({'class': 9018027, 'subclass': 1289884816, 'text': mapcss.tr(u'ausência do tempo de duração ({0}) da balsa', mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[name=~/^(?i)(?u)praça.*/][!leisure][landuse=~/^(forest|grass|greenfield|meadow|orchard)$/]
        # *[name=~/^(?i)(?u)praça.*/][!leisure][natural=~/^(grassland|heath|scrub|wood)$/]
        if (u'landuse' in keys and u'name' in keys) or (u'name' in keys and u'natural' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_4a8ca94e), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'leisure') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_05a345c7), mapcss._tag_capture(capture_tags, 2, tags, u'landuse')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_4a8ca94e), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'leisure') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_12b48afb), mapcss._tag_capture(capture_tags, 2, tags, u'natural')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("possível definição incorreta para praça: ''{0}''","{2.key}")
                # suggestAlternative:"leisure=park"
                err.append({'class': 9018029, 'subclass': 80498829, 'text': mapcss.tr(u'possível definição incorreta para praça: \'\'{0}\'\'', mapcss._tag_uncapture(capture_tags, u'{2.key}'))})

        # *[wikipedia][wikipedia!~/^pt:/]
        if (u'wikipedia' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_17fd35b3), mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("utilizar prefixo em português (pt:) para {0}","{0.key}")
                err.append({'class': 9018030, 'subclass': 1219382195, 'text': mapcss.tr(u'utilizar prefixo em português (pt:) para {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name=~/.*\(.*\).*/]
        # Rule Blacklisted

        # *[name=~/ - /]
        # Rule Blacklisted

        # *[name=~/, /]
        # Rule Blacklisted

        # *[name=~/: /]
        # Rule Blacklisted

        # *[name=~/ ou /]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_131cc885), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("nome utilizado de forma incorreta")
                # suggestAlternative:"name e alt_name"
                err.append({'class': 9018031, 'subclass': 23034604, 'text': mapcss.tr(u'nome utilizado de forma incorreta')})

        # relation[boundary][type!=boundary]
        if (u'boundary' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') and mapcss._tag_capture(capture_tags, 1, tags, u'type') != mapcss._value_capture(capture_tags, 1, u'boundary'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve possuir ''type=boundary''","{0.key}")
                err.append({'class': 9018048, 'subclass': 404484969, 'text': mapcss.tr(u'{0} deve possuir \'\'type=boundary\'\'', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # relation[type=boundary][!boundary]
        if (u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'type') == mapcss._value_capture(capture_tags, 0, u'boundary') and not mapcss._tag_capture(capture_tags, 1, tags, u'boundary'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve ser utilizado junto com {1}","{0.tag}","{1.key}")
                err.append({'class': 9018049, 'subclass': 919335957, 'text': mapcss.tr(u'{0} deve ser utilizado junto com {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # relation[admin_level][boundary!=administrative]
        if (u'admin_level' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'admin_level') and mapcss._tag_capture(capture_tags, 1, tags, u'boundary') != mapcss._value_capture(capture_tags, 1, u'administrative'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwError:tr("ausência de boundary=administrative")
                # fixAdd:"boundary=administrative"
                err.append({'class': 9018006, 'subclass': 585818652, 'text': mapcss.tr(u'ausência de boundary=administrative'), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'boundary',u'administrative']])
                }})

        # relation[boundary=administrative][!admin_level]
        if (u'boundary' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'administrative') and not mapcss._tag_capture(capture_tags, 1, tags, u'admin_level'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
                err.append({'class': 9018033, 'subclass': 1254141393, 'text': mapcss.tr(u'{0} deve possuir {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # relation[place][place!~/^(city_block|farm|hamlet|island|islet|isolated_dwelling|neighbourhood|square)$/][!admin_level][!boundary]
        if (u'place' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'place') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_58f616c9), mapcss._tag_capture(capture_tags, 1, tags, u'place')) and not mapcss._tag_capture(capture_tags, 2, tags, u'admin_level') and not mapcss._tag_capture(capture_tags, 3, tags, u'boundary'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("local com ausência/incoerência de limite administrativo")
                err.append({'class': 9018002, 'subclass': 1798440430, 'text': mapcss.tr(u'local com ausência/incoerência de limite administrativo')})

        # relation[boundary=administrative][type=multipolygon]
        if (u'boundary' in keys and u'type' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'administrative') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == mapcss._value_capture(capture_tags, 1, u'multipolygon'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwError:tr("relação deve ser do tipo ''type=boundary''")
                # fixAdd:"type=boundary"
                err.append({'class': 9018006, 'subclass': 150723186, 'text': mapcss.tr(u'relação deve ser do tipo \'\'type=boundary\'\''), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'type',u'boundary']])
                }})

        # *[boundary=national_park][!name]
        # *[boundary=protected_area][!name]
        # *[leisure=nature_reserve][!name]
        if (u'boundary' in keys) or (u'leisure' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'national_park') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'protected_area') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'nature_reserve') and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
                err.append({'class': 9018033, 'subclass': 1492609299, 'text': mapcss.tr(u'{0} deve possuir {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[boundary=protected_area][!protect_class]
        if (u'boundary' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == mapcss._value_capture(capture_tags, 0, u'protected_area') and not mapcss._tag_capture(capture_tags, 1, tags, u'protect_class'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
                err.append({'class': 9018033, 'subclass': 822952800, 'text': mapcss.tr(u'{0} deve possuir {1}', mapcss._tag_uncapture(capture_tags, u'{0.tag}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[protect_class][protect_class!~/^(1(a|b)?|[1-9][0-9]?)$/]
        if (u'protect_class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'protect_class') and not mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_5ac7053e), mapcss._tag_capture(capture_tags, 1, tags, u'protect_class')))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("valor incorreto para {0}","{0.key}")
                err.append({'class': 9018034, 'subclass': 1459161459, 'text': mapcss.tr(u'valor incorreto para {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[protect_class][boundary!=protected_area]
        if (u'protect_class' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'protect_class') and mapcss._tag_capture(capture_tags, 1, tags, u'boundary') != mapcss._value_capture(capture_tags, 1, u'protected_area'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("ausência de boundary=protected_area")
                err.append({'class': 9018035, 'subclass': 1208814760, 'text': mapcss.tr(u'ausência de boundary=protected_area')})

        # relation[destination][type!=waterway]
        if (u'destination' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'destination') and mapcss._tag_capture(capture_tags, 1, tags, u'type') != mapcss._value_capture(capture_tags, 1, u'waterway'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("{0} deve ser usado apenas em ways","{0.key}")
                err.append({'class': 9018036, 'subclass': 1752813638, 'text': mapcss.tr(u'{0} deve ser usado apenas em ways', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name=~/.* D(a|e|o)s? .*/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_2ffc377d), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("''da'', ''de'' e ''do'' são minúsculos nos nomes em português")
                err.append({'class': 9018002, 'subclass': 1986668346, 'text': mapcss.tr(u'\'\'da\'\', \'\'de\'\' e \'\'do\'\' são minúsculos nos nomes em português')})

        # *[name=~/^[a-z].*/]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_39d67968), mapcss._tag_capture(capture_tags, 0, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("nome iniciando com letra minúscula")
                err.append({'class': 9018002, 'subclass': 167462302, 'text': mapcss.tr(u'nome iniciando com letra minúscula')})

        # *[alt_ref]
        if (u'alt_ref' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'alt_ref'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("o conteúdo de {0} deve fazer parte de ref, separado por ;","{0.key}")
                # suggestAlternative:"ref"
                err.append({'class': 9018039, 'subclass': 722411109, 'text': mapcss.tr(u'o conteúdo de {0} deve fazer parte de ref, separado por ;', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[surface][eval(number_of_tags())=1]
        if (u'surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'surface') and len(tags) == 1)
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto incompleto: possui apenas {0}","{0.key}")
                err.append({'class': 9018041, 'subclass': 1776991136, 'text': mapcss.tr(u'objeto incompleto: possui apenas {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *[name][surface][eval(number_of_tags())=2]
        # *[name][website][eval(number_of_tags())=2]
        if (u'name' in keys and u'surface' in keys) or (u'name' in keys and u'website' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'surface') and len(tags) == 2)
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'website') and len(tags) == 2)
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("objeto incompleto: possui apenas {0} e {1}","{0.key}","{1.key}")
                err.append({'class': 9018042, 'subclass': 626126700, 'text': mapcss.tr(u'objeto incompleto: possui apenas {0} e {1}', mapcss._tag_uncapture(capture_tags, u'{0.key}'), mapcss._tag_uncapture(capture_tags, u'{1.key}'))})

        # *[leisure=pitch][sport=tennis][surface=unpaved]
        if (u'leisure' in keys and u'sport' in keys and u'surface' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == mapcss._value_capture(capture_tags, 0, u'pitch') and mapcss._tag_capture(capture_tags, 1, tags, u'sport') == mapcss._value_capture(capture_tags, 1, u'tennis') and mapcss._tag_capture(capture_tags, 2, tags, u'surface') == mapcss._value_capture(capture_tags, 2, u'unpaved'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("{0} com superfície incorreta","{2.key}")
                # suggestAlternative:"surface=clay"
                # fixAdd:"surface=clay"
                err.append({'class': 9018006, 'subclass': 1659179489, 'text': mapcss.tr(u'{0} com superfície incorreta', mapcss._tag_uncapture(capture_tags, u'{2.key}')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'surface',u'clay']])
                }})

        # *[amenity=fuel][name=~/(?i)(?u)\b(Ale|BR|Esso|Ipiranga|Petrobr(á|a)s|Shell|Texaco)\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'fuel') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_604bb645), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("uso incorreto da bandeira do posto")
                # suggestAlternative:"brand"
                err.append({'class': 9018002, 'subclass': 935774110, 'text': mapcss.tr(u'uso incorreto da bandeira do posto')})

        # *[/_[0-9]$/][!"is_in:iso_3166_2"]
        if True:
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, self.re_57b8ef8e) and not mapcss._tag_capture(capture_tags, 1, tags, u'is_in:iso_3166_2'))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("chave inválida: {0}","{0.key}")
                err.append({'class': 9018022, 'subclass': 331369569, 'text': mapcss.tr(u'chave inválida: {0}', mapcss._tag_uncapture(capture_tags, u'{0.key}'))})

        # *["addr:housenumber"=~/(?i)^s(\.|-| )?\/?n\.?º?$/][!note]
        if (u'addr:housenumber' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_0b27200b), mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber')) and not mapcss._tag_capture(capture_tags, 1, tags, u'note'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Correções e melhorias")
                # throwWarning:tr("não utilizar ''{0}'' para locais sem número",tag("addr:housenumber"))
                # suggestAlternative:"note"
                # fixRemove:"addr:housenumber"
                # fixAdd:"note=Local sem número"
                err.append({'class': 9018006, 'subclass': 931902546, 'text': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', mapcss.tag(tags, u'addr:housenumber')), 'allow_fix_override': True, 'fix': {
                    '+': dict([
                    [u'note',u'Local sem número']]),
                    '-': ([
                    u'addr:housenumber'])
                }})

        # *["addr:housenumber"=~/(?i)^s(\.|-| )?\/?n\.?º?$/][note]
        if (u'addr:housenumber' in keys and u'note' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_0b27200b), mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber')) and mapcss._tag_capture(capture_tags, 1, tags, u'note'))
                except mapcss.RuleAbort: pass
            if match:
                # throwWarning:tr("não utilizar ''{0}'' para locais sem número",tag("addr:housenumber"))
                # suggestAlternative:"note"
                err.append({'class': 9018043, 'subclass': 1717284811, 'text': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', mapcss.tag(tags, u'addr:housenumber'))})

        # *[source=~/(?i)google/]
        if (u'source' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_2e8e4f2b), mapcss._tag_capture(capture_tags, 0, tags, u'source')))
                except mapcss.RuleAbort: pass
            if match:
                # throwError:tr("objeto contém Google como source")
                err.append({'class': 9018044, 'subclass': 1313403884, 'text': mapcss.tr(u'objeto contém Google como source')})

        # *[amenity=townhall][name=~/^(?i)(?u)c(â|a)mara\b/]
        if (u'amenity' in keys and u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'townhall') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_46ab4d8d), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("câmara de vereadores mapeada incorretamente")
                # suggestAlternative:"office=government + government=legislative"
                err.append({'class': 9018002, 'subclass': 129695507, 'text': mapcss.tr(u'câmara de vereadores mapeada incorretamente')})

        # *[office=government][government!=legislative][name=~/^(?i)(?u)c(â|a)mara\b/]
        if (u'name' in keys and u'office' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'government') and mapcss._tag_capture(capture_tags, 1, tags, u'government') != mapcss._value_capture(capture_tags, 1, u'legislative') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 2, self.re_46ab4d8d), mapcss._tag_capture(capture_tags, 2, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("ausência de government=legislative")
                err.append({'class': 9018002, 'subclass': 869412796, 'text': mapcss.tr(u'ausência de government=legislative')})

        # *[amenity=townhall][name=~/^(?i)(?u)c((â|a)me|ama)ra\b/]
        # *[office=government][name=~/^(?i)(?u)c((â|a)me|ama)ra\b/]
        if (u'amenity' in keys and u'name' in keys) or (u'name' in keys and u'office' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'townhall') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_793b22ec), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'office') == mapcss._value_capture(capture_tags, 0, u'government') and mapcss.regexp_test_(mapcss._value_capture(capture_tags, 1, self.re_793b22ec), mapcss._tag_capture(capture_tags, 1, tags, u'name')))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("erro de ortografia em ''câmara''")
                err.append({'class': 9018002, 'subclass': 212328084, 'text': mapcss.tr(u'erro de ortografia em \'\'câmara\'\'')})

        # *[amenity=charging_station]
        if (u'amenity' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == mapcss._value_capture(capture_tags, 0, u'charging_station'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("possivelmente deve ser amenity=fuel")
                err.append({'class': 9018002, 'subclass': 128902291, 'text': mapcss.tr(u'possivelmente deve ser amenity=fuel')})

        # *[name=~/(?i)^Borrach(aria|eiro)/][shop=tyres][!repair]
        if (u'name' in keys and u'shop' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_126ba9a9), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'shop') == mapcss._value_capture(capture_tags, 1, u'tyres') and not mapcss._tag_capture(capture_tags, 2, tags, u'repair'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("borracharia sem ''repair=yes''")
                # suggestAlternative:"repair=yes"
                err.append({'class': 9018002, 'subclass': 817061630, 'text': mapcss.tr(u'borracharia sem \'\'repair=yes\'\'')})

        # *[name=~/(?i)^Borrach(aria|eiro)/][shop!=tyres]
        if (u'name' in keys):
            match = False
            if not match:
                capture_tags = {}
                try: match = (mapcss.regexp_test_(mapcss._value_capture(capture_tags, 0, self.re_126ba9a9), mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'shop') != mapcss._value_capture(capture_tags, 1, u'tyres'))
                except mapcss.RuleAbort: pass
            if match:
                # group:tr("Brasil - Verificar")
                # throwWarning:tr("borracharia sem ''shop=tyres''")
                # suggestAlternative:"shop=tyres"
                err.append({'class': 9018002, 'subclass': 1324999258, 'text': mapcss.tr(u'borracharia sem \'\'shop=tyres\'\'')})

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


