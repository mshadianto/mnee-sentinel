"""
MNEE Sentinel - AI Auditor Agent
Multi-provider AI compliance engine for treasury governance

Compatible with LangChain 0.1.0+ and Streamlit Cloud
"""

import os
import logging
from typing import Dict, Optional, Any
from datetime import datetime

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

EXTRACTED DATA:
- Vendor: {vendor_name}
- Amount: {amount} MNEE
- Wallet: {wallet_address}
- Category: {category}

Analyze the proposal and respond with:
1. DECISION: APPROVED or REJECTED
2. CONFIDENCE: High/Medium/Low
3. REASONING: Brief explanation (2-3 sentences)
4. RISK_FLAGS: Any concerns (or "None")

Format your response EXACTLY as:
DECISION: [APPROVED/REJECTED]
CONFIDENCE: [High/Medium/Low]
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
    
    def __init__(self, db=None, provider: str = "groq"):
        """
        Initialize the auditor agent.
        
        Args:
            db: Database connection (optional, for backward compatibility)
            provider: AI provider - "groq", "openai", or "anthropic"
        """
        self.db = db  # Store db reference if needed
        self.provider = provider.lower()
        self.llm = self._initialize_llm()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", AUDITOR_SYSTEM_PROMPT),
            ("human", "Please analyze this proposal and provide your decision.")
        ])
        self.chain = self.prompt | self.llm | StrOutputParser()
        
        logger.info(f"✅ AuditorAgent initialized with provider: {self.provider}")
    
    def _initialize_llm(self):
        """Initialize the LLM based on provider selection."""
        
        if self.provider == "groq":
            if not GROQ_AVAILABLE:
                raise ImportError("langchain-groq not installed. Run: pip install langchain-groq")
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not found in environment")
            return ChatGroq(
                model="llama-3.1-70b-versatile",
                temperature=0.1,
                api_key=api_key
            )
        
        elif self.provider == "openai":
            if not OPENAI_AVAILABLE:
                raise ImportError("langchain-openai not installed. Run: pip install langchain-openai")
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment")
            return ChatOpenAI(
                model="gpt-4-turbo-preview",
                temperature=0.1,
                api_key=api_key
            )
        
        elif self.provider == "anthropic":
            if not ANTHROPIC_AVAILABLE:
                raise ImportError("langchain-anthropic not installed. Run: pip install langchain-anthropic")
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment")
            return ChatAnthropic(
                model="claude-3-sonnet-20240229",
                temperature=0.1,
                api_key=api_key
            )
        
        else:
            raise ValueError(f"Unknown provider: {self.provider}. Use 'groq', 'openai', or 'anthropic'")
    
    def audit_proposal(
        self,
        proposal_text: str,
        vendor_name: str = "Unknown",
        amount: float = 0.0,
        wallet_address: str = "",
        category: str = "Unknown",
        whitelisted_vendors: str = "None provided",
        budget_limits: str = "None provided",
        velocity_info: str = "None provided"
    ) -> Dict[str, Any]:
        """
        Audit a treasury proposal.
        
        Args:
            proposal_text: The full proposal text
            vendor_name: Extracted vendor name
            amount: Amount in MNEE
            wallet_address: Target wallet address
            category: Expense category
            whitelisted_vendors: List of approved vendors
            budget_limits: Budget constraints
            velocity_info: Recent transaction velocity
            
        Returns:
            Dictionary with decision, confidence, reasoning, risk_flags
        """
        try:
            # Invoke the chain
            response = self.chain.invoke({
                "proposal_text": proposal_text,
                "vendor_name": vendor_name,
                "amount": amount,
                "wallet_address": wallet_address,
                "category": category,
                "whitelisted_vendors": whitelisted_vendors,
                "budget_limits": budget_limits,
                "velocity_info": velocity_info
            })
            
            # Parse response
            result = self._parse_response(response)
            result["provider"] = self.provider
            result["timestamp"] = datetime.now().isoformat()
            result["raw_response"] = response
            
            return result
            
        except Exception as e:
            logger.error(f"Audit failed: {e}")
            return {
                "decision": "ERROR",
                "confidence": "Low",
                "reasoning": f"Audit failed: {str(e)}",
                "risk_flags": "System error",
                "provider": self.provider,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def _parse_response(self, response: str) -> Dict[str, str]:
        """Parse the LLM response into structured data."""
        result = {
            "decision": "UNKNOWN",
            "confidence": "Low",
            "reasoning": "",
            "risk_flags": "None"
        }
        
        lines = response.strip().split("\n")
        
        for line in lines:
            line = line.strip()
            if line.startswith("DECISION:"):
                decision = line.replace("DECISION:", "").strip().upper()
                if "APPROVED" in decision:
                    result["decision"] = "APPROVED"
                elif "REJECTED" in decision or "REJECT" in decision:
                    result["decision"] = "REJECTED"
                else:
                    result["decision"] = decision
            elif line.startswith("CONFIDENCE:"):
                result["confidence"] = line.replace("CONFIDENCE:", "").strip()
            elif line.startswith("REASONING:"):
                result["reasoning"] = line.replace("REASONING:", "").strip()
            elif line.startswith("RISK_FLAGS:"):
                result["risk_flags"] = line.replace("RISK_FLAGS:", "").strip()
        
        # If reasoning spans multiple lines, try to capture more
        if not result["reasoning"] and len(lines) > 2:
            result["reasoning"] = " ".join(lines[2:4])
        
        return result
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about the current provider."""
        providers = {
            "groq": {
                "name": "Groq (Llama 3.1)",
                "model": "llama-3.1-70b-versatile",
                "speed": "Fastest",
                "cost": "Free tier available"
            },
            "openai": {
                "name": "OpenAI (GPT-4)",
                "model": "gpt-4-turbo-preview",
                "speed": "Medium",
                "cost": "Pay per token"
            },
            "anthropic": {
                "name": "Anthropic (Claude)",
                "model": "claude-3-sonnet-20240229",
                "speed": "Medium",
                "cost": "Pay per token"
            }
        }
        return providers.get(self.provider, {"name": "Unknown"})


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