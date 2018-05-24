from PIL import Image, ImageDraw, ImageFont

def openLocalImage(imageFile):
    image = Image.open(imageFile)
    draw = ImageDraw.Draw(image);
    return [image,draw]

def saveImage(imageFile, imageInfo, prefix='reko_', format='PNG'):
    image = getImage(imageInfo)
    newImageFile = prefix+imageFile
    image.save(newImageFile, format)
    return newImageFile

def getImage(imageInfo):
    return imageInfo[0]     # PIL.Image object

def getDraw(imageInfo):
    return imageInfo[1]     # PIL.Draw object

def drawLinesAroundFace(imageInfo, face, color='orange', width=3):
    image = getImage(imageInfo)
    draw = getDraw(imageInfo)
    lines = computeFaceCoordinates(image, face)
    draw.line(lines, fill=color, width=width)

def printFaceInformation(face, faceCounter):
    print('*** Face ' + str(faceCounter) + ' detected, confidence: ')+str(face['Confidence'])
    print('Gender: ')+face['Gender']['Value']
    # You need boto3>=1.4.4 for AgeRange
    print('Age: ')+str(face['AgeRange']['Low'])+"-"+str(face['AgeRange']['High'])
    if (face['Beard']['Value']):
        print ('Beard')
    if (face['Mustache']['Value']):
        print ('Mustache')
    if (face['Eyeglasses']['Value']):
        print ('Eyeglasses')
    if (face['Sunglasses']['Value']):
        print ('Sunglasses')
    for e in face['Emotions']:
        print e['Type']+' '+str(e['Confidence'])

def printLabelsInformation(labels):
    for l in labels:
        print('Label ' + l['Name'] + ', confidence: ' + str(l['Confidence']))

def drawLegendForFace(imageInfo, face, counter=0,
        font='/usr/share/fonts/truetype/freefont/FreeSans.ttf', fontSize=24, fill=(255,255,255,255)):
    font = ImageFont.truetype(font, fontSize)
    image = getImage(imageInfo)
    draw = getDraw(imageInfo)
    faceCoordinates = computeFaceCoordinates(image, face)
    legendCoordinates = computeLegendCoordinates(faceCoordinates)
    legendText = buildLegendText(counter)
    draw.text(legendCoordinates, legendText, fill, font)

def computeFaceCoordinates(image, face):
    # Extract fractional values
    left   = face['BoundingBox']['Left']
    top    = face['BoundingBox']['Top']
    width  = face['BoundingBox']['Width']
    height = face['BoundingBox']['Height']
    # Convert fractional values to pixel values
    topLeftX        = (int)(image.width*left)
    topLeftY        = (int)(image.height*top)
    topRightX       = (int)(topLeftX + image.width*width)
    topRightY       = topLeftY
    bottomRightX    = topRightX
    bottomRightY    = (int)(topRightY + image.height*height)
    bottomLeftX     = topLeftX
    bottomLeftY     = bottomRightY
    return [topLeftX, topLeftY, topRightX, topRightY,
            bottomRightX, bottomRightY, bottomLeftX, bottomLeftY,
            topLeftX, topLeftY]

def computeLegendCoordinates(imageCoordinates):
    x = imageCoordinates[6]     # bottomLeftX
    y = imageCoordinates[7]+10  # bottomLeftY+10: write legend 10 pixels lower
    return (x,y)

def buildLegendText(counter, prefix='Face'):
    return prefix+str(counter)

# Instead of drawing lines, we could draw a rectangle
# around a face. However, draw.rectangle() doesn't
# have a 'width' option, which often makes rectangles very hard to see

def addRectangleAroundFace(imageInfo, face, fill=None, color='white'):
    rectangle = computeRectangleCoordinates(getImage(imageInfo), face)
    draw.rectangle(rectangle, fill, color)

def computeRectangleCoordinates(image, face):
    # Extract fractional values
    left   = face['BoundingBox']['Left']
    top    = face['BoundingBox']['Top']
    width  = face['BoundingBox']['Width']
    height = face['BoundingBox']['Height']
    # Convert fractional values to pixel values
    x0 = (int)(image.width*left)
    y0 = (int)(image.height*top)
    x1 = (int)(x0 + image.width*width)
    y1 = (int)(y0 + image.height*height)
    return [x0, y0, x1, y1]

def generateOutputImage(image, faceList):
	imageInfo   = openLocalImage(image)
	faceCounter = 0
	for face in faceList:
    		printFaceInformation(face, faceCounter)
    		drawLinesAroundFace(imageInfo, face)
    		drawLegendForFace(imageInfo, face, faceCounter)
    		faceCounter=faceCounter+1
	newImage = saveImage(image, imageInfo)
	return newImage, faceCounter

def generateMessages(faceCounter, celebs, labels):
	if (faceCounter == 0):
    		faceMessage = "No face has been detected, sorry."
	elif (faceCounter == 1):
		faceMessage = "A single face has been detected. "
    	else:
		faceMessage = str(faceCounter) + " faces have been detected. "

        if len(celebs) != 0:
                for c in celebs:
                   faceMessage = faceMessage + c['Name'] + ' ' 
	labelMessage = "Here are some keywords about this picture: "
	for l in labels:
    		if (l['Confidence'] > 80.0):
        		labelMessage = labelMessage + l['Name'] + ", "
	if labelMessage == "Here are some keywords about this picture: ":
    		labelMessage = "No reliable labels have been detected, sorry."
	return faceMessage, labelMessage
