import time
from gopigo import *
import iot_connect
from iot_topics import *
import camera, awsUtils, tweet
import PollyApi, RekognitionApi, RekognitionUtils, TranslateApi, ComprehendApi
import inception

def callbackSee(client, userdata, message):
	print "Topic="+message.topic
	print "Message="+message.payload
	image = camera.takePicture()
	if message.payload.startswith("mxnet"):
		# Detect image with MXNet
		mxnetimage = inception.load_image(image)
    		prob = inception.predict(mxnetimage, model)
    	        topN = inception.get_top_categories(prob, synsets)
		print topN
		speech = inception.get_top1_message(topN)
		print speech
		PollyApi.speak(polly, speech)
		if message.payload.endswith("tweet"):
			tweet.tweet(image, speech)
			print "Tweet sent"
	elif message.payload.startswith("reko"):
		# Detect image with Rekognition
		awsUtils.copyLocalFileToS3(image)
		print "Picture uploaded"
		labels = RekognitionApi.detectLabels(reko, image)
		RekognitionUtils.printLabelsInformation(labels)
		faces = RekognitionApi.detectFaces(reko, image)
		celebs = RekognitionApi.detectCelebrities(reko, image)
		newImage, faceCounter = RekognitionUtils.generateOutputImage(image, faces)
		faceMessage, labelMessage = RekognitionUtils.generateMessages(faceCounter, celebs, labels)
		print "Face message: " + faceMessage
		#print "Label message: " + labelMessage
		PollyApi.speak(polly, faceMessage)
		#PollyApi.speak(polly, labelMessage)
		if message.payload.endswith("tweet"):
			tweet.tweet(newImage, faceMessage)
			print "Tweet sent"
	else:
                print "Wrong Command, Please Enter Again"

language_info  = {
    'English'    : {'code': 'en', 'voice': 'Brian'},
    'French'     : {'code': 'fr', 'voice': 'Mathieu'},
    'German'     : {'code': 'de', 'voice': 'Hans'},
    'Spanish'    : {'code': 'es', 'voice': 'Enrique'},
    'Portuguese' : {'code': 'pt', 'voice': 'Cristiano'}
}

language_name = {'en':'English', 'fr':'French', 'de':'German', 'es':'Spanish'}

def callbackRead(client, userdata, message):
	print "Topic="+message.topic
	print "Message="+message.payload
	image = camera.takePicture()
	awsUtils.copyLocalFileToS3(image)
	print "Picture uploaded"
        text = RekognitionApi.detectText(reko, image)
	print text

	if message.payload.startswith("read"):
	       PollyApi.speak(polly, text)
	elif message.payload.startswith("translate"):
               src_language_code = ComprehendApi.detectLanguage(comprehend, text)
               dest_language = message.payload.split(' ')[1]
               dest_language_code = language_info[dest_language]['code']
               voice = language_info[dest_language]['voice']
               print src_language_code, dest_language_code, voice
               if src_language_code == 'en' or dest_language_code == 'en':
                   text = TranslateApi.translateText(translate, text, src_language_code, dest_language_code)
               else:
                   text = TranslateApi.translateText(translate, text, src_language_code, 'en')
                   text = TranslateApi.translateText(translate, text, 'en', dest_language_code)
	       print text
	       PollyApi.speak(polly, text, voice=voice)
	elif message.payload.startswith("language"):
               language_code = ComprehendApi.detectLanguage(comprehend, text)
               language = language_name[language_code]
               print language_code, language
               text = "I believe this is " + language
               PollyApi.speak(polly, text)
	else:
               print "Wrong Command, Please Enter Again"
	       return

	if message.payload.endswith("tweet"):
		tweet.tweet(image, text)
		print "Tweet sent"

def callbackSpeak(client, userdata, message):
	print "Topic="+message.topic
	print "Message="+message.payload
	if not message.payload:
		msg = "Nothing to say, sorry"
	else:
		msg = message.payload
	PollyApi.speak(polly, msg)

def callbackMove(client, userdata, message):
	print "Topic="+message.topic
	print "Message="+message.payload
	cmd = message.payload
	if cmd=="forward":
		fwd()	# Move forward
	elif cmd=="left":
		left()	# Turn left
	elif cmd=="right":
		right()	# Turn Right
	elif cmd=="backward":
		bwd()	# Move back
	elif cmd=="stop":
		stop()	# Stop
	elif cmd=="faster":
		increase_speed()
	elif cmd=="slower":
		decrease_speed()
	else:
		print "Wrong Command, Please Enter Again"
	time.sleep(1)
	stop()

def callbackScan(client, userdata, message):
	print "Topic="+message.topic
	print "Message="+message.payload
	cmd = message.payload
	if cmd=="scan":
                dist=(str)(us_dist(15))
                message = "There is something "+dist+" centimeters away"
                PollyApi.speak(polly, message)
        elif cmd=="left":
		angle = angle + 30
		if (angle > 180):
			angle = 180
                servo(angle)
        elif cmd=="right":
		angle = angle - 30
		if (angle < 0):
			angle = 0
                servo(angle)
        elif cmd=="reset":
                servo(90)
        else:
                print "Wrong Command, Please Enter Again"

global angle, polly, reko, model, synsets

# Reset servo to center position
enable_servo()
angle = 90
servo(angle)

# Connect to IoT Gateway and subscribe to topics
client = iot_connect.connectIot()
client.subscribe(topicMove, 1, callbackMove)
client.subscribe(topicScan, 1, callbackScan)
client.subscribe(topicSpeak, 1, callbackSpeak)
client.subscribe(topicSee, 1, callbackSee)
client.subscribe(topicRead, 1, callbackRead)

polly = PollyApi.connectToPolly()
reko = RekognitionApi.connectToRekognition()
translate = TranslateApi.connectToTranslate()
comprehend = ComprehendApi.connectToComprehend()
model, synsets = inception.load_inception_model()

while True:
	time.sleep(10)

client.unsubscribe(topicMove)
client.unsubscribe(topicScan)
client.unsubscribe(topicSpeak)
client.unsubscribe(topicSee)
client.unsubscribe(topicRead)
iot_connect.disconnectIot(client)
disable_servo()

