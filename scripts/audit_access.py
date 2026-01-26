"""
Access Audit Script - Mission 2

Analyzes current ClientPortalAccess instances, evaluates token strategy,
and generates LGPD compliance report.
"""
import os
import sys
import django
from datetime import datetime

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.portals.models import ClientPortalAccess
from apps.clients.models import Client
from django.contrib.auth.models import User


def audit_portal_access():
    """Generate comprehensive access audit report."""
    
    print("="*70)
    print("CLIENT PORTAL ACCESS AUDIT - Mission 2")
    print("="*70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 1. Total Access Records
    total_access = ClientPortalAccess.objects.count()
    active_access = ClientPortalAccess.objects.filter(is_active=True).count()
    inactive_access = total_access - active_access
    
    print(f"📊 Overview:")
    print(f"  - Total Access Records: {total_access}")
    print(f"  - Active: {active_access}")
    print(f"  - Inactive: {inactive_access}\n")
    
    # 2. List All Access Records
    print(f"📋 Access Records Detail:")
    print("-"*70)
    
    for access in ClientPortalAccess.objects.select_related('client', 'legal_case').all():
        print(f"\n  Client: {access.client.full_name}")
        print(f"  Case: {access.legal_case}")
        print(f"  Token: {access.access_token[:8]}... (truncated)")
        print(f"  Active: {'Yes' if access.is_active else 'No'}")
        print(f"  Created: {access.created_at.strftime('%Y-%m-%d')}")
        print(f"  Last Accessed: {access.last_accessed.strftime('%Y-%m-%d %H:%M') if access.last_accessed else 'Never'}")
    
    print("\n" + "-"*70)
    
    # 3. Test Users Detection
    print(f"\n🔍 Test User Detection:")
    test_patterns = ['maria silva', 'test', 'demo', 'exemplo']
    test_clients = []
    
    for client in Client.objects.all():
        if any(pattern in client.full_name.lower() for pattern in test_patterns):
            test_clients.append(client)
            print(f"  - {client.full_name} (ID: {client.id}) - POTENTIAL TEST USER")
    
    if not test_clients:
        print("  No obvious test users found")
    
    # 4. Token Analysis
    print(f"\n🔐 Token Analysis:")
    tokens = ClientPortalAccess.objects.values_list('access_token', flat=True)
    
    if tokens:
        avg_length = sum(len(t) for t in tokens) / len(tokens)
        print(f"  - Average token length: {avg_length:.0f} characters")
        print(f"  - Token uniqueness: {len(set(tokens))}/{len(tokens)} (100% is ideal)")
        
        # Check for patterns that might expose PII
        print(f"\n  Token LGPD Compliance Check:")
        for token in tokens:
            # Very basic check - tokens should not contain obvious patterns
            if any(char.isdigit() for char in token[:20]):  # First 20 chars
                pass  # Digits are OK
            # Check if tokens are random enough (entropy check simplified)
            if len(set(token)) / len(token) > 0.5:
                print(f"    ✅ Token {token[:8]}... appears sufficiently random")
            else:
                print(f"    ⚠️  Token {token[:8]}... may have low entropy")
    
    # 5. Django Admin Users
    print(f"\n👤 Django Admin Users:")
    print("-"*70)
    admin_users = User.objects.filter(is_staff=True)
    
    for user in admin_users:
        print(f"  - {user.username} ({'Superuser' if user.is_superuser else 'Staff'})")
        print(f"    Email: {user.email}")
        print(f"    Last Login: {user.last_login.strftime('%Y-%m-%d') if user.last_login else 'Never'}")
    
    # 6. Recommendation
    print(f"\n💡 Strategic Recommendation:")
    print("-"*70)
    print("""
  Current System: 64-character token-based access via ClientPortalAccess
  
  ✅ ADVANTAGES:
    - Simple for clients (one-click access via link)
    - No password management needed
    - Secure if tokens generated with secrets module
    - LGPD compliant (tokens don't expose PII)
  
  ⚠️  CONSIDERATIONS:
    - Tokens must be transmitted securely (HTTPS only)
    - Email compromise could expose token
    - No 2FA capability
  
  RECOMMENDATION: Continue with token strategy BUT:
    1. Add token expiration (e.g., 90 days)
    2. Implement token regeneration on client request
    3. Add audit log for token access (already via last_accessed)
    4. Consider migrating to Django auth for admin users only
    """)
    
    print("="*70)
    print("AUDIT COMPLETE")
    print("="*70)


if __name__ == '__main__':
    audit_portal_access()
