"""
Database Operations for Supabase
Handles all CRUD operations for governance rules and audit logs
"""
from supabase import create_client, Client
from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from datetime import datetime, timedelta
import logging

from config.settings import SUPABASE_URL, SUPABASE_KEY, VELOCITY_WINDOW_HOURS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GovernanceDB:
    """Database manager for governance rules and audit trails"""
    
    def __init__(self):
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Supabase credentials not configured")
        
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("✅ Connected to Supabase")
    
    # ===================================
    # Budget Management
    # ===================================
    
    def get_budget_limit(self, category: str) -> Optional[Decimal]:
        """Get monthly budget limit for a category"""
        try:
            response = self.client.table("budgets").select("monthly_limit_mnee, current_spent").eq("category", category).execute()
            if response.data:
                return Decimal(str(response.data[0]['monthly_limit_mnee']))
            return None
        except Exception as e:
            logger.error(f"Error fetching budget: {e}")
            return None
    
    def get_remaining_budget(self, category: str) -> Tuple[Decimal, Decimal]:
        """
        Get remaining budget for a category
        
        Returns:
            Tuple[Decimal, Decimal]: (remaining, total_limit)
        """
        try:
            response = self.client.table("budgets").select("*").eq("category", category).execute()
            if response.data:
                data = response.data[0]
                limit = Decimal(str(data['monthly_limit_mnee']))
                spent = Decimal(str(data['current_spent']))
                return (limit - spent, limit)
            return (Decimal(0), Decimal(0))
        except Exception as e:
            logger.error(f"Error calculating remaining budget: {e}")
            return (Decimal(0), Decimal(0))
    
    def update_budget_spent(self, category: str, amount: Decimal) -> bool:
        """Increment current_spent for a category"""
        try:
            # Fetch current value
            current = self.client.table("budgets").select("current_spent").eq("category", category).execute()
            if current.data:
                new_spent = Decimal(str(current.data[0]['current_spent'])) + amount
                self.client.table("budgets").update({
                    "current_spent": float(new_spent),
                    "updated_at": datetime.now().isoformat()
                }).eq("category", category).execute()
                logger.info(f"✅ Updated budget for {category}: +{amount} MNEE")
                return True
        except Exception as e:
            logger.error(f"Error updating budget: {e}")
        return False
    
    # ===================================
    # Vendor Whitelist
    # ===================================
    
    def is_vendor_whitelisted(self, wallet_address: str) -> Tuple[bool, Optional[Dict]]:
        """
        Check if vendor is whitelisted
        
        Returns:
            Tuple[bool, Optional[Dict]]: (is_whitelisted, vendor_data)
        """
        try:
            response = self.client.table("whitelisted_vendors")\
                .select("*")\
                .eq("wallet_address", wallet_address.lower())\
                .eq("is_active", True)\
                .execute()
            
            if response.data:
                return True, response.data[0]
            return False, None
        except Exception as e:
            logger.error(f"Error checking whitelist: {e}")
            return False, None
    
    def get_vendor_limit(self, wallet_address: str) -> Optional[Decimal]:
        """Get max transaction limit for a vendor"""
        is_whitelisted, vendor_data = self.is_vendor_whitelisted(wallet_address)
        if is_whitelisted:
            return Decimal(str(vendor_data['max_transaction_limit']))
        return None
    
    # ===================================
    # Velocity Tracking (Anti-Fraud)
    # ===================================
    
    def check_transaction_velocity(self, vendor_address: str, amount: Decimal) -> Tuple[bool, str]:
        """
        Check if transaction violates velocity rules
        
        Returns:
            Tuple[bool, str]: (is_safe, reason)
        """
        try:
            window_start = datetime.now() - timedelta(hours=VELOCITY_WINDOW_HOURS)
            
            response = self.client.table("transaction_velocity")\
                .select("*")\
                .eq("vendor_address", vendor_address.lower())\
                .gte("window_start", window_start.isoformat())\
                .execute()
            
            if response.data:
                data = response.data[0]
                tx_count = data['transaction_count']
                total_amount = Decimal(str(data['total_amount']))
                
                # Check limits
                from config.settings import MAX_TRANSACTIONS_PER_VENDOR_PER_DAY
                if tx_count >= MAX_TRANSACTIONS_PER_VENDOR_PER_DAY:
                    return False, f"Exceeded max transactions ({MAX_TRANSACTIONS_PER_VENDOR_PER_DAY}/day)"
                
                # Could add amount-based velocity checks here
                # e.g., if total_amount + amount > some_threshold
            
            return True, "Velocity check passed"
        except Exception as e:
            logger.error(f"Velocity check error: {e}")
            return True, "Velocity check unavailable (defaulting to allow)"
    
    def update_velocity_tracker(self, vendor_address: str, amount: Decimal) -> None:
        """Update velocity tracker after successful transaction"""
        try:
            window_start = datetime.now() - timedelta(hours=VELOCITY_WINDOW_HOURS)
            
            # Check if record exists
            response = self.client.table("transaction_velocity")\
                .select("*")\
                .eq("vendor_address", vendor_address.lower())\
                .gte("window_start", window_start.isoformat())\
                .execute()
            
            if response.data:
                # Update existing
                data = response.data[0]
                self.client.table("transaction_velocity").update({
                    "transaction_count": data['transaction_count'] + 1,
                    "total_amount": float(Decimal(str(data['total_amount'])) + amount),
                    "last_updated": datetime.now().isoformat()
                }).eq("id", data['id']).execute()
            else:
                # Insert new
                self.client.table("transaction_velocity").insert({
                    "vendor_address": vendor_address.lower(),
                    "transaction_count": 1,
                    "total_amount": float(amount),
                    "window_start": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat()
                }).execute()
            
            logger.info(f"✅ Updated velocity tracker for {vendor_address}")
        except Exception as e:
            logger.error(f"Error updating velocity tracker: {e}")
    
    # ===================================
    # Audit Logging (Immutable Trail)
    # ===================================
    
    def log_audit_decision(
        self,
        proposal_text: str,
        vendor_name: str,
        vendor_address: str,
        amount: Decimal,
        category: str,
        decision: str,
        reasoning: str,
        ai_confidence: float,
        transaction_hash: Optional[str] = None
    ) -> bool:
        """
        Create immutable audit log entry
        
        Args:
            decision: "APPROVED" or "REJECTED"
        """
        try:
            self.client.table("audit_logs").insert({
                "proposal_text": proposal_text,
                "vendor_name": vendor_name,
                "vendor_address": vendor_address.lower(),
                "amount": float(amount),
                "category": category,
                "decision": decision,
                "reasoning": reasoning,
                "ai_confidence": ai_confidence,
                "transaction_hash": transaction_hash,
                "created_at": datetime.now().isoformat()
            }).execute()
            logger.info(f"📝 Audit log created: {decision}")
            return True
        except Exception as e:
            logger.error(f"Error creating audit log: {e}")
            return False
    
    def get_recent_audits(self, limit: int = 10) -> List[Dict]:
        """Get recent audit logs for dashboard"""
        try:
            response = self.client.table("audit_logs")\
                .select("*")\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Error fetching audits: {e}")
            return []
