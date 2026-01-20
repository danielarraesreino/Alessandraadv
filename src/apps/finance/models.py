from django.db import models
from django.utils import timezone

class AccountPayable(models.Model):
    """
    Finance Module: Accounts Payable.
    Simple administration of office expenses.
    """
    
    STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('PAID', 'Pago'),
        ('CANCELLED', 'Cancelado'),
    ]
    
    CATEGORY_CHOICES = [
        ('OFFICE', 'Escritório'),
        ('SOFTWARE', 'Software/Sistemas'),
        ('MARKETING', 'Marketing'),
        ('LEGAL_FEES', 'Custas Processuais'),
        ('TAXES', 'Impostos'),
        ('OTHER', 'Outros'),
    ]
    
    description = models.CharField("Descrição", max_length=255)
    supplier = models.CharField("Fornecedor", max_length=255, blank=True)
    
    amount = models.DecimalField("Valor (R$)", max_digits=10, decimal_places=2)
    due_date = models.DateField("Data de Vencimento")
    
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='PENDING')
    category = models.CharField("Categoria", max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    
    notes = models.TextField("Observações", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def is_late(self):
        return self.status == 'PENDING' and self.due_date < timezone.now().date()
    
    def __str__(self):
        return f"{self.description} - R$ {self.amount}"

    class Meta:
        verbose_name = "Conta a Pagar"
        verbose_name_plural = "Contas a Pagar"
        ordering = ['due_date']

class AccountReceivable(models.Model):
    """
    Finance Module: Accounts Receivable (Honorários e Custas).
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('RECEIVED', 'Recebido'),
        ('CANCELLED', 'Cancelado'),
    ]
    
    CATEGORY_CHOICES = [
        ('FEES', 'Honorários'),
        ('REIMBURSEMENT', 'Reembolso de Custas'),
        ('SUCCESS_FEE', 'Honorários de Êxito'),
        ('OTHER', 'Outros'),
    ]
    
    legal_case = models.ForeignKey(
        'legal_cases.LegalCase', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='receivables'
    )
    
    description = models.CharField("Descrição", max_length=255)
    client_name = models.CharField("Nome do Cliente", max_length=255, blank=True)
    
    amount = models.DecimalField("Valor (R$)", max_digits=12, decimal_places=2)
    due_date = models.DateField("Data de Vencimento")
    received_date = models.DateField("Data de Recebimento", null=True, blank=True)
    
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='PENDING')
    category = models.CharField("Categoria", max_length=20, choices=CATEGORY_CHOICES, default='FEES')
    
    notes = models.TextField("Observações", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.description} - R$ {self.amount}"

    class Meta:
        verbose_name = "Conta a Receber"
        verbose_name_plural = "Contas a Receber"
        ordering = ['due_date']
