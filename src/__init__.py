"""
AI-Driven Flight Booking System

A comprehensive flight booking system powered by AI, featuring:
- Voice-based conversation interface
- Natural language understanding via Groq LLM
- Real-time flight search via Airlabs API
- Secure booking and payment processing
- Automated email confirmations
- Airtable integration for data management
"""

__version__ = "1.0.0"
__author__ = "Pratik Prajapati"
__license__ = "MIT"

from src.main import FlightBookingSystem
from src.config import load_config, Config

__all__ = [
    "FlightBookingSystem",
    "load_config",
    "Config",
]
