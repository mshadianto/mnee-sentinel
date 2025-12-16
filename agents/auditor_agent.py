"""
MNEE Sentinel - AI Auditor Agent
Multi-provider AI compliance engine for treasury governance

Compatible with LangChain 0.1.0+ and Streamlit Cloud
Fully compatible with app.py interface
"""

import os
import re
import logging
from typing import Dict, Optional, Any, NamedTuple
from datetime import datetime
from decimal import Decimal

# Updated imports for LangChain 0.1.0+
try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
except ImportError:
    # Fallback for older versions
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema.output_parser import StrOutputParser

# AI Provider imports
try:
    from langchain_groq import ChatGroq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    ChatGroq = None

try:
    from langchain_openai import ChatOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    ChatOpenAI = None

try:
    from langchain_anthropic import ChatAnthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    ChatAnthropic = None

logger = logging.getLogger(__name__)


class ParsedProposal(NamedTuple):
    """Structured data from parsed proposal"""
    vendor_name: str
    vendor_address: str
    amount: float
    category: str
    confidence: float


# System prompt for the auditor
AUDITOR_SYSTEM_PROMPT = """You are an AI Treasury Auditor for a DAO/Company. Your role is to analyze payment proposals and determine if they should be APPROVED or REJECTED based on governance rules.

GOVERNANCE RULES:
1. Vendor must be in the whitelist
2. Amount must not exceed budget limits for the category
3. Amount must not exceed per-transaction limits
4. Wallet address must be valid (42 characters, starts with 0x)
5. Purpose must be clearly stated

CONTEXT:
- Whitelisted Vendors: {whitelisted_vendors}
- Budget Limits: {budget_limits}
- Transaction Velocity: {velocity_info}

PROPOSAL TO ANALYZE:
{proposal_text}

Analyze the proposal and respond with:
1. DECISION: APPROVED or REJECTED
2. CONFIDENCE: A decimal between 0.0 and 1.0
3. REASONING: Brief explanation (2-3 sentences)
4. RISK_FLAGS: Any concerns (or "None")

Format your response EXACTLY as:
DECISION: [APPROVED/REJECTED]
CONFIDENCE: [0.0-1.0]
REASONING: [Your explanation]
RISK_FLAGS: [Any concerns or None]
"""


