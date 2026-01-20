from apps.intake.models import Lead, LeadAnalysis

def calculate_claim_score(lead: Lead) -> int:
    """
    Calculates the ClaimScore based on lead data.
    
    Rules (Simplified for Phase 1):
    - Lipedema: +20 points (Niche focus)
    - Super: +20 points
    - Contact Info (Email + Phone): +10 points
    - Negative keywords: -30 points
    """
    score = 50 # Base score
    analysis_log = {
        "positive": [],
        "negative": [],
        "summary": "Análise Inicial Automática"
    }
    
    # 1. Case Type Analysis
    if lead.case_type == 'LIPEDEMA':
        score += 20
        analysis_log["positive"].append("Nicho de Alto Valor: Lipedema")
    elif lead.case_type == 'SUPER':
        score += 20
        analysis_log["positive"].append("Demanda Recorrente: Superendividamento")
        
    # 2. Data Completeness
    if lead.contact_info and '@' in lead.contact_info:
        score += 10
        analysis_log["positive"].append("Dados de contato completos")
        
    # 3. Triage Data Analysis (Simulated)
    # real implementation would parse the 'triage_data' JSON
    triage = lead.triage_data or {}
    
    # Example logic: if client has medical "laudo"
    if triage.get('tem_laudo'):
        score += 15
        analysis_log["positive"].append("Possui Laudo Médico")
    
    # Cap score
    score = max(0, min(100, score))
    
    # Update Lead
    lead.score = score
    if score >= 70:
        lead.viability_status = 'HIGH'
        lead.is_qualified = True
    elif score >= 50:
        lead.viability_status = 'MEDIUM'
    else:
        lead.viability_status = 'LOW'
        
    lead.save()
    
    # Create Analysis Record
    LeadAnalysis.objects.update_or_create(
        lead=lead,
        defaults={
            "summary": f"Lead classificado com score {score}. {analysis_log['summary']}",
            "positive_points": analysis_log["positive"],
            "negative_points": analysis_log["negative"],
            "recommended_action": "Agendar Triagem Humana" if score >= 50 else "Monitorar"
        }
    )
    
    return score
