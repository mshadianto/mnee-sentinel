"""
AI Auditor Agent using LangChain (Enhanced)
Supports: Groq (Llama 3), OpenAI (GPT-4), Anthropic (Claude)
Evaluates treasury proposals against governance rules
"""
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Dict, Tuple, Literal
from decimal import Decimal
import logging
import re
import os

from config.settings import (
    OPENAI_API_KEY,
    ANTHROPIC_API_KEY,
    CONFIDENCE_THRESHOLD
)
from utils.db_utils import GovernanceDB

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ===================================
# Structured Output Model
# ===================================

class ProposalAnalysis(BaseModel):
    """Structured output from AI analysis"""
    vendor_name: str = Field(description="Name of the vendor/recipient (e.g., PT Nusantara FX Services)")
    vendor_address: str = Field(description="Ethereum wallet address (0x...)")
    amount: float = Field(description="Amount in MNEE tokens")
    category: str = Field(description="Budget category (FX, Remittance, Settlement, Software, Consulting, Travel, Office, Data, Cybersecurity, Legal)")
    confidence: float = Field(description="Confidence score 0-1", ge=0, le=1)
    interpretation: str = Field(description="Brief explanation of what was parsed")


class AuditorAgent:
    """AI-powered compliance auditor for treasury operations"""
    
    SUPPORTED_PROVIDERS = {
        "groq": "Groq (Llama 3.1 70B) - ⚡ Fastest",
        "openai": "OpenAI (GPT-4 Turbo) - 🎯 Most Accurate",
        "anthropic": "Anthropic (Claude Sonnet 4) - 🧠 Best Reasoning"
    }
    
    def __init__(
        self, 
        db: GovernanceDB,
        provider: Literal["groq", "openai", "anthropic"] = "groq"
    ):
        self.db = db
        self.provider = provider
        self.llm = self._initialize_llm(provider)
        
        # Output parser
        self.parser = PydanticOutputParser(pydantic_object=ProposalAnalysis)
        
        # Enhanced prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a financial compliance AI for an Indonesian DAO treasury system managing MNEE tokens.

Your job is to extract key information from payment proposals with HIGH PRECISION.

Extract the following fields:
1. **vendor_name**: Full company name (e.g., "PT Nusantara FX Services")
2. **vendor_address**: Ethereum wallet address (must start with 0x and be 42 characters)
3. **amount**: Numerical amount in MNEE tokens (just the number, no currency symbol)
4. **category**: One of these EXACT categories:
   - FX (Foreign Exchange)
   - Remittance (Money Transfer)
   - Settlement (Bank Settlement)
   - Software (Software/Cloud Services)
   - Consulting (Advisory/Consulting)
   - Travel (Corporate Travel)
   - Office (Office Supplies)
   - Data (Data Feeds/Analytics)
   - Cybersecurity (Security Services)
   - Legal (Legal Services)

**IMPORTANT RULES:**
- If wallet address is missing or invalid, set confidence < 0.5
- If amount is unclear, set confidence < 0.6
- Category MUST be one of the 10 listed above
- Indonesian vendor names often start with "PT" (Perseroan Terbatas)

{format_instructions}

