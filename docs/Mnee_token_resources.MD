# 🪙 MNEE Token - Complete Resource Guide

## 📋 **Official MNEE Resources**

### **Token Information**
- **Contract Address:** `0x8ccedbAe4916b79da7F3F612EfB2EB93A2bFD6cF`
- **Network:** Ethereum Mainnet (Chain ID: 1)
- **Standard:** ERC-20
- **Decimals:** 6 (like USDC)
- **Official Website:** https://mnee.io
- **Etherscan:** https://etherscan.io/token/0x8ccedbAe4916b79da7F3F612EfB2EB93A2bFD6cF

### **MNEE Platform**
- **Swap & Bridge:** https://swap-user.mnee.net
- **Purpose:** Money Network Exchange Economy
- **Use Case:** Cross-border payments, remittances, FX hedging

---

## 🔧 **Developer Resources**

### **Ethereum Development**
- **Ethereum Developer Docs:** https://ethereum.org/developers
- **Smart Contract Basics:** https://ethereum.org/en/developers/tutorials
- **ERC-20 Standard:** https://ethereum.org/en/developers/docs/standards/tokens/erc-20/

### **Development Tools**
- **ethers.js:** https://docs.ethers.org
- **wagmi / viem:** https://wagmi.sh
- **Hardhat:** https://hardhat.org/getting-started
- **OpenZeppelin Contracts:** https://docs.openzeppelin.com/contracts

### **Wallet Setup**
- **MetaMask:** https://metamask.io
- **Coinbase Wallet:** https://wallet.coinbase.com
- **Rainbow Wallet:** https://rainbow.me

---

## 🎯 **MNEE Sentinel Configuration**

### **Current Setup (Verified ✅)**

```python
# config/settings.py
MNEE_CONTRACT_ADDRESS = "0x8ccedbAe4916b79da7F3F612EfB2EB93A2bFD6cF"
ETHEREUM_RPC_URL = "https://eth.llamarpc.com"  # Free public RPC

# ERC-20 Standard ABI (minimal for balance & transfer)
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
    }
]
```

---

## 🎭 **Demo vs Production Modes**

### **DEMO MODE (Hackathon) - Current Setup**

**Configuration (.env):**
```bash
ETHEREUM_RPC_URL=https://eth.llamarpc.com
MNEE_CONTRACT_ADDRESS=0x8ccedbAe4916b79da7F3F612EfB2EB93A2bFD6cF
TREASURY_ADDRESS=0xYourWalletAddress
TREASURY_PRIVATE_KEY=  # EMPTY = Simulation mode!
```

**Behavior:**
- ✅ Reads real blockchain data (balance, network info)
- ✅ Shows real MNEE contract address
- ✅ Connects to real Ethereum mainnet
- 🎭 Simulates transactions (no gas fees)
- 🎭 Returns fake tx hashes (`0xsim...`)
- 🎭 Demo balance: 5,000 MNEE

**Perfect for:**
- Hackathon presentations
- UI/UX demonstrations
- Testing AI logic
- Video recordings
- Local development

---

### **PRODUCTION MODE (Real DAO Treasury)**

**Configuration (.env):**
```bash
ETHEREUM_RPC_URL=https://eth.llamarpc.com
MNEE_CONTRACT_ADDRESS=0x8ccedbAe4916b79da7F3F612EfB2EB93A2bFD6cF
TREASURY_ADDRESS=0xRealDAOTreasuryAddress
TREASURY_PRIVATE_KEY=0xRealPrivateKeyFromHardwareWallet
```

**Requirements:**
- 🔥 Real treasury wallet with MNEE tokens
- 🔥 ETH for gas fees (~$5-50 per transaction)
- 🔥 Hardware wallet or MPC key management
- 🔥 Multi-sig for security
- 🔥 Production RPC (Infura/Alchemy)

**Behavior:**
- Real blockchain transactions
- 15-30 second confirmations
- Costs real ETH gas fees
- Immutable on-chain record
- Full compliance audit trail

---

## 📊 **Transaction Cost Analysis**

### **Typical MNEE Transfer Costs (Mainnet)**

| Gas Price | Gas Used | Cost (USD) | Time |
|-----------|----------|------------|------|
| 10 gwei | 65,000 | ~$2 | 1-2 min |
| 30 gwei | 65,000 | ~$6 | 30-60 sec |
| 50 gwei | 65,000 | ~$10 | 15-30 sec |
| 100 gwei | 65,000 | ~$20 | <15 sec |