class AuditorAgent:
    """
    Multi-provider AI Auditor Agent for treasury governance.
    
    Supports:
    - Groq (Llama 3.1) - Fastest
    - OpenAI (GPT-4) - Most accurate
    - Anthropic (Claude) - Best reasoning
    """
    
    # Provider display names (required by app.py)
    SUPPORTED_PROVIDERS = {
        "groq": "⚡ Groq (Llama 3.1)",
        "openai": "🎯 OpenAI (GPT-4)",
        "anthropic": "🧠 Claude (Sonnet 4)"
    }
    
    def __init__(self, db=None, provider: str = "groq"):
        """
        Initialize the auditor agent.
        
        Args:
            db: Database connection (GovernanceDB instance)
            provider: AI provider - "groq", "openai", or "anthropic"
        """
        self.db = db
        self.provider = provider.lower()
        self.llm = None
        self._initialize_llm()
        
        logger.info(f"✅ AuditorAgent initialized with provider: {self.provider}")
    
    def _initialize_llm(self):
        """Initialize the LLM based on provider selection."""
        
        if self.provider == "groq":
            if not GROQ_AVAILABLE:
                logger.warning("langchain-groq not installed")
                return
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                logger.warning("GROQ_API_KEY not found")
                return
            self.llm = ChatGroq(
                model="llama-3.1-70b-versatile",
                temperature=0.1,
                api_key=api_key
            )
        
        elif self.provider == "openai":
            if not OPENAI_AVAILABLE:
                logger.warning("langchain-openai not installed")
                return
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                logger.warning("OPENAI_API_KEY not found")
                return
            self.llm = ChatOpenAI(
                model="gpt-4-turbo-preview",
                temperature=0.1,
                api_key=api_key
            )
        
        elif self.provider == "anthropic":
            if not ANTHROPIC_AVAILABLE:
                logger.warning("langchain-anthropic not installed")
                return
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                logger.warning("ANTHROPIC_API_KEY not found")
                return
            self.llm = ChatAnthropic(
                model="claude-3-sonnet-20240229",
                temperature=0.1,
                api_key=api_key
            )
        
        if self.llm:
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", AUDITOR_SYSTEM_PROMPT),
                ("human", "Please analyze this proposal and provide your decision.")
            ])
            self.chain = self.prompt | self.llm | StrOutputParser()
    
    def switch_provider(self, new_provider: str):
        """Switch to a different AI provider."""
        self.provider = new_provider.lower()
        self._initialize_llm()
        logger.info(f"🔄 Switched to provider: {self.provider}")
    
    def _parse_proposal_text(self, proposal_text: str) -> ParsedProposal:
        """Extract structured data from proposal text using regex."""
        
        # Extract vendor name (look for PT, CV, or company patterns)
        vendor_match = re.search(
            r'(?:to|pay|transfer to)\s+([A-Za-z\s]+(?:PT|CV|Inc|LLC|Ltd)?[A-Za-z\s]*)',
            proposal_text, 
            re.IGNORECASE
        )
        vendor_name = vendor_match.group(1).strip() if vendor_match else "Unknown Vendor"
        
        # Clean up vendor name
        vendor_name = re.sub(r'\s+', ' ', vendor_name)
        vendor_name = vendor_name.replace(" for ", "").replace(" at ", "").strip()
        
        # Extract wallet address (0x followed by 40 hex chars)
        address_match = re.search(r'(0x[a-fA-F0-9]{40})', proposal_text)
        vendor_address = address_match.group(1) if address_match else ""
        
        # Extract amount
        amount_match = re.search(r'(\d+(?:\.\d+)?)\s*MNEE', proposal_text, re.IGNORECASE)
        amount = float(amount_match.group(1)) if amount_match else 0.0
        
        # Detect category from keywords
        text_lower = proposal_text.lower()
        if any(kw in text_lower for kw in ['fx', 'forex', 'hedging', 'currency']):
            category = "FX"
        elif any(kw in text_lower for kw in ['remittance', 'transfer', 'wire']):
            category = "Remittance"
        elif any(kw in text_lower for kw in ['settlement', 'clearing']):
            category = "Settlement"
        elif any(kw in text_lower for kw in ['software', 'license', 'subscription']):
            category = "Software"
        elif any(kw in text_lower for kw in ['consulting', 'advisory']):
            category = "Consulting"
        elif any(kw in text_lower for kw in ['security', 'cyber', 'audit']):
            category = "Cybersecurity"
        elif any(kw in text_lower for kw in ['office', 'supplies', 'stationery']):
            category = "Office"
        elif any(kw in text_lower for kw in ['data', 'analytics', 'market data']):
            category = "Data"
        elif any(kw in text_lower for kw in ['travel', 'flight', 'hotel']):
            category = "Travel"
        elif any(kw in text_lower for kw in ['legal', 'compliance']):
            category = "Legal"
        else:
            category = "General"
        
        # Calculate confidence based on extracted fields
        confidence = 0.0
        if vendor_name and vendor_name != "Unknown Vendor":
            confidence += 0.3
        if vendor_address:
            confidence += 0.3
        if amount > 0:
            confidence += 0.2
        if category != "General":
            confidence += 0.2
        
        return ParsedProposal(
            vendor_name=vendor_name,
            vendor_address=vendor_address,
            amount=amount,
            category=category,
            confidence=confidence
        )
    
    def _get_governance_context(self) -> Dict[str, str]:
        """Fetch governance context from database."""
        context = {
            "whitelisted_vendors": "No data available",
            "budget_limits": "No data available",
            "velocity_info": "No data available"
        }
        
        if not self.db:
            return context
        
        try:
            # Get whitelisted vendors
            vendors = self.db.client.table("whitelisted_vendors").select("vendor_name, category, max_transaction_limit").execute()
            if vendors.data:
                vendor_list = [f"{v['vendor_name']} ({v['category']}, max: {v['max_transaction_limit']} MNEE)" for v in vendors.data]
                context["whitelisted_vendors"] = ", ".join(vendor_list)
            
            # Get budget limits
            budgets = self.db.client.table("budgets").select("category, monthly_limit_mnee, current_spent").execute()
            if budgets.data:
                budget_list = [f"{b['category']}: {b['current_spent']}/{b['monthly_limit_mnee']} MNEE used" for b in budgets.data]
                context["budget_limits"] = ", ".join(budget_list)
            
            # Get velocity info
            velocity = self.db.client.table("transaction_velocity").select("*").execute()
            if velocity.data:
                context["velocity_info"] = f"{len(velocity.data)} vendors tracked"
        
        except Exception as e:
            logger.error(f"Error fetching governance context: {e}")
        
        return context
    
    def _check_compliance(self, parsed: ParsedProposal) -> Dict[str, Any]:
        """Run compliance checks against governance rules."""
        checks = {
            "vendor_whitelisted": False,
            "within_budget": False,
            "within_tx_limit": False,
            "valid_address": False,
            "velocity_ok": True,
            "details": {}
        }
        
        # Check address validity
        if parsed.vendor_address and len(parsed.vendor_address) == 42 and parsed.vendor_address.startswith("0x"):
            checks["valid_address"] = True
        
        if not self.db:
            return checks
        
        try:
            # Check vendor whitelist
            vendor_result = self.db.client.table("whitelisted_vendors")\
                .select("*")\
                .ilike("vendor_name", f"%{parsed.vendor_name.split()[0]}%")\
                .execute()
            
            if vendor_result.data:
                checks["vendor_whitelisted"] = True
                vendor = vendor_result.data[0]
                checks["details"]["vendor"] = vendor
                
                # Check transaction limit
                if parsed.amount <= float(vendor['max_transaction_limit']):
                    checks["within_tx_limit"] = True
            
            # Check budget
            budget_result = self.db.client.table("budgets")\
                .select("*")\
                .eq("category", parsed.category)\
                .execute()
            
            if budget_result.data:
                budget = budget_result.data[0]
                remaining = float(budget['monthly_limit_mnee']) - float(budget['current_spent'])
                if parsed.amount <= remaining:
                    checks["within_budget"] = True
                checks["details"]["budget"] = {
                    "limit": float(budget['monthly_limit_mnee']),
                    "spent": float(budget['current_spent']),
                    "remaining": remaining
                }
            
        except Exception as e:
            logger.error(f"Compliance check error: {e}")
        
        return checks
    
    def audit_proposal(self, proposal_text: str) -> Dict[str, Any]:
        """
        Audit a treasury proposal.
        
        Args:
            proposal_text: The full proposal text in natural language
            
        Returns:
            Dictionary with decision, confidence, reasoning, parsed_data, details
        """
        # Parse proposal
        parsed = self._parse_proposal_text(proposal_text)
        
        # Run compliance checks
        compliance = self._check_compliance(parsed)
        
        # Get governance context for AI
        context = self._get_governance_context()
        
        # Determine initial decision based on compliance
        if not compliance["vendor_whitelisted"]:
            decision = "REJECTED"
            reasoning = f"Vendor '{parsed.vendor_name}' is not in the whitelist. Only pre-approved vendors can receive payments."
            confidence = 0.95
        elif not compliance["within_budget"]:
            decision = "REJECTED"
            remaining = compliance["details"].get("budget", {}).get("remaining", 0)
            reasoning = f"Insufficient budget. Requested {parsed.amount} MNEE but only {remaining:.2f} MNEE remaining in {parsed.category} category."
            confidence = 0.95
        elif not compliance["within_tx_limit"]:
            decision = "REJECTED"
            max_limit = compliance["details"].get("vendor", {}).get("max_transaction_limit", 0)
            reasoning = f"Amount {parsed.amount} MNEE exceeds vendor's transaction limit of {max_limit} MNEE."
            confidence = 0.95
        elif not compliance["valid_address"] and parsed.vendor_address:
            decision = "REJECTED"
            reasoning = f"Invalid wallet address format. Must be 42 characters starting with 0x."
            confidence = 0.90
        else:
            # Use AI for nuanced decision if basic checks pass
            if self.llm:
                try:
                    response = self.chain.invoke({
                        "proposal_text": proposal_text,
                        "whitelisted_vendors": context["whitelisted_vendors"],
                        "budget_limits": context["budget_limits"],
                        "velocity_info": context["velocity_info"]
                    })
                    
                    # Parse AI response
                    ai_result = self._parse_ai_response(response)
                    decision = ai_result.get("decision", "APPROVED")
                    reasoning = ai_result.get("reasoning", "All compliance checks passed.")
                    confidence = ai_result.get("confidence", 0.85)
                    
                except Exception as e:
                    logger.error(f"AI audit error: {e}")
                    decision = "APPROVED"
                    reasoning = "All compliance checks passed. AI verification unavailable."
                    confidence = 0.80
            else:
                decision = "APPROVED"
                reasoning = "All compliance checks passed. Vendor is whitelisted and within budget limits."
                confidence = 0.85
        
        return {
            "decision": decision,
            "confidence": confidence,
            "reasoning": reasoning,
            "parsed_data": parsed,
            "details": compliance,
            "provider": self.provider,
            "timestamp": datetime.now().isoformat()
        }
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Parse the LLM response into structured data."""
        result = {
            "decision": "APPROVED",
            "confidence": 0.85,
            "reasoning": "",
            "risk_flags": "None"
        }
        
        lines = response.strip().split("\n")
        
        for line in lines:
            line = line.strip()
            if line.startswith("DECISION:"):
                decision = line.replace("DECISION:", "").strip().upper()
                if "REJECT" in decision:
                    result["decision"] = "REJECTED"
                else:
                    result["decision"] = "APPROVED"
            elif line.startswith("CONFIDENCE:"):
                try:
                    conf_str = line.replace("CONFIDENCE:", "").strip()
                    conf = float(conf_str)
                    if conf > 1:
                        conf = conf / 100  # Convert percentage to decimal
                    result["confidence"] = conf
                except:
                    result["confidence"] = 0.85
            elif line.startswith("REASONING:"):
                result["reasoning"] = line.replace("REASONING:", "").strip()
            elif line.startswith("RISK_FLAGS:"):
                result["risk_flags"] = line.replace("RISK_FLAGS:", "").strip()
        
        if not result["reasoning"]:
            result["reasoning"] = "Analysis complete."
        
        return result
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about the current provider."""
        return {
            "name": self.SUPPORTED_PROVIDERS.get(self.provider, "Unknown"),
            "provider": self.provider,
            "available": self.llm is not None
        }


def get_available_providers() -> Dict[str, bool]:
    """Check which AI providers are available."""
    return {
        "groq": GROQ_AVAILABLE and bool(os.getenv("GROQ_API_KEY")),
        "openai": OPENAI_AVAILABLE and bool(os.getenv("OPENAI_API_KEY")),
        "anthropic": ANTHROPIC_AVAILABLE and bool(os.getenv("ANTHROPIC_API_KEY"))
    }


if __name__ == "__main__":
    print("🤖 MNEE Sentinel - AI Auditor Agent")
    print("=" * 50)
    print("\nAvailable providers:")
    for provider, available in get_available_providers().items():
        status = "✅" if available else "❌"
        print(f"  {status} {provider}")