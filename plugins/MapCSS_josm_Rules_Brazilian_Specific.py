#-*- coding: utf-8 -*-
import modules.mapcss_lib as mapcss
import regex as re

from plugins.Plugin import Plugin

class MapCSS_josm_Rules_Brazilian_Specific(Plugin):

    only_for = ['BR']

    def init(self, logger):
        Plugin.init(self, logger)
        tags = capture_tags = {}
        self.errors[9018001] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} com logradouro ausente, errado ou abreviado', capture_tags, u'{0.key}')}
        self.errors[9018002] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'Brasil - Verificar', capture_tags)}
        self.errors[9018003] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'palavra abreviada em {0}', capture_tags, u'{0.key}')}
        self.errors[9018004] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'nome supérfluo/incompleto de local de lazer', capture_tags)}
        self.errors[9018005] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'nome supérfluo/incompleto de local de saúde', capture_tags)}
        self.errors[9018006] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'Brasil - Correções e melhorias', capture_tags)}
        self.errors[9018007] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'objeto com nomenclatura incorreta', capture_tags)}
        self.errors[9018008] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} não deve ser utilizado em nó; utilizar a restrição na via', capture_tags, u'{0.key}')}
        self.errors[9018009] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} é uma chave utilizada apenas no Reino Unido', capture_tags, u'{0.key}')}
        self.errors[9018010] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} sem pelo menos uma das tags: {1} ou {2}', capture_tags, u'{0.value}', u'{1.key}', u'{2.key}')}
        self.errors[9018011] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} sem tag de população (population)', capture_tags, u'{0.value}')}
        self.errors[9018012] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} sem nome', capture_tags, u'{0.value}')}
        self.errors[9018013] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} deve conter apenas o nome da cidade', capture_tags, u'{0.key}')}
        self.errors[9018014] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} com valor = {1}', capture_tags, u'{0.key}', u'{0.value}')}
        self.errors[9018015] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'postos/unidades de saúde devem ser amenity=clinic', capture_tags)}
        self.errors[9018016] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'SAMU classificado de forma errada', capture_tags)}
        self.errors[9018017] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'objeto não deve possuir {0}', capture_tags, u'{1.key}')}
        self.errors[9018018] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'adicionar {0} ao {1}', capture_tags, u'{1.key}', u'{0.tag}')}
        self.errors[9018019] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} deve ser utilizado com {1}={0} ou {2}={0}', capture_tags, u'{0.key}', u'{1.key}', u'{2.key}')}
        self.errors[9018020] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} deve estar incluído em {1}, separado por \'\';\'\' caso necessário', capture_tags, u'{0.key}', u'{1.key}')}
        self.errors[9018021] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'especificar valor correto para {0} ao invés de \'\'{1}\'\'', capture_tags, u'{0.key}', mapcss.tag(tags, u'landuse'))}
        self.errors[9018022] = {'item': 9018, 'level': 1, 'tag': [], 'desc': mapcss.tr(u'chave inválida: {0}', capture_tags, u'{0.key}')}
        self.errors[9018023] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'não se deve utilizar {0} para demarcar áreas de cobertura de imagem', capture_tags, u'{0.key}')}
        self.errors[9018024] = {'item': 9018, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'ausência do tipo de torre ({0})', capture_tags, u'{1.key}')}
        self.errors[9018025] = {'item': 9018, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'{0} sem tag {1}', capture_tags, u'{0.value}', u'{1.key}')}
        self.errors[9018026] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'possível ausência de tag {0}', capture_tags, u'{1.key}')}
        self.errors[9018027] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'ausência do tempo de duração ({0}) da balsa', capture_tags, u'{1.key}')}
        self.errors[9018028] = {'item': 9018, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'{0} sem tag de acessibilidade ({1})', capture_tags, u'{0.key}', u'{1.key}')}
        self.errors[9018029] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'possível definição incorreta para praça: \'\'{0}\'\'', capture_tags, u'{2.key}')}
        self.errors[9018030] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'utilizar prefixo em português (pt:) para {0}', capture_tags, u'{0.key}')}
        self.errors[9018031] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'nome utilizado de forma incorreta', capture_tags)}
        self.errors[9018032] = {'item': 9018, 'level': 1, 'tag': [], 'desc': mapcss.tr(u'nó não deve possuir {0}', capture_tags, u'{0.tag}')}
        self.errors[9018033] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} deve possuir {1}', capture_tags, u'{0.tag}', u'{1.key}')}
        self.errors[9018034] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'valor incorreto para {0}', capture_tags, u'{0.key}')}
        self.errors[9018035] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'ausência de boundary=protected_area', capture_tags)}
        self.errors[9018036] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} deve ser usado apenas em ways', capture_tags, u'{0.key}')}
        self.errors[9018037] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'utilize \'\'destination\'\' no caminho de saída ao invés de \'\'exit_to\'\'', capture_tags)}
        self.errors[9018038] = {'item': 9018, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'{0} sem {1}', capture_tags, u'{0.key}', u'{1.key}')}
        self.errors[9018039] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'o conteúdo de {0} deve fazer parte de ref, separado por ;', capture_tags, u'{0.key}')}
        self.errors[9018040] = {'item': 9018, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'utilizar ; como separador de valores em {0}', capture_tags, u'{0.key}')}
        self.errors[9018041] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'objeto incompleto: possui apenas {0}', capture_tags, u'{0.key}')}
        self.errors[9018042] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'objeto incompleto: possui apenas {0} e {1}', capture_tags, u'{0.key}', u'{1.key}')}
        self.errors[9018043] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', capture_tags, mapcss.tag(tags, u'addr:housenumber'))}
        self.errors[9018044] = {'item': 9018, 'level': 1, 'tag': [], 'desc': mapcss.tr(u'objeto contém Google como source', capture_tags)}
        self.errors[9018045] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'rodovia com ref no nome', capture_tags)}
        self.errors[9018046] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'relação não deve possuir {0}', capture_tags, u'{1.key}')}
        self.errors[9018047] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} deve ser utilizado apenas em nós', capture_tags, u'{0.tag}')}
        self.errors[9018048] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} deve possuir \'\'type=boundary\'\'', capture_tags, u'{0.key}')}
        self.errors[9018049] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} deve ser utilizado junto com {1}', capture_tags, u'{0.tag}', u'{1.key}')}
        self.errors[9018050] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} e {1} são iguais; adicionar nome completo da rodovia', capture_tags, u'{0.key}', u'{0.value}')}
        self.errors[9018051] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'não classificar via como {0}', capture_tags, u'{0.tag}')}
        self.errors[9018052] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} com nome supérfluo/incompleto', capture_tags, u'{0.key}')}
        self.errors[9018053] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} não deve possuir {1}', capture_tags, u'{0.key}', u'{1.tag}')}
        self.errors[9018054] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'ausência de "{0}" na {1}', capture_tags, u'{1.key}', u'{0.key}')}
        self.errors[9018055] = {'item': 9018, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'link sem tag {0}', capture_tags, u'{1.key}')}
        self.errors[9018056] = {'item': 9018, 'level': 1, 'tag': [], 'desc': mapcss.tr(u'{0} deve ser utilizado apenas no nó de saída da rodovia', capture_tags, u'{0.tag}')}
        self.errors[9018057] = {'item': 9018, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'{0} sem superfície ({1}) definida', capture_tags, u'{0.key}', u'{1.key}')}
        self.errors[9018058] = {'item': 9018, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'{0} sem número de faixas ({1}) definido', capture_tags, u'{0.key}', u'{1.key}')}
        self.errors[9018059] = {'item': 9018, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'{0} sem velocidade máxima ({1}) definida', capture_tags, u'{0.key}', u'{1.key}')}
        self.errors[9018060] = {'item': 9018, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'ausência do tipo de serviço ({0}) na {1}', capture_tags, u'{1.key}', u'{0.key}')}
        self.errors[9018061] = {'item': 9018, 'level': 3, 'tag': [], 'desc': mapcss.tr(u'ausência do tipo de track ({0}) na {1}', capture_tags, u'{1.key}', u'{0.key}')}
        self.errors[9018062] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'{0} com {1}', capture_tags, u'{0.key}', u'{1.tag}')}
        self.errors[9018063] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'uso incorreto de {0} com {1}', capture_tags, u'{0.tag}', u'{1.tag}')}
        self.errors[9018064] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'uso incorreto de {0}', capture_tags, u'{1.key}')}
        self.errors[9018065] = {'item': 9018, 'level': 2, 'tag': [], 'desc': mapcss.tr(u'utilizar {0} apenas em {1}={2}', capture_tags, u'{1.key}', u'{0.key}', u'{0.value}')}

        self.re_002de70b = re.compile(ur'^(?i)(?u)Fórum .*')
        self.re_01454d46 = re.compile(ur'(?i)\bmotel\b')
        self.re_029b8e58 = re.compile(ur'construction|give_way|motorway_junction|proposed|raceway|speed_camera|stop')
        self.re_044c8944 = re.compile(ur'^(?i)(?u)(SENAC|SENAI|Serviço Nacional de Aprendizagem)')
        self.re_04873a60 = re.compile(ur'^(river|stream)$')
        self.re_0575cb27 = re.compile(ur'bus_stop|milestone|motorway_junction|traffic_signals')
        self.re_05a345c7 = re.compile(ur'^(forest|grass|greenfield|meadow|orchard)$')
        self.re_073e5345 = re.compile(ur'\b[A-Z]{2,3} (- )?[0-9]{2,3}\b')
        self.re_07f31a73 = re.compile(ur'^(living_street|pedestrian|residential|road|service|track)$')
        self.re_0b27200b = re.compile(ur'(?i)^s(\.|-| )?\/?n\.?º?$')
        self.re_0db5b64e = re.compile(ur'village|town|city')
        self.re_1054eb5a = re.compile(ur'bridleway|bus_stop|cycleway|crossing|footway|give_way|motorway_junction|path|raceway|rest_area|services|speed_camera|steps|stop')
        self.re_105662b4 = re.compile(ur'^(?i)Capela .*')
        self.re_10f1c360 = re.compile(ur'(,|( |-) ?[A-Z]{2})')
        self.re_126ba9a9 = re.compile(ur'(?i)^Borrach(aria|eiro)')
        self.re_12b48afb = re.compile(ur'^(grassland|heath|scrub|wood)$')
        self.re_1319292c = re.compile(ur'^(trunk|motorway)$')
        self.re_131cc885 = re.compile(ur' ou ')
        self.re_139e342b = re.compile(ur'(?i)^Helipo(n|r)to.*')
        self.re_152c10ee = re.compile(ur'hamlet|isolated_dwelling|town|village')
        self.re_15690541 = re.compile(ur'^(?i)estrada de ferro')
        self.re_160d1bfc = re.compile(ur'^(?i)creche\b')
        self.re_178f5446 = re.compile(ur'(?i)(^|.* )(Cel|Cmte|Cond|Conj|Dª|Dr|Eng|Gov|Hab|Jd|Jr|Marg|Mun|p\/|Pde|Pe|Pq|Pst|Pref|Profa|Profª|Prof|Res|s\/|Sr(a|ª)?|Sta|Sto|Ver)\.? .*')
        self.re_17fd35b3 = re.compile(ur'^pt:')
        self.re_1d232d4c = re.compile(ur'^(?i)(?u)(Centro Universitário|Faculdades?|FATEC|Instituto Federal)\b')
        self.re_1e8e69a3 = re.compile(ur'^(?i)Catedral .*')
        self.re_1ffe94a9 = re.compile(ur'^[0-9]{5}-[0-9]{3}$')
        self.re_20188fb1 = re.compile(ur'^[0-9]+( |-)*([A-Z])?$')
        self.re_20c7dd98 = re.compile(ur'^(?i)(?u)(aldeia|borrach(aria|eiro)|bosque|capela|cemit(é|e)rio|c(ó|o)rrego|escola|estacionamento|fazenda|floresta|hospital|igreja|lago|lagoa|mata( nativa)?|praça|parque|parquinho|posto( de gasolina)?|riacho|rio|rodovi(á|a)ria|vila)$')
        self.re_20cf30ba = re.compile(ur'^(?i)(?u)(alameda|avenida|beco|estrada|ladeira|rodovia|rotatória|rua|travessa|trevo|viela) .*')
        self.re_20fc5143 = re.compile(ur'^(?i)Bairro\b')
        self.re_25871691 = re.compile(ur'^(?i)Hospital .*')
        self.re_280004fd = re.compile(ur'^(Água|Arroio|Cabeceira|Córrego|Furo|Grota|Igarapé|Lajeado|Paraná|Restinga|Riacho|Ribeirão|Rio|Sanga)\b')
        self.re_2cd1e949 = re.compile(ur'^(?i)(?u)(Faz\.|Fazenda|Sítio|Chácara)')
        self.re_2dbaea13 = re.compile(ur'^(?i)\bSAMU\b')
        self.re_2dbf771a = re.compile(ur'^[0-9]{8}$')
        self.re_2e8e4f2b = re.compile(ur'(?i)google')
        self.re_2fcb6bab = re.compile(ur'^(?i)ciclovia .*')
        self.re_2ffc377d = re.compile(ur'.* D(a|e|o)s? .*')
        self.re_32b6342d = re.compile(ur'motorway|trunk|primary|secondary|tertiary|unclassified|residential')
        self.re_34f65002 = re.compile(ur'.*,.*')
        self.re_35bb0f2f = re.compile(ur'^(?i)(?u)(auto(-| )?( moto )?escola|centro de formação de condutores|cfc|moto escola)\b')
        self.re_362f879f = re.compile(ur'college|school')
        self.re_375e3de4 = re.compile(ur'.*([A-Z]{2,3}-[0-9]{2,4}|SPM(-| )[0-9]{3} ?(D|E)?|SP(A|D|I)(-| )[0-9]{3}\/[0-9]{3}|[A-Z]{3}-[0-9]{3}\/[0-9]{3}).*')
        self.re_381002af = re.compile(ur'^(?i)Fazenda .*')
        self.re_38494ef5 = re.compile(ur'motorway|trunk|primary|secondary|tertiary')
        self.re_38a8f0ff = re.compile(ur'^(?i)(?u)edifício.*')
        self.re_39d67968 = re.compile(ur'^[a-z].*')
        self.re_3aeda39d = re.compile(ur'hamlet|island|isolated_dwelling|neighbourhood|suburb|village')
        self.re_3b304b9b = re.compile(ur'(?i)(?u)\b(Centro Paula Souza|Escola Técnica|ETEC)\b')
        self.re_3b777b9d = re.compile(ur'^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodovia|Rotatória|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*')
        self.re_3e2e3488 = re.compile(ur'^(([A-Z]{2,3}-[0-9]{2,4}|SPM(-| )[0-9]{3} ?(D|E)?|SP(A|D|I)(-| )[0-9]{3}\/[0-9]{3}|[A-Z]{3}-[0-9]{3}\/[0-9]{3});?)+$')
        self.re_3eb0ab44 = re.compile(ur'clinic|doctors|hospital')
        self.re_407995b9 = re.compile(ur'(?i)^Estacionamento ')
        self.re_458e02d8 = re.compile(ur'^(?i)Hotel .*')
        self.re_46ab4d8d = re.compile(ur'^(?i)(?u)c(â|a)mara\b')
        self.re_486d02c4 = re.compile(ur'^(?i)Supermercado .*')
        self.re_4a8ca94e = re.compile(ur'^(?i)(?u)praça.*')
        self.re_4bd3b925 = re.compile(ur'^(?i)(?u)[a-z0-9]+_([a-z0-9]_?)+$')
        self.re_4cf86823 = re.compile(ur'(?i)\bsaude\b')
        self.re_4da7cb86 = re.compile(ur', ')
        self.re_52ab3b8b = re.compile(ur'^(?i)(?u)((Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF|hospital)$')
        self.re_53abc074 = re.compile(ur'^(give_way|mini_roundabout|stop|turning_circle)$')
        self.re_568a42f4 = re.compile(ur'\b[A-Z]{2,4} (- )?[0-9]{2,3}\b')
        self.re_57a9f888 = re.compile(ur'^(?i)Escola .*')
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
        self.re_657f3be3 = re.compile(ur': ')
        self.re_667ce569 = re.compile(ur'^(?i)(?u)((via de )?(acesso|ligação)(( (a|à))? propriedade)?|entrada|entroncamento|rampa|retorno|rotat(ó|o)ria|r(ó|o)tula|sa(í|i)da|trevo|estrada( municipal| de terra)?|rua|rodovia|via)( (de acesso|sem nome|projetad(a|o)))?$')
        self.re_69d0dc1a = re.compile(ur'^(?i)(?u)Subestação .*')
        self.re_6b25b0c5 = re.compile(ur' - ')
        self.re_6b6e390d = re.compile(ur'(Alameda|Avenida|Rua|Travessa|Viela) .*')
        self.re_6c0d6e9e = re.compile(ur'school|university')
        self.re_6e928d7b = re.compile(ur'^(?i)Universidade .*')
        self.re_6efb8049 = re.compile(ur'(?i).*airport$')
        self.re_72d45155 = re.compile(ur'route|street')
        self.re_73b50a21 = re.compile(ur'^(\p{Upper}| )+$')
        self.re_752011f2 = re.compile(ur'^(?i)Igreja .*')
        self.re_7633bf4e = re.compile(ur'Rodovia ([A-Z]{2,3}-[0-9]{2,4})')
        self.re_793b22ec = re.compile(ur'^(?i)(?u)c((â|a)me|ama)ra\b')
        self.re_7afc6883 = re.compile(ur'^[A-Z]{4}$')
        self.re_7b7c453d = re.compile(ur'^(?i)(?u)(AM(A|E)|(Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF).*')
        self.re_7e9dfbe7 = re.compile(ur'.*\(.*\).*')
        self.re_7f53e992 = re.compile(ur'^(?i)(?u)(campo|est(á|a)dio|gin(á|a)sio|quadra)( de (futebol|esportes?))?$')


    def node(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # *["addr:street"]["addr:street"!~/^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodovia|Rotatória|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*/]
        if (u'addr:street' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'addr:street') and not mapcss.regexp_test_(self.re_3b777b9d, mapcss._tag_capture(capture_tags, 1, tags, u'addr:street')))):
            # throwWarning:tr("{0} com logradouro ausente, errado ou abreviado","{0.key}")
            err.append({'class': 9018001, 'subclass': 588331445, 'text': mapcss.tr(u'{0} com logradouro ausente, errado ou abreviado', capture_tags, u'{0.key}')})

        # *[!highway][route!=road][!public_transport][type!~/route|street/][name][name=~/^(?i)(?u)(alameda|avenida|beco|estrada|ladeira|passarela|rodovia|rotatória|rua|travessa|trevo|viela|(anel|complexo|dispositivo) viário) .*/][name!~/^(?i)estrada de ferro/]
        if (u'name' in keys) and \
            ((not mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'route') != u'road' and not mapcss._tag_capture(capture_tags, 2, tags, u'public_transport') and not mapcss.regexp_test_(self.re_72d45155, mapcss._tag_capture(capture_tags, 3, tags, u'type')) and mapcss._tag_capture(capture_tags, 4, tags, u'name') and mapcss.regexp_test_(self.re_5849be19, mapcss._tag_capture(capture_tags, 5, tags, u'name')) and not mapcss.regexp_test_(self.re_15690541, mapcss._tag_capture(capture_tags, 6, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("objeto com nome de via mas sem tag de {0}","{0.key}")
            err.append({'class': 9018002, 'subclass': 874993957, 'text': mapcss.tr(u'objeto com nome de via mas sem tag de {0}', capture_tags, u'{0.key}')})

        # *[name=~/^(?i)(?u)[a-z0-9]+_([a-z0-9]_?)+$/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_4bd3b925, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("utilizar espaço ao invés de underscore")
            err.append({'class': 9018002, 'subclass': 378801374, 'text': mapcss.tr(u'utilizar espaço ao invés de underscore', capture_tags)})

        # *[name=~/(?i)(^|.* )(Cel|Cmte|Cond|Conj|Dª|Dr|Eng|Gov|Hab|Jd|Jr|Marg|Mun|p\/|Pde|Pe|Pq|Pst|Pref|Profa|Profª|Prof|Res|s\/|Sr(a|ª)?|Sta|Sto|Ver)\.? .*/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_178f5446, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # throwWarning:tr("palavra abreviada em {0}","{0.key}")
            err.append({'class': 9018003, 'subclass': 1784756763, 'text': mapcss.tr(u'palavra abreviada em {0}', capture_tags, u'{0.key}')})

        # *[leisure][name=~/^(?i)(?u)(campo|est(á|a)dio|gin(á|a)sio|quadra)( de (futebol|esportes?))?$/]
        if (u'leisure' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'leisure') and mapcss.regexp_test_(self.re_7f53e992, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # throwWarning:tr("nome supérfluo/incompleto de local de lazer")
            err.append({'class': 9018004, 'subclass': 790401825, 'text': mapcss.tr(u'nome supérfluo/incompleto de local de lazer', capture_tags)})

        # *[name=~/^(?i)(?u)((Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF|hospital)$/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_52ab3b8b, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # throwWarning:tr("nome supérfluo/incompleto de local de saúde")
            err.append({'class': 9018005, 'subclass': 1792576894, 'text': mapcss.tr(u'nome supérfluo/incompleto de local de saúde', capture_tags)})

        # *[amenity=~/^(clinic|doctors|hospital)$/][name=~/(?i)\bsaude\b/]
        if (u'amenity' in keys) and \
            ((mapcss.regexp_test_(self.re_5ab76b11, mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test_(self.re_4cf86823, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("erro de ortografia em ''saúde''")
            err.append({'class': 9018002, 'subclass': 1455303428, 'text': mapcss.tr(u'erro de ortografia em \'\'saúde\'\'', capture_tags)})

        # *[place=farm][name^="Sitio "]
        if (u'place' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'farm' and mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, u'name'), u'Sitio '))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("faltando acento em ''Sítio''")
            err.append({'class': 9018002, 'subclass': 962677162, 'text': mapcss.tr(u'faltando acento em \'\'Sítio\'\'', capture_tags)})

        # *[name=~/^(?i)(?u)(aldeia|borrach(aria|eiro)|bosque|capela|cemit(é|e)rio|c(ó|o)rrego|escola|estacionamento|fazenda|floresta|hospital|igreja|lago|lagoa|mata( nativa)?|praça|parque|parquinho|posto( de gasolina)?|riacho|rio|rodovi(á|a)ria|vila)$/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_20c7dd98, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("local com nome supérfluo, incompleto ou descritivo")
            err.append({'class': 9018002, 'subclass': 501162763, 'text': mapcss.tr(u'local com nome supérfluo, incompleto ou descritivo', capture_tags)})

        # *[amenity=parking][name=~/(?i)^Estacionamento /]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'parking' and mapcss.regexp_test_(self.re_407995b9, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("possível nome descritivo do estacionamento")
            # suggestAlternative:"operator"
            err.append({'class': 9018002, 'subclass': 698950828, 'text': mapcss.tr(u'possível nome descritivo do estacionamento', capture_tags)})

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
        if (u'designation' in keys or u'name' in keys or u'ref' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'designation') == mapcss.tag(tags, u'addr:housename')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'ref') == mapcss.tag(tags, u'designation')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'ref') == mapcss.tag(tags, u'old_ref')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'addr:housename')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'designation')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'alt_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'int_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'loc_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'nat_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'official_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'old_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'reg_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'short_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'sorting_name'))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("{0} e {1} são iguais; remover chave {1} desnecessária","{0.key}","{0.value}")
            # fixRemove:"{0.value}"
            err.append({'class': 9018006, 'subclass': 1882388489, 'text': mapcss.tr(u'{0} e {1} são iguais; remover chave {1} desnecessária', capture_tags, u'{0.key}', u'{0.value}'), 'fix': {
                '-': ([
                    u'{0.value}'])
            }})

        # *[source=*name]
        if (u'source' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'source') == mapcss.tag(tags, u'name'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} e {1} são iguais","{0.key}","{0.value}")
            err.append({'class': 9018002, 'subclass': 1403015964, 'text': mapcss.tr(u'{0} e {1} são iguais', capture_tags, u'{0.key}', u'{0.value}')})

        # *[name=~/(?i)(?u)((sem (denomina(ç|c)(ã|a)o|nome|sa(i|í)da))|desconhecido|n(ã|a)o conhecido)/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_65710fdb, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # throwWarning:tr("objeto com nomenclatura incorreta")
            # suggestAlternative:"noname"
            err.append({'class': 9018007, 'subclass': 506924923, 'text': mapcss.tr(u'objeto com nomenclatura incorreta', capture_tags)})

        # node[maxheight][barrier!=height_restrictor][!traffic_sign]
        # node[maxspeed][highway!=speed_camera][!traffic_sign]
        if (u'maxheight' in keys or u'maxspeed' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'maxheight') and mapcss._tag_capture(capture_tags, 1, tags, u'barrier') != u'height_restrictor' and not mapcss._tag_capture(capture_tags, 2, tags, u'traffic_sign')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'maxspeed') and mapcss._tag_capture(capture_tags, 1, tags, u'highway') != u'speed_camera' and not mapcss._tag_capture(capture_tags, 2, tags, u'traffic_sign'))):
            # throwWarning:tr("{0} não deve ser utilizado em nó; utilizar a restrição na via","{0.key}")
            err.append({'class': 9018008, 'subclass': 1663448238, 'text': mapcss.tr(u'{0} não deve ser utilizado em nó; utilizar a restrição na via', capture_tags, u'{0.key}')})

        # node[noname?]
        if (u'noname' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'noname') in ('yes', 'true', '1'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("uso suspeito de {0} em nó","{0.key}")
            err.append({'class': 9018002, 'subclass': 1281771763, 'text': mapcss.tr(u'uso suspeito de {0} em nó', capture_tags, u'{0.key}')})

        # *[designation]
        if (u'designation' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'designation'))):
            # throwWarning:tr("{0} é uma chave utilizada apenas no Reino Unido","{0.key}")
            # suggestAlternative:"description"
            # suggestAlternative:"name"
            err.append({'class': 9018009, 'subclass': 1259259930, 'text': mapcss.tr(u'{0} é uma chave utilizada apenas no Reino Unido', capture_tags, u'{0.key}')})

        # node[highway=motorway_junction][!name][!ref]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'motorway_junction' and not mapcss._tag_capture(capture_tags, 1, tags, u'name') and not mapcss._tag_capture(capture_tags, 2, tags, u'ref'))):
            # throwWarning:tr("{0} sem pelo menos uma das tags: {1} ou {2}","{0.value}","{1.key}","{2.key}")
            err.append({'class': 9018010, 'subclass': 1402053593, 'text': mapcss.tr(u'{0} sem pelo menos uma das tags: {1} ou {2}', capture_tags, u'{0.value}', u'{1.key}', u'{2.key}')})

        # *[place=~/hamlet|isolated_dwelling|town|village/][population>=100000]
        if (u'place' in keys) and \
            ((mapcss.regexp_test_(self.re_152c10ee, mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'population') >= 100000)):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("local com 100.000 habitantes ou mais deve ser classificado como city")
            # fixAdd:"place=city"
            err.append({'class': 9018006, 'subclass': 149235075, 'text': mapcss.tr(u'local com 100.000 habitantes ou mais deve ser classificado como city', capture_tags), 'fix': {
                '+': dict([
                    [u'place',u'city']])
            }})

        # *[place=~/city|hamlet|isolated_dwelling|village/][population>=10000][population<100000]
        if (u'place' in keys) and \
            ((mapcss.regexp_test_(self.re_591572a5, mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'population') >= 10000 and mapcss._tag_capture(capture_tags, 2, tags, u'population') < 100000)):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("local com população entre 10.000 e 100.000 deve ser classificado como town")
            # fixAdd:"place=town"
            err.append({'class': 9018006, 'subclass': 1174321645, 'text': mapcss.tr(u'local com população entre 10.000 e 100.000 deve ser classificado como town', capture_tags), 'fix': {
                '+': dict([
                    [u'place',u'town']])
            }})

        # *[place][place!~/hamlet|island|isolated_dwelling|neighbourhood|suburb|village/][population<10000]
        if (u'place' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'place') and not mapcss.regexp_test_(self.re_3aeda39d, mapcss._tag_capture(capture_tags, 1, tags, u'place')) and mapcss._tag_capture(capture_tags, 2, tags, u'population') < 10000)):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("local com menos de 10.000 habitantes deve ser classificado como village")
            # fixAdd:"place=village"
            err.append({'class': 9018006, 'subclass': 719699918, 'text': mapcss.tr(u'local com menos de 10.000 habitantes deve ser classificado como village', capture_tags), 'fix': {
                '+': dict([
                    [u'place',u'village']])
            }})

        # *[place=city][!population]
        # *[place=town][!population]
        # *[place=village][!population]
        if (u'place' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'city' and not mapcss._tag_capture(capture_tags, 1, tags, u'population')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'town' and not mapcss._tag_capture(capture_tags, 1, tags, u'population')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'village' and not mapcss._tag_capture(capture_tags, 1, tags, u'population'))):
            # throwWarning:tr("{0} sem tag de população (population)","{0.value}")
            err.append({'class': 9018011, 'subclass': 1582438505, 'text': mapcss.tr(u'{0} sem tag de população (population)', capture_tags, u'{0.value}')})

        # *[place=city][!name]
        # *[place=town][!name]
        # *[place=village][!name]
        if (u'place' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'city' and not mapcss._tag_capture(capture_tags, 1, tags, u'name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'town' and not mapcss._tag_capture(capture_tags, 1, tags, u'name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'village' and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))):
            # throwWarning:tr("{0} sem nome","{0.value}")
            err.append({'class': 9018012, 'subclass': 828568305, 'text': mapcss.tr(u'{0} sem nome', capture_tags, u'{0.value}')})

        # node[place=~/village|town|city/]["addr:city"=*name]
        # node[place=suburb]["addr:suburb"=*name]
        if (u'place' in keys) and \
            ((mapcss.regexp_test_(self.re_0db5b64e, mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'addr:city') == mapcss.tag(tags, u'name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'suburb' and mapcss._tag_capture(capture_tags, 1, tags, u'addr:suburb') == mapcss.tag(tags, u'name'))):
            # group:tr("Brasil - Correções e melhorias")
            # throwError:tr("não deve possuir {0}","{1.key}")
            # fixRemove:"{1.key}"
            err.append({'class': 9018006, 'subclass': 1782871982, 'text': mapcss.tr(u'não deve possuir {0}', capture_tags, u'{1.key}'), 'fix': {
                '-': ([
                    u'{1.key}'])
            }})

        # *["addr:city"=~/(,|( |-) ?[A-Z]{2})/]
        if (u'addr:city' in keys) and \
            ((mapcss.regexp_test_(self.re_10f1c360, mapcss._tag_capture(capture_tags, 0, tags, u'addr:city')))):
            # throwWarning:tr("{0} deve conter apenas o nome da cidade","{0.key}")
            err.append({'class': 9018013, 'subclass': 223700239, 'text': mapcss.tr(u'{0} deve conter apenas o nome da cidade', capture_tags, u'{0.key}')})

        # *[name=~/^(?i)(?u)(Faz\.|Fazenda|Sítio|Chácara)/][place][place!~/city|farm|neighbourhood|suburb|town|village/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_2cd1e949, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'place') and not mapcss.regexp_test_(self.re_5d3348cb, mapcss._tag_capture(capture_tags, 2, tags, u'place')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("objeto talvez deva ser {0}=farm","{1.key}")
            err.append({'class': 9018002, 'subclass': 414255329, 'text': mapcss.tr(u'objeto talvez deva ser {0}=farm', capture_tags, u'{1.key}')})

        # *[place][name=~/^(?i)Bairro\b/][name!~/^(?i)Bairro d(a|e|o)s?\b/]
        if (u'place' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'place') and mapcss.regexp_test_(self.re_20fc5143, mapcss._tag_capture(capture_tags, 1, tags, u'name')) and not mapcss.regexp_test_(self.re_64387998, mapcss._tag_capture(capture_tags, 2, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("objeto talvez não deva ter ''Bairro'' no nome")
            err.append({'class': 9018002, 'subclass': 457937105, 'text': mapcss.tr(u'objeto talvez não deva ter \'\'Bairro\'\' no nome', capture_tags)})

        # node[place=~/^(island|islet)$/]
        if (u'place' in keys) and \
            ((mapcss.regexp_test_(self.re_6416be64, mapcss._tag_capture(capture_tags, 0, tags, u'place')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("representar a ilha, se possível, como uma área")
            err.append({'class': 9018002, 'subclass': 903906160, 'text': mapcss.tr(u'representar a ilha, se possível, como uma área', capture_tags)})

        # *[iata="0"]
        if (u'iata' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'iata') == u'0')):
            # throwWarning:tr("{0} com valor = {1}","{0.key}","{0.value}")
            err.append({'class': 9018014, 'subclass': 1389202412, 'text': mapcss.tr(u'{0} com valor = {1}', capture_tags, u'{0.key}', u'{0.value}')})

        # *[amenity=~/college|school/][name=~/^(?i)(?u)(Centro Universitário|Faculdades?|FATEC|Instituto Federal)\b/]
        if (u'amenity' in keys) and \
            ((mapcss.regexp_test_(self.re_362f879f, mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test_(self.re_1d232d4c, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("estabelecimento de ensino classificado incorretamente")
            # suggestAlternative:"amenity=university"
            # fixAdd:"{0.key}=university"
            err.append({'class': 9018006, 'subclass': 221523813, 'text': mapcss.tr(u'estabelecimento de ensino classificado incorretamente', capture_tags), 'fix': {
                '+': dict([
                    [u'{0.key}',u'university']])
            }})

        # *[amenity=school][name=~/^(?i)(?u)(SENAC|SENAI|Serviço Nacional de Aprendizagem)/]
        # *[amenity=~/school|university/][name=~/(?i)(?u)\b(Centro Paula Souza|Escola Técnica|ETEC)\b/]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'school' and mapcss.regexp_test_(self.re_044c8944, mapcss._tag_capture(capture_tags, 1, tags, u'name'))) or \
            (mapcss.regexp_test_(self.re_6c0d6e9e, mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test_(self.re_3b304b9b, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("estabelecimento de ensino classificado incorretamente")
            # suggestAlternative:"amenity=college"
            # fixAdd:"{0.key}=college"
            err.append({'class': 9018006, 'subclass': 897019825, 'text': mapcss.tr(u'estabelecimento de ensino classificado incorretamente', capture_tags), 'fix': {
                '+': dict([
                    [u'{0.key}',u'college']])
            }})

        # *[amenity=school][name=~/^(?i)(?u)(auto(-| )?( moto )?escola|centro de formação de condutores|cfc|moto escola)\b/]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'school' and mapcss.regexp_test_(self.re_35bb0f2f, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("autoescola classificada incorretamente")
            # suggestAlternative:"amenity=driving_school"
            # fixAdd:"{0.key}=driving_school"
            err.append({'class': 9018006, 'subclass': 1796023580, 'text': mapcss.tr(u'autoescola classificada incorretamente', capture_tags), 'fix': {
                '+': dict([
                    [u'{0.key}',u'driving_school']])
            }})

        # *[amenity=school][name=~/^(?i)creche\b/]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'school' and mapcss.regexp_test_(self.re_160d1bfc, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("creche classificada incorretamente")
            # suggestAlternative:"amenity=kindergarten"
            # fixAdd:"{0.key}=kindergarten"
            err.append({'class': 9018006, 'subclass': 121701344, 'text': mapcss.tr(u'creche classificada incorretamente', capture_tags), 'fix': {
                '+': dict([
                    [u'{0.key}',u'kindergarten']])
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
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_69d0dc1a, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'power') and mapcss._tag_capture(capture_tags, 2, tags, u'power') != u'substation') or \
            (mapcss.regexp_test_(self.re_002de70b, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') != u'courthouse') or \
            (mapcss.regexp_test_(self.re_25871691, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'hospital') or \
            (mapcss.regexp_test_(self.re_6e928d7b, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'university') or \
            (mapcss.regexp_test_(self.re_57a9f888, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'school') or \
            (mapcss.regexp_test_(self.re_458e02d8, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'hotel') or \
            (mapcss.regexp_test_(self.re_105662b4, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'chapel') or \
            (mapcss.regexp_test_(self.re_752011f2, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'church') or \
            (mapcss.regexp_test_(self.re_1e8e69a3, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'cathedral') or \
            (mapcss.regexp_test_(self.re_381002af, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'farm') or \
            (mapcss.regexp_test_(self.re_486d02c4, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'supermarket')):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("{0} provavelmente deveria ser {1}","{2.key}","{2.value}")
            # fixAdd:"{2.key}={2.value}"
            err.append({'class': 9018006, 'subclass': 1930177472, 'text': mapcss.tr(u'{0} provavelmente deveria ser {1}', capture_tags, u'{2.key}', u'{2.value}'), 'fix': {
                '+': dict([
                    [u'{2.key}',u'{2.value}']])
            }})

        # *[name=~/^(?i)(?u)(AM(A|E)|(Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF).*/][amenity=hospital]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_7b7c453d, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') == u'hospital')):
            # throwWarning:tr("postos/unidades de saúde devem ser amenity=clinic")
            err.append({'class': 9018015, 'subclass': 2108543140, 'text': mapcss.tr(u'postos/unidades de saúde devem ser amenity=clinic', capture_tags)})

        # *[name=~/^(?i)\bSAMU\b/][amenity=~/clinic|doctors|hospital/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_2dbaea13, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.regexp_test_(self.re_3eb0ab44, mapcss._tag_capture(capture_tags, 1, tags, u'amenity')))):
            # throwWarning:tr("SAMU classificado de forma errada")
            # suggestAlternative:"emergency=ambulance_station"
            err.append({'class': 9018016, 'subclass': 2090365947, 'text': mapcss.tr(u'SAMU classificado de forma errada', capture_tags)})

        # node[highway=~/^(give_way|mini_roundabout|stop|turning_circle)$/][name]
        if (u'highway' in keys) and \
            ((mapcss.regexp_test_(self.re_53abc074, mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'name'))):
            # throwWarning:tr("objeto não deve possuir {0}","{1.key}")
            err.append({'class': 9018017, 'subclass': 306235762, 'text': mapcss.tr(u'objeto não deve possuir {0}', capture_tags, u'{1.key}')})

        # node[highway=speed_camera][!maxspeed]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'speed_camera' and not mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed'))):
            # throwWarning:tr("adicionar {0} ao {1}","{1.key}","{0.tag}")
            err.append({'class': 9018018, 'subclass': 1369285067, 'text': mapcss.tr(u'adicionar {0} ao {1}', capture_tags, u'{1.key}', u'{0.tag}')})

        # *[crossing][!highway][!railway]
        if (u'crossing' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'crossing') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway'))):
            # throwWarning:tr("{0} deve ser utilizado com {1}={0} ou {2}={0}","{0.key}","{1.key}","{2.key}")
            err.append({'class': 9018019, 'subclass': 139983185, 'text': mapcss.tr(u'{0} deve ser utilizado com {1}={0} ou {2}={0}', capture_tags, u'{0.key}', u'{1.key}', u'{2.key}')})

        # *[aeroway][designation=~/^[A-Z]{4}$/][!icao]
        # *[aeroway][ref=~/^[A-Z]{4}$/][!icao]
        if (u'aeroway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') and mapcss.regexp_test_(self.re_7afc6883, mapcss._tag_capture(capture_tags, 1, tags, u'designation')) and not mapcss._tag_capture(capture_tags, 2, tags, u'icao')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') and mapcss.regexp_test_(self.re_7afc6883, mapcss._tag_capture(capture_tags, 1, tags, u'ref')) and not mapcss._tag_capture(capture_tags, 2, tags, u'icao'))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("{0} provavelmente deve ser utilizado como {1}","{1.key}","{2.key}")
            # fixChangeKey:"{1.key} => {2.key}"
            err.append({'class': 9018006, 'subclass': 662001655, 'text': mapcss.tr(u'{0} provavelmente deve ser utilizado como {1}', capture_tags, u'{1.key}', u'{2.key}'), 'fix': {
                '+': dict([
                    [u'{2.key}', mapcss.tag(tags, u'{1.key}')]]),
                '-': ([
                    u'{1.key}'])
            }})

        # *[access=permissive]
        if (u'access' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'access') == u'permissive')):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} deve ser utilizado apenas em vias privadas com permissão de acesso e não em vias de acesso público","{0.tag}")
            err.append({'class': 9018002, 'subclass': 1918455197, 'text': mapcss.tr(u'{0} deve ser utilizado apenas em vias privadas com permissão de acesso e não em vias de acesso público', capture_tags, u'{0.tag}')})

        # *[name=~/^(?U)(\p{Upper}| )+$/]
        # *["addr:street"=~/^(?U)(\p{Upper}| )+$/]
        if (u'addr:street' in keys or u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_73b50a21, mapcss._tag_capture(capture_tags, 0, tags, u'name'))) or \
            (mapcss.regexp_test_(self.re_73b50a21, mapcss._tag_capture(capture_tags, 0, tags, u'addr:street')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} totalmente em maiúsculo; usar nome completo ou short_name se for sigla","{0.key}")
            err.append({'class': 9018002, 'subclass': 386880794, 'text': mapcss.tr(u'{0} totalmente em maiúsculo; usar nome completo ou short_name se for sigla', capture_tags, u'{0.key}')})

        # *["addr:postcode"=~/^[0-9]{8}$/]
        if (u'addr:postcode' in keys) and \
            ((mapcss.regexp_test_(self.re_2dbf771a, mapcss._tag_capture(capture_tags, 0, tags, u'addr:postcode')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("formato do CEP pode ser melhorado")
            # fixAdd:concat("addr:postcode=",substring(tag("addr:postcode"),0,5),"-",substring(tag("addr:postcode"),5,8))
            err.append({'class': 9018006, 'subclass': 523931624, 'text': mapcss.tr(u'formato do CEP pode ser melhorado', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'addr:postcode=', mapcss.substring(mapcss.tag(tags, u'addr:postcode'), 0, 5), u'-', mapcss.substring(mapcss.tag(tags, u'addr:postcode'), 5, 8))).split('=', 1)])
            }})

        # *[postal_code=~/^[0-9]{8}$/]
        if (u'postal_code' in keys) and \
            ((mapcss.regexp_test_(self.re_2dbf771a, mapcss._tag_capture(capture_tags, 0, tags, u'postal_code')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("formato do CEP pode ser melhorado")
            # fixAdd:concat("postal_code=",substring(tag("postal_code"),0,5),"-",substring(tag("postal_code"),5,8))
            err.append({'class': 9018006, 'subclass': 1234269468, 'text': mapcss.tr(u'formato do CEP pode ser melhorado', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'postal_code=', mapcss.substring(mapcss.tag(tags, u'postal_code'), 0, 5), u'-', mapcss.substring(mapcss.tag(tags, u'postal_code'), 5, 8))).split('=', 1)])
            }})

        # *["addr:postcode"=~/^[0-9]{5}( |\.)[0-9]{3}$/]
        if (u'addr:postcode' in keys) and \
            ((mapcss.regexp_test_(self.re_57bee688, mapcss._tag_capture(capture_tags, 0, tags, u'addr:postcode')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("formato do CEP pode ser melhorado")
            # fixAdd:concat("addr:postcode=",replace(replace(tag("addr:postcode")," ","-"),".","-"))
            err.append({'class': 9018006, 'subclass': 308348773, 'text': mapcss.tr(u'formato do CEP pode ser melhorado', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'addr:postcode=', mapcss.replace(mapcss.replace(mapcss.tag(tags, u'addr:postcode'), u' ', u'-'), u'.', u'-'))).split('=', 1)])
            }})

        # *["postal_code"=~/^[0-9]{5}( |\.)[0-9]{3}$/]
        if (u'postal_code' in keys) and \
            ((mapcss.regexp_test_(self.re_57bee688, mapcss._tag_capture(capture_tags, 0, tags, u'postal_code')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("formato do CEP pode ser melhorado")
            # fixAdd:concat("postal_code=",replace(replace(tag("postal_code")," ","-"),".","-"))
            err.append({'class': 9018006, 'subclass': 1211220107, 'text': mapcss.tr(u'formato do CEP pode ser melhorado', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'postal_code=', mapcss.replace(mapcss.replace(mapcss.tag(tags, u'postal_code'), u' ', u'-'), u'.', u'-'))).split('=', 1)])
            }})

        # *["addr:postcode"]["addr:postcode"!~/^[0-9]{5}-[0-9]{3}$/]
        # *[postal_code][postal_code!~/^[0-9]{5}-[0-9]{3}$/]
        if (u'addr:postcode' in keys or u'postal_code' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'addr:postcode') and not mapcss.regexp_test_(self.re_1ffe94a9, mapcss._tag_capture(capture_tags, 1, tags, u'addr:postcode'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'postal_code') and not mapcss.regexp_test_(self.re_1ffe94a9, mapcss._tag_capture(capture_tags, 1, tags, u'postal_code')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} (CEP) em formato diferente de NNNNN-NNN","{0.key}")
            err.append({'class': 9018002, 'subclass': 1843994632, 'text': mapcss.tr(u'{0} (CEP) em formato diferente de NNNNN-NNN', capture_tags, u'{0.key}')})

        # *[alt_source][source]
        if (u'alt_source' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'alt_source') and mapcss._tag_capture(capture_tags, 1, tags, u'source'))):
            # throwWarning:tr("{0} deve estar incluído em {1}, separado por '';'' caso necessário","{0.key}","{1.key}")
            err.append({'class': 9018020, 'subclass': 512568644, 'text': mapcss.tr(u'{0} deve estar incluído em {1}, separado por \'\';\'\' caso necessário', capture_tags, u'{0.key}', u'{1.key}')})

        # *[landuse?]
        if (u'landuse' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'landuse') in ('yes', 'true', '1'))):
            # throwWarning:tr("especificar valor correto para {0} ao invés de ''{1}''","{0.key}",tag("landuse"))
            err.append({'class': 9018021, 'subclass': 2004192493, 'text': mapcss.tr(u'especificar valor correto para {0} ao invés de \'\'{1}\'\'', capture_tags, u'{0.key}', mapcss.tag(tags, u'landuse'))})

        # *[long_name]
        if (u'long_name' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'long_name'))):
            # throwWarning:tr("chave inválida: {0}","{0.key}")
            # suggestAlternative:"alt_name"
            # suggestAlternative:"name"
            # suggestAlternative:"official_name"
            err.append({'class': 9018022, 'subclass': 1648910015, 'text': mapcss.tr(u'chave inválida: {0}', capture_tags, u'{0.key}')})

        # *["building:levels"<1]
        if (u'building:levels' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'building:levels') < 1)):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com valor inválido","{0.key}")
            err.append({'class': 9018002, 'subclass': 154478605, 'text': mapcss.tr(u'{0} com valor inválido', capture_tags, u'{0.key}')})

        # *[hires?]
        if (u'hires' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'hires') in ('yes', 'true', '1'))):
            # throwWarning:tr("não se deve utilizar {0} para demarcar áreas de cobertura de imagem","{0.key}")
            err.append({'class': 9018023, 'subclass': 1394305840, 'text': mapcss.tr(u'não se deve utilizar {0} para demarcar áreas de cobertura de imagem', capture_tags, u'{0.key}')})

        # node[man_made=tower][!"tower:type"]
        if (u'man_made' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'man_made') == u'tower' and not mapcss._tag_capture(capture_tags, 1, tags, u'tower:type'))):
            # throwOther:tr("ausência do tipo de torre ({0})","{1.key}")
            err.append({'class': 9018024, 'subclass': 85637620, 'text': mapcss.tr(u'ausência do tipo de torre ({0})', capture_tags, u'{1.key}')})

        # *[tourism=motel][amenity!=love_hotel]
        # *[name=~/(?i)\bmotel\b/][amenity!=love_hotel]
        if (u'name' in keys or u'tourism' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == u'motel' and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != u'love_hotel') or \
            (mapcss.regexp_test_(self.re_01454d46, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != u'love_hotel')):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("ausência de tag ''{0}''","{1.value}")
            # fixAdd:"{1.key}={1.value}"
            err.append({'class': 9018006, 'subclass': 444111908, 'text': mapcss.tr(u'ausência de tag \'\'{0}\'\'', capture_tags, u'{1.value}'), 'fix': {
                '+': dict([
                    [u'{1.key}',u'{1.value}']])
            }})

        # *[amenity=love_hotel][tourism][tourism!=motel]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'love_hotel' and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') and mapcss._tag_capture(capture_tags, 2, tags, u'tourism') != u'motel')):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("provavelmente deve ser ''{0}={1}''","{2.key}","{2.value}")
            err.append({'class': 9018002, 'subclass': 2021262051, 'text': mapcss.tr(u'provavelmente deve ser \'\'{0}={1}\'\'', capture_tags, u'{2.key}', u'{2.value}')})

        # *[name=~/(?i)^motel\b/][tourism!=motel]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_5cd37790, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') != u'motel')):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("motel classificado incorretamente")
            # suggestAlternative:"tourism=motel"
            err.append({'class': 9018002, 'subclass': 2096064741, 'text': mapcss.tr(u'motel classificado incorretamente', capture_tags)})

        # *[aeroway=aerodrome][!icao]
        # *[aeroway=helipad][!icao]
        if (u'aeroway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'aerodrome' and not mapcss._tag_capture(capture_tags, 1, tags, u'icao')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'helipad' and not mapcss._tag_capture(capture_tags, 1, tags, u'icao'))):
            # throwOther:tr("{0} sem tag {1}","{0.value}","{1.key}")
            err.append({'class': 9018025, 'subclass': 1760501517, 'text': mapcss.tr(u'{0} sem tag {1}', capture_tags, u'{0.value}', u'{1.key}')})

        # *[aeroway=aerodrome][name=~/(?i).*airport$/]
        # *[aeroway=helipad][name=~/(?i).*heliport$/]
        if (u'aeroway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'aerodrome' and mapcss.regexp_test_(self.re_6efb8049, mapcss._tag_capture(capture_tags, 1, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'helipad' and mapcss.regexp_test_(self.re_6566db6a, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com nome em inglês","{0.tag}")
            err.append({'class': 9018002, 'subclass': 134725283, 'text': mapcss.tr(u'{0} com nome em inglês', capture_tags, u'{0.tag}')})

        # *[aeroway=aerodrome][name=~/(?i)^Aer(ódromo|oporto) de.*/]
        # *[aeroway=helipad][name=~/(?i)^Helipo(n|r)to.*/]
        if (u'aeroway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'aerodrome' and mapcss.regexp_test_(self.re_6024a566, mapcss._tag_capture(capture_tags, 1, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'helipad' and mapcss.regexp_test_(self.re_139e342b, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("conferir se existe nome oficial do {0}","{0.value}")
            err.append({'class': 9018002, 'subclass': 2002284471, 'text': mapcss.tr(u'conferir se existe nome oficial do {0}', capture_tags, u'{0.value}')})

        # *[aeroway=aerodrome][ref]
        if (u'aeroway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'aerodrome' and mapcss._tag_capture(capture_tags, 1, tags, u'ref'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("''{0}'' não faz sentido em aeroporto","{1.key}")
            err.append({'class': 9018002, 'subclass': 339634841, 'text': mapcss.tr(u'\'\'{0}\'\' não faz sentido em aeroporto', capture_tags, u'{1.key}')})

        # node[surface][!traffic_calming]
        if (u'surface' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'surface') and not mapcss._tag_capture(capture_tags, 1, tags, u'traffic_calming'))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("superfície ({0}) erroneamente definida no nó","{0.key}")
            # fixRemove:"{0.key}"
            err.append({'class': 9018006, 'subclass': 645857049, 'text': mapcss.tr(u'superfície ({0}) erroneamente definida no nó', capture_tags, u'{0.key}'), 'fix': {
                '-': ([
                    u'{0.key}'])
            }})

        # *[waterway][layer<0][!tunnel]
        if (u'waterway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'layer') < 0 and not mapcss._tag_capture(capture_tags, 2, tags, u'tunnel'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} negativo de {1} com ausência de {2}","{1.key}","{0.key}","{2.key}")
            err.append({'class': 9018002, 'subclass': 1476002587, 'text': mapcss.tr(u'{0} negativo de {1} com ausência de {2}', capture_tags, u'{1.key}', u'{0.key}', u'{2.key}')})

        # *[waterway][layer>0][!bridge]
        if (u'waterway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'layer') > 0 and not mapcss._tag_capture(capture_tags, 2, tags, u'bridge'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} positivo de {1} com ausência de {2}","{1.key}","{0.key}","{2.key}")
            err.append({'class': 9018002, 'subclass': 1137415389, 'text': mapcss.tr(u'{0} positivo de {1} com ausência de {2}', capture_tags, u'{1.key}', u'{0.key}', u'{2.key}')})

        # *[layer][!building][!highway][man_made!=pipeline][!railway][!waterway]
        if (u'layer' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'layer') and not mapcss._tag_capture(capture_tags, 1, tags, u'building') and not mapcss._tag_capture(capture_tags, 2, tags, u'highway') and mapcss._tag_capture(capture_tags, 3, tags, u'man_made') != u'pipeline' and not mapcss._tag_capture(capture_tags, 4, tags, u'railway') and not mapcss._tag_capture(capture_tags, 5, tags, u'waterway'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("possível uso incorreto de {0} no objeto","{0.key}")
            err.append({'class': 9018002, 'subclass': 373443518, 'text': mapcss.tr(u'possível uso incorreto de {0} no objeto', capture_tags, u'{0.key}')})

        # *[name=~/^(?i)(?u)edifício.*/][!building]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_38a8f0ff, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'building'))):
            # throwWarning:tr("possível ausência de tag {0}","{1.key}")
            err.append({'class': 9018026, 'subclass': 1417041710, 'text': mapcss.tr(u'possível ausência de tag {0}', capture_tags, u'{1.key}')})

        # *[route=ferry][!duration]
        if (u'route' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'route') == u'ferry' and not mapcss._tag_capture(capture_tags, 1, tags, u'duration'))):
            # throwWarning:tr("ausência do tempo de duração ({0}) da balsa","{1.key}")
            err.append({'class': 9018027, 'subclass': 1289884816, 'text': mapcss.tr(u'ausência do tempo de duração ({0}) da balsa', capture_tags, u'{1.key}')})

        # *[building][!wheelchair]
        if (u'building' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'building') and not mapcss._tag_capture(capture_tags, 1, tags, u'wheelchair'))):
            # throwOther:tr("{0} sem tag de acessibilidade ({1})","{0.key}","{1.key}")
            err.append({'class': 9018028, 'subclass': 1627625912, 'text': mapcss.tr(u'{0} sem tag de acessibilidade ({1})', capture_tags, u'{0.key}', u'{1.key}')})

        # *[name=~/^(?i)(?u)praça.*/][!leisure][landuse=~/^(forest|grass|greenfield|meadow|orchard)$/]
        # *[name=~/^(?i)(?u)praça.*/][!leisure][natural=~/^(grassland|heath|scrub|wood)$/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_4a8ca94e, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'leisure') and mapcss.regexp_test_(self.re_05a345c7, mapcss._tag_capture(capture_tags, 2, tags, u'landuse'))) or \
            (mapcss.regexp_test_(self.re_4a8ca94e, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'leisure') and mapcss.regexp_test_(self.re_12b48afb, mapcss._tag_capture(capture_tags, 2, tags, u'natural')))):
            # throwWarning:tr("possível definição incorreta para praça: ''{0}''","{2.key}")
            # suggestAlternative:"leisure=park"
            err.append({'class': 9018029, 'subclass': 80498829, 'text': mapcss.tr(u'possível definição incorreta para praça: \'\'{0}\'\'', capture_tags, u'{2.key}')})

        # *[wikipedia][wikipedia!~/^pt:/]
        if (u'wikipedia' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia') and not mapcss.regexp_test_(self.re_17fd35b3, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')))):
            # throwWarning:tr("utilizar prefixo em português (pt:) para {0}","{0.key}")
            err.append({'class': 9018030, 'subclass': 1219382195, 'text': mapcss.tr(u'utilizar prefixo em português (pt:) para {0}', capture_tags, u'{0.key}')})

        # *[name=~/.*\(.*\).*/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_7e9dfbe7, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com parênteses. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.","{0.key}")
            err.append({'class': 9018002, 'subclass': 1406083581, 'text': mapcss.tr(u'{0} com parênteses. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.', capture_tags, u'{0.key}')})

        # *[name=~/ - /]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_6b25b0c5, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com traço. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.","{0.key}")
            err.append({'class': 9018002, 'subclass': 1992839086, 'text': mapcss.tr(u'{0} com traço. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.', capture_tags, u'{0.key}')})

        # *[name=~/, /]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_4da7cb86, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com vírgula. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.","{0.key}")
            err.append({'class': 9018002, 'subclass': 659472938, 'text': mapcss.tr(u'{0} com vírgula. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.', capture_tags, u'{0.key}')})

        # *[name=~/: /]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_657f3be3, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com dois pontos. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.","{0.key}")
            err.append({'class': 9018002, 'subclass': 338682039, 'text': mapcss.tr(u'{0} com dois pontos. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.', capture_tags, u'{0.key}')})

        # *[name=~/ ou /]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_131cc885, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # throwWarning:tr("nome utilizado de forma incorreta")
            # suggestAlternative:"name e alt_name"
            err.append({'class': 9018031, 'subclass': 23034604, 'text': mapcss.tr(u'nome utilizado de forma incorreta', capture_tags)})

        # node[admin_level][!capital]
        # node[border_type]
        # node[boundary]
        # node[type=boundary]
        if (u'admin_level' in keys or u'border_type' in keys or u'boundary' in keys or u'type' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'admin_level') and not mapcss._tag_capture(capture_tags, 1, tags, u'capital')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'border_type')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'boundary')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'type') == u'boundary')):
            # throwError:tr("nó não deve possuir {0}","{0.tag}")
            err.append({'class': 9018032, 'subclass': 573228766, 'text': mapcss.tr(u'nó não deve possuir {0}', capture_tags, u'{0.tag}')})

        # *[boundary=national_park][!name]
        # *[boundary=protected_area][!name]
        # *[leisure=nature_reserve][!name]
        if (u'boundary' in keys or u'leisure' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == u'national_park' and not mapcss._tag_capture(capture_tags, 1, tags, u'name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == u'protected_area' and not mapcss._tag_capture(capture_tags, 1, tags, u'name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == u'nature_reserve' and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))):
            # throwWarning:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
            err.append({'class': 9018033, 'subclass': 1492609299, 'text': mapcss.tr(u'{0} deve possuir {1}', capture_tags, u'{0.tag}', u'{1.key}')})

        # *[boundary=protected_area][!protect_class]
        if (u'boundary' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == u'protected_area' and not mapcss._tag_capture(capture_tags, 1, tags, u'protect_class'))):
            # throwWarning:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
            err.append({'class': 9018033, 'subclass': 822952800, 'text': mapcss.tr(u'{0} deve possuir {1}', capture_tags, u'{0.tag}', u'{1.key}')})

        # *[protect_class][protect_class!~/^(1(a|b)?|[1-9][0-9]?)$/]
        if (u'protect_class' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'protect_class') and not mapcss.regexp_test_(self.re_5ac7053e, mapcss._tag_capture(capture_tags, 1, tags, u'protect_class')))):
            # throwWarning:tr("valor incorreto para {0}","{0.key}")
            err.append({'class': 9018034, 'subclass': 1459161459, 'text': mapcss.tr(u'valor incorreto para {0}', capture_tags, u'{0.key}')})

        # *[protect_class][boundary!=protected_area]
        if (u'protect_class' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'protect_class') and mapcss._tag_capture(capture_tags, 1, tags, u'boundary') != u'protected_area')):
            # throwWarning:tr("ausência de boundary=protected_area")
            err.append({'class': 9018035, 'subclass': 1208814760, 'text': mapcss.tr(u'ausência de boundary=protected_area', capture_tags)})

        # node[destination]
        if (u'destination' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'destination'))):
            # throwWarning:tr("{0} deve ser usado apenas em ways","{0.key}")
            err.append({'class': 9018036, 'subclass': 1394019686, 'text': mapcss.tr(u'{0} deve ser usado apenas em ways', capture_tags, u'{0.key}')})

        # node[exit_to]
        if (u'exit_to' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'exit_to'))):
            # throwWarning:tr("utilize ''destination'' no caminho de saída ao invés de ''exit_to''")
            err.append({'class': 9018037, 'subclass': 2117439762, 'text': mapcss.tr(u'utilize \'\'destination\'\' no caminho de saída ao invés de \'\'exit_to\'\'', capture_tags)})

        # *[amenity][!opening_hours]
        # *[shop][!opening_hours]
        if (u'amenity' in keys or u'shop' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') and not mapcss._tag_capture(capture_tags, 1, tags, u'opening_hours')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'shop') and not mapcss._tag_capture(capture_tags, 1, tags, u'opening_hours'))):
            # throwOther:tr("{0} sem {1}","{0.key}","{1.key}")
            err.append({'class': 9018038, 'subclass': 1861306703, 'text': mapcss.tr(u'{0} sem {1}', capture_tags, u'{0.key}', u'{1.key}')})

        # node[highway=motorway_junction][ref][ref!~/^[0-9]+( |-)*([A-Z])?$/]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'motorway_junction' and mapcss._tag_capture(capture_tags, 1, tags, u'ref') and not mapcss.regexp_test_(self.re_20188fb1, mapcss._tag_capture(capture_tags, 2, tags, u'ref')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("saída de rodovia ({0}) fora do padrão","{1.key}")
            err.append({'class': 9018002, 'subclass': 2069822365, 'text': mapcss.tr(u'saída de rodovia ({0}) fora do padrão', capture_tags, u'{1.key}')})

        # node[highway=motorway_junction][name]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'motorway_junction' and mapcss._tag_capture(capture_tags, 1, tags, u'name'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} geralmente não possui nome; use ''destination'' no caminho de saída","{0.tag}")
            err.append({'class': 9018002, 'subclass': 1930778720, 'text': mapcss.tr(u'{0} geralmente não possui nome; use \'\'destination\'\' no caminho de saída', capture_tags, u'{0.tag}')})

        # node[junction]
        if (u'junction' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'junction'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("junção ({0}) em um nó","{0.value}")
            # suggestAlternative:"highway=mini_roundabout"
            # suggestAlternative:"highway=turning_circle"
            err.append({'class': 9018002, 'subclass': 1193804268, 'text': mapcss.tr(u'junção ({0}) em um nó', capture_tags, u'{0.value}')})

        # *[name=~/.* D(a|e|o)s? .*/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_2ffc377d, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("''da'', ''de'' e ''do'' são minúsculos nos nomes em português")
            err.append({'class': 9018002, 'subclass': 1986668346, 'text': mapcss.tr(u'\'\'da\'\', \'\'de\'\' e \'\'do\'\' são minúsculos nos nomes em português', capture_tags)})

        # *[name=~/^[a-z].*/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_39d67968, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("nome iniciando com letra minúscula")
            err.append({'class': 9018002, 'subclass': 167462302, 'text': mapcss.tr(u'nome iniciando com letra minúscula', capture_tags)})

        # *[alt_ref]
        if (u'alt_ref' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'alt_ref'))):
            # throwWarning:tr("o conteúdo de {0} deve fazer parte de ref, separado por ;","{0.key}")
            # suggestAlternative:"ref"
            err.append({'class': 9018039, 'subclass': 722411109, 'text': mapcss.tr(u'o conteúdo de {0} deve fazer parte de ref, separado por ;', capture_tags, u'{0.key}')})

        # *[source=~/.*,.*/]
        # *["source:ref"=~/.*,.*/]
        # *["source:name"=~/.*,.*/]
        if (u'source' in keys or u'source:name' in keys or u'source:ref' in keys) and \
            ((mapcss.regexp_test_(self.re_34f65002, mapcss._tag_capture(capture_tags, 0, tags, u'source'))) or \
            (mapcss.regexp_test_(self.re_34f65002, mapcss._tag_capture(capture_tags, 0, tags, u'source:ref'))) or \
            (mapcss.regexp_test_(self.re_34f65002, mapcss._tag_capture(capture_tags, 0, tags, u'source:name')))):
            # throwOther:tr("utilizar ; como separador de valores em {0}","{0.key}")
            err.append({'class': 9018040, 'subclass': 2114349281, 'text': mapcss.tr(u'utilizar ; como separador de valores em {0}', capture_tags, u'{0.key}')})

        # *[surface][eval(number_of_tags())=1]
        if (u'surface' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'surface') and len(tags) == 1)):
            # throwWarning:tr("objeto incompleto: possui apenas {0}","{0.key}")
            err.append({'class': 9018041, 'subclass': 1776991136, 'text': mapcss.tr(u'objeto incompleto: possui apenas {0}', capture_tags, u'{0.key}')})

        # *[name][surface][eval(number_of_tags())=2]
        # *[name][website][eval(number_of_tags())=2]
        if (u'name' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'surface') and len(tags) == 2) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'website') and len(tags) == 2)):
            # throwWarning:tr("objeto incompleto: possui apenas {0} e {1}","{0.key}","{1.key}")
            err.append({'class': 9018042, 'subclass': 626126700, 'text': mapcss.tr(u'objeto incompleto: possui apenas {0} e {1}', capture_tags, u'{0.key}', u'{1.key}')})

        # *[leisure=pitch][sport=tennis][surface=unpaved]
        if (u'leisure' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == u'pitch' and mapcss._tag_capture(capture_tags, 1, tags, u'sport') == u'tennis' and mapcss._tag_capture(capture_tags, 2, tags, u'surface') == u'unpaved')):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("{0} com superfície incorreta","{2.key}")
            # suggestAlternative:"surface=clay"
            # fixAdd:"surface=clay"
            err.append({'class': 9018006, 'subclass': 1659179489, 'text': mapcss.tr(u'{0} com superfície incorreta', capture_tags, u'{2.key}'), 'fix': {
                '+': dict([
                    [u'surface',u'clay']])
            }})

        # *[amenity=fuel][name=~/(?i)(?u)\b(Ale|BR|Esso|Ipiranga|Petrobr(á|a)s|Shell|Texaco)\b/]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'fuel' and mapcss.regexp_test_(self.re_604bb645, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("uso incorreto da bandeira do posto")
            # suggestAlternative:"brand"
            err.append({'class': 9018002, 'subclass': 935774110, 'text': mapcss.tr(u'uso incorreto da bandeira do posto', capture_tags)})

        # *[/_[0-9]$/][!"is_in:iso_3166_2"]
        if ((mapcss._tag_capture(capture_tags, 0, tags, self.re_57b8ef8e) and not mapcss._tag_capture(capture_tags, 1, tags, u'is_in:iso_3166_2'))):
            # throwError:tr("chave inválida: {0}","{0.key}")
            err.append({'class': 9018022, 'subclass': 331369569, 'text': mapcss.tr(u'chave inválida: {0}', capture_tags, u'{0.key}')})

        # *["addr:housenumber"=~/(?i)^s(\.|-| )?\/?n\.?º?$/][!note]
        if (u'addr:housenumber' in keys) and \
            ((mapcss.regexp_test_(self.re_0b27200b, mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber')) and not mapcss._tag_capture(capture_tags, 1, tags, u'note'))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("não utilizar ''{0}'' para locais sem número",tag("addr:housenumber"))
            # suggestAlternative:"note"
            # fixRemove:"addr:housenumber"
            # fixAdd:"note=Local sem número"
            err.append({'class': 9018006, 'subclass': 931902546, 'text': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', capture_tags, mapcss.tag(tags, u'addr:housenumber')), 'fix': {
                '+': dict([
                    [u'note',u'Local sem número']]),
                '-': ([
                    u'addr:housenumber'])
            }})

        # *["addr:housenumber"=~/(?i)^s(\.|-| )?\/?n\.?º?$/][note]
        if (u'addr:housenumber' in keys) and \
            ((mapcss.regexp_test_(self.re_0b27200b, mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber')) and mapcss._tag_capture(capture_tags, 1, tags, u'note'))):
            # throwWarning:tr("não utilizar ''{0}'' para locais sem número",tag("addr:housenumber"))
            # suggestAlternative:"note"
            err.append({'class': 9018043, 'subclass': 1717284811, 'text': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', capture_tags, mapcss.tag(tags, u'addr:housenumber'))})

        # *[source=~/(?i)google/]
        if (u'source' in keys) and \
            ((mapcss.regexp_test_(self.re_2e8e4f2b, mapcss._tag_capture(capture_tags, 0, tags, u'source')))):
            # throwError:tr("objeto contém Google como source")
            err.append({'class': 9018044, 'subclass': 1313403884, 'text': mapcss.tr(u'objeto contém Google como source', capture_tags)})

        # *[amenity=townhall][name=~/^(?i)(?u)c(â|a)mara\b/]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'townhall' and mapcss.regexp_test_(self.re_46ab4d8d, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("câmara de vereadores mapeada incorretamente")
            # suggestAlternative:"office=government + government=legislative"
            err.append({'class': 9018002, 'subclass': 129695507, 'text': mapcss.tr(u'câmara de vereadores mapeada incorretamente', capture_tags)})

        # *[office=government][government!=legislative][name=~/^(?i)(?u)c(â|a)mara\b/]
        if (u'office' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'office') == u'government' and mapcss._tag_capture(capture_tags, 1, tags, u'government') != u'legislative' and mapcss.regexp_test_(self.re_46ab4d8d, mapcss._tag_capture(capture_tags, 2, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("ausência de government=legislative")
            err.append({'class': 9018002, 'subclass': 869412796, 'text': mapcss.tr(u'ausência de government=legislative', capture_tags)})

        # *[amenity=townhall][name=~/^(?i)(?u)c((â|a)me|ama)ra\b/]
        # *[office=government][name=~/^(?i)(?u)c((â|a)me|ama)ra\b/]
        if (u'amenity' in keys or u'office' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'townhall' and mapcss.regexp_test_(self.re_793b22ec, mapcss._tag_capture(capture_tags, 1, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'office') == u'government' and mapcss.regexp_test_(self.re_793b22ec, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("erro de ortografia em ''câmara''")
            err.append({'class': 9018002, 'subclass': 212328084, 'text': mapcss.tr(u'erro de ortografia em \'\'câmara\'\'', capture_tags)})

        # *[amenity=charging_station]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'charging_station')):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("possivelmente deve ser amenity=fuel")
            err.append({'class': 9018002, 'subclass': 128902291, 'text': mapcss.tr(u'possivelmente deve ser amenity=fuel', capture_tags)})

        # *[name=~/(?i)^Borrach(aria|eiro)/][shop=tyres][!repair]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_126ba9a9, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'shop') == u'tyres' and not mapcss._tag_capture(capture_tags, 2, tags, u'repair'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("borracharia sem ''repair=yes''")
            # suggestAlternative:"repair=yes"
            err.append({'class': 9018002, 'subclass': 817061630, 'text': mapcss.tr(u'borracharia sem \'\'repair=yes\'\'', capture_tags)})

        # *[name=~/(?i)^Borrach(aria|eiro)/][shop!=tyres]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_126ba9a9, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'shop') != u'tyres')):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("borracharia sem ''shop=tyres''")
            # suggestAlternative:"shop=tyres"
            err.append({'class': 9018002, 'subclass': 1324999258, 'text': mapcss.tr(u'borracharia sem \'\'shop=tyres\'\'', capture_tags)})

        return err

    def way(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # way[name=*ref][highway]
        if (u'name' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'ref') and mapcss._tag_capture(capture_tags, 1, tags, u'highway'))):
            # throwWarning:tr("{0} e {1} são iguais; adicionar nome completo da rodovia","{0.key}","{0.value}")
            err.append({'class': 9018050, 'subclass': 969441033, 'text': mapcss.tr(u'{0} e {1} são iguais; adicionar nome completo da rodovia', capture_tags, u'{0.key}', u'{0.value}')})

        # way[highway][name=~/\b[A-Z]{2,4} (- )?[0-9]{2,3}\b/]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test_(self.re_568a42f4, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # throwWarning:tr("rodovia com ref no nome")
            err.append({'class': 9018045, 'subclass': 63246253, 'text': mapcss.tr(u'rodovia com ref no nome', capture_tags)})

        # way[highway=cycleway][name][name!~/^(?i)ciclovia .*/]
        # way[highway][highway!~/bridleway|bus_stop|cycleway|crossing|footway|give_way|motorway_junction|path|raceway|rest_area|services|speed_camera|steps|stop/][name][name!~/^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodoanel|Rodovia|Rotatória|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*/]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'cycleway' and mapcss._tag_capture(capture_tags, 1, tags, u'name') and not mapcss.regexp_test_(self.re_2fcb6bab, mapcss._tag_capture(capture_tags, 2, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'highway') and not mapcss.regexp_test_(self.re_1054eb5a, mapcss._tag_capture(capture_tags, 1, tags, u'highway')) and mapcss._tag_capture(capture_tags, 2, tags, u'name') and not mapcss.regexp_test_(self.re_57eb9fe5, mapcss._tag_capture(capture_tags, 3, tags, u'name')))):
            # throwWarning:tr("{0} com logradouro ausente, errado ou abreviado","{0.key}")
            err.append({'class': 9018001, 'subclass': 1231643071, 'text': mapcss.tr(u'{0} com logradouro ausente, errado ou abreviado', capture_tags, u'{0.key}')})

        # *["addr:street"]["addr:street"!~/^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodovia|Rotatória|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*/]
        if (u'addr:street' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'addr:street') and not mapcss.regexp_test_(self.re_3b777b9d, mapcss._tag_capture(capture_tags, 1, tags, u'addr:street')))):
            # throwWarning:tr("{0} com logradouro ausente, errado ou abreviado","{0.key}")
            err.append({'class': 9018001, 'subclass': 588331445, 'text': mapcss.tr(u'{0} com logradouro ausente, errado ou abreviado', capture_tags, u'{0.key}')})

        # *[!highway][route!=road][!public_transport][type!~/route|street/][name][name=~/^(?i)(?u)(alameda|avenida|beco|estrada|ladeira|passarela|rodovia|rotatória|rua|travessa|trevo|viela|(anel|complexo|dispositivo) viário) .*/][name!~/^(?i)estrada de ferro/]
        if (u'name' in keys) and \
            ((not mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'route') != u'road' and not mapcss._tag_capture(capture_tags, 2, tags, u'public_transport') and not mapcss.regexp_test_(self.re_72d45155, mapcss._tag_capture(capture_tags, 3, tags, u'type')) and mapcss._tag_capture(capture_tags, 4, tags, u'name') and mapcss.regexp_test_(self.re_5849be19, mapcss._tag_capture(capture_tags, 5, tags, u'name')) and not mapcss.regexp_test_(self.re_15690541, mapcss._tag_capture(capture_tags, 6, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("objeto com nome de via mas sem tag de {0}","{0.key}")
            err.append({'class': 9018002, 'subclass': 874993957, 'text': mapcss.tr(u'objeto com nome de via mas sem tag de {0}', capture_tags, u'{0.key}')})

        # way[highway=track][name][name=~/^(?i)(?u)(alameda|avenida|beco|estrada|ladeira|rodovia|rotatória|rua|travessa|trevo|viela) .*/]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'track' and mapcss._tag_capture(capture_tags, 1, tags, u'name') and mapcss.regexp_test_(self.re_20cf30ba, mapcss._tag_capture(capture_tags, 2, tags, u'name')))):
            # throwWarning:tr("não classificar via como {0}","{0.tag}")
            # suggestAlternative:"highway=residential"
            # suggestAlternative:"highway=unclassified"
            err.append({'class': 9018051, 'subclass': 450185002, 'text': mapcss.tr(u'não classificar via como {0}', capture_tags, u'{0.tag}')})

        # *[name=~/^(?i)(?u)[a-z0-9]+_([a-z0-9]_?)+$/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_4bd3b925, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("utilizar espaço ao invés de underscore")
            err.append({'class': 9018002, 'subclass': 378801374, 'text': mapcss.tr(u'utilizar espaço ao invés de underscore', capture_tags)})

        # *[name=~/(?i)(^|.* )(Cel|Cmte|Cond|Conj|Dª|Dr|Eng|Gov|Hab|Jd|Jr|Marg|Mun|p\/|Pde|Pe|Pq|Pst|Pref|Profa|Profª|Prof|Res|s\/|Sr(a|ª)?|Sta|Sto|Ver)\.? .*/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_178f5446, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # throwWarning:tr("palavra abreviada em {0}","{0.key}")
            err.append({'class': 9018003, 'subclass': 1784756763, 'text': mapcss.tr(u'palavra abreviada em {0}', capture_tags, u'{0.key}')})

        # way[highway][name=~/^(?i)(?u)((via de )?(acesso|ligação)(( (a|à))? propriedade)?|entrada|entroncamento|rampa|retorno|rotat(ó|o)ria|r(ó|o)tula|sa(í|i)da|trevo|estrada( municipal| de terra)?|rua|rodovia|via)( (de acesso|sem nome|projetad(a|o)))?$/]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test_(self.re_667ce569, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # throwWarning:tr("{0} com nome supérfluo/incompleto","{0.key}")
            # suggestAlternative:"description"
            # suggestAlternative:"destination"
            err.append({'class': 9018052, 'subclass': 729248989, 'text': mapcss.tr(u'{0} com nome supérfluo/incompleto', capture_tags, u'{0.key}')})

        # *[leisure][name=~/^(?i)(?u)(campo|est(á|a)dio|gin(á|a)sio|quadra)( de (futebol|esportes?))?$/]
        if (u'leisure' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'leisure') and mapcss.regexp_test_(self.re_7f53e992, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # throwWarning:tr("nome supérfluo/incompleto de local de lazer")
            err.append({'class': 9018004, 'subclass': 790401825, 'text': mapcss.tr(u'nome supérfluo/incompleto de local de lazer', capture_tags)})

        # *[name=~/^(?i)(?u)((Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF|hospital)$/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_52ab3b8b, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # throwWarning:tr("nome supérfluo/incompleto de local de saúde")
            err.append({'class': 9018005, 'subclass': 1792576894, 'text': mapcss.tr(u'nome supérfluo/incompleto de local de saúde', capture_tags)})

        # *[amenity=~/^(clinic|doctors|hospital)$/][name=~/(?i)\bsaude\b/]
        if (u'amenity' in keys) and \
            ((mapcss.regexp_test_(self.re_5ab76b11, mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test_(self.re_4cf86823, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("erro de ortografia em ''saúde''")
            err.append({'class': 9018002, 'subclass': 1455303428, 'text': mapcss.tr(u'erro de ortografia em \'\'saúde\'\'', capture_tags)})

        # *[place=farm][name^="Sitio "]
        if (u'place' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'farm' and mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, u'name'), u'Sitio '))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("faltando acento em ''Sítio''")
            err.append({'class': 9018002, 'subclass': 962677162, 'text': mapcss.tr(u'faltando acento em \'\'Sítio\'\'', capture_tags)})

        # *[name=~/^(?i)(?u)(aldeia|borrach(aria|eiro)|bosque|capela|cemit(é|e)rio|c(ó|o)rrego|escola|estacionamento|fazenda|floresta|hospital|igreja|lago|lagoa|mata( nativa)?|praça|parque|parquinho|posto( de gasolina)?|riacho|rio|rodovi(á|a)ria|vila)$/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_20c7dd98, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("local com nome supérfluo, incompleto ou descritivo")
            err.append({'class': 9018002, 'subclass': 501162763, 'text': mapcss.tr(u'local com nome supérfluo, incompleto ou descritivo', capture_tags)})

        # *[amenity=parking][name=~/(?i)^Estacionamento /]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'parking' and mapcss.regexp_test_(self.re_407995b9, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("possível nome descritivo do estacionamento")
            # suggestAlternative:"operator"
            err.append({'class': 9018002, 'subclass': 698950828, 'text': mapcss.tr(u'possível nome descritivo do estacionamento', capture_tags)})

        # way[highway][type=route]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'type') == u'route')):
            # throwWarning:tr("{0} não deve possuir {1}","{0.key}","{1.tag}")
            err.append({'class': 9018053, 'subclass': 1357959449, 'text': mapcss.tr(u'{0} não deve possuir {1}', capture_tags, u'{0.key}', u'{1.tag}')})

        # way[highway][highway!~/bus_stop|milestone|motorway_junction|traffic_signals/][ref][ref!~/^(([A-Z]{2,3}-[0-9]{2,4}|SPM(-| )[0-9]{3} ?(D|E)?|SP(A|D|I)(-| )[0-9]{3}\/[0-9]{3}|[A-Z]{3}-[0-9]{3}\/[0-9]{3});?)+$/]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') and not mapcss.regexp_test_(self.re_0575cb27, mapcss._tag_capture(capture_tags, 1, tags, u'highway')) and mapcss._tag_capture(capture_tags, 2, tags, u'ref') and not mapcss.regexp_test_(self.re_3e2e3488, mapcss._tag_capture(capture_tags, 3, tags, u'ref')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} fora do padrão ''sigla-numeração'' ou separador de múltiplos valores diferente de '';''","{2.key}")
            err.append({'class': 9018002, 'subclass': 1532674501, 'text': mapcss.tr(u'{0} fora do padrão \'\'sigla-numeração\'\' ou separador de múltiplos valores diferente de \'\';\'\'', capture_tags, u'{2.key}')})

        # way[highway][!ref][name=~/.*([A-Z]{2,3}-[0-9]{2,4}|SPM(-| )[0-9]{3} ?(D|E)?|SP(A|D|I)(-| )[0-9]{3}\/[0-9]{3}|[A-Z]{3}-[0-9]{3}\/[0-9]{3}).*/]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') and not mapcss._tag_capture(capture_tags, 1, tags, u'ref') and mapcss.regexp_test_(self.re_375e3de4, mapcss._tag_capture(capture_tags, 2, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("utilizar o código/sigla da rodovia também na tag {0}","{1.key}")
            err.append({'class': 9018002, 'subclass': 1854606955, 'text': mapcss.tr(u'utilizar o código/sigla da rodovia também na tag {0}', capture_tags, u'{1.key}')})

        # way[highway][name=~/Rodovia ([A-Z]{2,3}-[0-9]{2,4})/]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test_(self.re_7633bf4e, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("nome incorreto de rodovia; utilizar o nome oficial ou apenas ref")
            err.append({'class': 9018002, 'subclass': 955724850, 'text': mapcss.tr(u'nome incorreto de rodovia; utilizar o nome oficial ou apenas ref', capture_tags)})

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
        if (u'designation' in keys or u'name' in keys or u'ref' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'addr:street') and mapcss._tag_capture(capture_tags, 1, tags, u'highway')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'designation') == mapcss.tag(tags, u'addr:housename')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'ref') == mapcss.tag(tags, u'designation')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'ref') == mapcss.tag(tags, u'old_ref')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'addr:housename')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'designation')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'alt_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'int_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'loc_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'nat_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'official_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'old_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'reg_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'short_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'sorting_name'))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("{0} e {1} são iguais; remover chave {1} desnecessária","{0.key}","{0.value}")
            # fixRemove:"{0.value}"
            err.append({'class': 9018006, 'subclass': 557015301, 'text': mapcss.tr(u'{0} e {1} são iguais; remover chave {1} desnecessária', capture_tags, u'{0.key}', u'{0.value}'), 'fix': {
                '-': ([
                    u'{0.value}'])
            }})

        # *[source=*name]
        if (u'source' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'source') == mapcss.tag(tags, u'name'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} e {1} são iguais","{0.key}","{0.value}")
            err.append({'class': 9018002, 'subclass': 1403015964, 'text': mapcss.tr(u'{0} e {1} são iguais', capture_tags, u'{0.key}', u'{0.value}')})

        # *[name=~/(?i)(?u)((sem (denomina(ç|c)(ã|a)o|nome|sa(i|í)da))|desconhecido|n(ã|a)o conhecido)/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_65710fdb, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # throwWarning:tr("objeto com nomenclatura incorreta")
            # suggestAlternative:"noname"
            err.append({'class': 9018007, 'subclass': 506924923, 'text': mapcss.tr(u'objeto com nomenclatura incorreta', capture_tags)})

        # *[designation]
        if (u'designation' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'designation'))):
            # throwWarning:tr("{0} é uma chave utilizada apenas no Reino Unido","{0.key}")
            # suggestAlternative:"description"
            # suggestAlternative:"name"
            err.append({'class': 9018009, 'subclass': 1259259930, 'text': mapcss.tr(u'{0} é uma chave utilizada apenas no Reino Unido', capture_tags, u'{0.key}')})

        # way[highway=~/^(trunk|motorway)$/][!operator]
        if (u'highway' in keys) and \
            ((mapcss.regexp_test_(self.re_1319292c, mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and not mapcss._tag_capture(capture_tags, 1, tags, u'operator'))):
            # throwWarning:tr("ausência de \"{0}\" na {1}","{1.key}","{0.key}")
            err.append({'class': 9018054, 'subclass': 1063481013, 'text': mapcss.tr(u'ausência de "{0}" na {1}', capture_tags, u'{1.key}', u'{0.key}')})

        # way[highway$=_link][name=~/(Alameda|Avenida|Rua|Travessa|Viela) .*/]
        if (u'highway' in keys) and \
            ((mapcss.endswith(mapcss._tag_capture(capture_tags, 0, tags, u'highway'), u'_link') and mapcss.regexp_test_(self.re_6b6e390d, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} classificado incorretamente",tag("highway"))
            err.append({'class': 9018002, 'subclass': 176141455, 'text': mapcss.tr(u'{0} classificado incorretamente', capture_tags, mapcss.tag(tags, u'highway'))})

        # way[highway][name=~/(Alameda|Avenida|Rua|Travessa|Viela) .*/][ref]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test_(self.re_6b6e390d, mapcss._tag_capture(capture_tags, 1, tags, u'name')) and mapcss._tag_capture(capture_tags, 2, tags, u'ref'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("possível uso desnecessário/errado de ref em {0}={1}","{0.key}",tag("highway"))
            err.append({'class': 9018002, 'subclass': 1325624158, 'text': mapcss.tr(u'possível uso desnecessário/errado de ref em {0}={1}', capture_tags, u'{0.key}', mapcss.tag(tags, u'highway'))})

        # way[highway$=_link][!destination]
        if (u'highway' in keys) and \
            ((mapcss.endswith(mapcss._tag_capture(capture_tags, 0, tags, u'highway'), u'_link') and not mapcss._tag_capture(capture_tags, 1, tags, u'destination'))):
            # throwOther:tr("link sem tag {0}","{1.key}")
            err.append({'class': 9018055, 'subclass': 926804996, 'text': mapcss.tr(u'link sem tag {0}', capture_tags, u'{1.key}')})

        # *[place=~/hamlet|isolated_dwelling|town|village/][population>=100000]
        if (u'place' in keys) and \
            ((mapcss.regexp_test_(self.re_152c10ee, mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'population') >= 100000)):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("local com 100.000 habitantes ou mais deve ser classificado como city")
            # fixAdd:"place=city"
            err.append({'class': 9018006, 'subclass': 149235075, 'text': mapcss.tr(u'local com 100.000 habitantes ou mais deve ser classificado como city', capture_tags), 'fix': {
                '+': dict([
                    [u'place',u'city']])
            }})

        # *[place=~/city|hamlet|isolated_dwelling|village/][population>=10000][population<100000]
        if (u'place' in keys) and \
            ((mapcss.regexp_test_(self.re_591572a5, mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'population') >= 10000 and mapcss._tag_capture(capture_tags, 2, tags, u'population') < 100000)):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("local com população entre 10.000 e 100.000 deve ser classificado como town")
            # fixAdd:"place=town"
            err.append({'class': 9018006, 'subclass': 1174321645, 'text': mapcss.tr(u'local com população entre 10.000 e 100.000 deve ser classificado como town', capture_tags), 'fix': {
                '+': dict([
                    [u'place',u'town']])
            }})

        # *[place][place!~/hamlet|island|isolated_dwelling|neighbourhood|suburb|village/][population<10000]
        if (u'place' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'place') and not mapcss.regexp_test_(self.re_3aeda39d, mapcss._tag_capture(capture_tags, 1, tags, u'place')) and mapcss._tag_capture(capture_tags, 2, tags, u'population') < 10000)):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("local com menos de 10.000 habitantes deve ser classificado como village")
            # fixAdd:"place=village"
            err.append({'class': 9018006, 'subclass': 719699918, 'text': mapcss.tr(u'local com menos de 10.000 habitantes deve ser classificado como village', capture_tags), 'fix': {
                '+': dict([
                    [u'place',u'village']])
            }})

        # *[place=city][!population]
        # *[place=town][!population]
        # *[place=village][!population]
        if (u'place' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'city' and not mapcss._tag_capture(capture_tags, 1, tags, u'population')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'town' and not mapcss._tag_capture(capture_tags, 1, tags, u'population')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'village' and not mapcss._tag_capture(capture_tags, 1, tags, u'population'))):
            # throwWarning:tr("{0} sem tag de população (population)","{0.value}")
            err.append({'class': 9018011, 'subclass': 1582438505, 'text': mapcss.tr(u'{0} sem tag de população (population)', capture_tags, u'{0.value}')})

        # *[place=city][!name]
        # *[place=town][!name]
        # *[place=village][!name]
        if (u'place' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'city' and not mapcss._tag_capture(capture_tags, 1, tags, u'name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'town' and not mapcss._tag_capture(capture_tags, 1, tags, u'name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'village' and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))):
            # throwWarning:tr("{0} sem nome","{0.value}")
            err.append({'class': 9018012, 'subclass': 828568305, 'text': mapcss.tr(u'{0} sem nome', capture_tags, u'{0.value}')})

        # *["addr:city"=~/(,|( |-) ?[A-Z]{2})/]
        if (u'addr:city' in keys) and \
            ((mapcss.regexp_test_(self.re_10f1c360, mapcss._tag_capture(capture_tags, 0, tags, u'addr:city')))):
            # throwWarning:tr("{0} deve conter apenas o nome da cidade","{0.key}")
            err.append({'class': 9018013, 'subclass': 223700239, 'text': mapcss.tr(u'{0} deve conter apenas o nome da cidade', capture_tags, u'{0.key}')})

        # *[name=~/^(?i)(?u)(Faz\.|Fazenda|Sítio|Chácara)/][place][place!~/city|farm|neighbourhood|suburb|town|village/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_2cd1e949, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'place') and not mapcss.regexp_test_(self.re_5d3348cb, mapcss._tag_capture(capture_tags, 2, tags, u'place')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("objeto talvez deva ser {0}=farm","{1.key}")
            err.append({'class': 9018002, 'subclass': 414255329, 'text': mapcss.tr(u'objeto talvez deva ser {0}=farm', capture_tags, u'{1.key}')})

        # *[place][name=~/^(?i)Bairro\b/][name!~/^(?i)Bairro d(a|e|o)s?\b/]
        if (u'place' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'place') and mapcss.regexp_test_(self.re_20fc5143, mapcss._tag_capture(capture_tags, 1, tags, u'name')) and not mapcss.regexp_test_(self.re_64387998, mapcss._tag_capture(capture_tags, 2, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("objeto talvez não deva ter ''Bairro'' no nome")
            err.append({'class': 9018002, 'subclass': 457937105, 'text': mapcss.tr(u'objeto talvez não deva ter \'\'Bairro\'\' no nome', capture_tags)})

        # *[iata="0"]
        if (u'iata' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'iata') == u'0')):
            # throwWarning:tr("{0} com valor = {1}","{0.key}","{0.value}")
            err.append({'class': 9018014, 'subclass': 1389202412, 'text': mapcss.tr(u'{0} com valor = {1}', capture_tags, u'{0.key}', u'{0.value}')})

        # *[amenity=~/college|school/][name=~/^(?i)(?u)(Centro Universitário|Faculdades?|FATEC|Instituto Federal)\b/]
        if (u'amenity' in keys) and \
            ((mapcss.regexp_test_(self.re_362f879f, mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test_(self.re_1d232d4c, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("estabelecimento de ensino classificado incorretamente")
            # suggestAlternative:"amenity=university"
            # fixAdd:"{0.key}=university"
            err.append({'class': 9018006, 'subclass': 221523813, 'text': mapcss.tr(u'estabelecimento de ensino classificado incorretamente', capture_tags), 'fix': {
                '+': dict([
                    [u'{0.key}',u'university']])
            }})

        # *[amenity=school][name=~/^(?i)(?u)(SENAC|SENAI|Serviço Nacional de Aprendizagem)/]
        # *[amenity=~/school|university/][name=~/(?i)(?u)\b(Centro Paula Souza|Escola Técnica|ETEC)\b/]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'school' and mapcss.regexp_test_(self.re_044c8944, mapcss._tag_capture(capture_tags, 1, tags, u'name'))) or \
            (mapcss.regexp_test_(self.re_6c0d6e9e, mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test_(self.re_3b304b9b, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("estabelecimento de ensino classificado incorretamente")
            # suggestAlternative:"amenity=college"
            # fixAdd:"{0.key}=college"
            err.append({'class': 9018006, 'subclass': 897019825, 'text': mapcss.tr(u'estabelecimento de ensino classificado incorretamente', capture_tags), 'fix': {
                '+': dict([
                    [u'{0.key}',u'college']])
            }})

        # *[amenity=school][name=~/^(?i)(?u)(auto(-| )?( moto )?escola|centro de formação de condutores|cfc|moto escola)\b/]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'school' and mapcss.regexp_test_(self.re_35bb0f2f, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("autoescola classificada incorretamente")
            # suggestAlternative:"amenity=driving_school"
            # fixAdd:"{0.key}=driving_school"
            err.append({'class': 9018006, 'subclass': 1796023580, 'text': mapcss.tr(u'autoescola classificada incorretamente', capture_tags), 'fix': {
                '+': dict([
                    [u'{0.key}',u'driving_school']])
            }})

        # *[amenity=school][name=~/^(?i)creche\b/]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'school' and mapcss.regexp_test_(self.re_160d1bfc, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("creche classificada incorretamente")
            # suggestAlternative:"amenity=kindergarten"
            # fixAdd:"{0.key}=kindergarten"
            err.append({'class': 9018006, 'subclass': 121701344, 'text': mapcss.tr(u'creche classificada incorretamente', capture_tags), 'fix': {
                '+': dict([
                    [u'{0.key}',u'kindergarten']])
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
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_69d0dc1a, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'power') and mapcss._tag_capture(capture_tags, 2, tags, u'power') != u'substation') or \
            (mapcss.regexp_test_(self.re_002de70b, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') != u'courthouse') or \
            (mapcss.regexp_test_(self.re_25871691, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'hospital') or \
            (mapcss.regexp_test_(self.re_6e928d7b, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'university') or \
            (mapcss.regexp_test_(self.re_57a9f888, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'school') or \
            (mapcss.regexp_test_(self.re_458e02d8, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'hotel') or \
            (mapcss.regexp_test_(self.re_105662b4, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'chapel') or \
            (mapcss.regexp_test_(self.re_752011f2, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'church') or \
            (mapcss.regexp_test_(self.re_1e8e69a3, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'cathedral') or \
            (mapcss.regexp_test_(self.re_381002af, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'farm') or \
            (mapcss.regexp_test_(self.re_486d02c4, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'supermarket')):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("{0} provavelmente deveria ser {1}","{2.key}","{2.value}")
            # fixAdd:"{2.key}={2.value}"
            err.append({'class': 9018006, 'subclass': 1930177472, 'text': mapcss.tr(u'{0} provavelmente deveria ser {1}', capture_tags, u'{2.key}', u'{2.value}'), 'fix': {
                '+': dict([
                    [u'{2.key}',u'{2.value}']])
            }})

        # *[name=~/^(?i)(?u)(AM(A|E)|(Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF).*/][amenity=hospital]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_7b7c453d, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') == u'hospital')):
            # throwWarning:tr("postos/unidades de saúde devem ser amenity=clinic")
            err.append({'class': 9018015, 'subclass': 2108543140, 'text': mapcss.tr(u'postos/unidades de saúde devem ser amenity=clinic', capture_tags)})

        # *[name=~/^(?i)\bSAMU\b/][amenity=~/clinic|doctors|hospital/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_2dbaea13, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.regexp_test_(self.re_3eb0ab44, mapcss._tag_capture(capture_tags, 1, tags, u'amenity')))):
            # throwWarning:tr("SAMU classificado de forma errada")
            # suggestAlternative:"emergency=ambulance_station"
            err.append({'class': 9018016, 'subclass': 2090365947, 'text': mapcss.tr(u'SAMU classificado de forma errada', capture_tags)})

        # way[highway=give_way]
        # way[highway=mini_roundabout]
        # way[highway=stop]
        # way[highway=turning_circle]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'give_way') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'mini_roundabout') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'stop') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'turning_circle')):
            # throwWarning:tr("{0} deve ser utilizado apenas em nós","{0.tag}")
            err.append({'class': 9018047, 'subclass': 2084016255, 'text': mapcss.tr(u'{0} deve ser utilizado apenas em nós', capture_tags, u'{0.tag}')})

        # *[crossing][!highway][!railway]
        if (u'crossing' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'crossing') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway'))):
            # throwWarning:tr("{0} deve ser utilizado com {1}={0} ou {2}={0}","{0.key}","{1.key}","{2.key}")
            err.append({'class': 9018019, 'subclass': 139983185, 'text': mapcss.tr(u'{0} deve ser utilizado com {1}={0} ou {2}={0}', capture_tags, u'{0.key}', u'{1.key}', u'{2.key}')})

        # *[aeroway][designation=~/^[A-Z]{4}$/][!icao]
        # *[aeroway][ref=~/^[A-Z]{4}$/][!icao]
        if (u'aeroway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') and mapcss.regexp_test_(self.re_7afc6883, mapcss._tag_capture(capture_tags, 1, tags, u'designation')) and not mapcss._tag_capture(capture_tags, 2, tags, u'icao')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') and mapcss.regexp_test_(self.re_7afc6883, mapcss._tag_capture(capture_tags, 1, tags, u'ref')) and not mapcss._tag_capture(capture_tags, 2, tags, u'icao'))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("{0} provavelmente deve ser utilizado como {1}","{1.key}","{2.key}")
            # fixChangeKey:"{1.key} => {2.key}"
            err.append({'class': 9018006, 'subclass': 662001655, 'text': mapcss.tr(u'{0} provavelmente deve ser utilizado como {1}', capture_tags, u'{1.key}', u'{2.key}'), 'fix': {
                '+': dict([
                    [u'{2.key}', mapcss.tag(tags, u'{1.key}')]]),
                '-': ([
                    u'{1.key}'])
            }})

        # *[access=permissive]
        if (u'access' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'access') == u'permissive')):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} deve ser utilizado apenas em vias privadas com permissão de acesso e não em vias de acesso público","{0.tag}")
            err.append({'class': 9018002, 'subclass': 1918455197, 'text': mapcss.tr(u'{0} deve ser utilizado apenas em vias privadas com permissão de acesso e não em vias de acesso público', capture_tags, u'{0.tag}')})

        # *[name=~/^(?U)(\p{Upper}| )+$/]
        # *["addr:street"=~/^(?U)(\p{Upper}| )+$/]
        if (u'addr:street' in keys or u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_73b50a21, mapcss._tag_capture(capture_tags, 0, tags, u'name'))) or \
            (mapcss.regexp_test_(self.re_73b50a21, mapcss._tag_capture(capture_tags, 0, tags, u'addr:street')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} totalmente em maiúsculo; usar nome completo ou short_name se for sigla","{0.key}")
            err.append({'class': 9018002, 'subclass': 386880794, 'text': mapcss.tr(u'{0} totalmente em maiúsculo; usar nome completo ou short_name se for sigla', capture_tags, u'{0.key}')})

        # *["addr:postcode"=~/^[0-9]{8}$/]
        if (u'addr:postcode' in keys) and \
            ((mapcss.regexp_test_(self.re_2dbf771a, mapcss._tag_capture(capture_tags, 0, tags, u'addr:postcode')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("formato do CEP pode ser melhorado")
            # fixAdd:concat("addr:postcode=",substring(tag("addr:postcode"),0,5),"-",substring(tag("addr:postcode"),5,8))
            err.append({'class': 9018006, 'subclass': 523931624, 'text': mapcss.tr(u'formato do CEP pode ser melhorado', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'addr:postcode=', mapcss.substring(mapcss.tag(tags, u'addr:postcode'), 0, 5), u'-', mapcss.substring(mapcss.tag(tags, u'addr:postcode'), 5, 8))).split('=', 1)])
            }})

        # *[postal_code=~/^[0-9]{8}$/]
        if (u'postal_code' in keys) and \
            ((mapcss.regexp_test_(self.re_2dbf771a, mapcss._tag_capture(capture_tags, 0, tags, u'postal_code')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("formato do CEP pode ser melhorado")
            # fixAdd:concat("postal_code=",substring(tag("postal_code"),0,5),"-",substring(tag("postal_code"),5,8))
            err.append({'class': 9018006, 'subclass': 1234269468, 'text': mapcss.tr(u'formato do CEP pode ser melhorado', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'postal_code=', mapcss.substring(mapcss.tag(tags, u'postal_code'), 0, 5), u'-', mapcss.substring(mapcss.tag(tags, u'postal_code'), 5, 8))).split('=', 1)])
            }})

        # *["addr:postcode"=~/^[0-9]{5}( |\.)[0-9]{3}$/]
        if (u'addr:postcode' in keys) and \
            ((mapcss.regexp_test_(self.re_57bee688, mapcss._tag_capture(capture_tags, 0, tags, u'addr:postcode')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("formato do CEP pode ser melhorado")
            # fixAdd:concat("addr:postcode=",replace(replace(tag("addr:postcode")," ","-"),".","-"))
            err.append({'class': 9018006, 'subclass': 308348773, 'text': mapcss.tr(u'formato do CEP pode ser melhorado', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'addr:postcode=', mapcss.replace(mapcss.replace(mapcss.tag(tags, u'addr:postcode'), u' ', u'-'), u'.', u'-'))).split('=', 1)])
            }})

        # *["postal_code"=~/^[0-9]{5}( |\.)[0-9]{3}$/]
        if (u'postal_code' in keys) and \
            ((mapcss.regexp_test_(self.re_57bee688, mapcss._tag_capture(capture_tags, 0, tags, u'postal_code')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("formato do CEP pode ser melhorado")
            # fixAdd:concat("postal_code=",replace(replace(tag("postal_code")," ","-"),".","-"))
            err.append({'class': 9018006, 'subclass': 1211220107, 'text': mapcss.tr(u'formato do CEP pode ser melhorado', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'postal_code=', mapcss.replace(mapcss.replace(mapcss.tag(tags, u'postal_code'), u' ', u'-'), u'.', u'-'))).split('=', 1)])
            }})

        # *["addr:postcode"]["addr:postcode"!~/^[0-9]{5}-[0-9]{3}$/]
        # *[postal_code][postal_code!~/^[0-9]{5}-[0-9]{3}$/]
        if (u'addr:postcode' in keys or u'postal_code' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'addr:postcode') and not mapcss.regexp_test_(self.re_1ffe94a9, mapcss._tag_capture(capture_tags, 1, tags, u'addr:postcode'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'postal_code') and not mapcss.regexp_test_(self.re_1ffe94a9, mapcss._tag_capture(capture_tags, 1, tags, u'postal_code')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} (CEP) em formato diferente de NNNNN-NNN","{0.key}")
            err.append({'class': 9018002, 'subclass': 1843994632, 'text': mapcss.tr(u'{0} (CEP) em formato diferente de NNNNN-NNN', capture_tags, u'{0.key}')})

        # way[highway]["addr:postcode"][highway!=services]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'addr:postcode') and mapcss._tag_capture(capture_tags, 2, tags, u'highway') != u'services')):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("uso incorreto de {0}","{1.key}","{0.key}")
            # suggestAlternative:"postal_code"
            # fixChangeKey:"{1.key} => postal_code"
            err.append({'class': 9018006, 'subclass': 1893232368, 'text': mapcss.tr(u'uso incorreto de {0}', capture_tags, u'{1.key}', u'{0.key}'), 'fix': {
                '+': dict([
                    [u'postal_code', mapcss.tag(tags, u'{1.key}')]]),
                '-': ([
                    u'{1.key}'])
            }})

        # *[alt_source][source]
        if (u'alt_source' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'alt_source') and mapcss._tag_capture(capture_tags, 1, tags, u'source'))):
            # throwWarning:tr("{0} deve estar incluído em {1}, separado por '';'' caso necessário","{0.key}","{1.key}")
            err.append({'class': 9018020, 'subclass': 512568644, 'text': mapcss.tr(u'{0} deve estar incluído em {1}, separado por \'\';\'\' caso necessário', capture_tags, u'{0.key}', u'{1.key}')})

        # *[landuse?]
        if (u'landuse' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'landuse') in ('yes', 'true', '1'))):
            # throwWarning:tr("especificar valor correto para {0} ao invés de ''{1}''","{0.key}",tag("landuse"))
            err.append({'class': 9018021, 'subclass': 2004192493, 'text': mapcss.tr(u'especificar valor correto para {0} ao invés de \'\'{1}\'\'', capture_tags, u'{0.key}', mapcss.tag(tags, u'landuse'))})

        # *[long_name]
        if (u'long_name' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'long_name'))):
            # throwWarning:tr("chave inválida: {0}","{0.key}")
            # suggestAlternative:"alt_name"
            # suggestAlternative:"name"
            # suggestAlternative:"official_name"
            err.append({'class': 9018022, 'subclass': 1648910015, 'text': mapcss.tr(u'chave inválida: {0}', capture_tags, u'{0.key}')})

        # *["building:levels"<1]
        if (u'building:levels' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'building:levels') < 1)):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com valor inválido","{0.key}")
            err.append({'class': 9018002, 'subclass': 154478605, 'text': mapcss.tr(u'{0} com valor inválido', capture_tags, u'{0.key}')})

        # *[hires?]
        if (u'hires' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'hires') in ('yes', 'true', '1'))):
            # throwWarning:tr("não se deve utilizar {0} para demarcar áreas de cobertura de imagem","{0.key}")
            err.append({'class': 9018023, 'subclass': 1394305840, 'text': mapcss.tr(u'não se deve utilizar {0} para demarcar áreas de cobertura de imagem', capture_tags, u'{0.key}')})

        # *[tourism=motel][amenity!=love_hotel]
        # *[name=~/(?i)\bmotel\b/][amenity!=love_hotel]
        if (u'name' in keys or u'tourism' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == u'motel' and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != u'love_hotel') or \
            (mapcss.regexp_test_(self.re_01454d46, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != u'love_hotel')):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("ausência de tag ''{0}''","{1.value}")
            # fixAdd:"{1.key}={1.value}"
            err.append({'class': 9018006, 'subclass': 444111908, 'text': mapcss.tr(u'ausência de tag \'\'{0}\'\'', capture_tags, u'{1.value}'), 'fix': {
                '+': dict([
                    [u'{1.key}',u'{1.value}']])
            }})

        # *[amenity=love_hotel][tourism][tourism!=motel]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'love_hotel' and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') and mapcss._tag_capture(capture_tags, 2, tags, u'tourism') != u'motel')):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("provavelmente deve ser ''{0}={1}''","{2.key}","{2.value}")
            err.append({'class': 9018002, 'subclass': 2021262051, 'text': mapcss.tr(u'provavelmente deve ser \'\'{0}={1}\'\'', capture_tags, u'{2.key}', u'{2.value}')})

        # *[name=~/(?i)^motel\b/][tourism!=motel]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_5cd37790, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') != u'motel')):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("motel classificado incorretamente")
            # suggestAlternative:"tourism=motel"
            err.append({'class': 9018002, 'subclass': 2096064741, 'text': mapcss.tr(u'motel classificado incorretamente', capture_tags)})

        # *[aeroway=aerodrome][!icao]
        # *[aeroway=helipad][!icao]
        if (u'aeroway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'aerodrome' and not mapcss._tag_capture(capture_tags, 1, tags, u'icao')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'helipad' and not mapcss._tag_capture(capture_tags, 1, tags, u'icao'))):
            # throwOther:tr("{0} sem tag {1}","{0.value}","{1.key}")
            err.append({'class': 9018025, 'subclass': 1760501517, 'text': mapcss.tr(u'{0} sem tag {1}', capture_tags, u'{0.value}', u'{1.key}')})

        # *[aeroway=aerodrome][name=~/(?i).*airport$/]
        # *[aeroway=helipad][name=~/(?i).*heliport$/]
        if (u'aeroway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'aerodrome' and mapcss.regexp_test_(self.re_6efb8049, mapcss._tag_capture(capture_tags, 1, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'helipad' and mapcss.regexp_test_(self.re_6566db6a, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com nome em inglês","{0.tag}")
            err.append({'class': 9018002, 'subclass': 134725283, 'text': mapcss.tr(u'{0} com nome em inglês', capture_tags, u'{0.tag}')})

        # *[aeroway=aerodrome][name=~/(?i)^Aer(ódromo|oporto) de.*/]
        # *[aeroway=helipad][name=~/(?i)^Helipo(n|r)to.*/]
        if (u'aeroway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'aerodrome' and mapcss.regexp_test_(self.re_6024a566, mapcss._tag_capture(capture_tags, 1, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'helipad' and mapcss.regexp_test_(self.re_139e342b, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("conferir se existe nome oficial do {0}","{0.value}")
            err.append({'class': 9018002, 'subclass': 2002284471, 'text': mapcss.tr(u'conferir se existe nome oficial do {0}', capture_tags, u'{0.value}')})

        # *[aeroway=aerodrome][ref]
        if (u'aeroway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'aerodrome' and mapcss._tag_capture(capture_tags, 1, tags, u'ref'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("''{0}'' não faz sentido em aeroporto","{1.key}")
            err.append({'class': 9018002, 'subclass': 339634841, 'text': mapcss.tr(u'\'\'{0}\'\' não faz sentido em aeroporto', capture_tags, u'{1.key}')})

        # way[waterway][tunnel=yes]
        if (u'waterway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'tunnel') == u'yes')):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("uso incorreto de {0}","{1.tag}")
            # suggestAlternative:"tunnel=culvert"
            # fixAdd:"tunnel=culvert"
            err.append({'class': 9018006, 'subclass': 807344112, 'text': mapcss.tr(u'uso incorreto de {0}', capture_tags, u'{1.tag}'), 'fix': {
                '+': dict([
                    [u'tunnel',u'culvert']])
            }})

        # way[highway][layer<0][!tunnel]
        # *[waterway][layer<0][!tunnel]
        if (u'highway' in keys or u'waterway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'layer') < 0 and not mapcss._tag_capture(capture_tags, 2, tags, u'tunnel')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'layer') < 0 and not mapcss._tag_capture(capture_tags, 2, tags, u'tunnel'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} negativo de {1} com ausência de {2}","{1.key}","{0.key}","{2.key}")
            err.append({'class': 9018002, 'subclass': 112286739, 'text': mapcss.tr(u'{0} negativo de {1} com ausência de {2}', capture_tags, u'{1.key}', u'{0.key}', u'{2.key}')})

        # way[highway][layer>0][!bridge][highway!=bus_stop]
        # *[waterway][layer>0][!bridge]
        if (u'highway' in keys or u'waterway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'layer') > 0 and not mapcss._tag_capture(capture_tags, 2, tags, u'bridge') and mapcss._tag_capture(capture_tags, 3, tags, u'highway') != u'bus_stop') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'layer') > 0 and not mapcss._tag_capture(capture_tags, 2, tags, u'bridge'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} positivo de {1} com ausência de {2}","{1.key}","{0.key}","{2.key}")
            err.append({'class': 9018002, 'subclass': 1956052894, 'text': mapcss.tr(u'{0} positivo de {1} com ausência de {2}', capture_tags, u'{1.key}', u'{0.key}', u'{2.key}')})

        # *[layer][!building][!highway][man_made!=pipeline][!railway][!waterway]
        if (u'layer' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'layer') and not mapcss._tag_capture(capture_tags, 1, tags, u'building') and not mapcss._tag_capture(capture_tags, 2, tags, u'highway') and mapcss._tag_capture(capture_tags, 3, tags, u'man_made') != u'pipeline' and not mapcss._tag_capture(capture_tags, 4, tags, u'railway') and not mapcss._tag_capture(capture_tags, 5, tags, u'waterway'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("possível uso incorreto de {0} no objeto","{0.key}")
            err.append({'class': 9018002, 'subclass': 373443518, 'text': mapcss.tr(u'possível uso incorreto de {0} no objeto', capture_tags, u'{0.key}')})

        # way[highway=motorway_junction]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'motorway_junction')):
            # throwError:tr("{0} deve ser utilizado apenas no nó de saída da rodovia","{0.tag}")
            # suggestAlternative:"highway=motorway_link"
            err.append({'class': 9018056, 'subclass': 260528564, 'text': mapcss.tr(u'{0} deve ser utilizado apenas no nó de saída da rodovia', capture_tags, u'{0.tag}')})

        # *[name=~/^(?i)(?u)edifício.*/][!building]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_38a8f0ff, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'building'))):
            # throwWarning:tr("possível ausência de tag {0}","{1.key}")
            err.append({'class': 9018026, 'subclass': 1417041710, 'text': mapcss.tr(u'possível ausência de tag {0}', capture_tags, u'{1.key}')})

        # way[highway][!surface][highway!=bus_stop]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') and not mapcss._tag_capture(capture_tags, 1, tags, u'surface') and mapcss._tag_capture(capture_tags, 2, tags, u'highway') != u'bus_stop')):
            # throwOther:tr("{0} sem superfície ({1}) definida","{0.key}","{1.key}")
            err.append({'class': 9018057, 'subclass': 1502430220, 'text': mapcss.tr(u'{0} sem superfície ({1}) definida', capture_tags, u'{0.key}', u'{1.key}')})

        # way[highway=~/motorway|trunk|primary|secondary|tertiary/][!lanes]
        # way[highway$=_link][!lanes]
        if (u'highway' in keys) and \
            ((mapcss.regexp_test_(self.re_38494ef5, mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and not mapcss._tag_capture(capture_tags, 1, tags, u'lanes')) or \
            (mapcss.endswith(mapcss._tag_capture(capture_tags, 0, tags, u'highway'), u'_link') and not mapcss._tag_capture(capture_tags, 1, tags, u'lanes'))):
            # throwOther:tr("{0} sem número de faixas ({1}) definido","{0.key}","{1.key}")
            err.append({'class': 9018058, 'subclass': 36601634, 'text': mapcss.tr(u'{0} sem número de faixas ({1}) definido', capture_tags, u'{0.key}', u'{1.key}')})

        # way[highway=~/motorway|trunk|primary|secondary|tertiary|unclassified|residential/][!maxspeed][!"maxspeed:forward"][!"maxspeed:backward"]
        # way[highway$=_link][!maxspeed][!"maxspeed:forward"][!"maxspeed:backward"]
        if (u'highway' in keys) and \
            ((mapcss.regexp_test_(self.re_32b6342d, mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and not mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed') and not mapcss._tag_capture(capture_tags, 2, tags, u'maxspeed:forward') and not mapcss._tag_capture(capture_tags, 3, tags, u'maxspeed:backward')) or \
            (mapcss.endswith(mapcss._tag_capture(capture_tags, 0, tags, u'highway'), u'_link') and not mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed') and not mapcss._tag_capture(capture_tags, 2, tags, u'maxspeed:forward') and not mapcss._tag_capture(capture_tags, 3, tags, u'maxspeed:backward'))):
            # throwOther:tr("{0} sem velocidade máxima ({1}) definida","{0.key}","{1.key}")
            err.append({'class': 9018059, 'subclass': 1384833507, 'text': mapcss.tr(u'{0} sem velocidade máxima ({1}) definida', capture_tags, u'{0.key}', u'{1.key}')})

        # way[highway=service][!service]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'service' and not mapcss._tag_capture(capture_tags, 1, tags, u'service'))):
            # throwOther:tr("ausência do tipo de serviço ({0}) na {1}","{1.key}","{0.key}")
            err.append({'class': 9018060, 'subclass': 1348501854, 'text': mapcss.tr(u'ausência do tipo de serviço ({0}) na {1}', capture_tags, u'{1.key}', u'{0.key}')})

        # way[highway=track][!tracktype]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'track' and not mapcss._tag_capture(capture_tags, 1, tags, u'tracktype'))):
            # throwOther:tr("ausência do tipo de track ({0}) na {1}","{1.key}","{0.key}")
            err.append({'class': 9018061, 'subclass': 685903200, 'text': mapcss.tr(u'ausência do tipo de track ({0}) na {1}', capture_tags, u'{1.key}', u'{0.key}')})

        # *[route=ferry][!duration]
        if (u'route' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'route') == u'ferry' and not mapcss._tag_capture(capture_tags, 1, tags, u'duration'))):
            # throwWarning:tr("ausência do tempo de duração ({0}) da balsa","{1.key}")
            err.append({'class': 9018027, 'subclass': 1289884816, 'text': mapcss.tr(u'ausência do tempo de duração ({0}) da balsa', capture_tags, u'{1.key}')})

        # way[highway][highway!~/construction|give_way|motorway_junction|proposed|raceway|speed_camera|stop/][!wheelchair]
        # *[building][!wheelchair]
        if (u'building' in keys or u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') and not mapcss.regexp_test_(self.re_029b8e58, mapcss._tag_capture(capture_tags, 1, tags, u'highway')) and not mapcss._tag_capture(capture_tags, 2, tags, u'wheelchair')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'building') and not mapcss._tag_capture(capture_tags, 1, tags, u'wheelchair'))):
            # throwOther:tr("{0} sem tag de acessibilidade ({1})","{0.key}","{1.key}")
            err.append({'class': 9018028, 'subclass': 766437561, 'text': mapcss.tr(u'{0} sem tag de acessibilidade ({1})', capture_tags, u'{0.key}', u'{1.key}')})

        # *[name=~/^(?i)(?u)praça.*/][!leisure][landuse=~/^(forest|grass|greenfield|meadow|orchard)$/]
        # *[name=~/^(?i)(?u)praça.*/][!leisure][natural=~/^(grassland|heath|scrub|wood)$/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_4a8ca94e, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'leisure') and mapcss.regexp_test_(self.re_05a345c7, mapcss._tag_capture(capture_tags, 2, tags, u'landuse'))) or \
            (mapcss.regexp_test_(self.re_4a8ca94e, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'leisure') and mapcss.regexp_test_(self.re_12b48afb, mapcss._tag_capture(capture_tags, 2, tags, u'natural')))):
            # throwWarning:tr("possível definição incorreta para praça: ''{0}''","{2.key}")
            # suggestAlternative:"leisure=park"
            err.append({'class': 9018029, 'subclass': 80498829, 'text': mapcss.tr(u'possível definição incorreta para praça: \'\'{0}\'\'', capture_tags, u'{2.key}')})

        # *[wikipedia][wikipedia!~/^pt:/]
        if (u'wikipedia' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia') and not mapcss.regexp_test_(self.re_17fd35b3, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')))):
            # throwWarning:tr("utilizar prefixo em português (pt:) para {0}","{0.key}")
            err.append({'class': 9018030, 'subclass': 1219382195, 'text': mapcss.tr(u'utilizar prefixo em português (pt:) para {0}', capture_tags, u'{0.key}')})

        # way[highway][lanes=1][!oneway?][!junction][!narrow]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'lanes') == 1 and not mapcss._tag_capture(capture_tags, 2, tags, u'oneway') in ('yes', 'true', '1') and not mapcss._tag_capture(capture_tags, 3, tags, u'junction') and not mapcss._tag_capture(capture_tags, 4, tags, u'narrow'))):
            # throwWarning:tr("{0} com {1}","{0.key}","{1.tag}")
            # suggestAlternative:"lanes=2"
            # suggestAlternative:"narrow=yes"
            err.append({'class': 9018062, 'subclass': 1652729911, 'text': mapcss.tr(u'{0} com {1}', capture_tags, u'{0.key}', u'{1.tag}')})

        # way[cycleway=lane]["cycleway:left"=lane]
        # way[cycleway=lane]["cycleway:right"=lane]
        if (u'cycleway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'cycleway') == u'lane' and mapcss._tag_capture(capture_tags, 1, tags, u'cycleway:left') == u'lane') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'cycleway') == u'lane' and mapcss._tag_capture(capture_tags, 1, tags, u'cycleway:right') == u'lane')):
            # throwWarning:tr("uso incorreto de {0} com {1}","{0.tag}","{1.tag}")
            # suggestAlternative:"{1.tag}"
            err.append({'class': 9018063, 'subclass': 528363416, 'text': mapcss.tr(u'uso incorreto de {0} com {1}', capture_tags, u'{0.tag}', u'{1.tag}')})

        # *[name=~/.*\(.*\).*/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_7e9dfbe7, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com parênteses. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.","{0.key}")
            err.append({'class': 9018002, 'subclass': 1406083581, 'text': mapcss.tr(u'{0} com parênteses. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.', capture_tags, u'{0.key}')})

        # *[name=~/ - /]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_6b25b0c5, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com traço. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.","{0.key}")
            err.append({'class': 9018002, 'subclass': 1992839086, 'text': mapcss.tr(u'{0} com traço. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.', capture_tags, u'{0.key}')})

        # *[name=~/, /]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_4da7cb86, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com vírgula. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.","{0.key}")
            err.append({'class': 9018002, 'subclass': 659472938, 'text': mapcss.tr(u'{0} com vírgula. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.', capture_tags, u'{0.key}')})

        # *[name=~/: /]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_657f3be3, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com dois pontos. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.","{0.key}")
            err.append({'class': 9018002, 'subclass': 338682039, 'text': mapcss.tr(u'{0} com dois pontos. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.', capture_tags, u'{0.key}')})

        # *[name=~/ ou /]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_131cc885, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # throwWarning:tr("nome utilizado de forma incorreta")
            # suggestAlternative:"name e alt_name"
            err.append({'class': 9018031, 'subclass': 23034604, 'text': mapcss.tr(u'nome utilizado de forma incorreta', capture_tags)})

        # way[boundary=administrative][!admin_level]!.way_in_relation
        # Use undeclared class way_in_relation

        # way[place][place!~/^(city_block|farm|hamlet|island|islet|isolated_dwelling|neighbourhood|square)$/][!admin_level][!boundary]
        if (u'place' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'place') and not mapcss.regexp_test_(self.re_58f616c9, mapcss._tag_capture(capture_tags, 1, tags, u'place')) and not mapcss._tag_capture(capture_tags, 2, tags, u'admin_level') and not mapcss._tag_capture(capture_tags, 3, tags, u'boundary'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("local com ausência/incoerência de limite administrativo")
            err.append({'class': 9018002, 'subclass': 372086249, 'text': mapcss.tr(u'local com ausência/incoerência de limite administrativo', capture_tags)})

        # way[admin_level][!boundary]!.way_in_relation
        # way[admin_level][boundary][boundary!=administrative]!.way_in_relation
        # Use undeclared class way_in_relation

        # *[boundary=national_park][!name]
        # *[boundary=protected_area][!name]
        # *[leisure=nature_reserve][!name]
        if (u'boundary' in keys or u'leisure' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == u'national_park' and not mapcss._tag_capture(capture_tags, 1, tags, u'name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == u'protected_area' and not mapcss._tag_capture(capture_tags, 1, tags, u'name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == u'nature_reserve' and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))):
            # throwWarning:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
            err.append({'class': 9018033, 'subclass': 1492609299, 'text': mapcss.tr(u'{0} deve possuir {1}', capture_tags, u'{0.tag}', u'{1.key}')})

        # *[boundary=protected_area][!protect_class]
        if (u'boundary' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == u'protected_area' and not mapcss._tag_capture(capture_tags, 1, tags, u'protect_class'))):
            # throwWarning:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
            err.append({'class': 9018033, 'subclass': 822952800, 'text': mapcss.tr(u'{0} deve possuir {1}', capture_tags, u'{0.tag}', u'{1.key}')})

        # *[protect_class][protect_class!~/^(1(a|b)?|[1-9][0-9]?)$/]
        if (u'protect_class' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'protect_class') and not mapcss.regexp_test_(self.re_5ac7053e, mapcss._tag_capture(capture_tags, 1, tags, u'protect_class')))):
            # throwWarning:tr("valor incorreto para {0}","{0.key}")
            err.append({'class': 9018034, 'subclass': 1459161459, 'text': mapcss.tr(u'valor incorreto para {0}', capture_tags, u'{0.key}')})

        # *[protect_class][boundary!=protected_area]
        if (u'protect_class' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'protect_class') and mapcss._tag_capture(capture_tags, 1, tags, u'boundary') != u'protected_area')):
            # throwWarning:tr("ausência de boundary=protected_area")
            err.append({'class': 9018035, 'subclass': 1208814760, 'text': mapcss.tr(u'ausência de boundary=protected_area', capture_tags)})

        # *[amenity][!opening_hours]
        # *[shop][!opening_hours]
        if (u'amenity' in keys or u'shop' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') and not mapcss._tag_capture(capture_tags, 1, tags, u'opening_hours')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'shop') and not mapcss._tag_capture(capture_tags, 1, tags, u'opening_hours'))):
            # throwOther:tr("{0} sem {1}","{0.key}","{1.key}")
            err.append({'class': 9018038, 'subclass': 1861306703, 'text': mapcss.tr(u'{0} sem {1}', capture_tags, u'{0.key}', u'{1.key}')})

        # *[name=~/.* D(a|e|o)s? .*/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_2ffc377d, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("''da'', ''de'' e ''do'' são minúsculos nos nomes em português")
            err.append({'class': 9018002, 'subclass': 1986668346, 'text': mapcss.tr(u'\'\'da\'\', \'\'de\'\' e \'\'do\'\' são minúsculos nos nomes em português', capture_tags)})

        # *[name=~/^[a-z].*/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_39d67968, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("nome iniciando com letra minúscula")
            err.append({'class': 9018002, 'subclass': 167462302, 'text': mapcss.tr(u'nome iniciando com letra minúscula', capture_tags)})

        # *[alt_ref]
        if (u'alt_ref' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'alt_ref'))):
            # throwWarning:tr("o conteúdo de {0} deve fazer parte de ref, separado por ;","{0.key}")
            # suggestAlternative:"ref"
            err.append({'class': 9018039, 'subclass': 722411109, 'text': mapcss.tr(u'o conteúdo de {0} deve fazer parte de ref, separado por ;', capture_tags, u'{0.key}')})

        # way[highway=path][tracktype]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'path' and mapcss._tag_capture(capture_tags, 1, tags, u'tracktype'))):
            # throwWarning:tr("uso incorreto de {0}","{1.key}")
            # suggestAlternative:"trail_visibility"
            err.append({'class': 9018064, 'subclass': 2113951549, 'text': mapcss.tr(u'uso incorreto de {0}', capture_tags, u'{1.key}')})

        # way[highway!=track][tracktype]
        if (u'tracktype' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') != u'track' and mapcss._tag_capture(capture_tags, 1, tags, u'tracktype'))):
            # throwWarning:tr("utilizar {0} apenas em {1}={2}","{1.key}","{0.key}","{0.value}")
            err.append({'class': 9018065, 'subclass': 965336283, 'text': mapcss.tr(u'utilizar {0} apenas em {1}={2}', capture_tags, u'{1.key}', u'{0.key}', u'{0.value}')})

        # *[source=~/.*,.*/]
        # *["source:ref"=~/.*,.*/]
        # *["source:name"=~/.*,.*/]
        if (u'source' in keys or u'source:name' in keys or u'source:ref' in keys) and \
            ((mapcss.regexp_test_(self.re_34f65002, mapcss._tag_capture(capture_tags, 0, tags, u'source'))) or \
            (mapcss.regexp_test_(self.re_34f65002, mapcss._tag_capture(capture_tags, 0, tags, u'source:ref'))) or \
            (mapcss.regexp_test_(self.re_34f65002, mapcss._tag_capture(capture_tags, 0, tags, u'source:name')))):
            # throwOther:tr("utilizar ; como separador de valores em {0}","{0.key}")
            err.append({'class': 9018040, 'subclass': 2114349281, 'text': mapcss.tr(u'utilizar ; como separador de valores em {0}', capture_tags, u'{0.key}')})

        # *[surface][eval(number_of_tags())=1]
        if (u'surface' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'surface') and len(tags) == 1)):
            # throwWarning:tr("objeto incompleto: possui apenas {0}","{0.key}")
            err.append({'class': 9018041, 'subclass': 1776991136, 'text': mapcss.tr(u'objeto incompleto: possui apenas {0}', capture_tags, u'{0.key}')})

        # *[name][surface][eval(number_of_tags())=2]
        # *[name][website][eval(number_of_tags())=2]
        if (u'name' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'surface') and len(tags) == 2) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'website') and len(tags) == 2)):
            # throwWarning:tr("objeto incompleto: possui apenas {0} e {1}","{0.key}","{1.key}")
            err.append({'class': 9018042, 'subclass': 626126700, 'text': mapcss.tr(u'objeto incompleto: possui apenas {0} e {1}', capture_tags, u'{0.key}', u'{1.key}')})

        # way[highway=~/^(living_street|pedestrian|residential|road|service|track)$/][ref]
        if (u'highway' in keys) and \
            ((mapcss.regexp_test_(self.re_07f31a73, mapcss._tag_capture(capture_tags, 0, tags, u'highway')) and mapcss._tag_capture(capture_tags, 1, tags, u'ref'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("a via deve ser ao menos tertiary")
            err.append({'class': 9018002, 'subclass': 1461580029, 'text': mapcss.tr(u'a via deve ser ao menos tertiary', capture_tags)})

        # way[bridge][!layer]
        # way[tunnel][!layer]
        if (u'bridge' in keys or u'tunnel' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'bridge') and not mapcss._tag_capture(capture_tags, 1, tags, u'layer')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'tunnel') and not mapcss._tag_capture(capture_tags, 1, tags, u'layer'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} sem {1}","{0.key}","{1.key}")
            err.append({'class': 9018002, 'subclass': 1290837584, 'text': mapcss.tr(u'{0} sem {1}', capture_tags, u'{0.key}', u'{1.key}')})

        # *[leisure=pitch][sport=tennis][surface=unpaved]
        if (u'leisure' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == u'pitch' and mapcss._tag_capture(capture_tags, 1, tags, u'sport') == u'tennis' and mapcss._tag_capture(capture_tags, 2, tags, u'surface') == u'unpaved')):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("{0} com superfície incorreta","{2.key}")
            # suggestAlternative:"surface=clay"
            # fixAdd:"surface=clay"
            err.append({'class': 9018006, 'subclass': 1659179489, 'text': mapcss.tr(u'{0} com superfície incorreta', capture_tags, u'{2.key}'), 'fix': {
                '+': dict([
                    [u'surface',u'clay']])
            }})

        # *[amenity=fuel][name=~/(?i)(?u)\b(Ale|BR|Esso|Ipiranga|Petrobr(á|a)s|Shell|Texaco)\b/]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'fuel' and mapcss.regexp_test_(self.re_604bb645, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("uso incorreto da bandeira do posto")
            # suggestAlternative:"brand"
            err.append({'class': 9018002, 'subclass': 935774110, 'text': mapcss.tr(u'uso incorreto da bandeira do posto', capture_tags)})

        # *[/_[0-9]$/][!"is_in:iso_3166_2"]
        if ((mapcss._tag_capture(capture_tags, 0, tags, self.re_57b8ef8e) and not mapcss._tag_capture(capture_tags, 1, tags, u'is_in:iso_3166_2'))):
            # throwError:tr("chave inválida: {0}","{0.key}")
            err.append({'class': 9018022, 'subclass': 331369569, 'text': mapcss.tr(u'chave inválida: {0}', capture_tags, u'{0.key}')})

        # *["addr:housenumber"=~/(?i)^s(\.|-| )?\/?n\.?º?$/][!note]
        if (u'addr:housenumber' in keys) and \
            ((mapcss.regexp_test_(self.re_0b27200b, mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber')) and not mapcss._tag_capture(capture_tags, 1, tags, u'note'))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("não utilizar ''{0}'' para locais sem número",tag("addr:housenumber"))
            # suggestAlternative:"note"
            # fixRemove:"addr:housenumber"
            # fixAdd:"note=Local sem número"
            err.append({'class': 9018006, 'subclass': 931902546, 'text': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', capture_tags, mapcss.tag(tags, u'addr:housenumber')), 'fix': {
                '+': dict([
                    [u'note',u'Local sem número']]),
                '-': ([
                    u'addr:housenumber'])
            }})

        # *["addr:housenumber"=~/(?i)^s(\.|-| )?\/?n\.?º?$/][note]
        if (u'addr:housenumber' in keys) and \
            ((mapcss.regexp_test_(self.re_0b27200b, mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber')) and mapcss._tag_capture(capture_tags, 1, tags, u'note'))):
            # throwWarning:tr("não utilizar ''{0}'' para locais sem número",tag("addr:housenumber"))
            # suggestAlternative:"note"
            err.append({'class': 9018043, 'subclass': 1717284811, 'text': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', capture_tags, mapcss.tag(tags, u'addr:housenumber'))})

        # *[source=~/(?i)google/]
        if (u'source' in keys) and \
            ((mapcss.regexp_test_(self.re_2e8e4f2b, mapcss._tag_capture(capture_tags, 0, tags, u'source')))):
            # throwError:tr("objeto contém Google como source")
            err.append({'class': 9018044, 'subclass': 1313403884, 'text': mapcss.tr(u'objeto contém Google como source', capture_tags)})

        # *[amenity=townhall][name=~/^(?i)(?u)c(â|a)mara\b/]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'townhall' and mapcss.regexp_test_(self.re_46ab4d8d, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("câmara de vereadores mapeada incorretamente")
            # suggestAlternative:"office=government + government=legislative"
            err.append({'class': 9018002, 'subclass': 129695507, 'text': mapcss.tr(u'câmara de vereadores mapeada incorretamente', capture_tags)})

        # *[office=government][government!=legislative][name=~/^(?i)(?u)c(â|a)mara\b/]
        if (u'office' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'office') == u'government' and mapcss._tag_capture(capture_tags, 1, tags, u'government') != u'legislative' and mapcss.regexp_test_(self.re_46ab4d8d, mapcss._tag_capture(capture_tags, 2, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("ausência de government=legislative")
            err.append({'class': 9018002, 'subclass': 869412796, 'text': mapcss.tr(u'ausência de government=legislative', capture_tags)})

        # *[amenity=townhall][name=~/^(?i)(?u)c((â|a)me|ama)ra\b/]
        # *[office=government][name=~/^(?i)(?u)c((â|a)me|ama)ra\b/]
        if (u'amenity' in keys or u'office' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'townhall' and mapcss.regexp_test_(self.re_793b22ec, mapcss._tag_capture(capture_tags, 1, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'office') == u'government' and mapcss.regexp_test_(self.re_793b22ec, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("erro de ortografia em ''câmara''")
            err.append({'class': 9018002, 'subclass': 212328084, 'text': mapcss.tr(u'erro de ortografia em \'\'câmara\'\'', capture_tags)})

        # *[amenity=charging_station]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'charging_station')):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("possivelmente deve ser amenity=fuel")
            err.append({'class': 9018002, 'subclass': 128902291, 'text': mapcss.tr(u'possivelmente deve ser amenity=fuel', capture_tags)})

        # *[name=~/(?i)^Borrach(aria|eiro)/][shop=tyres][!repair]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_126ba9a9, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'shop') == u'tyres' and not mapcss._tag_capture(capture_tags, 2, tags, u'repair'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("borracharia sem ''repair=yes''")
            # suggestAlternative:"repair=yes"
            err.append({'class': 9018002, 'subclass': 817061630, 'text': mapcss.tr(u'borracharia sem \'\'repair=yes\'\'', capture_tags)})

        # *[name=~/(?i)^Borrach(aria|eiro)/][shop!=tyres]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_126ba9a9, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'shop') != u'tyres')):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("borracharia sem ''shop=tyres''")
            # suggestAlternative:"shop=tyres"
            err.append({'class': 9018002, 'subclass': 1324999258, 'text': mapcss.tr(u'borracharia sem \'\'shop=tyres\'\'', capture_tags)})

        # way[waterway=~/^(river|stream)$/][name][name!~/^(?U)(Água|Arroio|Cabeceira|Córrego|Furo|Grota|Igarapé|Lajeado|Paraná|Restinga|Riacho|Ribeirão|Rio|Sanga)\b/]
        # way[waterway=~/^(river|stream)$/][alt_name][alt_name!~/^(?U)(Água|Arroio|Cabeceira|Córrego|Furo|Grota|Igarapé|Lajeado|Paraná|Restinga|Riacho|Ribeirão|Rio|Sanga)\b/]
        if (u'waterway' in keys) and \
            ((mapcss.regexp_test_(self.re_04873a60, mapcss._tag_capture(capture_tags, 0, tags, u'waterway')) and mapcss._tag_capture(capture_tags, 1, tags, u'name') and not mapcss.regexp_test_(self.re_280004fd, mapcss._tag_capture(capture_tags, 2, tags, u'name'))) or \
            (mapcss.regexp_test_(self.re_04873a60, mapcss._tag_capture(capture_tags, 0, tags, u'waterway')) and mapcss._tag_capture(capture_tags, 1, tags, u'alt_name') and not mapcss.regexp_test_(self.re_280004fd, mapcss._tag_capture(capture_tags, 2, tags, u'alt_name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com possível nome errado/incompleto",tag(waterway))
            err.append({'class': 9018002, 'subclass': 1906904535, 'text': mapcss.tr(u'{0} com possível nome errado/incompleto', capture_tags, mapcss.tag(tags, u'waterway'))})

        return err

    def relation(self, data, tags, *args):
        capture_tags = {}
        keys = tags.keys()
        err = []


        # relation[highway][name=~/\b[A-Z]{2,3} (- )?[0-9]{2,3}\b/]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss.regexp_test_(self.re_073e5345, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # throwWarning:tr("rodovia com ref no nome")
            err.append({'class': 9018045, 'subclass': 523480189, 'text': mapcss.tr(u'rodovia com ref no nome', capture_tags)})

        # *["addr:street"]["addr:street"!~/^(Aeroporto|Alameda|Área|Avenida|([1-9][0-9]?º )?Beco|Boulevard|Caminho|Campo|Chácara|Colônia|Condomínio|Conjunto|Contorno|Distrito|Elevado|Esplanada|Estação|Estrada|Favela|Fazenda|Feira|Jardim|Ladeira|Lago|Lagoa|Largo|Loteamento|Marginal|Morro|Núcleo|([1-9][0-9]?ª )?Paralela|Parque|Passagem|Passarela|Pátio|Ponte|Praça|Quadra|Recanto|Residencial|Rodovia|Rotatória|Rua|Servidão|Setor|Sítio|([1-9][0-9]?ª )?Subida|([1-9][0-9]?ª )?Travessa|Trecho|Trevo|Túnel|Vale|Vereda|Via|Viadutos?|Viela|Vila|(Anel|Complexo|Dispositivo) (Rodo)?(V|v)iário) .*/]
        if (u'addr:street' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'addr:street') and not mapcss.regexp_test_(self.re_3b777b9d, mapcss._tag_capture(capture_tags, 1, tags, u'addr:street')))):
            # throwWarning:tr("{0} com logradouro ausente, errado ou abreviado","{0.key}")
            err.append({'class': 9018001, 'subclass': 588331445, 'text': mapcss.tr(u'{0} com logradouro ausente, errado ou abreviado', capture_tags, u'{0.key}')})

        # *[!highway][route!=road][!public_transport][type!~/route|street/][name][name=~/^(?i)(?u)(alameda|avenida|beco|estrada|ladeira|passarela|rodovia|rotatória|rua|travessa|trevo|viela|(anel|complexo|dispositivo) viário) .*/][name!~/^(?i)estrada de ferro/]
        if (u'name' in keys) and \
            ((not mapcss._tag_capture(capture_tags, 0, tags, u'highway') and mapcss._tag_capture(capture_tags, 1, tags, u'route') != u'road' and not mapcss._tag_capture(capture_tags, 2, tags, u'public_transport') and not mapcss.regexp_test_(self.re_72d45155, mapcss._tag_capture(capture_tags, 3, tags, u'type')) and mapcss._tag_capture(capture_tags, 4, tags, u'name') and mapcss.regexp_test_(self.re_5849be19, mapcss._tag_capture(capture_tags, 5, tags, u'name')) and not mapcss.regexp_test_(self.re_15690541, mapcss._tag_capture(capture_tags, 6, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("objeto com nome de via mas sem tag de {0}","{0.key}")
            err.append({'class': 9018002, 'subclass': 874993957, 'text': mapcss.tr(u'objeto com nome de via mas sem tag de {0}', capture_tags, u'{0.key}')})

        # *[name=~/^(?i)(?u)[a-z0-9]+_([a-z0-9]_?)+$/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_4bd3b925, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("utilizar espaço ao invés de underscore")
            err.append({'class': 9018002, 'subclass': 378801374, 'text': mapcss.tr(u'utilizar espaço ao invés de underscore', capture_tags)})

        # *[name=~/(?i)(^|.* )(Cel|Cmte|Cond|Conj|Dª|Dr|Eng|Gov|Hab|Jd|Jr|Marg|Mun|p\/|Pde|Pe|Pq|Pst|Pref|Profa|Profª|Prof|Res|s\/|Sr(a|ª)?|Sta|Sto|Ver)\.? .*/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_178f5446, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # throwWarning:tr("palavra abreviada em {0}","{0.key}")
            err.append({'class': 9018003, 'subclass': 1784756763, 'text': mapcss.tr(u'palavra abreviada em {0}', capture_tags, u'{0.key}')})

        # *[leisure][name=~/^(?i)(?u)(campo|est(á|a)dio|gin(á|a)sio|quadra)( de (futebol|esportes?))?$/]
        if (u'leisure' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'leisure') and mapcss.regexp_test_(self.re_7f53e992, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # throwWarning:tr("nome supérfluo/incompleto de local de lazer")
            err.append({'class': 9018004, 'subclass': 790401825, 'text': mapcss.tr(u'nome supérfluo/incompleto de local de lazer', capture_tags)})

        # *[name=~/^(?i)(?u)((Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF|hospital)$/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_52ab3b8b, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # throwWarning:tr("nome supérfluo/incompleto de local de saúde")
            err.append({'class': 9018005, 'subclass': 1792576894, 'text': mapcss.tr(u'nome supérfluo/incompleto de local de saúde', capture_tags)})

        # *[amenity=~/^(clinic|doctors|hospital)$/][name=~/(?i)\bsaude\b/]
        if (u'amenity' in keys) and \
            ((mapcss.regexp_test_(self.re_5ab76b11, mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test_(self.re_4cf86823, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("erro de ortografia em ''saúde''")
            err.append({'class': 9018002, 'subclass': 1455303428, 'text': mapcss.tr(u'erro de ortografia em \'\'saúde\'\'', capture_tags)})

        # *[place=farm][name^="Sitio "]
        if (u'place' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'farm' and mapcss.startswith(mapcss._tag_capture(capture_tags, 1, tags, u'name'), u'Sitio '))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("faltando acento em ''Sítio''")
            err.append({'class': 9018002, 'subclass': 962677162, 'text': mapcss.tr(u'faltando acento em \'\'Sítio\'\'', capture_tags)})

        # *[name=~/^(?i)(?u)(aldeia|borrach(aria|eiro)|bosque|capela|cemit(é|e)rio|c(ó|o)rrego|escola|estacionamento|fazenda|floresta|hospital|igreja|lago|lagoa|mata( nativa)?|praça|parque|parquinho|posto( de gasolina)?|riacho|rio|rodovi(á|a)ria|vila)$/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_20c7dd98, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("local com nome supérfluo, incompleto ou descritivo")
            err.append({'class': 9018002, 'subclass': 501162763, 'text': mapcss.tr(u'local com nome supérfluo, incompleto ou descritivo', capture_tags)})

        # *[amenity=parking][name=~/(?i)^Estacionamento /]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'parking' and mapcss.regexp_test_(self.re_407995b9, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("possível nome descritivo do estacionamento")
            # suggestAlternative:"operator"
            err.append({'class': 9018002, 'subclass': 698950828, 'text': mapcss.tr(u'possível nome descritivo do estacionamento', capture_tags)})

        # relation[type=route][highway]
        if (u'type' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'type') == u'route' and mapcss._tag_capture(capture_tags, 1, tags, u'highway'))):
            # throwWarning:tr("relação não deve possuir {0}","{1.key}")
            err.append({'class': 9018046, 'subclass': 890277462, 'text': mapcss.tr(u'relação não deve possuir {0}', capture_tags, u'{1.key}')})

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
        if (u'designation' in keys or u'name' in keys or u'ref' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'designation') == mapcss.tag(tags, u'addr:housename')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'ref') == mapcss.tag(tags, u'designation')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'ref') == mapcss.tag(tags, u'old_ref')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'addr:housename')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'designation')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'alt_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'int_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'loc_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'nat_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'official_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'old_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'reg_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'short_name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') == mapcss.tag(tags, u'sorting_name'))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("{0} e {1} são iguais; remover chave {1} desnecessária","{0.key}","{0.value}")
            # fixRemove:"{0.value}"
            err.append({'class': 9018006, 'subclass': 1882388489, 'text': mapcss.tr(u'{0} e {1} são iguais; remover chave {1} desnecessária', capture_tags, u'{0.key}', u'{0.value}'), 'fix': {
                '-': ([
                    u'{0.value}'])
            }})

        # *[source=*name]
        if (u'source' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'source') == mapcss.tag(tags, u'name'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} e {1} são iguais","{0.key}","{0.value}")
            err.append({'class': 9018002, 'subclass': 1403015964, 'text': mapcss.tr(u'{0} e {1} são iguais', capture_tags, u'{0.key}', u'{0.value}')})

        # *[name=~/(?i)(?u)((sem (denomina(ç|c)(ã|a)o|nome|sa(i|í)da))|desconhecido|n(ã|a)o conhecido)/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_65710fdb, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # throwWarning:tr("objeto com nomenclatura incorreta")
            # suggestAlternative:"noname"
            err.append({'class': 9018007, 'subclass': 506924923, 'text': mapcss.tr(u'objeto com nomenclatura incorreta', capture_tags)})

        # *[designation]
        if (u'designation' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'designation'))):
            # throwWarning:tr("{0} é uma chave utilizada apenas no Reino Unido","{0.key}")
            # suggestAlternative:"description"
            # suggestAlternative:"name"
            err.append({'class': 9018009, 'subclass': 1259259930, 'text': mapcss.tr(u'{0} é uma chave utilizada apenas no Reino Unido', capture_tags, u'{0.key}')})

        # *[place=~/hamlet|isolated_dwelling|town|village/][population>=100000]
        if (u'place' in keys) and \
            ((mapcss.regexp_test_(self.re_152c10ee, mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'population') >= 100000)):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("local com 100.000 habitantes ou mais deve ser classificado como city")
            # fixAdd:"place=city"
            err.append({'class': 9018006, 'subclass': 149235075, 'text': mapcss.tr(u'local com 100.000 habitantes ou mais deve ser classificado como city', capture_tags), 'fix': {
                '+': dict([
                    [u'place',u'city']])
            }})

        # *[place=~/city|hamlet|isolated_dwelling|village/][population>=10000][population<100000]
        if (u'place' in keys) and \
            ((mapcss.regexp_test_(self.re_591572a5, mapcss._tag_capture(capture_tags, 0, tags, u'place')) and mapcss._tag_capture(capture_tags, 1, tags, u'population') >= 10000 and mapcss._tag_capture(capture_tags, 2, tags, u'population') < 100000)):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("local com população entre 10.000 e 100.000 deve ser classificado como town")
            # fixAdd:"place=town"
            err.append({'class': 9018006, 'subclass': 1174321645, 'text': mapcss.tr(u'local com população entre 10.000 e 100.000 deve ser classificado como town', capture_tags), 'fix': {
                '+': dict([
                    [u'place',u'town']])
            }})

        # *[place][place!~/hamlet|island|isolated_dwelling|neighbourhood|suburb|village/][population<10000]
        if (u'place' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'place') and not mapcss.regexp_test_(self.re_3aeda39d, mapcss._tag_capture(capture_tags, 1, tags, u'place')) and mapcss._tag_capture(capture_tags, 2, tags, u'population') < 10000)):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("local com menos de 10.000 habitantes deve ser classificado como village")
            # fixAdd:"place=village"
            err.append({'class': 9018006, 'subclass': 719699918, 'text': mapcss.tr(u'local com menos de 10.000 habitantes deve ser classificado como village', capture_tags), 'fix': {
                '+': dict([
                    [u'place',u'village']])
            }})

        # *[place=city][!population]
        # *[place=town][!population]
        # *[place=village][!population]
        if (u'place' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'city' and not mapcss._tag_capture(capture_tags, 1, tags, u'population')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'town' and not mapcss._tag_capture(capture_tags, 1, tags, u'population')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'village' and not mapcss._tag_capture(capture_tags, 1, tags, u'population'))):
            # throwWarning:tr("{0} sem tag de população (population)","{0.value}")
            err.append({'class': 9018011, 'subclass': 1582438505, 'text': mapcss.tr(u'{0} sem tag de população (population)', capture_tags, u'{0.value}')})

        # *[place=city][!name]
        # *[place=town][!name]
        # *[place=village][!name]
        if (u'place' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'city' and not mapcss._tag_capture(capture_tags, 1, tags, u'name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'town' and not mapcss._tag_capture(capture_tags, 1, tags, u'name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'place') == u'village' and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))):
            # throwWarning:tr("{0} sem nome","{0.value}")
            err.append({'class': 9018012, 'subclass': 828568305, 'text': mapcss.tr(u'{0} sem nome', capture_tags, u'{0.value}')})

        # *["addr:city"=~/(,|( |-) ?[A-Z]{2})/]
        if (u'addr:city' in keys) and \
            ((mapcss.regexp_test_(self.re_10f1c360, mapcss._tag_capture(capture_tags, 0, tags, u'addr:city')))):
            # throwWarning:tr("{0} deve conter apenas o nome da cidade","{0.key}")
            err.append({'class': 9018013, 'subclass': 223700239, 'text': mapcss.tr(u'{0} deve conter apenas o nome da cidade', capture_tags, u'{0.key}')})

        # *[name=~/^(?i)(?u)(Faz\.|Fazenda|Sítio|Chácara)/][place][place!~/city|farm|neighbourhood|suburb|town|village/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_2cd1e949, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'place') and not mapcss.regexp_test_(self.re_5d3348cb, mapcss._tag_capture(capture_tags, 2, tags, u'place')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("objeto talvez deva ser {0}=farm","{1.key}")
            err.append({'class': 9018002, 'subclass': 414255329, 'text': mapcss.tr(u'objeto talvez deva ser {0}=farm', capture_tags, u'{1.key}')})

        # *[place][name=~/^(?i)Bairro\b/][name!~/^(?i)Bairro d(a|e|o)s?\b/]
        if (u'place' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'place') and mapcss.regexp_test_(self.re_20fc5143, mapcss._tag_capture(capture_tags, 1, tags, u'name')) and not mapcss.regexp_test_(self.re_64387998, mapcss._tag_capture(capture_tags, 2, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("objeto talvez não deva ter ''Bairro'' no nome")
            err.append({'class': 9018002, 'subclass': 457937105, 'text': mapcss.tr(u'objeto talvez não deva ter \'\'Bairro\'\' no nome', capture_tags)})

        # *[iata="0"]
        if (u'iata' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'iata') == u'0')):
            # throwWarning:tr("{0} com valor = {1}","{0.key}","{0.value}")
            err.append({'class': 9018014, 'subclass': 1389202412, 'text': mapcss.tr(u'{0} com valor = {1}', capture_tags, u'{0.key}', u'{0.value}')})

        # *[amenity=~/college|school/][name=~/^(?i)(?u)(Centro Universitário|Faculdades?|FATEC|Instituto Federal)\b/]
        if (u'amenity' in keys) and \
            ((mapcss.regexp_test_(self.re_362f879f, mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test_(self.re_1d232d4c, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("estabelecimento de ensino classificado incorretamente")
            # suggestAlternative:"amenity=university"
            # fixAdd:"{0.key}=university"
            err.append({'class': 9018006, 'subclass': 221523813, 'text': mapcss.tr(u'estabelecimento de ensino classificado incorretamente', capture_tags), 'fix': {
                '+': dict([
                    [u'{0.key}',u'university']])
            }})

        # *[amenity=school][name=~/^(?i)(?u)(SENAC|SENAI|Serviço Nacional de Aprendizagem)/]
        # *[amenity=~/school|university/][name=~/(?i)(?u)\b(Centro Paula Souza|Escola Técnica|ETEC)\b/]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'school' and mapcss.regexp_test_(self.re_044c8944, mapcss._tag_capture(capture_tags, 1, tags, u'name'))) or \
            (mapcss.regexp_test_(self.re_6c0d6e9e, mapcss._tag_capture(capture_tags, 0, tags, u'amenity')) and mapcss.regexp_test_(self.re_3b304b9b, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("estabelecimento de ensino classificado incorretamente")
            # suggestAlternative:"amenity=college"
            # fixAdd:"{0.key}=college"
            err.append({'class': 9018006, 'subclass': 897019825, 'text': mapcss.tr(u'estabelecimento de ensino classificado incorretamente', capture_tags), 'fix': {
                '+': dict([
                    [u'{0.key}',u'college']])
            }})

        # *[amenity=school][name=~/^(?i)(?u)(auto(-| )?( moto )?escola|centro de formação de condutores|cfc|moto escola)\b/]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'school' and mapcss.regexp_test_(self.re_35bb0f2f, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("autoescola classificada incorretamente")
            # suggestAlternative:"amenity=driving_school"
            # fixAdd:"{0.key}=driving_school"
            err.append({'class': 9018006, 'subclass': 1796023580, 'text': mapcss.tr(u'autoescola classificada incorretamente', capture_tags), 'fix': {
                '+': dict([
                    [u'{0.key}',u'driving_school']])
            }})

        # *[amenity=school][name=~/^(?i)creche\b/]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'school' and mapcss.regexp_test_(self.re_160d1bfc, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("creche classificada incorretamente")
            # suggestAlternative:"amenity=kindergarten"
            # fixAdd:"{0.key}=kindergarten"
            err.append({'class': 9018006, 'subclass': 121701344, 'text': mapcss.tr(u'creche classificada incorretamente', capture_tags), 'fix': {
                '+': dict([
                    [u'{0.key}',u'kindergarten']])
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
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_69d0dc1a, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'power') and mapcss._tag_capture(capture_tags, 2, tags, u'power') != u'substation') or \
            (mapcss.regexp_test_(self.re_002de70b, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') and mapcss._tag_capture(capture_tags, 2, tags, u'amenity') != u'courthouse') or \
            (mapcss.regexp_test_(self.re_25871691, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'hospital') or \
            (mapcss.regexp_test_(self.re_6e928d7b, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'university') or \
            (mapcss.regexp_test_(self.re_57a9f888, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'school') or \
            (mapcss.regexp_test_(self.re_458e02d8, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'hotel') or \
            (mapcss.regexp_test_(self.re_105662b4, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'chapel') or \
            (mapcss.regexp_test_(self.re_752011f2, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'church') or \
            (mapcss.regexp_test_(self.re_1e8e69a3, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'cathedral') or \
            (mapcss.regexp_test_(self.re_381002af, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'farm') or \
            (mapcss.regexp_test_(self.re_486d02c4, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'building') and mapcss._tag_capture(capture_tags, 2, tags, u'building') != u'supermarket')):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("{0} provavelmente deveria ser {1}","{2.key}","{2.value}")
            # fixAdd:"{2.key}={2.value}"
            err.append({'class': 9018006, 'subclass': 1930177472, 'text': mapcss.tr(u'{0} provavelmente deveria ser {1}', capture_tags, u'{2.key}', u'{2.value}'), 'fix': {
                '+': dict([
                    [u'{2.key}',u'{2.value}']])
            }})

        # *[name=~/^(?i)(?u)(AM(A|E)|(Posto|Unidade (Básica)?) de Sa(u|ú)de|UBS|PSF).*/][amenity=hospital]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_7b7c453d, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') == u'hospital')):
            # throwWarning:tr("postos/unidades de saúde devem ser amenity=clinic")
            err.append({'class': 9018015, 'subclass': 2108543140, 'text': mapcss.tr(u'postos/unidades de saúde devem ser amenity=clinic', capture_tags)})

        # *[name=~/^(?i)\bSAMU\b/][amenity=~/clinic|doctors|hospital/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_2dbaea13, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss.regexp_test_(self.re_3eb0ab44, mapcss._tag_capture(capture_tags, 1, tags, u'amenity')))):
            # throwWarning:tr("SAMU classificado de forma errada")
            # suggestAlternative:"emergency=ambulance_station"
            err.append({'class': 9018016, 'subclass': 2090365947, 'text': mapcss.tr(u'SAMU classificado de forma errada', capture_tags)})

        # relation[highway=give_way]
        # relation[highway=mini_roundabout]
        # relation[highway=stop]
        # relation[highway=turning_circle]
        if (u'highway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'give_way') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'mini_roundabout') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'stop') or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'highway') == u'turning_circle')):
            # throwWarning:tr("{0} deve ser utilizado apenas em nós","{0.tag}")
            err.append({'class': 9018047, 'subclass': 1663665792, 'text': mapcss.tr(u'{0} deve ser utilizado apenas em nós', capture_tags, u'{0.tag}')})

        # relation[enforcement=maxspeed][!maxspeed]
        # relation[enforcement=maxheight][!maxheight]
        # relation[enforcement=maxweight][!maxweight]
        if (u'enforcement' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'enforcement') == u'maxspeed' and not mapcss._tag_capture(capture_tags, 1, tags, u'maxspeed')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'enforcement') == u'maxheight' and not mapcss._tag_capture(capture_tags, 1, tags, u'maxheight')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'enforcement') == u'maxweight' and not mapcss._tag_capture(capture_tags, 1, tags, u'maxweight'))):
            # throwWarning:tr("adicionar {0} ao {1}","{1.key}","{0.tag}")
            err.append({'class': 9018018, 'subclass': 73808614, 'text': mapcss.tr(u'adicionar {0} ao {1}', capture_tags, u'{1.key}', u'{0.tag}')})

        # *[crossing][!highway][!railway]
        if (u'crossing' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'crossing') and not mapcss._tag_capture(capture_tags, 1, tags, u'highway') and not mapcss._tag_capture(capture_tags, 2, tags, u'railway'))):
            # throwWarning:tr("{0} deve ser utilizado com {1}={0} ou {2}={0}","{0.key}","{1.key}","{2.key}")
            err.append({'class': 9018019, 'subclass': 139983185, 'text': mapcss.tr(u'{0} deve ser utilizado com {1}={0} ou {2}={0}', capture_tags, u'{0.key}', u'{1.key}', u'{2.key}')})

        # *[aeroway][designation=~/^[A-Z]{4}$/][!icao]
        # *[aeroway][ref=~/^[A-Z]{4}$/][!icao]
        if (u'aeroway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') and mapcss.regexp_test_(self.re_7afc6883, mapcss._tag_capture(capture_tags, 1, tags, u'designation')) and not mapcss._tag_capture(capture_tags, 2, tags, u'icao')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') and mapcss.regexp_test_(self.re_7afc6883, mapcss._tag_capture(capture_tags, 1, tags, u'ref')) and not mapcss._tag_capture(capture_tags, 2, tags, u'icao'))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("{0} provavelmente deve ser utilizado como {1}","{1.key}","{2.key}")
            # fixChangeKey:"{1.key} => {2.key}"
            err.append({'class': 9018006, 'subclass': 662001655, 'text': mapcss.tr(u'{0} provavelmente deve ser utilizado como {1}', capture_tags, u'{1.key}', u'{2.key}'), 'fix': {
                '+': dict([
                    [u'{2.key}', mapcss.tag(tags, u'{1.key}')]]),
                '-': ([
                    u'{1.key}'])
            }})

        # *[access=permissive]
        if (u'access' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'access') == u'permissive')):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} deve ser utilizado apenas em vias privadas com permissão de acesso e não em vias de acesso público","{0.tag}")
            err.append({'class': 9018002, 'subclass': 1918455197, 'text': mapcss.tr(u'{0} deve ser utilizado apenas em vias privadas com permissão de acesso e não em vias de acesso público', capture_tags, u'{0.tag}')})

        # *[name=~/^(?U)(\p{Upper}| )+$/]
        # *["addr:street"=~/^(?U)(\p{Upper}| )+$/]
        if (u'addr:street' in keys or u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_73b50a21, mapcss._tag_capture(capture_tags, 0, tags, u'name'))) or \
            (mapcss.regexp_test_(self.re_73b50a21, mapcss._tag_capture(capture_tags, 0, tags, u'addr:street')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} totalmente em maiúsculo; usar nome completo ou short_name se for sigla","{0.key}")
            err.append({'class': 9018002, 'subclass': 386880794, 'text': mapcss.tr(u'{0} totalmente em maiúsculo; usar nome completo ou short_name se for sigla', capture_tags, u'{0.key}')})

        # *["addr:postcode"=~/^[0-9]{8}$/]
        if (u'addr:postcode' in keys) and \
            ((mapcss.regexp_test_(self.re_2dbf771a, mapcss._tag_capture(capture_tags, 0, tags, u'addr:postcode')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("formato do CEP pode ser melhorado")
            # fixAdd:concat("addr:postcode=",substring(tag("addr:postcode"),0,5),"-",substring(tag("addr:postcode"),5,8))
            err.append({'class': 9018006, 'subclass': 523931624, 'text': mapcss.tr(u'formato do CEP pode ser melhorado', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'addr:postcode=', mapcss.substring(mapcss.tag(tags, u'addr:postcode'), 0, 5), u'-', mapcss.substring(mapcss.tag(tags, u'addr:postcode'), 5, 8))).split('=', 1)])
            }})

        # *[postal_code=~/^[0-9]{8}$/]
        if (u'postal_code' in keys) and \
            ((mapcss.regexp_test_(self.re_2dbf771a, mapcss._tag_capture(capture_tags, 0, tags, u'postal_code')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("formato do CEP pode ser melhorado")
            # fixAdd:concat("postal_code=",substring(tag("postal_code"),0,5),"-",substring(tag("postal_code"),5,8))
            err.append({'class': 9018006, 'subclass': 1234269468, 'text': mapcss.tr(u'formato do CEP pode ser melhorado', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'postal_code=', mapcss.substring(mapcss.tag(tags, u'postal_code'), 0, 5), u'-', mapcss.substring(mapcss.tag(tags, u'postal_code'), 5, 8))).split('=', 1)])
            }})

        # *["addr:postcode"=~/^[0-9]{5}( |\.)[0-9]{3}$/]
        if (u'addr:postcode' in keys) and \
            ((mapcss.regexp_test_(self.re_57bee688, mapcss._tag_capture(capture_tags, 0, tags, u'addr:postcode')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("formato do CEP pode ser melhorado")
            # fixAdd:concat("addr:postcode=",replace(replace(tag("addr:postcode")," ","-"),".","-"))
            err.append({'class': 9018006, 'subclass': 308348773, 'text': mapcss.tr(u'formato do CEP pode ser melhorado', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'addr:postcode=', mapcss.replace(mapcss.replace(mapcss.tag(tags, u'addr:postcode'), u' ', u'-'), u'.', u'-'))).split('=', 1)])
            }})

        # *["postal_code"=~/^[0-9]{5}( |\.)[0-9]{3}$/]
        if (u'postal_code' in keys) and \
            ((mapcss.regexp_test_(self.re_57bee688, mapcss._tag_capture(capture_tags, 0, tags, u'postal_code')))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("formato do CEP pode ser melhorado")
            # fixAdd:concat("postal_code=",replace(replace(tag("postal_code")," ","-"),".","-"))
            err.append({'class': 9018006, 'subclass': 1211220107, 'text': mapcss.tr(u'formato do CEP pode ser melhorado', capture_tags), 'fix': {
                '+': dict([
                    (mapcss.concat(u'postal_code=', mapcss.replace(mapcss.replace(mapcss.tag(tags, u'postal_code'), u' ', u'-'), u'.', u'-'))).split('=', 1)])
            }})

        # *["addr:postcode"]["addr:postcode"!~/^[0-9]{5}-[0-9]{3}$/]
        # *[postal_code][postal_code!~/^[0-9]{5}-[0-9]{3}$/]
        if (u'addr:postcode' in keys or u'postal_code' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'addr:postcode') and not mapcss.regexp_test_(self.re_1ffe94a9, mapcss._tag_capture(capture_tags, 1, tags, u'addr:postcode'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'postal_code') and not mapcss.regexp_test_(self.re_1ffe94a9, mapcss._tag_capture(capture_tags, 1, tags, u'postal_code')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} (CEP) em formato diferente de NNNNN-NNN","{0.key}")
            err.append({'class': 9018002, 'subclass': 1843994632, 'text': mapcss.tr(u'{0} (CEP) em formato diferente de NNNNN-NNN', capture_tags, u'{0.key}')})

        # *[alt_source][source]
        if (u'alt_source' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'alt_source') and mapcss._tag_capture(capture_tags, 1, tags, u'source'))):
            # throwWarning:tr("{0} deve estar incluído em {1}, separado por '';'' caso necessário","{0.key}","{1.key}")
            err.append({'class': 9018020, 'subclass': 512568644, 'text': mapcss.tr(u'{0} deve estar incluído em {1}, separado por \'\';\'\' caso necessário', capture_tags, u'{0.key}', u'{1.key}')})

        # *[landuse?]
        if (u'landuse' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'landuse') in ('yes', 'true', '1'))):
            # throwWarning:tr("especificar valor correto para {0} ao invés de ''{1}''","{0.key}",tag("landuse"))
            err.append({'class': 9018021, 'subclass': 2004192493, 'text': mapcss.tr(u'especificar valor correto para {0} ao invés de \'\'{1}\'\'', capture_tags, u'{0.key}', mapcss.tag(tags, u'landuse'))})

        # *[long_name]
        if (u'long_name' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'long_name'))):
            # throwWarning:tr("chave inválida: {0}","{0.key}")
            # suggestAlternative:"alt_name"
            # suggestAlternative:"name"
            # suggestAlternative:"official_name"
            err.append({'class': 9018022, 'subclass': 1648910015, 'text': mapcss.tr(u'chave inválida: {0}', capture_tags, u'{0.key}')})

        # *["building:levels"<1]
        if (u'building:levels' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'building:levels') < 1)):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com valor inválido","{0.key}")
            err.append({'class': 9018002, 'subclass': 154478605, 'text': mapcss.tr(u'{0} com valor inválido', capture_tags, u'{0.key}')})

        # *[hires?]
        if (u'hires' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'hires') in ('yes', 'true', '1'))):
            # throwWarning:tr("não se deve utilizar {0} para demarcar áreas de cobertura de imagem","{0.key}")
            err.append({'class': 9018023, 'subclass': 1394305840, 'text': mapcss.tr(u'não se deve utilizar {0} para demarcar áreas de cobertura de imagem', capture_tags, u'{0.key}')})

        # *[tourism=motel][amenity!=love_hotel]
        # *[name=~/(?i)\bmotel\b/][amenity!=love_hotel]
        if (u'name' in keys or u'tourism' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'tourism') == u'motel' and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != u'love_hotel') or \
            (mapcss.regexp_test_(self.re_01454d46, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'amenity') != u'love_hotel')):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("ausência de tag ''{0}''","{1.value}")
            # fixAdd:"{1.key}={1.value}"
            err.append({'class': 9018006, 'subclass': 444111908, 'text': mapcss.tr(u'ausência de tag \'\'{0}\'\'', capture_tags, u'{1.value}'), 'fix': {
                '+': dict([
                    [u'{1.key}',u'{1.value}']])
            }})

        # *[amenity=love_hotel][tourism][tourism!=motel]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'love_hotel' and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') and mapcss._tag_capture(capture_tags, 2, tags, u'tourism') != u'motel')):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("provavelmente deve ser ''{0}={1}''","{2.key}","{2.value}")
            err.append({'class': 9018002, 'subclass': 2021262051, 'text': mapcss.tr(u'provavelmente deve ser \'\'{0}={1}\'\'', capture_tags, u'{2.key}', u'{2.value}')})

        # *[name=~/(?i)^motel\b/][tourism!=motel]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_5cd37790, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'tourism') != u'motel')):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("motel classificado incorretamente")
            # suggestAlternative:"tourism=motel"
            err.append({'class': 9018002, 'subclass': 2096064741, 'text': mapcss.tr(u'motel classificado incorretamente', capture_tags)})

        # *[aeroway=aerodrome][!icao]
        # *[aeroway=helipad][!icao]
        if (u'aeroway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'aerodrome' and not mapcss._tag_capture(capture_tags, 1, tags, u'icao')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'helipad' and not mapcss._tag_capture(capture_tags, 1, tags, u'icao'))):
            # throwOther:tr("{0} sem tag {1}","{0.value}","{1.key}")
            err.append({'class': 9018025, 'subclass': 1760501517, 'text': mapcss.tr(u'{0} sem tag {1}', capture_tags, u'{0.value}', u'{1.key}')})

        # *[aeroway=aerodrome][name=~/(?i).*airport$/]
        # *[aeroway=helipad][name=~/(?i).*heliport$/]
        if (u'aeroway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'aerodrome' and mapcss.regexp_test_(self.re_6efb8049, mapcss._tag_capture(capture_tags, 1, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'helipad' and mapcss.regexp_test_(self.re_6566db6a, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com nome em inglês","{0.tag}")
            err.append({'class': 9018002, 'subclass': 134725283, 'text': mapcss.tr(u'{0} com nome em inglês', capture_tags, u'{0.tag}')})

        # *[aeroway=aerodrome][name=~/(?i)^Aer(ódromo|oporto) de.*/]
        # *[aeroway=helipad][name=~/(?i)^Helipo(n|r)to.*/]
        if (u'aeroway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'aerodrome' and mapcss.regexp_test_(self.re_6024a566, mapcss._tag_capture(capture_tags, 1, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'helipad' and mapcss.regexp_test_(self.re_139e342b, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("conferir se existe nome oficial do {0}","{0.value}")
            err.append({'class': 9018002, 'subclass': 2002284471, 'text': mapcss.tr(u'conferir se existe nome oficial do {0}', capture_tags, u'{0.value}')})

        # *[aeroway=aerodrome][ref]
        if (u'aeroway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'aeroway') == u'aerodrome' and mapcss._tag_capture(capture_tags, 1, tags, u'ref'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("''{0}'' não faz sentido em aeroporto","{1.key}")
            err.append({'class': 9018002, 'subclass': 339634841, 'text': mapcss.tr(u'\'\'{0}\'\' não faz sentido em aeroporto', capture_tags, u'{1.key}')})

        # *[waterway][layer<0][!tunnel]
        if (u'waterway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'layer') < 0 and not mapcss._tag_capture(capture_tags, 2, tags, u'tunnel'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} negativo de {1} com ausência de {2}","{1.key}","{0.key}","{2.key}")
            err.append({'class': 9018002, 'subclass': 1476002587, 'text': mapcss.tr(u'{0} negativo de {1} com ausência de {2}', capture_tags, u'{1.key}', u'{0.key}', u'{2.key}')})

        # *[waterway][layer>0][!bridge]
        if (u'waterway' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'waterway') and mapcss._tag_capture(capture_tags, 1, tags, u'layer') > 0 and not mapcss._tag_capture(capture_tags, 2, tags, u'bridge'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} positivo de {1} com ausência de {2}","{1.key}","{0.key}","{2.key}")
            err.append({'class': 9018002, 'subclass': 1137415389, 'text': mapcss.tr(u'{0} positivo de {1} com ausência de {2}', capture_tags, u'{1.key}', u'{0.key}', u'{2.key}')})

        # *[layer][!building][!highway][man_made!=pipeline][!railway][!waterway]
        if (u'layer' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'layer') and not mapcss._tag_capture(capture_tags, 1, tags, u'building') and not mapcss._tag_capture(capture_tags, 2, tags, u'highway') and mapcss._tag_capture(capture_tags, 3, tags, u'man_made') != u'pipeline' and not mapcss._tag_capture(capture_tags, 4, tags, u'railway') and not mapcss._tag_capture(capture_tags, 5, tags, u'waterway'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("possível uso incorreto de {0} no objeto","{0.key}")
            err.append({'class': 9018002, 'subclass': 373443518, 'text': mapcss.tr(u'possível uso incorreto de {0} no objeto', capture_tags, u'{0.key}')})

        # *[name=~/^(?i)(?u)edifício.*/][!building]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_38a8f0ff, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'building'))):
            # throwWarning:tr("possível ausência de tag {0}","{1.key}")
            err.append({'class': 9018026, 'subclass': 1417041710, 'text': mapcss.tr(u'possível ausência de tag {0}', capture_tags, u'{1.key}')})

        # *[route=ferry][!duration]
        if (u'route' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'route') == u'ferry' and not mapcss._tag_capture(capture_tags, 1, tags, u'duration'))):
            # throwWarning:tr("ausência do tempo de duração ({0}) da balsa","{1.key}")
            err.append({'class': 9018027, 'subclass': 1289884816, 'text': mapcss.tr(u'ausência do tempo de duração ({0}) da balsa', capture_tags, u'{1.key}')})

        # *[building][!wheelchair]
        if (u'building' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'building') and not mapcss._tag_capture(capture_tags, 1, tags, u'wheelchair'))):
            # throwOther:tr("{0} sem tag de acessibilidade ({1})","{0.key}","{1.key}")
            err.append({'class': 9018028, 'subclass': 1627625912, 'text': mapcss.tr(u'{0} sem tag de acessibilidade ({1})', capture_tags, u'{0.key}', u'{1.key}')})

        # *[name=~/^(?i)(?u)praça.*/][!leisure][landuse=~/^(forest|grass|greenfield|meadow|orchard)$/]
        # *[name=~/^(?i)(?u)praça.*/][!leisure][natural=~/^(grassland|heath|scrub|wood)$/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_4a8ca94e, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'leisure') and mapcss.regexp_test_(self.re_05a345c7, mapcss._tag_capture(capture_tags, 2, tags, u'landuse'))) or \
            (mapcss.regexp_test_(self.re_4a8ca94e, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and not mapcss._tag_capture(capture_tags, 1, tags, u'leisure') and mapcss.regexp_test_(self.re_12b48afb, mapcss._tag_capture(capture_tags, 2, tags, u'natural')))):
            # throwWarning:tr("possível definição incorreta para praça: ''{0}''","{2.key}")
            # suggestAlternative:"leisure=park"
            err.append({'class': 9018029, 'subclass': 80498829, 'text': mapcss.tr(u'possível definição incorreta para praça: \'\'{0}\'\'', capture_tags, u'{2.key}')})

        # *[wikipedia][wikipedia!~/^pt:/]
        if (u'wikipedia' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'wikipedia') and not mapcss.regexp_test_(self.re_17fd35b3, mapcss._tag_capture(capture_tags, 1, tags, u'wikipedia')))):
            # throwWarning:tr("utilizar prefixo em português (pt:) para {0}","{0.key}")
            err.append({'class': 9018030, 'subclass': 1219382195, 'text': mapcss.tr(u'utilizar prefixo em português (pt:) para {0}', capture_tags, u'{0.key}')})

        # *[name=~/.*\(.*\).*/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_7e9dfbe7, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com parênteses. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.","{0.key}")
            err.append({'class': 9018002, 'subclass': 1406083581, 'text': mapcss.tr(u'{0} com parênteses. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.', capture_tags, u'{0.key}')})

        # *[name=~/ - /]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_6b25b0c5, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com traço. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.","{0.key}")
            err.append({'class': 9018002, 'subclass': 1992839086, 'text': mapcss.tr(u'{0} com traço. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.', capture_tags, u'{0.key}')})

        # *[name=~/, /]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_4da7cb86, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com vírgula. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.","{0.key}")
            err.append({'class': 9018002, 'subclass': 659472938, 'text': mapcss.tr(u'{0} com vírgula. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.', capture_tags, u'{0.key}')})

        # *[name=~/: /]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_657f3be3, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("{0} com dois pontos. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.","{0.key}")
            err.append({'class': 9018002, 'subclass': 338682039, 'text': mapcss.tr(u'{0} com dois pontos. Usar short_name para siglas. Se necessário alt_name ou description para outros casos.', capture_tags, u'{0.key}')})

        # *[name=~/ ou /]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_131cc885, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # throwWarning:tr("nome utilizado de forma incorreta")
            # suggestAlternative:"name e alt_name"
            err.append({'class': 9018031, 'subclass': 23034604, 'text': mapcss.tr(u'nome utilizado de forma incorreta', capture_tags)})

        # relation[boundary][type!=boundary]
        if (u'boundary' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'boundary') and mapcss._tag_capture(capture_tags, 1, tags, u'type') != u'boundary')):
            # throwWarning:tr("{0} deve possuir ''type=boundary''","{0.key}")
            err.append({'class': 9018048, 'subclass': 404484969, 'text': mapcss.tr(u'{0} deve possuir \'\'type=boundary\'\'', capture_tags, u'{0.key}')})

        # relation[type=boundary][!boundary]
        if (u'type' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'type') == u'boundary' and not mapcss._tag_capture(capture_tags, 1, tags, u'boundary'))):
            # throwWarning:tr("{0} deve ser utilizado junto com {1}","{0.tag}","{1.key}")
            err.append({'class': 9018049, 'subclass': 919335957, 'text': mapcss.tr(u'{0} deve ser utilizado junto com {1}', capture_tags, u'{0.tag}', u'{1.key}')})

        # relation[admin_level][boundary!=administrative]
        if (u'admin_level' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'admin_level') and mapcss._tag_capture(capture_tags, 1, tags, u'boundary') != u'administrative')):
            # group:tr("Brasil - Correções e melhorias")
            # throwError:tr("ausência de boundary=administrative")
            # fixAdd:"boundary=administrative"
            err.append({'class': 9018006, 'subclass': 585818652, 'text': mapcss.tr(u'ausência de boundary=administrative', capture_tags), 'fix': {
                '+': dict([
                    [u'boundary',u'administrative']])
            }})

        # relation[boundary=administrative][!admin_level]
        if (u'boundary' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == u'administrative' and not mapcss._tag_capture(capture_tags, 1, tags, u'admin_level'))):
            # throwError:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
            err.append({'class': 9018033, 'subclass': 1254141393, 'text': mapcss.tr(u'{0} deve possuir {1}', capture_tags, u'{0.tag}', u'{1.key}')})

        # relation[place][place!~/^(city_block|farm|hamlet|island|islet|isolated_dwelling|neighbourhood|square)$/][!admin_level][!boundary]
        if (u'place' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'place') and not mapcss.regexp_test_(self.re_58f616c9, mapcss._tag_capture(capture_tags, 1, tags, u'place')) and not mapcss._tag_capture(capture_tags, 2, tags, u'admin_level') and not mapcss._tag_capture(capture_tags, 3, tags, u'boundary'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("local com ausência/incoerência de limite administrativo")
            err.append({'class': 9018002, 'subclass': 1798440430, 'text': mapcss.tr(u'local com ausência/incoerência de limite administrativo', capture_tags)})

        # relation[boundary=administrative][type=multipolygon]
        if (u'boundary' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == u'administrative' and mapcss._tag_capture(capture_tags, 1, tags, u'type') == u'multipolygon')):
            # group:tr("Brasil - Correções e melhorias")
            # throwError:tr("relação deve ser do tipo ''type=boundary''")
            # fixAdd:"type=boundary"
            err.append({'class': 9018006, 'subclass': 150723186, 'text': mapcss.tr(u'relação deve ser do tipo \'\'type=boundary\'\'', capture_tags), 'fix': {
                '+': dict([
                    [u'type',u'boundary']])
            }})

        # *[boundary=national_park][!name]
        # *[boundary=protected_area][!name]
        # *[leisure=nature_reserve][!name]
        if (u'boundary' in keys or u'leisure' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == u'national_park' and not mapcss._tag_capture(capture_tags, 1, tags, u'name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == u'protected_area' and not mapcss._tag_capture(capture_tags, 1, tags, u'name')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == u'nature_reserve' and not mapcss._tag_capture(capture_tags, 1, tags, u'name'))):
            # throwWarning:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
            err.append({'class': 9018033, 'subclass': 1492609299, 'text': mapcss.tr(u'{0} deve possuir {1}', capture_tags, u'{0.tag}', u'{1.key}')})

        # *[boundary=protected_area][!protect_class]
        if (u'boundary' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'boundary') == u'protected_area' and not mapcss._tag_capture(capture_tags, 1, tags, u'protect_class'))):
            # throwWarning:tr("{0} deve possuir {1}","{0.tag}","{1.key}")
            err.append({'class': 9018033, 'subclass': 822952800, 'text': mapcss.tr(u'{0} deve possuir {1}', capture_tags, u'{0.tag}', u'{1.key}')})

        # *[protect_class][protect_class!~/^(1(a|b)?|[1-9][0-9]?)$/]
        if (u'protect_class' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'protect_class') and not mapcss.regexp_test_(self.re_5ac7053e, mapcss._tag_capture(capture_tags, 1, tags, u'protect_class')))):
            # throwWarning:tr("valor incorreto para {0}","{0.key}")
            err.append({'class': 9018034, 'subclass': 1459161459, 'text': mapcss.tr(u'valor incorreto para {0}', capture_tags, u'{0.key}')})

        # *[protect_class][boundary!=protected_area]
        if (u'protect_class' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'protect_class') and mapcss._tag_capture(capture_tags, 1, tags, u'boundary') != u'protected_area')):
            # throwWarning:tr("ausência de boundary=protected_area")
            err.append({'class': 9018035, 'subclass': 1208814760, 'text': mapcss.tr(u'ausência de boundary=protected_area', capture_tags)})

        # relation[destination][type!=waterway]
        if (u'destination' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'destination') and mapcss._tag_capture(capture_tags, 1, tags, u'type') != u'waterway')):
            # throwWarning:tr("{0} deve ser usado apenas em ways","{0.key}")
            err.append({'class': 9018036, 'subclass': 1752813638, 'text': mapcss.tr(u'{0} deve ser usado apenas em ways', capture_tags, u'{0.key}')})

        # *[amenity][!opening_hours]
        # *[shop][!opening_hours]
        if (u'amenity' in keys or u'shop' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') and not mapcss._tag_capture(capture_tags, 1, tags, u'opening_hours')) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'shop') and not mapcss._tag_capture(capture_tags, 1, tags, u'opening_hours'))):
            # throwOther:tr("{0} sem {1}","{0.key}","{1.key}")
            err.append({'class': 9018038, 'subclass': 1861306703, 'text': mapcss.tr(u'{0} sem {1}', capture_tags, u'{0.key}', u'{1.key}')})

        # *[name=~/.* D(a|e|o)s? .*/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_2ffc377d, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("''da'', ''de'' e ''do'' são minúsculos nos nomes em português")
            err.append({'class': 9018002, 'subclass': 1986668346, 'text': mapcss.tr(u'\'\'da\'\', \'\'de\'\' e \'\'do\'\' são minúsculos nos nomes em português', capture_tags)})

        # *[name=~/^[a-z].*/]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_39d67968, mapcss._tag_capture(capture_tags, 0, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("nome iniciando com letra minúscula")
            err.append({'class': 9018002, 'subclass': 167462302, 'text': mapcss.tr(u'nome iniciando com letra minúscula', capture_tags)})

        # *[alt_ref]
        if (u'alt_ref' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'alt_ref'))):
            # throwWarning:tr("o conteúdo de {0} deve fazer parte de ref, separado por ;","{0.key}")
            # suggestAlternative:"ref"
            err.append({'class': 9018039, 'subclass': 722411109, 'text': mapcss.tr(u'o conteúdo de {0} deve fazer parte de ref, separado por ;', capture_tags, u'{0.key}')})

        # *[source=~/.*,.*/]
        # *["source:ref"=~/.*,.*/]
        # *["source:name"=~/.*,.*/]
        if (u'source' in keys or u'source:name' in keys or u'source:ref' in keys) and \
            ((mapcss.regexp_test_(self.re_34f65002, mapcss._tag_capture(capture_tags, 0, tags, u'source'))) or \
            (mapcss.regexp_test_(self.re_34f65002, mapcss._tag_capture(capture_tags, 0, tags, u'source:ref'))) or \
            (mapcss.regexp_test_(self.re_34f65002, mapcss._tag_capture(capture_tags, 0, tags, u'source:name')))):
            # throwOther:tr("utilizar ; como separador de valores em {0}","{0.key}")
            err.append({'class': 9018040, 'subclass': 2114349281, 'text': mapcss.tr(u'utilizar ; como separador de valores em {0}', capture_tags, u'{0.key}')})

        # *[surface][eval(number_of_tags())=1]
        if (u'surface' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'surface') and len(tags) == 1)):
            # throwWarning:tr("objeto incompleto: possui apenas {0}","{0.key}")
            err.append({'class': 9018041, 'subclass': 1776991136, 'text': mapcss.tr(u'objeto incompleto: possui apenas {0}', capture_tags, u'{0.key}')})

        # *[name][surface][eval(number_of_tags())=2]
        # *[name][website][eval(number_of_tags())=2]
        if (u'name' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'surface') and len(tags) == 2) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'name') and mapcss._tag_capture(capture_tags, 1, tags, u'website') and len(tags) == 2)):
            # throwWarning:tr("objeto incompleto: possui apenas {0} e {1}","{0.key}","{1.key}")
            err.append({'class': 9018042, 'subclass': 626126700, 'text': mapcss.tr(u'objeto incompleto: possui apenas {0} e {1}', capture_tags, u'{0.key}', u'{1.key}')})

        # *[leisure=pitch][sport=tennis][surface=unpaved]
        if (u'leisure' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'leisure') == u'pitch' and mapcss._tag_capture(capture_tags, 1, tags, u'sport') == u'tennis' and mapcss._tag_capture(capture_tags, 2, tags, u'surface') == u'unpaved')):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("{0} com superfície incorreta","{2.key}")
            # suggestAlternative:"surface=clay"
            # fixAdd:"surface=clay"
            err.append({'class': 9018006, 'subclass': 1659179489, 'text': mapcss.tr(u'{0} com superfície incorreta', capture_tags, u'{2.key}'), 'fix': {
                '+': dict([
                    [u'surface',u'clay']])
            }})

        # *[amenity=fuel][name=~/(?i)(?u)\b(Ale|BR|Esso|Ipiranga|Petrobr(á|a)s|Shell|Texaco)\b/]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'fuel' and mapcss.regexp_test_(self.re_604bb645, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("uso incorreto da bandeira do posto")
            # suggestAlternative:"brand"
            err.append({'class': 9018002, 'subclass': 935774110, 'text': mapcss.tr(u'uso incorreto da bandeira do posto', capture_tags)})

        # *[/_[0-9]$/][!"is_in:iso_3166_2"]
        if ((mapcss._tag_capture(capture_tags, 0, tags, self.re_57b8ef8e) and not mapcss._tag_capture(capture_tags, 1, tags, u'is_in:iso_3166_2'))):
            # throwError:tr("chave inválida: {0}","{0.key}")
            err.append({'class': 9018022, 'subclass': 331369569, 'text': mapcss.tr(u'chave inválida: {0}', capture_tags, u'{0.key}')})

        # *["addr:housenumber"=~/(?i)^s(\.|-| )?\/?n\.?º?$/][!note]
        if (u'addr:housenumber' in keys) and \
            ((mapcss.regexp_test_(self.re_0b27200b, mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber')) and not mapcss._tag_capture(capture_tags, 1, tags, u'note'))):
            # group:tr("Brasil - Correções e melhorias")
            # throwWarning:tr("não utilizar ''{0}'' para locais sem número",tag("addr:housenumber"))
            # suggestAlternative:"note"
            # fixRemove:"addr:housenumber"
            # fixAdd:"note=Local sem número"
            err.append({'class': 9018006, 'subclass': 931902546, 'text': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', capture_tags, mapcss.tag(tags, u'addr:housenumber')), 'fix': {
                '+': dict([
                    [u'note',u'Local sem número']]),
                '-': ([
                    u'addr:housenumber'])
            }})

        # *["addr:housenumber"=~/(?i)^s(\.|-| )?\/?n\.?º?$/][note]
        if (u'addr:housenumber' in keys) and \
            ((mapcss.regexp_test_(self.re_0b27200b, mapcss._tag_capture(capture_tags, 0, tags, u'addr:housenumber')) and mapcss._tag_capture(capture_tags, 1, tags, u'note'))):
            # throwWarning:tr("não utilizar ''{0}'' para locais sem número",tag("addr:housenumber"))
            # suggestAlternative:"note"
            err.append({'class': 9018043, 'subclass': 1717284811, 'text': mapcss.tr(u'não utilizar \'\'{0}\'\' para locais sem número', capture_tags, mapcss.tag(tags, u'addr:housenumber'))})

        # *[source=~/(?i)google/]
        if (u'source' in keys) and \
            ((mapcss.regexp_test_(self.re_2e8e4f2b, mapcss._tag_capture(capture_tags, 0, tags, u'source')))):
            # throwError:tr("objeto contém Google como source")
            err.append({'class': 9018044, 'subclass': 1313403884, 'text': mapcss.tr(u'objeto contém Google como source', capture_tags)})

        # *[amenity=townhall][name=~/^(?i)(?u)c(â|a)mara\b/]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'townhall' and mapcss.regexp_test_(self.re_46ab4d8d, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("câmara de vereadores mapeada incorretamente")
            # suggestAlternative:"office=government + government=legislative"
            err.append({'class': 9018002, 'subclass': 129695507, 'text': mapcss.tr(u'câmara de vereadores mapeada incorretamente', capture_tags)})

        # *[office=government][government!=legislative][name=~/^(?i)(?u)c(â|a)mara\b/]
        if (u'office' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'office') == u'government' and mapcss._tag_capture(capture_tags, 1, tags, u'government') != u'legislative' and mapcss.regexp_test_(self.re_46ab4d8d, mapcss._tag_capture(capture_tags, 2, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("ausência de government=legislative")
            err.append({'class': 9018002, 'subclass': 869412796, 'text': mapcss.tr(u'ausência de government=legislative', capture_tags)})

        # *[amenity=townhall][name=~/^(?i)(?u)c((â|a)me|ama)ra\b/]
        # *[office=government][name=~/^(?i)(?u)c((â|a)me|ama)ra\b/]
        if (u'amenity' in keys or u'office' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'townhall' and mapcss.regexp_test_(self.re_793b22ec, mapcss._tag_capture(capture_tags, 1, tags, u'name'))) or \
            (mapcss._tag_capture(capture_tags, 0, tags, u'office') == u'government' and mapcss.regexp_test_(self.re_793b22ec, mapcss._tag_capture(capture_tags, 1, tags, u'name')))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("erro de ortografia em ''câmara''")
            err.append({'class': 9018002, 'subclass': 212328084, 'text': mapcss.tr(u'erro de ortografia em \'\'câmara\'\'', capture_tags)})

        # *[amenity=charging_station]
        if (u'amenity' in keys) and \
            ((mapcss._tag_capture(capture_tags, 0, tags, u'amenity') == u'charging_station')):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("possivelmente deve ser amenity=fuel")
            err.append({'class': 9018002, 'subclass': 128902291, 'text': mapcss.tr(u'possivelmente deve ser amenity=fuel', capture_tags)})

        # *[name=~/(?i)^Borrach(aria|eiro)/][shop=tyres][!repair]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_126ba9a9, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'shop') == u'tyres' and not mapcss._tag_capture(capture_tags, 2, tags, u'repair'))):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("borracharia sem ''repair=yes''")
            # suggestAlternative:"repair=yes"
            err.append({'class': 9018002, 'subclass': 817061630, 'text': mapcss.tr(u'borracharia sem \'\'repair=yes\'\'', capture_tags)})

        # *[name=~/(?i)^Borrach(aria|eiro)/][shop!=tyres]
        if (u'name' in keys) and \
            ((mapcss.regexp_test_(self.re_126ba9a9, mapcss._tag_capture(capture_tags, 0, tags, u'name')) and mapcss._tag_capture(capture_tags, 1, tags, u'shop') != u'tyres')):
            # group:tr("Brasil - Verificar")
            # throwWarning:tr("borracharia sem ''shop=tyres''")
            # suggestAlternative:"shop=tyres"
            err.append({'class': 9018002, 'subclass': 1324999258, 'text': mapcss.tr(u'borracharia sem \'\'shop=tyres\'\'', capture_tags)})

        return err


from plugins.Plugin import TestPluginCommon


class Test(TestPluginCommon):
    def test(self):
        n = MapCSS_josm_Rules_Brazilian_Specific(None)
        n.init(None)
        data = {'id': 0, 'lat': 0, 'lon': 0}


