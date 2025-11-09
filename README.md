# Inter-sight: AI-Powered Recruitment Platform

<div align="center">

![Inter-sight Logo](https://img.shields.io/badge/Inter--sight-🎯-blue?style=for-the-badge)
![Python Version](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

**An intelligent recruitment assistant powered by Google Gemini AI, designed to streamline candidate evaluation with 360° analysis, risk assessment, and actionable insights.**

[Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Configuration](#-configuration)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [🎯 Features](#-features)
- [🏗️ Architecture](#-architecture)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [⚙️ Configuration](#-configuration)
- [💻 Usage Guide](#-usage-guide)
- [📁 Project Structure](#-project-structure)
- [🔧 API Integration](#-api-integration)
- [🗄️ Database Schema](#-database-schema)
- [🤖 AI Analysis Framework](#-ai-analysis-framework)
- [🐳 Docker Setup](#-docker-setup)
- [📚 File Documentation](#-file-documentation)
- [🐛 Troubleshooting](#-troubleshooting)
- [📝 License](#-license)

---

## Overview

**Inter-sight** is an advanced recruitment platform that leverages artificial intelligence to automate and enhance the candidate screening process. Using Google's Gemini 2.0 Flash model, Inter-sight performs comprehensive 360° candidate analysis across three critical dimensions:

1. **Evidence Pillar**: Technical fit and cultural alignment assessment
2. **Risk Pillar**: Identification of red flags and potential concerns
3. **Potential Pillar**: Discovery of hidden gems and growth opportunities

The platform provides recruiters with an intuitive swipe interface for rapid candidate evaluation, automated feedback generation, and persistent data storage for future reference.

---

## 🎯 Features

### Core Recruitment Features

- **📄 Multi-Format Document Support**
  - PDF resume processing
  - DOCX document parsing
  - Automatic text extraction from various document formats

- **🔍 Intelligent Candidate Triage**
  - Automatic job category classification (Tech, Design, Sales, Manual Labor, Other)
  - Relevant skill detection
  - External profile identification (GitHub, LinkedIn, Behance, Dribbble)

- **🎨 360° Candidate Analysis**
  - **Technical Fit Assessment**: Skill matching with detailed fit scores
  - **Cultural Fit Evaluation**: Value alignment with company culture
  - **Risk Assessment**: Red flag identification and risk analysis
  - **Potential Discovery**: Hidden gems and growth opportunities
  - **Match Accuracy Scoring**: Overall compatibility percentage (0-100%)

- **🎮 Interactive Swipe Interface**
  - Modern, intuitive candidate review cards
  - Smooth animations and transitions
  - Three-button action system (Accept, Reject, On Hold)
  - Real-time candidate progression tracking

- **🚨 Traffic Light System**
  - Color-coded candidate status indicators
  - **Green**: Strong candidate match
  - **Yellow**: Potential fit, needs consideration
  - **Red**: Poor match or significant concerns

- **📧 Automated Feedback Generation**
  - AI-powered rejection emails
  - Empathetic, constructive feedback
  - Personalized improvement suggestions
  - Professional communication templates

- **📊 Executive Summary Reports**
  - Concise candidate overviews for leadership
  - Pros and cons analysis
  - Interview recommendations
  - Decision support documentation

- **🔗 External Profile Integration**
  - GitHub repository analysis and star metrics
  - Portfolio website scraping and content extraction
  - Public profile contextual information
  - Developer contributions assessment

- **💾 Persistent Data Storage**
  - PostgreSQL database integration
  - Candidate history tracking
  - Analysis result archiving
  - Audit trail maintenance

- **🔐 Privacy Features**
  - Blind mode candidate review (anonymized candidates)
  - Name and identifier masking options
  - Secure file handling

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                        │
│          (Interactive UI, Animations, Controls)              │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼────┐ ┌────▼────┐ ┌────▼──────┐
│   Config   │ │ Prompts │ │   Utils   │
│  (Settings)│ │ (Prompts)│ │ (Helpers) │
└────────────┘ └─────────┘ └────┬──────┘
                                 │
                    ┌────────────┼─────────────┐
                    │            │             │
            ┌───────▼──┐  ┌──────▼───┐  ┌────▼────┐
            │  Gemini  │  │  GitHub  │  │ BeautifulSoup
            │   API    │  │   API    │  │ (Portfolio)
            └──────────┘  └──────────┘  └─────────┘
                    │
            ┌───────▼─────────┐
            │   PostgreSQL    │
            │    Database     │
            └─────────────────┘
```

### Data Flow

1. **Upload Phase**: User uploads CV files (PDF/DOCX)
2. **Parsing Phase**: Documents are converted to text
3. **Triage Phase**: AI classifies job category and identifies external profiles
4. **Enrichment Phase**: GitHub/Portfolio data is fetched
5. **Analysis Phase**: 360° analysis is performed
6. **Storage Phase**: Results are saved to database
7. **Review Phase**: Recruiter reviews and makes decisions
8. **Feedback Phase**: Automated communications are generated

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose (for database)
- Google Gemini API Key
- 2GB+ available disk space

### 5-Minute Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/intersight.git
   cd intersight
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Google API Key
   echo "GOOGLE_API_KEY=your-api-key-here" >> .env
   ```

3. **Start the database**
   ```bash
   docker-compose up -d
   ```

4. **Install dependencies and run**
   ```bash
   pip install -r requirements.txt
   cd src
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501` and start using Inter-sight!

---

## 📦 Installation

### Complete Installation Guide

#### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/intersight.git
cd intersight
```

#### Step 2: Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### Step 3: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Package Details:**
- `streamlit`: Web application framework
- `google-generativeai`: Gemini API client
- `PyMuPDF`: PDF document processing
- `python-docx`: Word document parsing
- `beautifulsoup4`: HTML parsing for portfolio scraping
- `requests`: HTTP client for API calls
- `psycopg2-binary`: PostgreSQL database adapter
- `python-dotenv`: Environment variable management

#### Step 4: Set Up PostgreSQL Database

**Option A: Using Docker (Recommended)**

```bash
docker-compose up -d
```

This will:
- Pull the official PostgreSQL 15 Alpine image
- Create a container named `intersight_db`
- Expose port 5433
- Initialize the database with schema

**Option B: Manual PostgreSQL Setup**

```bash
# Create database and user
createdb intersight_db
createuser intersight_user
psql intersight_db -c "ALTER USER intersight_user WITH PASSWORD 'intersight@pass@123';"

# Run the schema (will be provided)
psql -U intersight_user -d intersight_db -f schema.sql
```

#### Step 5: Configure Environment

Create a `.env` file in the project root:

```env
# Google Gemini API Configuration
GOOGLE_API_KEY=your-actual-api-key-here

# Database Configuration
DB_NAME=intersight_db
DB_USER=intersight_user
DB_PASS=intersight@pass@123
DB_HOST=localhost
DB_PORT=5433

# Application Settings
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=50MB
```

#### Step 6: Verify Installation

```bash
# Test Python imports
python -c "import streamlit, google.generativeai, psycopg2; print('✅ All imports successful')"

# Test database connection
cd src && python -c "from utils import get_db_connection; print('✅ Database connection OK' if get_db_connection() else '❌ Database connection failed')"
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GOOGLE_API_KEY` | Google Gemini API authentication key | N/A | ✅ Yes |
| `DB_NAME` | PostgreSQL database name | intersight_db | ❌ No |
| `DB_USER` | PostgreSQL username | intersight_user | ❌ No |
| `DB_PASS` | PostgreSQL password | intersight@pass@123 | ❌ No |
| `DB_HOST` | PostgreSQL host address | localhost | ❌ No |
| `DB_PORT` | PostgreSQL port number | 5433 | ❌ No |
| `UPLOAD_DIR` | Directory for file uploads | ./uploads | ❌ No |
| `MAX_FILE_SIZE` | Maximum uploadable file size | 50MB | ❌ No |

### Configuration Files

#### `config.py`
- Loads environment variables
- Initializes Gemini API
- Provides database connection settings
- Manages API credentials securely

#### `.env` File Template

```bash
# API Configuration
GOOGLE_API_KEY=AIzaSy...

# Database Connection
DB_NAME=intersight_db
DB_USER=intersight_user
DB_PASS=intersight@pass@123
DB_HOST=localhost
DB_PORT=5433

# File Management
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=50MB
DELETE_FILES_AFTER_DAYS=30
```

---

## 💻 Usage Guide

### Starting the Application

```bash
cd src
streamlit run app.py
```

The application will launch at `http://localhost:8501`

### User Interface Walkthrough

#### Step 1: Upload CVs & Job Context

1. **Upload Job Description**
   - Paste the job description in the text area
   - Include required skills and responsibilities
   - Optionally add company culture information

2. **Upload CVs**
   - Drag and drop CV files (PDF or DOCX)
   - Multiple files can be uploaded simultaneously
   - Supported formats: PDF, DOCX, TXT

3. **Enable Optional Features**
   - Toggle "Blind Mode" for anonymous reviews
   - Enable "GitHub Analysis" for tech positions
   - Activate "Portfolio Analysis" for design roles

#### Step 2: Candidate Review (Swipe Interface)

For each candidate, you'll see:

- **Traffic Light Indicator**: Overall match status (Green/Yellow/Red)
- **Match Score**: Overall compatibility percentage
- **Analyst Verdict**: AI summary of the candidate
- **Technical Fit**: Skill-by-skill breakdown with evidence
- **Hidden Gems**: Potential strengths and growth opportunities
- **Red Flags**: Concerns and risk indicators

**Action Buttons:**
- ⬅️ **Reject**: Not a fit for the position
- ⏸️ **On Hold**: Needs further consideration
- ✅ **Accept**: Strong candidate, move forward

#### Step 3: Final Decision (On Hold Candidates)

For candidates marked "On Hold":
- Review their detailed analysis again
- Request an executive summary report
- Make a final accept/reject decision

#### Step 4: Review Feedback Emails

- View auto-generated rejection emails
- Copy and customize as needed
- Send to candidates via your email system

### Advanced Features

#### Blind Mode
```python
# Hides candidate names and shows only avatars
# Reduces unconscious bias in the hiring process
```

#### GitHub Integration
- Automatically fetches top repositories
- Analyzes programming languages used
- Reviews project stars and community engagement

#### Portfolio Analysis
- Scrapes design portfolio websites
- Extracts project descriptions
- Analyzes design trends and capabilities

---

## 📁 Project Structure

```
intersight/
├── src/
│   ├── __pycache__/              # Python cache files
│   ├── uploads/                  # Temporary upload directory
│   ├── app.py                    # Main Streamlit application
│   ├── config.py                 # Configuration and settings
│   ├── prompts.py                # AI prompt templates
│   └── utils.py                  # Utility functions
│
├── uploads/                      # Persistent upload storage
│
├── .env                          # Environment variables (create this)
├── .env.example                  # Example environment file
├── .gitignore                    # Git ignore rules
├── docker-compose.yml            # Docker services configuration
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

### Key Directories

- **`src/`**: Core application code
  - `app.py`: Main Streamlit UI and orchestration
  - `config.py`: Configuration management
  - `prompts.py`: AI prompt templates
  - `utils.py`: Helper functions

- **`uploads/`**: Where uploaded CVs are stored
  - Named with timestamp prefix for tracking
  - Example: `1762667205_resume.pdf`

---

## 🔧 API Integration

### Google Gemini API

#### Setup

1. Go to [Google AI Studio](https://aistudio.google.com)
2. Create a free account
3. Generate an API key
4. Add to `.env` file

#### Usage

```python
from utils import call_gemini_api

prompt = "Analyze this CV..."
response = call_gemini_api(prompt)
```

#### API Endpoints Used

- `genai.GenerativeModel('gemini-2.0-flash-exp')`
  - Model: Gemini 2.0 Flash (latest)
  - Max Tokens: Auto (up to 32k context)
  - Temperature: Default (0.7)

#### Rate Limits

- Free tier: 60 requests per minute
- Paid tier: Higher limits available
- Batch processing: Recommended for large uploads

### GitHub API

#### Integration

```python
from utils import get_github_context

github_url = "https://github.com/username"
context = get_github_context(github_url)
```

#### What's Fetched

- Repository names and descriptions
- Star counts and popularity metrics
- Programming languages used
- Top 3 repositories by stars

#### Limitations

- Public repositories only
- No authentication required
- Rate limit: 60 requests per hour (unauthenticated)

### Portfolio Website Scraping

#### Integration

```python
from utils import get_portfolio_context

portfolio_url = "https://designer.portfolio.com"
content = get_portfolio_context(portfolio_url)
```

#### Capabilities

- Extracts visible text content
- Handles dynamic and static websites
- Timeout: 10 seconds per request
- Max content: 2000 characters

---

## 🗄️ Database Schema

### PostgreSQL Tables

#### `candidates` Table

```sql
CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    cv_filename VARCHAR(255) NOT NULL,
    cv_filepath TEXT NOT NULL,
    analysis_360 JSONB NOT NULL,
    feedback_email_html TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Table Fields

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PRIMARY KEY | Unique candidate identifier |
| cv_filename | VARCHAR(255) | Original uploaded filename |
| cv_filepath | TEXT | Path to stored CV file |
| analysis_360 | JSONB | Full 360° analysis JSON |
| feedback_email_html | TEXT | Generated rejection email |
| status | VARCHAR(50) | Current status (pending, analyzed, rejected, accepted) |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Last update time |

### Example Data Structure

```json
{
  "id": 1,
  "cv_filename": "resume.pdf",
  "cv_filepath": "/uploads/1762667205_resume.pdf",
  "analysis_360": {
    "traffic_light": "green",
    "overall_match_accuracy": 85,
    "risk_pillar": { "red_flags": [] },
    "potential_pillar": { "green_flags": [], "plus_skills": [] },
    "evidence_pillar": { "technical_fit": [], "cultural_fit": [] },
    "analyst_summary": "Strong candidate match..."
  },
  "status": "analyzed",
  "created_at": "2024-11-09 13:53:00"
}
```

---

## 🤖 AI Analysis Framework

### Three Pillars of Analysis

#### 1️⃣ Evidence Pillar (Verifiable Skills & Alignment)

**Technical Fit Assessment**
```json
{
  "skill": "Python",
  "fit_score_%": 95,
  "cv_evidence": "5 years Python development experience..."
}
```

**Cultural Fit Evaluation**
```json
{
  "value": "Innovation",
  "cv_evidence": "Led 3 successful product launches..."
}
```

#### 2️⃣ Risk Pillar (Concerns & Red Flags)

**Red Flag Categories**
- Employment gaps
- Skill mismatches
- Geographic concerns
- Compensation expectations
- Career trajectory concerns
- Language/communication barriers

```json
{
  "alert": "3-Year Employment Gap",
  "detail": "No employment from 2020-2023, unclear reason"
}
```

#### 3️⃣ Potential Pillar (Growth & Hidden Opportunities)

**Green Flags (Positive Indicators)**
```json
{
  "hidden_gem": "Self-Learning Capability",
  "detail": "Completed 15 online certifications in 2023"
}
```

**Plus Skills (Bonus Competencies)**
```json
{
  "plus_skills": ["Public Speaking", "Team Leadership", "Technical Writing"]
}
```

### Traffic Light System

| Status | Criteria | Action |
|--------|----------|--------|
| 🟢 **Green** | 80%+ match, no major red flags | Fast-track to interview |
| 🟡 **Yellow** | 60-79% match, mixed signals | Further consideration needed |
| 🔴 **Red** | <60% match, significant concerns | Consider for alternative roles |

### Match Accuracy Score

Calculation based on:
- Skills alignment (40% weight)
- Experience level (30% weight)
- Cultural fit (20% weight)
- Education and certifications (10% weight)

---

## 🐳 Docker Setup

### Docker Compose Configuration

```yaml
services:
  db:
    image: postgres:15-alpine
    container_name: intersight_db
    environment:
      POSTGRES_USER: intersight_user
      POSTGRES_PASSWORD: intersight@pass@123
      POSTGRES_DB: intersight_db
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### Docker Commands

#### Start Services
```bash
docker-compose up -d
```

#### View Logs
```bash
docker-compose logs -f db
```

#### Stop Services
```bash
docker-compose down
```

#### Remove All Data
```bash
docker-compose down -v
```

#### Access PostgreSQL CLI
```bash
docker exec -it intersight_db psql -U intersight_user -d intersight_db
```

### Verification

```bash
# Check if database is running
docker ps | grep intersight_db

# Test connection
psql -h localhost -p 5433 -U intersight_user -d intersight_db -c "SELECT 1;"
```

---

## 📚 File Documentation

### `app.py` - Main Application

**Purpose**: Streamlit UI orchestration and main application logic

**Key Components**:
- Session state management
- File upload handling
- Candidate review interface
- Swipe animation controls
- Feedback generation

**Main Functions**:
- `set_page_config()`: Configure page settings
- `initialize_session_state()`: Set up session variables
- Upload logic: Handle CV file processing
- Review logic: Manage candidate swiping
- Feedback logic: Generate emails

**Dependencies**: streamlit, config, prompts, utils

---

### `config.py` - Configuration Management

**Purpose**: Environment setup and API configuration

**Contents**:
- Load environment variables
- Google Gemini API initialization
- Database connection parameters
- File storage settings

**Key Variables**:
```python
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DB_NAME = "intersight_db"
DB_USER = "intersight_user"
DB_PASS = "intersight@pass@123"
DB_HOST = "localhost"
DB_PORT = "5433"
```

---

### `prompts.py` - AI Prompt Templates

**Purpose**: Define structured prompts for Gemini API

**Prompts Included**:

1. **PROMPT_TRIAGE** - Job classification
   - Input: Job description + CV
   - Output: Job category + relevant URLs

2. **PROMPT_MATCHING_360** - Full candidate analysis
   - Input: Job description + CV + external context
   - Output: Complete 360° analysis JSON

3. **PROMPT_EXECUTIVE_SUMMARY** - Leadership summary
   - Input: Analysis JSON + company culture
   - Output: Concise recommendation summary

4. **PROMPT_FEEDBACK** - Rejection email
   - Input: Candidate info + analysis
   - Output: Professional feedback email

---

### `utils.py` - Utility Functions

**Purpose**: Helper functions and API integrations

**Key Functions**:

#### Document Processing
```python
def read_document(uploaded_file):
    """Extract text from PDF, DOCX, or TXT files"""
```

#### Link Detection
```python
def find_links(cv_text):
    """Extract URLs from CV text"""
```

#### External Profile Analysis
```python
def get_github_context(github_url):
    """Fetch public GitHub profile data"""

def get_portfolio_context(portfolio_url):
    """Scrape portfolio website content"""
```

#### AI Integration
```python
def call_gemini_api(prompt_with_data):
    """Call Gemini API and return response"""
```

#### Database Operations
```python
def get_db_connection():
    """Establish PostgreSQL connection"""

def save_to_db(filename, filepath, analysis_json, feedback_email, status):
    """Store candidate analysis in database"""
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Issue: "API Key Invalid"
**Solution**:
```bash
# Verify API key in .env file
cat .env | grep GOOGLE_API_KEY

# Test API connection
python -c "import google.generativeai as genai; print('✅ API OK')"
```

#### Issue: "Database Connection Failed"
**Solution**:
```bash
# Check if Docker container is running
docker ps | grep intersight_db

# If not running, start it
docker-compose up -d

# Verify connection
psql -h localhost -p 5433 -U intersight_user -d intersight_db -c "SELECT 1;"
```

#### Issue: "ModuleNotFoundError" for imports
**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify installation
python -c "import streamlit, google.generativeai; print('✅ Imports OK')"
```

#### Issue: "Port 5433 Already in Use"
**Solution**:
```bash
# Find process using port
lsof -i :5433

# Kill the process (Unix/Mac)
kill -9 <PID>

# Or change port in docker-compose.yml
# Change "5433:5432" to "5434:5432"
```

#### Issue: "Streamlit Connection Timeout"
**Solution**:
```bash
# Increase Streamlit timeout
streamlit run app.py --logger.level=debug

# Check network connectivity
ping localhost
telnet localhost 8501
```

#### Issue: "Large File Upload Fails"
**Solution**:
```python
# In config.py, increase file size limit
MAX_FILE_SIZE = 100  # MB
UPLOAD_CHUNK_SIZE = 1024 * 1024 * 5  # 5MB chunks
```

---

## 🚀 Performance Optimization

### Tips for Better Performance

1. **Batch Processing**
   - Upload multiple CVs at once
   - Reduces database calls
   - Faster processing pipeline

2. **Cache Management**
   - Clear temporary uploads regularly
   - Archive old analysis results
   - Maintain database performance

3. **API Optimization**
   - Use Gemini API batch processing for 10+ candidates
   - Implement request queuing
   - Monitor rate limits

4. **Database Optimization**
   ```sql
   -- Add indexes for faster queries
   CREATE INDEX idx_candidate_status ON candidates(status);
   CREATE INDEX idx_candidate_created ON candidates(created_at);
   ```

---

## 📊 Analytics & Reporting

### Accessing Historical Data

```python
# Query candidates by status
SELECT * FROM candidates WHERE status = 'analyzed';

# Get average match score
SELECT AVG(analysis_360->>'overall_match_accuracy') FROM candidates;

# Find top matches
SELECT * FROM candidates 
ORDER BY (analysis_360->>'overall_match_accuracy')::int DESC 
LIMIT 10;
```

---

## 🔐 Security Considerations

### Best Practices

1. **API Key Protection**
   - Never commit .env files
   - Use environment variables only
   - Rotate keys periodically

2. **Database Security**
   - Use strong passwords
   - Limit database access
   - Enable SSL connections in production

3. **File Upload Security**
   - Validate file types
   - Scan for malware
   - Clean up temporary files

4. **Data Privacy**
   - Use blind mode for anonymity
   - Implement access controls
   - Regular security audits

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black src/

# Lint code
flake8 src/
```

---

## 📧 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/intersight/issues)
- **Email**: support@intersight.app
- **Documentation**: [Full Docs](https://docs.intersight.app)

---

## 🙏 Acknowledgments

- Google AI for the Gemini API
- Streamlit team for the amazing framework
- PostgreSQL for reliable data storage
- Open-source community for dependencies

---

<div align="center">

**Made with ❤️ for better recruitment**

[⬆ Back to Top](#inter-sight-ai-powered-recruitment-platform)

</div>
