# -*- coding: utf-8 -*-
"""Simple fact sample app."""

import random
import logging
import requests
import datetime
import requests
import json
import html

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response


# =========================================================================================================================================
# TODO: The items below this comment need your attention.
# =========================================================================================================================================
SKILL_NAME = "Trending topics"
GET_FACT_MESSAGE = "Here's your trending topic: "
HELP_MESSAGE = "You can say tell me tell me about trendng topics, or, you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye! Thank you for listening to trending topics by Learn in 60 seconds"
FALLBACK_MESSAGE = "The Trending Topics skill can't help you with that.  It can help you discover trending topics if you say tell me about trending topics. What can I help you with?"
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."


sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Built-in Intent Handlers
class GetNewFactHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewFact Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("GetNewFactIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNewFactHandler")

        url="https://script.google.com/macros/s/AKfycbzJr6kWPBZF5Kpi7cOkCAvrdJd6BWYCZTRCP5uACff2_nCor_FY/exec"
        trending_data=requests.get(url)
        trend_list = json.loads(trending_data.text)

        response="The trending topics are "
        for item in trend_list:
            response=response+str(item[0])+"<break time='1s'/>"+", "

        display = str(trend_list[0][0])+", "+str(trend_list[1][0])+", "+str(trend_list[2][0])+", "+str(trend_list[3][0])+", "+str(trend_list[4][0])
        attr = handler_input.attributes_manager.session_attributes
        #session_attributes['speech'] = response
        handler_input.response_builder.speak(response).set_card(
            SimpleCard(SKILL_NAME, display))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response

# Interceptor classes
class CacheResponseForRepeatInterceptor(AbstractResponseInterceptor):
    """Cache the response sent to the user in session.
    The interceptor is used to cache the handler response that is
    being sent to the user. This can be used to repeat the response
    back to the user, in case a RepeatIntent is being used and the
    skill developer wants to repeat the same information back to
    the user.
    """
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["recent_response"] = response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        logger.info("in CatchAllExceptionHandler")
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


class RepeatIntentHandler(AbstractRequestHandler):
    """Handler for Repeat Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In RepeatIntentHandler")
        attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        if "recent_response" in attr:
            cached_response_str = json.dumps(attr["recent_response"])
            cached_response = DefaultSerializer().deserialize(
                cached_response_str, Response)
            return cached_response
        else:
            response_builder.speak(FALLBACK_MESSAGE).ask(HELP_MESSAGE)

            return response_builder.response




# Register intent handlers
sb.add_request_handler(GetNewFactHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(RepeatIntentHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# TODO: Uncomment the following lines of code for request, response logs.
sb.add_global_response_interceptor(CacheResponseForRepeatInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
