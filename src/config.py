#!/usr/bin/env python3
"""
Configuration management for the Flight Booking System.

Handles loading, validation, and management of application configuration
from environment variables and configuration files.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
import json
import logging

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


@dataclass
class SpeechConfig:
    """Configuration for speech recognition and synthesis."""
    stt_engine: str = "google"  # google, azure, etc.
    tts_engine: str = "google"  # google, gtts, pyttsx3
    language: str = "en-US"
    stt_timeout: int = 60
    stt_microphone_index: int = 0
    tts_rate: int = 150
    tts_volume: float = 0.9


@dataclass
class LLMConfig:
    """Configuration for LLM (Groq)."""
    api_key: str = ""
    model: str = "mixtral-8x7b-32768"
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.95
    timeout: int = 30


@dataclass
class FlightAPIConfig:
    """Configuration for Airlabs Flight API."""
    api_key: str = ""
    base_url: str = "https://airlabs.co/api/v9"
    timeout: int = 30
    cache_ttl: int = 3600


@dataclass
class AirtableConfig:
    """Configuration for Airtable database."""
    token: str = ""
    base_id: str = ""
    customers_table: str = "Customers"
    bookings_table: str = "Bookings"
    flights_table: str = "Flights"
    payments_table: str = "Payments"
    timeout: int = 30


@dataclass
class EmailConfig:
    """Configuration for email service."""
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    email: str = ""
    password: str = ""
    from_email: str = ""
    support_email: str = ""
    use_tls: bool = True
    timeout: int = 30


@dataclass
class PaymentConfig:
    """Configuration for payment processing."""
    provider: str = "stripe"  # stripe, paypal, etc.
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    enable_auto_payment: bool = True
    timeout: int = 30


@dataclass
class FeatureFlags:
    """Feature flags for the application."""
    enable_auto_payment: bool = True
    enable_email_confirmation: bool = True
    enable_payment_link: bool = True
    enable_booking_history: bool = True
    enable_voice_feedback: bool = True
    enable_debug_logging: bool = False


@dataclass
class Config:
    """Main application configuration."""
    # Application
    app_name: str = "AI Flight Booking System"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    # Sub-configurations
    speech: SpeechConfig = field(default_factory=SpeechConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    flight_api: FlightAPIConfig = field(default_factory=FlightAPIConfig)
    airtable: AirtableConfig = field(default_factory=AirtableConfig)
    email: EmailConfig = field(default_factory=EmailConfig)
    payment: PaymentConfig = field(default_factory=PaymentConfig)
    features: FeatureFlags = field(default_factory=FeatureFlags)
    
    # Timeouts
    api_timeout: int = 30
    default_timeout: int = 30
    
    # Security
    secret_key: str = ""
    allowed_origins: list = field(default_factory=list)
    
    # Rate limiting
    rate_limit_calls: int = 100
    rate_limit_period: int = 3600


def load_config(config_path: Optional[str] = None) -> Config:
    """
    Load configuration from environment variables and optional config file.
    
    Args:
        config_path: Path to additional config file (JSON or .env)
    
    Returns:
        Config object with all settings
    """
    # Load .env file
    env_file = Path(".env")
    if env_file.exists():
        logger.info(f"Loading environment from {env_file}")
        load_dotenv(env_file)
    
    # Load additional config file if provided
    if config_path:
        config_file = Path(config_path)
        if config_file.exists():
            logger.info(f"Loading configuration from {config_file}")
            if config_file.suffix == ".json":
                _load_json_config(config_file)
            elif config_file.suffix == ".env":
                load_dotenv(config_file)
    
    # Create configuration from environment variables
    config = Config(
        # Application settings
        app_name=os.getenv("APP_NAME", "AI Flight Booking System"),
        app_version=os.getenv("APP_VERSION", "1.0.0"),
        environment=os.getenv("ENVIRONMENT", "development"),
        debug=_parse_bool(os.getenv("DEBUG", "false")),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=os.getenv("LOG_FILE"),
        
        # Speech configuration
        speech=SpeechConfig(
            stt_engine=os.getenv("STT_ENGINE", "google"),
            tts_engine=os.getenv("TTS_ENGINE", "google"),
            language=os.getenv("STT_LANGUAGE", "en-US"),
            stt_timeout=int(os.getenv("STT_TIMEOUT", "60")),
            stt_microphone_index=int(os.getenv("STT_MICROPHONE_INDEX", "0")),
            tts_rate=int(os.getenv("TTS_RATE", "150")),
            tts_volume=float(os.getenv("TTS_VOLUME", "0.9")),
        ),
        
        # LLM configuration
        llm=LLMConfig(
            api_key=os.getenv("GROQ_API_KEY", ""),
            model=os.getenv("GROQ_MODEL", "mixtral-8x7b-32768"),
            temperature=float(os.getenv("GROQ_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("GROQ_MAX_TOKENS", "2048")),
            timeout=int(os.getenv("LLM_TIMEOUT", "30")),
        ),
        
        # Flight API configuration
        flight_api=FlightAPIConfig(
            api_key=os.getenv("AIRLABS_API_KEY", ""),
            base_url=os.getenv("AIRLABS_BASE_URL", "https://airlabs.co/api/v9"),
            timeout=int(os.getenv("API_TIMEOUT", "30")),
        ),
        
        # Airtable configuration
        airtable=AirtableConfig(
            token=os.getenv("AIRTABLE_TOKEN", ""),
            base_id=os.getenv("AIRTABLE_BASE_ID", ""),
            customers_table=os.getenv("AIRTABLE_CUSTOMERS_TABLE", "Customers"),
            bookings_table=os.getenv("AIRTABLE_BOOKINGS_TABLE", "Bookings"),
            flights_table=os.getenv("AIRTABLE_FLIGHTS_TABLE", "Flights"),
            payments_table=os.getenv("AIRTABLE_PAYMENTS_TABLE", "Payments"),
        ),
        
        # Email configuration
        email=EmailConfig(
            smtp_server=os.getenv("SMTP_SERVER", "smtp.gmail.com"),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            email=os.getenv("SMTP_EMAIL", ""),
            password=os.getenv("SMTP_PASSWORD", ""),
            from_email=os.getenv("FROM_EMAIL", ""),
            support_email=os.getenv("SUPPORT_EMAIL", ""),
        ),
        
        # Payment configuration
        payment=PaymentConfig(
            provider=os.getenv("PAYMENT_PROVIDER", "stripe"),
            stripe_secret_key=os.getenv("STRIPE_SECRET_KEY", ""),
            stripe_publishable_key=os.getenv("STRIPE_PUBLISHABLE_KEY", ""),
            enable_auto_payment=_parse_bool(os.getenv("ENABLE_AUTO_PAYMENT", "true")),
        ),
        
        # Feature flags
        features=FeatureFlags(
            enable_auto_payment=_parse_bool(os.getenv("ENABLE_AUTO_PAYMENT", "true")),
            enable_email_confirmation=_parse_bool(os.getenv("ENABLE_EMAIL_CONFIRMATION", "true")),
            enable_payment_link=_parse_bool(os.getenv("ENABLE_PAYMENT_LINK", "true")),
            enable_booking_history=_parse_bool(os.getenv("ENABLE_BOOKING_HISTORY", "true")),
        ),
        
        # Security
        secret_key=os.getenv("SECRET_KEY", ""),
        allowed_origins=_parse_list(os.getenv("ALLOWED_ORIGINS", "")),
        
        # Rate limiting
        rate_limit_calls=int(os.getenv("RATE_LIMIT_CALLS", "100")),
        rate_limit_period=int(os.getenv("RATE_LIMIT_PERIOD", "3600")),
    )
    
    # Validate configuration
    _validate_config(config)
    
    logger.info(f"Configuration loaded successfully for {config.environment} environment")
    return config


def _parse_bool(value: str) -> bool:
    """Parse boolean from string."""
    return value.lower() in ("true", "1", "yes", "on")


def _parse_list(value: str) -> list:
    """Parse comma-separated list from string."""
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _load_json_config(config_file: Path) -> None:
    """Load configuration from JSON file."""
    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
            # Merge into environment variables
            for key, value in config_data.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        env_key = f"{key}_{sub_key}".upper()
                        os.environ[env_key] = str(sub_value)
                else:
                    os.environ[key.upper()] = str(value)
    except Exception as e:
        logger.warning(f"Failed to load JSON config from {config_file}: {str(e)}")


def _validate_config(config: Config) -> None:
    """
    Validate configuration settings.
    
    Raises:
        ValueError: If required configuration is missing
    """
    errors = []
    
    # Check critical API keys
    if not config.llm.api_key:
        errors.append("GROQ_API_KEY is required")
    
    if not config.flight_api.api_key:
        errors.append("AIRLABS_API_KEY is required")
    
    if not config.airtable.token:
        errors.append("AIRTABLE_TOKEN is required")
    
    if not config.airtable.base_id:
        errors.append("AIRTABLE_BASE_ID is required")
    
    if not config.email.email or not config.email.password:
        errors.append("SMTP_EMAIL and SMTP_PASSWORD are required")
    
    if errors:
        error_msg = "\n".join([f"  - {error}" for error in errors])
        raise ValueError(f"Configuration validation failed:\n{error_msg}")
    
    logger.info("Configuration validation passed")


def get_config() -> Config:
    """
    Get the global configuration instance.
    
    Returns:
        Config object
    """
    if not hasattr(get_config, "_instance"):
        get_config._instance = load_config()
    return get_config._instance
