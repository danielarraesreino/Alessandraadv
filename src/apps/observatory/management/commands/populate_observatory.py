from django.core.management.base import BaseCommand
from apps.observatory.models import HumanRightsCase
from datetime import date

class Command(BaseCommand):
    help = 'Popula o Observatório com casos históricos'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populando Observatório...')
        
        casos = [
            # Século XX
            {
                "name": "Vladimir Herzog",
                "period": "SEC_20",
                "violation_type": "TORTURA",
                "description": "Jornalista assassinado sob tortura nas dependências do DOI-CODI, em São Paulo, durante a Ditadura Militar. Sua morte gerou comoção nacional e impulsionou o movimento pela redemocratização.",
                "date_event": date(1975, 10, 25),
                "location": "São Paulo, SP",
                "impact_level": 10,
                "status": "RECONHECIDO"
            },
            {
                "name": "Rubens Paiva",
                "period": "SEC_20",
                "violation_type": "PERSEGUICAO_POLITICA",
                "description": "Engenheiro e ex-deputado federal, sequestrado e desaparecido por agentes da repressão. Seu caso tornou-se símbolo dos desaparecidos políticos.",
                "date_event": date(1971, 1, 20),
                "location": "Rio de Janeiro, RJ",
                "impact_level": 9,
                "status": "RECONHECIDO"
            },
            {
                "name": "Olga Benário",
                "period": "SEC_20",
                "violation_type": "PERSEGUICAO_POLITICA",
                "description": "Militante comunista deportada pelo governo Getúlio Vargas para a Alemanha Nazista, onde foi morta em uma câmara de gás.",
                "date_event": date(1936, 10, 18),
                "location": "Rio de Janeiro (Deportação)",
                "impact_level": 10,
                "status": "MEMORIA"
            },
            {
                "name": "Chico Mendes",
                "period": "SEC_20",
                "violation_type": "DIREITOS_INDIGENAS",
                "description": "Líder seringueiro e ambientalista assassinado a mando de fazendeiros no Acre. Defensor da Amazônia e dos povos da floresta.",
                "date_event": date(1988, 12, 22),
                "location": "Xapuri, AC",
                "impact_level": 9,
                "status": "RECONHECIDO"
            },
             {
                "name": "Massacre de Eldorado dos Carajás",
                "period": "SEC_20",
                "violation_type": "MASSACRE",
                "description": "Morte de 19 trabalhadores rurais sem-terra pela Polícia Militar do Pará durante uma marcha pacífica.",
                "date_event": date(1996, 4, 17),
                "location": "Eldorado dos Carajás, PA",
                "impact_level": 9,
                "status": "RECONHECIDO"
            },

            # Século XXI
            {
                "name": "Marielle Franco",
                "period": "SEC_21",
                "violation_type": "PERSEGUICAO_POLITICA",
                "description": "Vereadora do Rio de Janeiro e defensora dos direitos humanos, assassinada em uma emboscada. Símbolo da luta contra a violência política e de gênero.",
                "date_event": date(2018, 3, 14),
                "location": "Rio de Janeiro, RJ",
                "impact_level": 10,
                "status": "EM_ANALISE"
            },
            {
                "name": "Amarildo de Souza",
                "period": "SEC_21",
                "violation_type": "VIOLENCIA_POLICIAL",
                "description": "Auxiliar de pedreiro desaparecido após ser detido por policiais militares na UPP da Rocinha. 'Cadê o Amarildo?' virou clamor mundial.",
                "date_event": date(2013, 7, 14),
                "location": "Rio de Janeiro, RJ",
                "impact_level": 9,
                "status": "RECONHECIDO"
            },
            {
                "name": "Bruno Pereira e Dom Phillips",
                "period": "SEC_21",
                "violation_type": "DIREITOS_INDIGENAS",
                "description": "Indigenista brasileiro e jornalista britânico assassinados no Vale do Javari enquanto documentavam crimes ambientais.",
                "date_event": date(2022, 6, 5),
                "location": "Atalaia do Norte, AM",
                "impact_level": 9,
                "status": "EM_ANALISE"
            },
            {
                "name": "Massacre de Paraisópolis",
                "period": "SEC_21",
                "violation_type": "VIOLENCIA_POLICIAL",
                "description": "Nove jovens mortos pisoteados após ação policial em um baile funk na comunidade de Paraisópolis.",
                "date_event": date(2019, 12, 1),
                "location": "São Paulo, SP",
                "impact_level": 8,
                "status": "EM_ANALISE"
            },
            {
                "name": "Crise Yanomami",
                "period": "SEC_21",
                "violation_type": "NEGLIGENCIA_ESTATAL",
                "description": "Crise humanitária e sanitária resultando em desnutrição e mortes evitáveis devido ao garimpo ilegal e negligência governamental.",
                "date_event": date(2023, 1, 20),
                "location": "Roraima, RR",
                "impact_level": 10,
                "status": "EM_ANALISE"
            },
             {
                "name": "João Pedro Mattos",
                "period": "SEC_21",
                "violation_type": "VIOLENCIA_POLICIAL",
                "description": "Adolescente de 14 anos morto dentro de casa durante operação policial conjunta em São Gonçalo.",
                "date_event": date(2020, 5, 18),
                "location": "São Gonçalo, RJ",
                "impact_level": 8,
                "status": "EM_ANALISE"
            },
             {
                "name": "Genivaldo de Jesus Santos",
                "period": "SEC_21",
                "violation_type": "TORTURA",
                "description": "Morto por asfixia mecânica e insuficiência respiratória aguda após ser trancado no porta-malas de uma viatura da PRF transformada em câmara de gás.",
                "date_event": date(2022, 5, 25),
                "location": "Umbaúba, SE",
                "impact_level": 9,
                "status": "EM_ANALISE"
            }
        ]

        for dados in casos:
            HumanRightsCase.objects.get_or_create(
                name=dados['name'],
                defaults=dados
            )
        
        self.stdout.write(self.style.SUCCESS(f'Sucesso! {len(casos)} casos verificados/criados.'))
