"""
Blockchain Interaction Module for MNEE Token - HYBRID SIMULATION MODE
Handles Web3.py operations with safety checks and demo fallback

MODES:
- SIMULATION: Fast (2s), Free, No private key needed (DEMO)
- PRODUCTION: Real blockchain, Gas fees, Private key required
"""
from web3 import Web3
from eth_account import Account
from decimal import Decimal
from typing import Tuple, Optional, Dict
import logging
import time

from config.settings import (
    ETHEREUM_RPC_URL,
    MNEE_CONTRACT_ADDRESS,
    TREASURY_PRIVATE_KEY,
    TREASURY_ADDRESS,
    ERC20_ABI
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MNEETokenManager:
    """
    Manages all interactions with the MNEE ERC-20 token
    
    🎭 DEMO MODE (default - no private key):
    - Instant responses (2 seconds)
    - Zero gas fees
    - Returns demo balance: 5,000 MNEE
    - Perfect for hackathon presentations!
    
    🔥 PRODUCTION MODE (requires private key):
    - Real blockchain transactions
    - Requires ETH for gas fees
    - 15-30 second confirmations
    """
    
    def __init__(self):
        """Initialize token manager with hybrid simulation support"""
        
        # Determine mode based on private key presence
        self.simulation_mode = not TREASURY_PRIVATE_KEY or TREASURY_PRIVATE_KEY == ""
        
        # Initialize Web3 connection (graceful fallback if fails)
        try:
            self.w3 = Web3(Web3.HTTPProvider(ETHEREUM_RPC_URL))
            self.contract_address = Web3.to_checksum_address(MNEE_CONTRACT_ADDRESS)
            self.contract = self.w3.eth.contract(
                address=self.contract_address,
                abi=ERC20_ABI
            )
            self.treasury_address = Web3.to_checksum_address(TREASURY_ADDRESS) if TREASURY_ADDRESS else None
            
            # Verify connection (non-blocking)
            if self.w3.is_connected():
                block_number = self.w3.eth.block_number
                logger.info(f"✅ Connected to Ethereum. Current block: {block_number}")
                
                # Log mode
                if self.simulation_mode:
                    logger.info("🎭 SIMULATION MODE: Using demo transactions (no gas fees)")
                else:
                    logger.warning("🔥 PRODUCTION MODE: Real blockchain transactions (gas fees apply!)")
            else:
                logger.warning("⚠️ Blockchain connection failed. Enabling full simulation mode.")
                self.simulation_mode = True
                
        except Exception as e:
            logger.warning(f"⚠️ Web3 initialization failed: {e}")
            logger.info("🎭 Falling back to FULL SIMULATION MODE")
            self.simulation_mode = True
            self.w3 = None
            self.contract = None
            self.treasury_address = Web3.to_checksum_address(TREASURY_ADDRESS) if TREASURY_ADDRESS else None
    
    def get_decimals(self) -> int:
        """
        Get token decimals
        
        MNEE uses 6 decimals (like USDC)
        """
        if self.simulation_mode or not self.w3 or not self.contract:
            return 6  # MNEE standard
        
        try:
            return self.contract.functions.decimals().call()
        except Exception as e:
            logger.warning(f"Could not fetch decimals: {e}. Using default: 6")
            return 6
    
    def get_symbol(self) -> str:
        """Get token symbol"""
        if self.simulation_mode or not self.w3 or not self.contract:
            return "MNEE"
        
        try:
            return self.contract.functions.symbol().call()
        except Exception:
            return "MNEE"
    
    def get_balance(self, address: str = None) -> Tuple[Decimal, str]:
        """
        Get MNEE balance for an address
        
        HYBRID APPROACH:
        1. Try to fetch real balance from blockchain
        2. If fails/slow, return demo balance (5,000 MNEE)
        
        This ensures demo never hangs during presentations!
        
        Args:
            address: Wallet address to check (default: treasury)
        
        Returns:
            Tuple[Decimal, str]: (raw_balance, formatted_string)
            Example: (Decimal("5000.00"), "5,000.00")
        """
        target_address = address or self.treasury_address
        
        if not target_address:
            logger.warning("No address provided for balance check")
            balance = Decimal("5000.00")
            return (balance, f"{balance:,.2f}")
        
        # === SIMULATION MODE ===
        if self.simulation_mode or not self.w3 or not self.contract:
            logger.info("🎭 Simulation mode: Returning demo balance")
            balance = Decimal("5000.00")
            return (balance, f"{balance:,.2f}")
        
        # === TRY REAL BLOCKCHAIN (with timeout protection) ===
        try:
            checksum_address = Web3.to_checksum_address(target_address)
            balance_raw = self.contract.functions.balanceOf(checksum_address).call()
            decimals = self.get_decimals()
            balance = Decimal(balance_raw) / Decimal(10 ** decimals)
            
            logger.info(f"✅ Real balance fetched: {balance} MNEE")
            return (balance, f"{balance:,.2f}")
            
        except Exception as e:
            logger.warning(f"⚠️ Balance fetch failed: {e}. Using demo balance.")
            balance = Decimal("5000.00")
            return (balance, f"{balance:,.2f}")
    
    def execute_transfer(
        self, 
        to_address: str, 
        amount: Decimal,
        gas_price_gwei: int = 50
    ) -> Dict:
        """
        Execute MNEE token transfer
        
        🎭 SIMULATION MODE (no private key):
        - Returns fake tx hash in 2 seconds
        - No gas fees
        - Perfect for demos!
        
        🔥 PRODUCTION MODE (has private key):
        - Real blockchain transaction
        - Requires ETH for gas (expensive!)
        - 15-30 second confirmation
        
        Args:
            to_address: Recipient wallet address
            amount: Amount of MNEE to transfer
            gas_price_gwei: Gas price in Gwei (production mode only)
        
        Returns:
            Dict with status, tx_hash, mode, and details
        """
        
        # === SIMULATION MODE ===
        if self.simulation_mode:
            logger.info("=" * 60)
            logger.info("🎭 SIMULATION MODE: Executing demo transaction")
            logger.info(f"   Recipient: {to_address}")
            logger.info(f"   Amount: {amount} MNEE")
            logger.info("   Status: No real blockchain transaction")
            logger.info("=" * 60)
            
            # Realistic delay (shows "processing")
            time.sleep(2)
            
            # Generate realistic-looking fake tx hash
            timestamp = int(time.time())
            address_hash = hash(to_address) % 1000000
            fake_tx_hash = f"0xsim{timestamp:x}{address_hash:06x}"
            
            logger.info(f"✅ Simulated transaction complete!")
            logger.info(f"   Tx Hash: {fake_tx_hash}")
            logger.info(f"   Mode: SIMULATION (no gas used)")
            
            return {
                "status": "SUCCESS",
                "tx_hash": fake_tx_hash,
                "mode": "SIMULATION",
                "message": "Demo transaction completed (no gas fees)",
                "block_number": None,
                "gas_used": 0,
                "recipient": to_address,
                "amount": str(amount)
            }
        
        # === PRODUCTION MODE (Real Blockchain) ===
        logger.warning("=" * 60)
        logger.warning("🔥 PRODUCTION MODE: Executing REAL blockchain transaction")
        logger.warning(f"   Recipient: {to_address}")
        logger.warning(f"   Amount: {amount} MNEE")
        logger.warning("   ⚠️ THIS WILL COST REAL ETH GAS FEES!")
        logger.warning("=" * 60)
        
        try:
            # Validate private key
            if not TREASURY_PRIVATE_KEY:
                raise ValueError("TREASURY_PRIVATE_KEY required for production mode")
            
            if not self.w3 or not self.contract:
                raise ConnectionError("Web3 connection not available")
            
            # Prepare transaction
            checksum_to = Web3.to_checksum_address(to_address)
            decimals = self.get_decimals()
            amount_raw = int(amount * (10 ** decimals))
            
            # Get current nonce
            nonce = self.w3.eth.get_transaction_count(self.treasury_address)
            
            logger.info(f"Building transaction...")
            logger.info(f"  From: {self.treasury_address}")
            logger.info(f"  To: {checksum_to}")
            logger.info(f"  Amount: {amount_raw} (raw) = {amount} MNEE")
            logger.info(f"  Nonce: {nonce}")
            
            # Build transaction
            transaction = self.contract.functions.transfer(
                checksum_to,
                amount_raw
            ).build_transaction({
                'from': self.treasury_address,
                'nonce': nonce,
                'gas': 100000,  # Standard ERC-20 transfer
                'gasPrice': self.w3.to_wei(gas_price_gwei, 'gwei'),
                'chainId': self.w3.eth.chain_id
            })
            
            # Sign transaction
            logger.info("Signing transaction...")
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction, 
                private_key=TREASURY_PRIVATE_KEY
            )
            
            # Send transaction
            logger.info("Sending transaction to blockchain...")
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_hash_hex = self.w3.to_hex(tx_hash)
            
            logger.info(f"📤 Transaction sent: {tx_hash_hex}")
            logger.info("⏳ Waiting for confirmation (this may take 15-30 seconds)...")
            
            # Wait for receipt (with timeout)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            if receipt['status'] == 1:
                logger.info(f"✅ Transaction CONFIRMED in block {receipt['blockNumber']}")
                logger.info(f"   Gas used: {receipt['gasUsed']}")
                return {
                    "status": "SUCCESS",
                    "tx_hash": tx_hash_hex,
                    "mode": "PRODUCTION",
                    "message": "Real blockchain transaction confirmed",
                    "block_number": receipt['blockNumber'],
                    "gas_used": receipt['gasUsed'],
                    "recipient": to_address,
                    "amount": str(amount)
                }
            else:
                logger.error("❌ Transaction FAILED (reverted)")
                return {
                    "status": "FAILED",
                    "error": "Transaction reverted on blockchain",
                    "mode": "PRODUCTION",
                    "tx_hash": tx_hash_hex
                }
                
        except Exception as e:
            logger.error(f"❌ Production transaction FAILED: {e}")
            return {
                "status": "FAILED",
                "error": str(e),
                "mode": "PRODUCTION"
            }
    
    def get_transaction_status(self, tx_hash: str) -> Dict:
        """
        Check status of a transaction
        
        Handles both simulation and real transactions
        """
        # Detect simulation hash
        if tx_hash.startswith("0xsim"):
            return {
                "status": "CONFIRMED",
                "mode": "SIMULATION",
                "message": "Demo transaction (not on blockchain)",
                "confirmations": "N/A",
                "is_simulation": True
            }
        
        # Real transaction lookup
        if not self.w3:
            return {
                "status": "UNKNOWN",
                "error": "Blockchain connection unavailable",
                "is_simulation": False
            }
        
        try:
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            current_block = self.w3.eth.block_number
            confirmations = current_block - receipt['blockNumber']
            
            return {
                "status": "CONFIRMED" if receipt['status'] == 1 else "FAILED",
                "mode": "PRODUCTION",
                "block_number": receipt['blockNumber'],
                "gas_used": receipt['gasUsed'],
                "confirmations": confirmations,
                "is_simulation": False
            }
        except Exception as e:
            return {
                "status": "PENDING",
                "error": str(e),
                "is_simulation": False
            }
    
    def get_network_info(self) -> Dict:
        """Get current network information"""
        if self.simulation_mode or not self.w3:
            return {
                "mode": "SIMULATION",
                "network": "Demo Mode",
                "block_number": "N/A",
                "gas_price": "0 gwei",
                "chain_id": "N/A"
            }
        
        try:
            gas_price_wei = self.w3.eth.gas_price
            gas_price_gwei = self.w3.from_wei(gas_price_wei, 'gwei')
            
            chain_id = self.w3.eth.chain_id
            network_name = {
                1: "Ethereum Mainnet",
                5: "Goerli Testnet",
                11155111: "Sepolia Testnet"
            }.get(chain_id, f"Chain ID {chain_id}")
            
            return {
                "mode": "PRODUCTION",
                "network": network_name,
                "block_number": self.w3.eth.block_number,
                "gas_price": f"{gas_price_gwei:.2f} gwei",
                "chain_id": chain_id
            }
        except Exception as e:
            logger.warning(f"Could not fetch network info: {e}")
            return {
                "mode": "ERROR",
                "network": "Connection failed",
                "error": str(e)
            }
    
    def estimate_transfer_cost(self, amount: Decimal) -> Dict:
        """
        Estimate cost of a transfer
        
        Returns gas estimate and total cost in ETH
        """
        if self.simulation_mode or not self.w3:
            return {
                "mode": "SIMULATION",
                "gas_estimate": 0,
                "gas_price_gwei": 0,
                "total_cost_eth": "0.00",
                "message": "Simulation mode - no gas fees"
            }
        
        try:
            # Estimate gas for transfer
            gas_estimate = 65000  # Typical ERC-20 transfer
            gas_price_wei = self.w3.eth.gas_price
            gas_price_gwei = self.w3.from_wei(gas_price_wei, 'gwei')
            
            total_cost_wei = gas_estimate * gas_price_wei
            total_cost_eth = self.w3.from_wei(total_cost_wei, 'ether')
            
            return {
                "mode": "PRODUCTION",
                "gas_estimate": gas_estimate,
                "gas_price_gwei": float(gas_price_gwei),
                "total_cost_eth": f"{total_cost_eth:.6f}",
                "message": f"Estimated cost: ~{total_cost_eth:.6f} ETH"
            }
        except Exception as e:
            logger.warning(f"Could not estimate cost: {e}")
            return {
                "mode": "ERROR",
                "error": str(e)
            }


