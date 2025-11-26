# IM 25/26 Interaction By Speech - Google Maps Speech Interactions

Voice-controlled Google Maps assistant using Python, Selenium, and RASA NLU.

## Quick Start

**IMPORTANT:** See SETUP.md for complete setup instructions!

### Prerequisites
- Python 3.12 ✅ (installed)
- Java 23 ✅ (installed)
- RASA NLU (need to install: `pip install --user rasa`)
- mmiframeworkV2.jar ❌ (MISSING - get from course materials)

### Running the System

1. Start MMI Framework: `cd Voice\mmiframeworkV2 && java -jar mmiframeworkV2.jar`
2. Start RASA: `cd Voice\rasaDemo && rasa run --enable-api --cors "*"`
3. Start Assistant: `cd Voice\Assistant && python main.py`

## Features
- Search locations and places
- Get directions (driving, walking, transit, cycling)
- Zoom, pan, change map views
- Show place details, reviews, photos
- Voice commands in Portuguese

## Project Structure
- `Voice/Assistant/` - Main assistant code
- `Voice/rasaDemo/` - RASA NLU configuration
- `Voice/mmiframeworkV2/` - MMI Framework server
- `SETUP.md` - Detailed setup guide

## Evaluation
To be seen

## Authors
* [Henrique Teixeira] - [@henriqueft04]
* [Duarte Santos] - [@duarters07]

---

Universidade de Aveiro, Ano letivo 2025/2026

