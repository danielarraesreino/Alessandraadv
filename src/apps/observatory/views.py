from django.shortcuts import render
from django.db.models import Count
from .models import HumanRightsCase

def observatory_dashboard(request):
    """
    Dashboard principal do Observatório de Direitos Humanos.
    """
    # KPI 1: Total de Casos
    total_cases = HumanRightsCase.objects.count()

    # KPI 2: Casos por Período (Comparativo Séc 20 vs 21)
    cases_by_period = HumanRightsCase.objects.values('period').annotate(count=Count('id')).order_by('period')
    
    # KPI 3: Casos por Tipo de Violação (Top 5)
    cases_by_type = HumanRightsCase.objects.values('violation_type').annotate(count=Count('id')).order_by('-count')[:5]

    # Lista: Memória Viva (Casos de alto impacto)
    highlight_cases = HumanRightsCase.objects.filter(impact_level__gte=8).order_by('-impact_level', '-date_event')[:6]

    # Lista: Todos os casos (para tabela simples)
    all_cases = HumanRightsCase.objects.all().order_by('-date_event')

    # Preparar dados para Chart.js (Arrays simples)
    period_labels = [c['period'] for c in cases_by_period]
    period_data = [c['count'] for c in cases_by_period]
    
    type_labels = [c['violation_type'] for c in cases_by_type]
    type_data = [c['count'] for c in cases_by_type]

    context = {
        'total_cases': total_cases,
        'highlight_cases': highlight_cases,
        'all_cases': all_cases,
        # Chart Data
        'period_labels': period_labels,
        'period_data': period_data,
        'type_labels': type_labels,
        'type_data': type_data,
    }

    return render(request, 'observatory/dashboard.html', context)
