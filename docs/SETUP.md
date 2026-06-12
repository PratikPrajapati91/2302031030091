# Setup Guide - AI Flight Booking System

## Prerequisites

- Python 3.9 or higher
- pip package manager
- Git
- API keys for:
  - Groq (for LLM)
  - Airlabs (for flight data)
  - Airtable (for database)
  - Email service (SMTP)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/PratikPrajapati91/AI-Flight-Booking-System.git
cd AI-Flight-Booking-System
```

### 2. Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy example configuration
cp .env.example .env

# Edit .env file with your credentials
vi .env  # or use your preferred editor
```

### 5. Obtain API Keys

#### Groq API Key
1. Go to https://console.groq.com/
2. Sign up for an account
3. Create API key in the dashboard
4. Copy to `.env` as `GROQ_API_KEY`

#### Airlabs API Key
1. Go to https://airlabs.co/
2. Register for API access
3. Get your API key from the dashboard
4. Copy to `.env` as `AIRLABS_API_KEY`

#### Airtable
1. Go to https://airtable.com/
2. Sign up for account
3. Create a workspace and base
4. Generate personal access token in account settings
5. Note the Base ID from your workspace URL
6. Copy to `.env`:
   - `AIRTABLE_TOKEN`
   - `AIRTABLE_BASE_ID`

#### Email Configuration
1. Use Gmail or SMTP provider
2. For Gmail:
   - Enable 2-Factor Authentication
   - Generate App Password
   - Copy to `.env`:
     - `SMTP_EMAIL`: your@gmail.com
     - `SMTP_PASSWORD`: your_app_password

### 6. Verify Installation

```bash
# Run health check
python -c "from src.main import FlightBookingSystem; app = FlightBookingSystem(); print(app.health_check())"
```

## Running the Application

### Direct Execution

```bash
python src/main.py
```

### Using Docker

```bash
# Build image
docker build -t flight-booking-system .

# Run container
docker run -it --env-file .env flight-booking-system

# Or use Docker Compose
docker-compose up --build
```

## Configuration Details

### Speech Recognition

- **Engine Options**: `google`, `azure`, `witai`
- **Language**: Use language codes (e.g., `en-US`, `es-ES`)
- **Timeout**: Maximum listening duration in seconds

### LLM (Groq) Configuration

- **Model Options**:
  - `mixtral-8x7b-32768` (Recommended)
  - `llama2-70b-4096`
  - `llama2-13b-chat`

- **Temperature**: 0.0 (deterministic) to 2.0 (creative)
  - Recommended: 0.7 for balanced responses

- **Max Tokens**: Maximum response length
  - Recommended: 2048 for detailed responses

### Flight API

- **Base URL**: https://airlabs.co/api/v9
- **Rate Limits**: Check Airlabs documentation
- **Cache TTL**: Time-to-live for cached flight data in seconds

### Airtable Schema

Create these tables in your Airtable base:

#### Customers Table
```
Fields:
- Name (Text)
- Email (Email)
- Phone (Phone Number)
- Date of Birth (Date)
- Passport Number (Text)
- Address (Text)
- Created At (Created time)
```

#### Bookings Table
```
Fields:
- Booking ID (Autonumber)
- Customer (Link to Customers)
- Flight Number (Text)
- Departure (Date)
- Arrival (Date)
- Seats (Number)
- Total Price (Currency)
- Status (Select: pending, confirmed, cancelled)
- Created At (Created time)
```

#### Flights Table
```
Fields:
- Flight Number (Text)
- Airline (Text)
- Departure Airport (Text)
- Arrival Airport (Text)
- Departure Time (DateTime)
- Arrival Time (DateTime)
- Duration (Number)
- Price (Currency)
- Available Seats (Number)
- Aircraft Type (Text)
```

#### Payments Table
```
Fields:
- Payment ID (Autonumber)
- Booking (Link to Bookings)
- Amount (Currency)
- Method (Select: card, link, manual)
- Status (Select: pending, completed, failed)
- Transaction ID (Text)
- Created At (Created time)
```

## Troubleshooting

### Common Issues

#### ImportError: No module named 'groq'
```bash
pip install --upgrade groq
```

#### API Key Errors
- Verify keys are correctly set in `.env`
- Check that keys are active in respective dashboards
- Ensure no extra spaces in `.env`

#### Speech Recognition Issues
- Check microphone input: `python -c "import pyaudio; import sounddevice"`
- Install system audio libraries:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install portaudio19-dev
  
  # macOS
  brew install portaudio
  ```

#### Airtable Connection Issues
- Verify token has proper permissions
- Check base ID from URL
- Ensure table names match configuration

### Debug Mode

Enable detailed logging:

```bash
# Set in .env
DEBUG=true
LOG_LEVEL=DEBUG
```

Or via environment variable:
```bash
export DEBUG=true
python src/main.py
```

## Testing

Run unit tests:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

Run specific test:

```bash
pytest tests/test_booking.py -v
```

## Performance Optimization

### Enable Caching
```python
# In config.py
FLIGHT_API_CACHE_TTL = 3600  # 1 hour
```

### Async Processing
```bash
# Use async version
python -c "from src.main import FlightBookingSystem; import asyncio; app = FlightBookingSystem(); asyncio.run(app.start_booking_session_async())"
```

### Rate Limiting
Set in `.env`:
```
RATE_LIMIT_CALLS=100
RATE_LIMIT_PERIOD=3600
```

## Security Considerations

1. **Never commit `.env` file** - Already in `.gitignore`
2. **Rotate API keys** regularly
3. **Use HTTPS** for all external APIs
4. **Enable 2FA** on all service accounts
5. **Encrypt sensitive data** in database
6. **Validate all user inputs** before processing
7. **Use environment-specific credentials**

## Production Deployment

### Using Docker

```bash
# Build production image
docker build -t flight-booking-system:latest .

# Push to registry
docker tag flight-booking-system:latest myregistry/flight-booking:latest
docker push myregistry/flight-booking:latest
```

### Using systemd

Create `/etc/systemd/system/flight-booking.service`:

```ini
[Unit]
Description=Flight Booking System
After=network.target

[Service]
Type=simple
User=flightbooking
WorkingDirectory=/opt/flight-booking
ExecStart=/opt/flight-booking/venv/bin/python src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl start flight-booking
sudo systemctl enable flight-booking
```

## Monitoring

### Log Analysis
```bash
# Follow logs
tail -f logs/app.log

# Search logs
grep "ERROR" logs/app.log
```

### Health Checks
```bash
python -c "from src.main import FlightBookingSystem; app = FlightBookingSystem(); import json; print(json.dumps(app.health_check(), indent=2))"
```

## Support

For issues and questions:
1. Check documentation in `docs/`
2. Review logs in `logs/` directory
3. Create GitHub issue with error details
4. Contact support team
