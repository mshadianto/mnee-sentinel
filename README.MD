# 🛡️ MNEE Sentinel: AI-Powered Treasury Guardian

**🏆 Hackathon Submission for MNEE - Programmable Finance Track**

> An AI-driven treasury management system that automates compliance checks, provides full audit trails, and executes transactions based on intelligent governance rules.

---

## 📁 Project Structure

```
mnee-sentinel/
│
├── 🤖 agents/                    # AI Agent Modules
│   ├── __init__.py
│   └── auditor_agent.py          # Multi-provider AI compliance engine
│
├── ⚙️ config/                    # Configuration
│   ├── __init__.py
│   └── settings.py               # Centralized settings & constants
│
├── 🗄️ database/                  # Database Layer
│   └── db_schema.sql             # Supabase PostgreSQL schema
│
├── 📚 docs/                      # Documentation
│   ├── INDEX.md                  # Documentation index
│   ├── DEMO_SCRIPT.md            # 2-minute demo walkthrough
│   ├── INSTALLATION_GUIDE.md     # Setup instructions
│   ├── PROJECT_SUMMARY.md        # Technical overview
│   ├── PDF_PARSING_GUIDE.md      # PDF feature guide
│   ├── PRE_DEMO_CHECKLIST.md     # Pre-presentation checklist
│   ├── SECURITY_CHECKLIST.md     # Security best practices
│   ├── TEST_PROPOSALS.md         # Sample test cases
│   └── ...                       # Other documentation
│
├── 📜 scripts/                   # Utility Scripts
│   ├── quick_start.sh            # Automated setup
│   └── process_invoices.py       # Batch PDF processing
│
├── 🛠️ utils/                     # Helper Utilities
│   ├── __init__.py
│   ├── crypto_utils.py           # Blockchain operations
│   ├── db_utils.py               # Database operations
│   └── document_parser.py        # Fast PDF parsing
│
├── 🎨 app.py                     # Main Streamlit Dashboard
├── 📋 requirements.txt           # Python dependencies
├── 📖 README.md                  # You are here!
├── 🔐 .env                       # Environment config (not in git)
└── 🚫 .gitignore                 # Git ignore rules
```

---

## 🎯 Problem Statement

Traditional DAO/Company treasuries face critical challenges:

| Problem | Impact |
|---------|--------|
| ⏱️ Manual Bottlenecks | Every payment requires human approval |
| 🔍 No Transparency | Unclear decision-making processes |
| ❌ Compliance Gaps | Hard to enforce budget rules consistently |
| 📝 Poor Audit Trails | Difficult to track historical decisions |

---

## 💡 Our Solution

MNEE Sentinel introduces an **AI Agent as Internal Auditor** that automates treasury governance:

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI Compliance** | Multi-provider AI (Groq/OpenAI/Claude) validates proposals |
| 📄 **PDF Parsing** | Upload invoices, auto-extract payment data (<1 sec) |
| 🔒 **Governance** | Vendor whitelist, budget limits, velocity checks |
| 📊 **Analytics** | Real-time budget visualization with Plotly |
| 📝 **Audit Trail** | Immutable decision logs with full reasoning |
| ⛓️ **Blockchain** | MNEE token integration on Ethereum mainnet |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Supabase account (free)
- AI API key (Groq recommended - free)

### Installation

```bash
# 1. Clone repository
git clone <your-repo>
cd mnee-sentinel

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Setup database
# Run database/db_schema.sql in Supabase SQL Editor

# 5. Launch
streamlit run app.py
```

The app opens at `http://localhost:8501` 🎉

---

## 🎮 How to Use

### Demo Flow

1. **Submit Proposal** → Type natural language request or upload PDF invoice
2. **AI Analysis** → AI parses and validates against governance rules
3. **Decision** → ✅ APPROVED (green) or 🚫 BLOCKED (red) with reasoning
4. **Execute** → Click to execute transaction (simulated or live)
5. **Audit Trail** → View complete history in Tab 3

### Example Proposal
```
Transfer 50 MNEE to PT Nusantara FX Services 
(0xA1b2C3D4e5F60718293aBcD4E5F6071829Ab) for FX hedging
```

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Streamlit + Plotly |
| **AI Engine** | LangChain (Groq/OpenAI/Anthropic) |
| **Database** | Supabase (PostgreSQL) |
| **Blockchain** | Web3.py + MNEE Token |
| **PDF Parser** | PyMuPDF (fast) |

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [docs/INDEX.md](docs/INDEX.md) | 📋 Documentation index |
| [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md) | 🎬 2-minute hackathon demo |
| [docs/INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md) | 🚀 Complete setup guide |
| [docs/PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md) | 🏗️ Technical architecture |
| [docs/TEST_PROPOSALS.md](docs/TEST_PROPOSALS.md) | 🧪 Sample test cases |
| [docs/SECURITY_CHECKLIST.md](docs/SECURITY_CHECKLIST.md) | 🔒 Security audit checklist |

---

## 🏆 Why This Wins

| Criteria | How We Excel |
|----------|--------------|
| ✅ **Real Problem** | Every DAO needs treasury governance |
| ✅ **MNEE Integration** | Native token support on Ethereum |
| ✅ **Innovation** | First AI-powered treasury compliance in DeFi |
| ✅ **Production Ready** | Clean architecture, full audit trail |
| ✅ **Scalable** | Modular design, easy to extend |

---

## 🔐 Security

- ✅ API keys stored in `.env` (gitignored)
- ✅ Address validation with checksums
- ✅ Transaction limits per vendor
- ✅ Velocity tracking (anti-fraud)
- ✅ Immutable audit logs

See [docs/SECURITY_CHECKLIST.md](docs/SECURITY_CHECKLIST.md) for full security guide.

---

## 📈 Future Roadmap

- [ ] Multi-signature approval workflows
- [ ] Gnosis Safe integration
- [ ] Scheduled recurring payments
- [ ] ML-based fraud detection
- [ ] Mobile app (React Native)
- [ ] Telegram/Slack notifications

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

MIT License - See LICENSE file for details

---

<div align="center">

## 🛡️ Securing Treasuries with AI, One Transaction at a Time

**Built with ❤️ for MNEE Hackathon 2024**

**Track**: Programmable Finance & Automation

---

[📺 Demo Video](#) • [🌐 Live Demo](#) • [📚 Documentation](docs/INDEX.md)

</div>