Be precise. Extract only facts, no assumptions."""),
            ("human", "{proposal}")
        ])
    
    def _initialize_llm(self, provider: str):
        """Initialize LLM based on selected provider"""
        groq_api_key = os.getenv("GROQ_API_KEY", "")
        
        if provider == "groq" and groq_api_key:
            logger.info("🚀 Initializing Groq (Llama 3.1 70B)")
            return ChatGroq(
                model="llama-3.1-70b-versatile",
                groq_api_key=groq_api_key,
                temperature=0,
                max_tokens=2048
            )
        elif provider == "anthropic" and ANTHROPIC_API_KEY:
            logger.info("🧠 Initializing Anthropic (Claude Sonnet 4)")
            return ChatAnthropic(
                model="claude-sonnet-4-20250514",
                anthropic_api_key=ANTHROPIC_API_KEY,
                temperature=0,
                max_tokens=2048
            )
        elif provider == "openai" and OPENAI_API_KEY:
            logger.info("🎯 Initializing OpenAI (GPT-4 Turbo)")
            return ChatOpenAI(
                model="gpt-4-turbo-preview",
                openai_api_key=OPENAI_API_KEY,
                temperature=0,
                max_tokens=2048
            )
        else:
            # Fallback to OpenAI
            if OPENAI_API_KEY:
                logger.warning(f"⚠️ {provider} not available, falling back to OpenAI")
                return ChatOpenAI(
                    model="gpt-4-turbo-preview",
                    openai_api_key=OPENAI_API_KEY,
                    temperature=0
                )
            raise ValueError(f"No valid API key for provider: {provider}")
    
    def switch_provider(self, new_provider: str):
        """Dynamically switch AI provider"""
        if new_provider not in self.SUPPORTED_PROVIDERS:
            raise ValueError(f"Unsupported provider: {new_provider}")
        
        self.provider = new_provider
        self.llm = self._initialize_llm(new_provider)
        logger.info(f"✅ Switched to {self.SUPPORTED_PROVIDERS[new_provider]}")
    
    def parse_proposal(self, proposal_text: str) -> Tuple[bool, ProposalAnalysis]:
        """
        Parse natural language proposal using AI
        
        Returns:
            Tuple[bool, ProposalAnalysis]: (success, parsed_data)
        """
        try:
            chain = self.prompt | self.llm | self.parser
            
            result = chain.invoke({
                "proposal": proposal_text,
                "format_instructions": self.parser.get_format_instructions()
            })
            
            logger.info(f"✅ [{self.provider.upper()}] Parsed with {result.confidence:.0%} confidence")
            return True, result
            
        except Exception as e:
            logger.error(f"❌ [{self.provider.upper()}] Parsing error: {e}")
            # Fallback to regex
            return self._fallback_parse(proposal_text)
    
    def _fallback_parse(self, proposal_text: str) -> Tuple[bool, ProposalAnalysis]:
        """Regex-based fallback parser for when AI fails"""
        try:
            # Extract amount
            amount_match = re.search(r'(\d+(?:\.\d+)?)\s*MNEE', proposal_text, re.IGNORECASE)
            amount = float(amount_match.group(1)) if amount_match else 0
            
            # Extract address
            address_match = re.search(r'(0x[a-fA-F0-9]{40})', proposal_text)
            address = address_match.group(1) if address_match else ""
            
            # Extract vendor name (PT companies)
            vendor_match = re.search(r'(PT\s+[A-Z][a-zA-Z\s&]+?)(?:\s+|,|for|at)', proposal_text)
            if not vendor_match:
                vendor_match = re.search(r'to\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', proposal_text)
            vendor = vendor_match.group(1).strip() if vendor_match else "Unknown Vendor"
            
            # Guess category from context
            category_keywords = {
                'FX': ['forex', 'fx', 'hedging', 'currency'],
                'Remittance': ['remittance', 'transfer', 'money transfer'],
                'Settlement': ['settlement', 'bank', 'clearing'],
                'Software': ['software', 'cloud', 'saas', 'tools'],
                'Consulting': ['consulting', 'advisory', 'audit'],
                'Travel': ['travel', 'trip', 'flight'],
                'Office': ['office', 'supplies', 'stationery'],
                'Data': ['data', 'feed', 'analytics'],
                'Cybersecurity': ['security', 'cybersecurity', 'protection'],
                'Legal': ['legal', 'law', 'compliance']
            }
            
            category = "Office"  # Default
            for cat, keywords in category_keywords.items():
                if any(kw in proposal_text.lower() for kw in keywords):
                    category = cat
                    break
            
            logger.warning("⚠️ Using fallback regex parser (low confidence)")
            return True, ProposalAnalysis(
                vendor_name=vendor,
                vendor_address=address,
                amount=amount,
                category=category,
                confidence=0.45,
                interpretation="⚠️ Parsed using fallback regex (AI parsing failed)"
            )
        except Exception as e:
            logger.error(f"❌ Fallback parse failed: {e}")
            return False, None
    
    def audit_proposal(self, proposal_text: str) -> Dict:
        """
        Main audit function - evaluates proposal against all rules
        
        Returns:
            Dict with keys: decision, reasoning, details, confidence, parsed_data, provider
        """
        # Step 1: Parse the proposal
        success, parsed = self.parse_proposal(proposal_text)
        
        if not success or parsed.confidence < CONFIDENCE_THRESHOLD:
            return {
                "decision": "REJECTED",
                "reasoning": f"❌ Unable to parse proposal with sufficient confidence\n\nGot {parsed.confidence:.0%} confidence, need {CONFIDENCE_THRESHOLD:.0%}\n\nIssue: {parsed.interpretation if parsed else 'Complete parsing failure'}",
                "details": {"parsing_failed": True},
                "confidence": parsed.confidence if parsed else 0,
                "parsed_data": parsed,
                "provider": self.provider
            }
        
        # Step 2: Validate wallet address format
        from utils.crypto_utils import MNEETokenManager
        token_manager = MNEETokenManager()
        if not token_manager.validate_address(parsed.vendor_address):
            return {
                "decision": "REJECTED",
                "reasoning": f"❌ Invalid Ethereum Address\n\nProvided: {parsed.vendor_address}\nExpected: Valid 0x... address (42 characters)",
                "details": {"parsed": parsed.dict(), "address_validation": "FAILED"},
                "confidence": parsed.confidence,
                "parsed_data": parsed,
                "provider": self.provider
            }
        
        # Step 3: Check vendor whitelist
        is_whitelisted, vendor_data = self.db.is_vendor_whitelisted(parsed.vendor_address)
        if not is_whitelisted:
            return {
                "decision": "REJECTED",
                "reasoning": f"❌ Vendor Not Whitelisted\n\nVendor: {parsed.vendor_name}\nAddress: {parsed.vendor_address}\n\nThis vendor is not authorized to receive treasury funds.",
                "details": {
                    "parsed": parsed.dict(),
                    "whitelist_check": "FAILED"
                },
                "confidence": parsed.confidence,
                "parsed_data": parsed,
                "provider": self.provider
            }
        
        # Step 4: Check vendor transaction limit
        vendor_limit = Decimal(str(vendor_data['max_transaction_limit']))
        if Decimal(str(parsed.amount)) > vendor_limit:
            return {
                "decision": "REJECTED",
                "reasoning": f"❌ Exceeds Vendor Transaction Limit\n\nRequested: {parsed.amount} MNEE\nVendor Limit: {vendor_limit} MNEE\nOverage: {Decimal(str(parsed.amount)) - vendor_limit} MNEE",
                "details": {
                    "parsed": parsed.dict(),
                    "whitelist_check": "PASSED",
                    "vendor_limit_check": "FAILED",
                    "vendor_limit": float(vendor_limit)
                },
                "confidence": parsed.confidence,
                "parsed_data": parsed,
                "provider": self.provider
            }
        
        # Step 5: Check category budget
        remaining, total = self.db.get_remaining_budget(vendor_data['category'])
        if Decimal(str(parsed.amount)) > remaining:
            return {
                "decision": "REJECTED",
                "reasoning": f"❌ Insufficient Budget in {vendor_data['category']} Category\n\nRequired: {parsed.amount} MNEE\nRemaining: {remaining} MNEE\nTotal Budget: {total} MNEE\nShortfall: {Decimal(str(parsed.amount)) - remaining} MNEE",
                "details": {
                    "parsed": parsed.dict(),
                    "whitelist_check": "PASSED",
                    "vendor_limit_check": "PASSED",
                    "budget_check": "FAILED",
                    "remaining_budget": float(remaining),
                    "total_budget": float(total)
                },
                "confidence": parsed.confidence,
                "parsed_data": parsed,
                "provider": self.provider
            }
        
        # Step 6: Check transaction velocity
        is_safe, velocity_reason = self.db.check_transaction_velocity(
            parsed.vendor_address,
            Decimal(str(parsed.amount))
        )
        if not is_safe:
            return {
                "decision": "REJECTED",
                "reasoning": f"❌ Transaction Velocity Alert\n\n{velocity_reason}\n\nThis may indicate fraudulent activity or duplicate submissions.",
                "details": {
                    "parsed": parsed.dict(),
                    "whitelist_check": "PASSED",
                    "vendor_limit_check": "PASSED",
                    "budget_check": "PASSED",
                    "velocity_check": "FAILED"
                },
                "confidence": parsed.confidence,
                "parsed_data": parsed,
                "provider": self.provider
            }
        
        # ✅ ALL CHECKS PASSED
        return {
            "decision": "APPROVED",
            "reasoning": f"""✅ **ALL COMPLIANCE CHECKS PASSED**

**Vendor Information:**
• Name: {parsed.vendor_name}
• Address: {parsed.vendor_address}
• Category: {vendor_data['category']}

**Financial Validation:**
• Amount: {parsed.amount} MNEE
• Vendor Limit: {vendor_limit} MNEE ✓
• Budget Remaining: {remaining} MNEE (of {total} total) ✓
• Velocity Check: PASSED ✓

**AI Analysis:**
• Confidence: {parsed.confidence:.0%}
• Provider: {self.SUPPORTED_PROVIDERS[self.provider]}
            """,
            "details": {
                "parsed": parsed.dict(),
                "whitelist_check": "PASSED",
                "vendor_limit_check": "PASSED",
                "budget_check": "PASSED",
                "velocity_check": "PASSED",
                "vendor_data": vendor_data,
                "remaining_budget": float(remaining),
                "total_budget": float(total)
            },
            "confidence": parsed.confidence,
            "parsed_data": parsed,
            "provider": self.provider
        }
