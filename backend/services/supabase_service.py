import os
import logging
from typing import Any, Optional, Dict, List
import json
from datetime import datetime

from supabase import create_client, Client
from pydantic import BaseModel

from config import settings

logger = logging.getLogger("policy-aware-api")


class SupabaseService:
    """
    Service for interacting with Supabase.
    Used for audit logging and fetching policies.
    Fail-safe: captures errors to prevent blocking main execution.
    """
    
    def __init__(self):
        self.url = settings.SUPABASE_URL
        self.key = settings.SUPABASE_KEY
        self.client: Optional[Client] = None
        
        if self.url and self.key:
            try:
                self.client = create_client(self.url, self.key)
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
        else:
            logger.warning("Supabase credentials not set. Audit logging disabled.")
    
    def insert_api_spec(self, name: str, spec_text: str) -> Optional[str]:
        """Insert API spec and return ID."""
        if not self.client:
            return None
        
        try:
            # Check if spec mainly exists to avoid dupes? 
            # For now just insert as new record
            data = {"name": name, "spec_text": spec_text}
            response = self.client.table("api_specs").insert(data).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]["id"]
            return None
        except Exception as e:
            logger.error(f"Supabase error inserting api_spec: {e}")
            return None

    def insert_verdict(
        self,
        api_spec_id: Optional[str],
        user_intent: str,
        verdict: Dict[str, Any],
        ui_contract: Dict[str, Any],
        risk_score: float
    ) -> Optional[str]:
        """Insert safety verdict for audit log."""
        if not self.client:
            return None
        
        try:
            data = {
                "api_spec_id": api_spec_id,
                "user_intent": user_intent,
                "verdict_json": verdict,
                "ui_contract_json": ui_contract,
                "risk_score": risk_score
            }
            response = self.client.table("safety_verdicts").insert(data).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]["id"]
            return None
        except Exception as e:
            # Log full error for debugging
            logger.error(f"Supabase error inserting verdict: {e}")
            return None

    def get_active_policies(self) -> List[Dict[str, Any]]:
        """Fetch active policies."""
        if not self.client:
            return []
        
        try:
            response = self.client.table("policies").select("*").eq("active", True).execute()
            return response.data
        except Exception as e:
            logger.error(f"Supabase error fetching policies: {e}")
            return []
