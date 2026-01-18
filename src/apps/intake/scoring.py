"""
Enhanced Lead Scoring Algorithm - ClaimScore™

Predictive qualification system for legal leads.
"""
from apps.intake.models import Lead
from typing import Dict


def calculate_claim_score(lead: Lead, triage_data: Dict) -> int:
    """
    ClaimScore™ - Predictive lead qualification algorithm.
    
    Factors (weighted):
    - Urgency indicators (30 points)
    - Documentation readiness (20 points)
    - Case complexity (20 points)
    - Financial viability (15 points)
    - Geographic proximity (15 points)
    
    Args:
        lead: Lead instance
        triage_data: Dictionary with triage responses
    
    Returns:
        Score 0-100 (>60 = qualified)
    """
    score = 50  # Base score
    
    # 1. Urgency Analysis (30 points)
    urgency_keywords = ['urgente', 'imediato', 'prazo', 'vencendo', 'emergência', 'rápido']
    urgency_count = sum(1 for kw in urgency_keywords if kw in str(triage_data).lower())
    score += min(urgency_count * 10, 30)
    
    # 2. Documentation Readiness (20 points)
    if triage_data.get('has_denial_letter') == 'sim':
        score += 20
    elif triage_data.get('has_medical_report') == 'sim':
        score += 15
    elif triage_data.get('has_evidence') == 'sim':
        score += 10
    
    # 3. Case Complexity (inverse scoring - simpler = higher)
    complexity_map = {
        'LIPEDEMA': 15,  # Well-defined legal precedent
        'SUPER': 10,     # More complex, case-by-case
        'CULTURAL': 12,  # Moderate complexity
        'OTHER': 5       # Unknown complexity
    }
    score += complexity_map.get(lead.case_type, 5)
    
    # 4. Financial Viability (15 points)
    employment_status = str(triage_data.get('employment_status', '')).lower()
    if 'empregado' in employment_status or 'clt' in employment_status:
        score += 15
    elif 'autonomo' in employment_status or 'mei' in employment_status:
        score += 10
    elif 'desempregado' in employment_status:
        score += 5  # Still viable with contingency fee
    
    # 5. Geographic Proximity (15 points)
    # DDD 19 = Campinas region (easier logistics)
    contact = lead.contact_info
    if '19' in contact or '(19)' in contact:
        score += 15
    elif any(ddd in contact for ddd in ['11', '13', '15']):  # SP state
        score += 10
    else:
        score += 5  # Remote but still viable
    
    # 6. Bonus: Referral or returning client
    if triage_data.get('referral_source') == 'client':
        score += 10  # Bonus for referrals
    
    return min(score, 100)  # Cap at 100


def get_score_breakdown(lead: Lead, triage_data: Dict) -> Dict:
    """
    Get detailed breakdown of score calculation.
    
    Useful for transparency and debugging.
    """
    breakdown = {
        'base_score': 50,
        'urgency_points': 0,
        'documentation_points': 0,
        'complexity_points': 0,
        'financial_points': 0,
        'geographic_points': 0,
        'bonus_points': 0,
        'total': 0
    }
    
    # Calculate each component
    urgency_keywords = ['urgente', 'imediato', 'prazo', 'vencendo', 'emergência']
    urgency_count = sum(1 for kw in urgency_keywords if kw in str(triage_data).lower())
    breakdown['urgency_points'] = min(urgency_count * 10, 30)
    
    if triage_data.get('has_denial_letter') == 'sim':
        breakdown['documentation_points'] = 20
    elif triage_data.get('has_medical_report') == 'sim':
        breakdown['documentation_points'] = 15
    
    complexity_map = {'LIPEDEMA': 15, 'SUPER': 10, 'CULTURAL': 12, 'OTHER': 5}
    breakdown['complexity_points'] = complexity_map.get(lead.case_type, 5)
    
    employment = str(triage_data.get('employment_status', '')).lower()
    if 'empregado' in employment or 'clt' in employment:
        breakdown['financial_points'] = 15
    elif 'autonomo' in employment:
        breakdown['financial_points'] = 10
    
    contact = lead.contact_info
    if '19' in contact:
        breakdown['geographic_points'] = 15
    elif any(ddd in contact for ddd in ['11', '13', '15']):
        breakdown['geographic_points'] = 10
    
    if triage_data.get('referral_source') == 'client':
        breakdown['bonus_points'] = 10
    
    breakdown['total'] = min(
        sum(breakdown.values()) - breakdown['total'],  # Exclude total from sum
        100
    )
    
    return breakdown
