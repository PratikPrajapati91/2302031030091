#!/usr/bin/env python3
"""
AI-Driven Flight Booking System - Main Application Entry Point

This module orchestrates the entire flight booking workflow, integrating
speech recognition, LLM processing, flight search, and booking management.
"""

import asyncio
import logging
from typing import Optional
from pathlib import Path

from src.config import load_config, Config
from src.speech.stt import SpeechToTextEngine
from src.speech.tts import TextToSpeechEngine
from src.ai.llm_handler import LLMHandler
from src.ai.intent_extractor import IntentExtractor
from src.flight.airlabs_api import AirlabsFlightAPI
from src.flight.flight_matcher import FlightMatcher
from src.booking.booking_manager import BookingManager
from src.database.airtable_client import AirtableClient
from src.email.email_sender import EmailSender
from src.conversation.conversation_flow import ConversationFlow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FlightBookingSystem:
    """
    Main application class that orchestrates the AI flight booking workflow.
    
    Integrates all components:
    - Speech recognition and synthesis
    - LLM for natural language understanding
    - Flight search and matching
    - Booking and payment processing
    - Database and email operations
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the Flight Booking System.
        
        Args:
            config_path: Path to configuration file (uses .env if not specified)
        """
        logger.info("Initializing AI Flight Booking System...")
        
        # Load configuration
        self.config: Config = load_config(config_path)
        logger.info(f"Configuration loaded: {self.config.app_name} v{self.config.app_version}")
        
        # Initialize components
        self._initialize_components()
        
        logger.info("System initialization complete")
    
    def _initialize_components(self) -> None:
        """
        Initialize all system components.
        """
        try:
            # Speech components
            logger.info("Initializing speech recognition...")
            self.stt = SpeechToTextEngine(self.config)
            logger.info("✓ Speech-to-Text engine initialized")
            
            logger.info("Initializing text-to-speech...")
            self.tts = TextToSpeechEngine(self.config)
            logger.info("✓ Text-to-Speech engine initialized")
            
            # AI components
            logger.info("Initializing LLM handler...")
            self.llm = LLMHandler(self.config)
            logger.info("✓ LLM handler initialized")
            
            logger.info("Initializing intent extractor...")
            self.intent_extractor = IntentExtractor(self.llm)
            logger.info("✓ Intent extractor initialized")
            
            # Flight components
            logger.info("Initializing Airlabs API client...")
            self.flight_api = AirlabsFlightAPI(self.config)
            logger.info("✓ Airlabs API client initialized")
            
            logger.info("Initializing flight matcher...")
            self.flight_matcher = FlightMatcher()
            logger.info("✓ Flight matcher initialized")
            
            # Database components
            logger.info("Initializing Airtable client...")
            self.airtable = AirtableClient(self.config)
            logger.info("✓ Airtable client initialized")
            
            # Email components
            logger.info("Initializing email sender...")
            self.email_sender = EmailSender(self.config)
            logger.info("✓ Email sender initialized")
            
            # Booking components
            logger.info("Initializing booking manager...")
            self.booking_manager = BookingManager(
                self.airtable,
                self.email_sender,
                self.config
            )
            logger.info("✓ Booking manager initialized")
            
            # Conversation flow
            logger.info("Initializing conversation flow...")
            self.conversation_flow = ConversationFlow(
                stt=self.stt,
                tts=self.tts,
                llm=self.llm,
                intent_extractor=self.intent_extractor,
                flight_api=self.flight_api,
                flight_matcher=self.flight_matcher,
                booking_manager=self.booking_manager,
                config=self.config
            )
            logger.info("✓ Conversation flow initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize system components: {str(e)}")
            raise
    
    def start_booking_session(self) -> None:
        """
        Start an interactive flight booking session.
        """
        logger.info("=" * 60)
        logger.info("STARTING NEW FLIGHT BOOKING SESSION")
        logger.info("=" * 60)
        
        try:
            self.conversation_flow.start_conversation()
        except KeyboardInterrupt:
            logger.info("\nSession interrupted by user")
            self.tts.speak("Thank you for using our flight booking service. Goodbye!")
        except Exception as e:
            logger.error(f"Error during booking session: {str(e)}")
            self.tts.speak("An error occurred. Please try again later.")
            raise
    
    async def start_booking_session_async(self) -> None:
        """
        Start an interactive flight booking session (async version).
        """
        logger.info("=" * 60)
        logger.info("STARTING NEW FLIGHT BOOKING SESSION (ASYNC)")
        logger.info("=" * 60)
        
        try:
            await self.conversation_flow.start_conversation_async()
        except KeyboardInterrupt:
            logger.info("\nSession interrupted by user")
            self.tts.speak("Thank you for using our flight booking service. Goodbye!")
        except Exception as e:
            logger.error(f"Error during booking session: {str(e)}")
            self.tts.speak("An error occurred. Please try again later.")
            raise
    
    def health_check(self) -> dict:
        """
        Perform a health check of all system components.
        
        Returns:
            Dictionary with health status of each component
        """
        logger.info("Performing system health check...")
        
        health_status = {
            "status": "healthy",
            "components": {}
        }
        
        try:
            # Check speech components
            health_status["components"]["stt"] = self.stt.health_check()
            health_status["components"]["tts"] = self.tts.health_check()
            
            # Check AI components
            health_status["components"]["llm"] = self.llm.health_check()
            
            # Check API components
            health_status["components"]["flight_api"] = self.flight_api.health_check()
            
            # Check database
            health_status["components"]["airtable"] = self.airtable.health_check()
            
            # Check email
            health_status["components"]["email"] = self.email_sender.health_check()
            
            # Determine overall status
            if any(not comp.get("healthy", False) for comp in health_status["components"].values()):
                health_status["status"] = "degraded"
            
            logger.info(f"Health check complete: {health_status['status']}")
            return health_status
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def shutdown(self) -> None:
        """
        Gracefully shutdown the system.
        """
        logger.info("Shutting down Flight Booking System...")
        
        try:
            # Cleanup resources
            if hasattr(self, 'stt'):
                self.stt.cleanup()
            if hasattr(self, 'tts'):
                self.tts.cleanup()
            if hasattr(self, 'airtable'):
                self.airtable.cleanup()
            if hasattr(self, 'email_sender'):
                self.email_sender.cleanup()
            
            logger.info("System shutdown complete")
        except Exception as e:
            logger.error(f"Error during shutdown: {str(e)}")


def main():
    """
    Main entry point for the application.
    """
    try:
        # Initialize system
        app = FlightBookingSystem()
        
        # Check system health
        health = app.health_check()
        if health["status"] != "healthy":
            logger.warning(f"System health: {health['status']}")
            logger.warning(f"Component status: {health['components']}")
        
        # Start booking session
        app.start_booking_session()
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        return 1
    finally:
        if 'app' in locals():
            app.shutdown()
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