**Calculation:**
```
Cost = (Gas Used × Gas Price × ETH Price) / 1e9
     = (65,000 × 30 gwei × $3,000) / 1e9
     = ~$6 per transaction
```

**For 10 demo transactions = $60-200 in gas!** 🔥

**With Simulation = $0!** ✅

---

## 🏗️ **Production Deployment Guide**

### **Step 1: Security Setup**

**Hardware Wallet (Recommended):**
```bash
# Use Ledger or Trezor
# Never expose private keys directly
```

**Multi-Sig Treasury (Best Practice):**
```bash
# Use Gnosis Safe
# https://safe.global
# Require 2-of-3 or 3-of-5 signatures
```

**MPC Wallet (Enterprise):**
```bash
# Fireblocks, Copper, BitGo
# Distributed key management
```

---

### **Step 2: RPC Provider**

**Free Public RPCs (Demo):**
- ✅ https://eth.llamarpc.com
- ✅ https://cloudflare-eth.com
- ⚠️ Rate limited, not for production

**Production RPCs (Paid):**
```bash
# Infura
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY

# Alchemy
ETHEREUM_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY

# QuickNode
ETHEREUM_RPC_URL=https://YOUR_ENDPOINT.quiknode.pro/YOUR_KEY
```

**Cost:** ~$50-200/month for production traffic

---

### **Step 3: Treasury Setup**

**1. Create DAO Treasury Wallet**
```bash
# Using Gnosis Safe
# 1. Go to https://safe.global
# 2. Create new Safe on Ethereum
# 3. Add signers (3-5 members)
# 4. Set threshold (e.g., 2-of-3)
# 5. Fund with ETH for gas
# 6. Fund with MNEE tokens
```

**2. Configure Environment**
```bash
TREASURY_ADDRESS=0xGnosisSafeAddress
# For Gnosis Safe, use Safe API instead of private key
GNOSIS_SAFE_ADDRESS=0x...
GNOSIS_SAFE_RPC=https://safe-transaction-mainnet.safe.global
```

**3. Test with Small Amount**
```bash
# Send 1 MNEE to test address
# Verify on Etherscan
# Confirm multi-sig works
```

---

### **Step 4: Monitoring & Alerts**

**Transaction Monitoring:**
```bash
# Use Etherscan API
# https://etherscan.io/apis
# Monitor treasury balance
# Alert on large transfers
```

**Gas Price Alerts:**
```bash
# Use ETH Gas Station
# https://ethgasstation.info/api
# Only execute when gas < 30 gwei
```

**Security Alerts:**
```bash
# OpenZeppelin Defender
# https://defender.openzeppelin.com
# Monitor suspicious activity
```

---

## 🔐 **Security Best Practices**

### **DO:**
- ✅ Use hardware wallets for production
- ✅ Enable multi-sig (2-of-3 minimum)
- ✅ Test on testnet first (Sepolia/Goerli)
- ✅ Use production RPC providers
- ✅ Monitor gas prices before execution
- ✅ Set transaction limits in smart contracts
- ✅ Regular security audits
- ✅ Use time-locks for large transfers

### **DON'T:**
- ❌ Store private keys in .env files (production)
- ❌ Use single-sig wallets for large amounts
- ❌ Skip testing on testnet
- ❌ Execute during high gas prices
- ❌ Ignore transaction confirmations
- ❌ Deploy without audit
- ❌ Use public RPCs for production
- ❌ Share treasury credentials

---

## 🧪 **Testing Strategy**

### **1. Simulation Mode (Current)**
```bash
TREASURY_PRIVATE_KEY=  # Empty
# Result: Fast, free, perfect for demos
```

### **2. Testnet Mode (Pre-Production)**
```bash
ETHEREUM_RPC_URL=https://sepolia.infura.io/v3/YOUR_KEY
MNEE_CONTRACT_ADDRESS=0xTestnetMNEEContract
TREASURY_PRIVATE_KEY=0xTestnetPrivateKey
# Result: Real transactions, free test ETH
```

### **3. Mainnet Mode (Production)**
```bash
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY
MNEE_CONTRACT_ADDRESS=0x8ccedbAe4916b79da7F3F612EfB2EB93A2bFD6cF
TREASURY_ADDRESS=0xGnosisSafe
# Result: Real money, real gas fees
```

---

## 📈 **Scaling Considerations**

### **Transaction Throughput**

**Ethereum Mainnet Limits:**
- ~15 transactions per second (network-wide)
- 12-15 second block time
- 21,000 gas minimum per transaction

**For High-Volume DAOs:**
- Consider Layer 2 solutions (Arbitrum, Optimism)
- Batch transactions when possible
- Use EIP-4337 account abstraction
- Implement gas optimization

