# -*- coding: utf-8 -*-
"""Simple fact sample app."""

import random
import logging
import requests
import datetime

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
SKILL_NAME = "COVID Facts"
GET_FACT_MESSAGE = "Here's your fact: "
HELP_MESSAGE = "You can say tell me a COVID fact, or, you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "The COVID Facts skill can't help you with that.  It can help you discover facts about COVID if you say tell me a COVID fact. What can I help you with?"
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

        #speech = GET_FACT_MESSAGE + random_fact
        #URL = "https://script.google.com/macros/s/AKfycbzdDlPW9-iZodsf45dEOTN2tlXqszE5atPDfuiIJCzdttjl_0f7/exec"
        #URL="https://jsonplaceholder.typicode.com/todos/1"
        URL = "https://api.covidtracking.com/v1/us/current.json"
        #r = requests.get(url = URL).json()["title"]
        # [{"date":20210122,"states":56,"positive":24483676,"negative":221900013,"pending":11247,"hospitalizedCurrently":116264,"hospitalizedCumulative":776384,"inIcuCurrently":22008,"inIcuCumulative":40687,"onVentilatorCurrently":7236,"onVentilatorCumulative":3919,"dateChecked":"2021-01-22T24:00:00Z","death":404695,"hospitalized":776384,"totalTestResults":291407518,"lastModified":"2021-01-22T24:00:00Z","recovered":null,"total":0,"posNeg":0,"deathIncrease":3980,"hospitalizedIncrease":4325,"negativeIncrease":1375093,"positiveIncrease":188983,"totalTestResultsIncrease":1988756,"hash":"97b028907bd40a1d4e37da0b967c2efc13befe38"}]


        covid_data = requests.get(url = URL).json()[0]
        keys = ['date', 'states', 'positive', 'negative', 'pending', 'hospitalizedCurrently', 'hospitalizedCumulative', 'inIcuCurrently', 'inIcuCumulative', 'onVentilatorCurrently', 'onVentilatorCumulative', 'dateChecked', 'death', 'hospitalized', 'totalTestResults', 'lastModified', 'recovered', 'total', 'posNeg','deathIncrease', 'hospitalizedIncrease', 'negativeIncrease', 'positiveIncrease', 'totalTestResultsIncrease', 'hash']

        months={ 1 : "January",2 : "February",3 : "March",4 : "April",5 : "May",6 : "June",7 : "July",8 : "August",9 : "September",10 : "October",11 : "November",12 : "December"}

        date = "As of " +months[(int(str(covid_data["date"])[4:6]))] +" "+str(covid_data["date"])[6:8] +", "+str(covid_data["date"])[0:4]+","
        #+" "+str(date[6:8])+" "+str(date[0:4])

        text =  date+" we have "+str(covid_data["positive"])+" positive COVID-19 cases. The total number of unique people with a completed PCR test that returns negative is "+str(covid_data["negative"])+". There are "+str(covid_data["hospitalizedCurrently"])+" individuals hospitalized currently, bringing the cumulative total of those hospitalized to "+str(covid_data["hospitalizedCumulative"]) +". There are "+str(covid_data["inIcuCurrently"]) +" individuals who are currently hospitalized in the Intensive Care Unit with COVID-19. There are "+str(covid_data["onVentilatorCurrently"])+" people on ventilator currently while the cumulative total of those on ventilator is "+str(covid_data["onVentilatorCumulative"])+". This cumulative total refers to individuals who have ever been hospitalized under advanced ventilation with COVID-19. There have been "+str(covid_data["death"])+" deaths, "+str(covid_data["hospitalized"])+" hospitalized, and "+str(covid_data["totalTestResults"])+" total test results. "+" The increase in deaths is "+str(covid_data["deathIncrease"])+" and the increase in those hospitalized is  "+str(covid_data["hospitalizedIncrease"])+". The negative increase is "+str(covid_data["negativeIncrease"])+". The positive increase is "+str(covid_data["positiveIncrease"])+". The daily increase in total test results, calculated from the previous day’s value is "+str(covid_data["totalTestResultsIncrease"])+"."
        #Total number of people that are identified as recovered from COVID-19.


        #speech = json.dumps(covid_data)
        #fact = result['results'][0][0]
        summary = date+ "the US has "+str(covid_data["positive"])+" positive COVID-19 cases"
        handler_input.response_builder.speak(text).set_card(
            SimpleCard(SKILL_NAME, summary))
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


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
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


# Register intent handlers
sb.add_request_handler(GetNewFactHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# TODO: Uncomment the following lines of code for request, response logs.
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
