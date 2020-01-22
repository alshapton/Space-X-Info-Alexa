# -*- coding: utf-8 -*-

# Version 0.0.1 - ALS - 12/01/2020      Initial release - distance only
#         0.0.2 - ALS - 21/01/2020      Added distance from Mars, Speed and orbit information
#                                       Commenced adding detailled, more granular help function
#                                       Split up code to make it tidier and more modular
#                                       Renamed from "Roadster in Space" to "Space/X Information"



import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

# Import core intent handling classes
from CoreIntentHandlers.LaunchRequestHandler import LaunchRequestHandler
from CoreIntentHandlers.CancelOrStopIntentHandler import CancelOrStopIntentHandler
from CoreIntentHandlers.CatchAllExceptionHandler import CatchAllExceptionHandler
from CoreIntentHandlers.IntentReflectorHandler import IntentReflectorHandler

# Granular Help Handler
from CoreIntentHandlers.AssistanceIntentHandler import AssistanceIntentHandler


# Import functional intent handling classes
from FunctionalIntentHandlers.Roadster.Handlers import \
RoadsterOrbitIntentHandler,SpeedIntentHandler,         \
RoadsterLocationIntentHandler,MarsIntentHandler


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from roadster import roadster




class ChangeUnitsIntentHandler(AbstractRequestHandler):
    """Handler for Change units Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ChangeUnitsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        units = slots['units'].value
        speak_output = "Your units are now," + str(units)
        handler_input.attributes_manager.session_attributes["Units"] = str(units)
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can find out about Elon Musks roadster, Space ex launches, and other things you can do by saying,, help me with,, and a specific area, such as roadster, launches or units"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for the skill, routing all request and response
# payloads to the handlers above. 

sb = SkillBuilder()

# Skill startup Handler
sb.add_request_handler(LaunchRequestHandler())

# Roadster Handlers
sb.add_request_handler(MarsIntentHandler())
sb.add_request_handler(AssistanceIntentHandler())
sb.add_request_handler(RoadsterOrbitIntentHandler())
sb.add_request_handler(RoadsterLocationIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(SpeedIntentHandler())

# Shared Component Handlers
sb.add_request_handler(ChangeUnitsIntentHandler())

# Core Handlers
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # This MUST be last so it doesn't override the custom intent handlers

# Exception Handler to deal with mop up
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()




# End of Lambda Function