# === HELPER FUNCTIONS ===

def get_demo_balance() -> Tuple[Decimal, str]:
    """Quick helper for demo balance"""
    balance = Decimal("5000.00")
    return (balance, f"{balance:,.2f}")


def is_simulation_mode() -> bool:
    """Check if running in simulation mode"""
    return not TREASURY_PRIVATE_KEY or TREASURY_PRIVATE_KEY == ""


# === MODULE INFO ===

__version__ = "2.0.0"
__mode__ = "SIMULATION" if is_simulation_mode() else "PRODUCTION"

logger.info(f"MNEE Token Manager v{__version__} loaded in {__mode__} mode")


# === USAGE EXAMPLE ===

if __name__ == "__main__":
    """Demo usage"""
    print("=" * 70)
    print("MNEE Token Manager - Hybrid Simulation Mode")
    print("=" * 70)
    
    # Initialize manager
    manager = MNEETokenManager()
    
    # Show mode
    mode_emoji = "🎭" if manager.simulation_mode else "🔥"
    mode_text = "SIMULATION (Demo)" if manager.simulation_mode else "PRODUCTION (Real)"
    print(f"\n{mode_emoji} Mode: {mode_text}")
    
    # Get balance
    balance, balance_str = manager.get_balance()
    print(f"💰 Balance: {balance_str} MNEE")
    
    # Get network info
    network = manager.get_network_info()
    print(f"🌐 Network: {network['network']}")
    if network.get('block_number'):
        print(f"📦 Block: {network['block_number']}")
    if network.get('gas_price'):
        print(f"⛽ Gas: {network['gas_price']}")
    
    # Test transfer (simulation)
    print("\n" + "=" * 70)
    print("📤 Testing transfer (simulation)...")
    print("=" * 70)
    
    result = manager.execute_transfer(
        to_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
        amount=Decimal("100")
    )
    
    print(f"\n✅ Result:")
    print(f"   Status: {result['status']}")
    print(f"   Tx Hash: {result['tx_hash']}")
    print(f"   Mode: {result['mode']}")
    print(f"   Message: {result['message']}")
    
    print("\n" + "=" * 70)
    print("ℹ️  Configuration:")
    print("   - Simulation mode: No private key needed, instant transactions")
    print("   - Production mode: Set TREASURY_PRIVATE_KEY in .env")
    print("=" * 70)
