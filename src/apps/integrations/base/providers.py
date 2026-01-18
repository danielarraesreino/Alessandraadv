"""
Base interfaces for Legal Ops integrations.

Provides abstract classes that all Legal Ops providers must implement,
ensuring consistent behavior across Clio, Jestor, and custom solutions.
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class MatterData:
    """Standardized case/matter data structure."""
    client_name: str
    case_type: str
    description: str
    contact_info: str
    score: int
    triage_data: Dict
    external_id: Optional[str] = None


@dataclass
class SyncResult:
    """Result of a sync operation."""
    success: bool
    external_id: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict] = None


class LegalOpsProvider(ABC):
    """
    Abstract base class for Legal Ops integrations.
    
    All providers (Clio, Jestor, etc.) must implement these methods.
    """
    
    @abstractmethod
    def create_matter(self, matter_data: MatterData) -> SyncResult:
        """
        Create a new case/matter in the Legal Ops system.
        
        Args:
            matter_data: Standardized matter information
            
        Returns:
            SyncResult with external_id if successful
        """
        pass
    
    @abstractmethod
    def update_matter(self, external_id: str, updates: Dict) -> SyncResult:
        """
        Update an existing matter.
        
        Args:
            external_id: ID in the external system
            updates: Fields to update
            
        Returns:
            SyncResult indicating success/failure
        """
        pass
    
    @abstractmethod
    def get_matter(self, external_id: str) -> Optional[Dict]:
        """
        Retrieve matter details from the external system.
        
        Args:
            external_id: ID in the external system
            
        Returns:
            Matter data or None if not found
        """
        pass
    
    @abstractmethod
    def list_matters(self, filters: Optional[Dict] = None) -> List[Dict]:
        """
        List matters with optional filters.
        
        Args:
            filters: Optional filtering criteria
            
        Returns:
            List of matter dictionaries
        """
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        """
        Verify connection to the Legal Ops system.
        
        Returns:
            True if connection is healthy
        """
        pass


class ProviderFactory:
    """
    Factory for creating Legal Ops provider instances.
    """
    
    _providers = {}
    
    @classmethod
    def register_provider(cls, name: str, provider_class):
        """Register a new provider."""
        cls._providers[name] = provider_class
    
    @classmethod
    def get_provider(cls, name: str, **config) -> LegalOpsProvider:
        """
        Get a provider instance by name.
        
        Args:
            name: Provider name ('clio', 'jestor', 'custom')
            **config: Provider-specific configuration
            
        Returns:
            Configured provider instance
        """
        if name not in cls._providers:
            raise ValueError(f"Unknown provider: {name}")
        
        return cls._providers[name](**config)
