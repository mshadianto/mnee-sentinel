"""
Configuration Management for MNEE Sentinel (Enhanced)
Supports: Groq, OpenAI, Anthropic
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ===================================
# Blockchain Configuration
# ===================================
ETHEREUM_RPC_URL = os.getenv("ETHEREUM_RPC_URL", "https://eth.llamarpc.com")
MNEE_CONTRACT_ADDRESS = "0x8ccedbAe4916b79da7F3F612EfB2EB93A2bFD6cF"
TREASURY_PRIVATE_KEY = os.getenv("TREASURY_PRIVATE_KEY", "")  # NEVER commit this
TREASURY_ADDRESS = os.getenv("TREASURY_ADDRESS", "")

# ===================================
# Database Configuration
# ===================================
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# ===================================
# AI Agent Configuration
# ===================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")  # NEW: Groq support

AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")  # "groq", "openai", or "anthropic"

# Model configurations
AI_MODELS = {
    "groq": "llama-3.1-70b-versatile",  # Fastest
    "openai": "gpt-4-turbo-preview",     # Most accurate
    "anthropic": "claude-sonnet-4-20250514"  # Best reasoning
}

# ===================================
# Business Logic Constants
# ===================================
VELOCITY_WINDOW_HOURS = 24
MAX_TRANSACTIONS_PER_VENDOR_PER_DAY = 10
CONFIDENCE_THRESHOLD = 0.70  # 70% minimum confidence for approval

# ===================================
# Standard ERC-20 ABI (Minimal)
# ===================================
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    }
]
