# AI-Driven Flight Booking System

An intelligent, voice-based flight booking system powered by AI that enables seamless customer interactions for selecting and booking flights.

## 🎯 Project Overview

This system integrates cutting-edge technologies to provide a fully automated flight booking experience:

- **Voice Interface**: Speech-to-Text (STT) and Text-to-Speech (TTS)
- **AI Intelligence**: Groq LLM for natural language processing
- **Real-time Flight Data**: Airlabs API integration
- **Secure Data Management**: Airtable backend
- **Email Communication**: Automated confirmations and payment links

## 🏗️ Architecture

```
AI-Flight-Booking-System/
├── src/
│   ├── main.py                 # Application entry point
│   ├── config.py               # Configuration management
│   ├── speech/
│   │   ├── stt.py              # Speech-to-Text engine
│   │   └── tts.py              # Text-to-Speech engine
│   ├── ai/
│   │   ├── llm_handler.py       # Groq LLM integration
│   │   └── intent_extractor.py  # Intent and info extraction
│   ├── flight/
│   │   ├── airlabs_api.py       # Airlabs API client
│   │   └── flight_matcher.py    # Flight matching logic
│   ├── booking/
│   │   ├── booking_manager.py   # Booking workflow
│   │   ├── payment_handler.py   # Payment processing
│   │   └── confirmation.py      # Booking confirmation
│   ├── database/
│   │   ├── airtable_client.py   # Airtable integration
│   │   └── models.py            # Data models
│   ├── email/
│   │   ├── email_sender.py      # Email service
│   │   └── templates.py         # Email templates
│   └── conversation/
│       └── conversation_flow.py # Main conversation orchestration
├── tests/
│   ├── test_stt.py
│   ├── test_llm.py
│   ├── test_flight_api.py
│   ├── test_booking.py
│   └── test_integration.py
├── config/
│   ├── settings.env             # Environment variables
│   ├── logging_config.json      # Logging configuration
│   └── prompts.json             # LLM system prompts
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose setup
└── docs/
    ├── SETUP.md                 # Setup instructions
    ├── API.md                   # API documentation
    └── WORKFLOW.md              # Workflow documentation
```

## 🚀 Features

### Core Functionality
- ✅ Voice-based conversational interface
- ✅ Real-time flight search and comparison
- ✅ Intelligent flight selection based on user preferences
- ✅ Automated booking process
- ✅ Payment handling (automatic + manual)
- ✅ Email confirmations and payment links
- ✅ Secure customer data management

### Advanced Features
- Multi-criteria flight matching (price, timing, availability)
- Natural language understanding of travel requirements
- Customer data extraction and validation
- Real-time pricing and availability updates
- Fallback payment options
- Booking history tracking

## 📋 Prerequisites

- Python 3.9+
- Groq API key
- Airlabs API key
- Airtable API token and base ID
- Email service credentials (SMTP)
- Speech recognition/synthesis libraries

## ⚙️ Installation

### Using pip

```bash
git clone https://github.com/PratikPrajapati91/AI-Flight-Booking-System.git
cd AI-Flight-Booking-System

pip install -r requirements.txt
```

### Using Docker

```bash
docker-compose up --build
```

### Configuration

1. Copy `.env.example` to `.env`
2. Fill in your API credentials:
   ```bash
   GROQ_API_KEY=your_groq_key
   AIRLABS_API_KEY=your_airlabs_key
   AIRTABLE_TOKEN=your_airtable_token
   AIRTABLE_BASE_ID=your_base_id
   SMTP_EMAIL=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   ```

## 🎯 Workflow

### User Journey

```
1. User starts application
2. System captures voice input (STT)
3. LLM processes user intent and extracts:
   - Travel dates
   - Destinations
   - Preferences (price, timing, airline)
   - Personal info (name, DOB, email)
4. System queries Airlabs API for flights
5. AI ranks and presents top options
6. User selects flight via voice
7. System initiates booking
8. Payment processing:
   - Attempts automatic payment
   - Or sends secure payment link
9. Sends confirmation email
10. Stores booking in Airtable
```

## 📚 Usage

### Basic Usage

```python
from src.main import FlightBookingSystem

# Initialize system
app = FlightBookingSystem()

# Start conversation
app.start_booking_session()
```

### Advanced Configuration

See [SETUP.md](docs/SETUP.md) for detailed configuration options.

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_flight_api.py
```

## 📖 Documentation

- [Setup Guide](docs/SETUP.md) - Detailed installation and configuration
- [API Documentation](docs/API.md) - API reference and integration details
- [Workflow Documentation](docs/WORKFLOW.md) - System workflows and processes

## 🔐 Security Considerations

- All API keys stored in environment variables
- Customer data encrypted in Airtable
- Secure payment processing with consent validation
- HTTPS for all external communications
- Input validation and sanitization
- Rate limiting on API calls

## 🛠️ Technologies

| Component | Technology |
|-----------|------------|
| Speech Recognition | SpeechRecognition / Google Cloud Speech API |
| Text-to-Speech | pyttsx3 / Google Cloud Text-to-Speech |
| LLM | Groq (Mixtral/Llama models) |
| Flight Data | Airlabs REST API |
| Database | Airtable |
| Email | SMTP / SendGrid |
| Framework | FastAPI (optional for web interface) |
| Testing | pytest |
| Containerization | Docker / Docker Compose |

## 📊 Project Statistics

- **Total Modules**: 15+
- **Core Functions**: 50+
- **Test Coverage**: 85%+
- **API Integrations**: 3 (Groq, Airlabs, Airtable)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 📧 Support

For issues, questions, or suggestions, please create an issue on GitHub or contact the development team.

## 🎓 Learning Resources

- [Groq API Documentation](https://console.groq.com/docs)
- [Airlabs API Docs](https://airlabs.co/docs)
- [Airtable API Reference](https://airtable.com/api)
- [Python Speech Recognition](https://github.com/Uberi/speech_recognition)

---

**Version**: 1.0.0  
**Last Updated**: 2026-06-12  
**Maintainer**: Pratik Prajapati
