
from __future__ import print_function
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from iot_config import *

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def connectIot():
	myMQTTClient = AWSIoTMQTTClient(CLIENT_ID)
	myMQTTClient.configureEndpoint(IOT_ENDPOINT, IOT_PORT)
	myMQTTClient.configureCredentials(ROOT_CA, PRIVATE_KEY, CERTIFICATE)
	result = myMQTTClient.connect()
	if result:
		print("Connected to IoT")
	else:
		print("Cannot connect to IoT")
	return myMQTTClient

def disconnectIot(myMQTTClient):
	myMQTTClient.disconnect()
	print("Disconnect from IoT")

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Johnny Pi is at your command, " \
                    "what would you like him to do?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me what to do, " \
                    "for example: go forward."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for interacting with Johnny Pi. Good bye."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def handle_direction(intent, session):
    """ Gets the direction from the slot and send it to the robot
    """
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    reprompt_text = "I'm afraid I can't do that. Please try again."

    if 'Direction' in intent['slots']:
        direction = intent['slots']['Direction']['value']
       	print("Received direction: " + direction)
	if direction in ['left','right','forward','backward','hold','faster', 'slower']:
		if direction == "hold":
			direction = "stop"
    		iotclient = connectIot()
    		result = iotclient.publish("JohnnyPi/move", direction, 1)
		disconnectIot(iotclient)
		if not result:
			print("Publish error")
        		speech_output = "I couldn't send the command, sorry."
		else:
			print("Publish OK")
        		speech_output = "OK."
	else:
        	speech_output = reprompt_text
    else:
        speech_output = reprompt_text

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_see(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    reprompt_text = "I can look at faces and objects. Please try again"

    if 'Target' in intent['slots']:
        target = intent['slots']['Target']['value']
        print("Looking at: " + target)
        if target in ['faces', 'people', 'humans', 'object']:
            iotclient = connectIot()
            if target in ['faces', 'people', 'humans']:
                message = 'reko tweet'
            elif target == 'object':
                message = 'mxnet tweet'
            result = iotclient.publish("JohnnyPi/see", message, 1)
            if not result:
                print("Publish error")
                speech_output = "I couldn't send the command, sorry."
            else:
                print("Publish OK")
                speech_output = "OK."
            disconnectIot(iotclient)
        else:
                speech_output = reprompt_text
    else:
        speech_output = reprompt_text

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_scan(intent, session):
	return

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "DirectionIntent":
        return handle_direction(intent, session)
    elif intent_name == "ScanIntent":
        return handle_scan(intent, session)
    elif intent_name == "SeeIntent":
        return handle_see(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    #if (event['session']['application']['applicationId'] !=
      #  "amzn1.ask.skill.122b82f1-7609-45e5-96dd-8fbe38650dbb"):
      #  raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