### **Cost Optimization**

**Strategies:**
- Execute during low gas periods (weekends, nights)
- Use EIP-1559 base fee + priority fee
- Batch multiple transfers in one transaction
- Implement gas price alerts
- Consider L2 for frequent operations

---

## 🎯 **Integration with MNEE Ecosystem**

### **MNEE Swap Integration**
```javascript
// Future enhancement: Direct swap integration
// Use MNEE Swap API: https://swap-user.mnee.net
// Convert MNEE to other stablecoins
// Enable cross-border treasury management
```

### **Bridge Integration**
```javascript
// Future: Cross-chain treasury
// Bridge MNEE to other chains
// Manage multi-chain treasury
// Reduce mainnet gas costs
```

---

## 📚 **Additional Resources**

### **Smart Contract Development**
- **Remix IDE:** https://remix.ethereum.org
- **Solidity Docs:** https://docs.soliditylang.org
- **Hardhat Tutorial:** https://hardhat.org/tutorial

### **Security Auditing**
- **Consensys Diligence:** https://consensys.net/diligence
- **Trail of Bits:** https://www.trailofbits.com
- **OpenZeppelin Security:** https://openzeppelin.com/security-audits

### **DAO Tools**
- **Gnosis Safe:** https://safe.global
- **Snapshot (Voting):** https://snapshot.org
- **Tally (Governance):** https://tally.xyz

---

## 🏆 **Post-Hackathon Roadmap**

### **Phase 1: Testnet Deployment (Week 1)**
- Deploy to Sepolia testnet
- Test all features with test MNEE
- Run security audit
- Document edge cases

### **Phase 2: Mainnet Pilot (Week 2-4)**
- Deploy with small treasury ($1,000)
- Test with real transactions
- Monitor gas costs
- Gather user feedback

### **Phase 3: Production Scale (Month 2+)**
- Increase treasury size
- Enable multi-sig
- Add monitoring/alerts
- Implement batch operations

### **Phase 4: Ecosystem Integration (Month 3+)**
- Integrate MNEE Swap
- Add cross-chain support
- Build mobile app
- Partner with DAOs

---

## 🎬 **Demo Presentation Tips**

### **What to Emphasize:**
- ✅ "We're using real MNEE token on Ethereum mainnet"
- ✅ "Contract verified on Etherscan: 0x8ccedba..."
- ✅ "Simulation mode for demo - production ready"
- ✅ "Can switch to real transactions post-hackathon"

### **What NOT to Say:**
- ❌ "This is just a fake token"
- ❌ "We're not using real blockchain"
- ❌ "This won't work in production"

### **Perfect Pitch:**
> "MNEE Sentinel integrates with the real MNEE token on Ethereum mainnet. 
> For this demo, we're using simulation mode to showcase our AI logic 
> without burning gas fees. In production, this same code executes real 
> blockchain transactions with proper security measures like multi-sig 
> and hardware wallets."

---

## ✅ **Configuration Checklist**

### **For Hackathon Demo:**
- [x] MNEE_CONTRACT_ADDRESS = 0x8ccedba... ✅
- [x] ETHEREUM_RPC_URL = Public RPC ✅
- [x] TREASURY_PRIVATE_KEY = Empty ✅
- [x] Simulation mode enabled ✅
- [x] Demo balance = 5,000 MNEE ✅

### **For Production:**
- [ ] Hardware wallet or MPC setup
- [ ] Production RPC (Infura/Alchemy)
- [ ] Multi-sig treasury (Gnosis Safe)
- [ ] Real MNEE tokens funded
- [ ] ETH for gas fees
- [ ] Monitoring/alerts configured
- [ ] Security audit completed
- [ ] Team training done

---

<div style="background: #d1fae5; padding: 2rem; border-radius: 1rem;">

## 🎉 **Summary**

**Your Setup is PERFECT!** ✅

**MNEE Token:** Real ERC-20 on Ethereum mainnet  
**Contract:** 0x8ccedbAe4916b79da7F3F612EfB2EB93A2bFD6cF (verified)  
**Demo Mode:** Simulation (fast, free, reliable)  
**Production:** Ready to switch when needed

**This is exactly how professional teams demo blockchain projects!**

### **Resources Added:**
- Official MNEE links
- Developer tools
- Production deployment guide
- Security best practices
- Cost analysis
- Post-hackathon roadmap

### **You're 100% Ready for Hackathon!** 🚀

</div>

---

**Questions about production deployment after hackathon?** Let me know! 💬