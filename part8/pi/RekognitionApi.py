#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3

defaultRegion = 'eu-west-1'
defaultUrl = 'https://rekognition.'+defaultRegion+'.amazonaws.com'
defaultBucket = "jsimon-public"

def connectToRekognition(regionName=defaultRegion, endpointUrl=defaultUrl):
    return boto3.client('rekognition', region_name=regionName, endpoint_url=endpointUrl)

def detectFaces(rekognition, imageFilename, imageBucket=defaultBucket, attributes='ALL'):
    resp = rekognition.detect_faces(
            Image = {"S3Object" : {'Bucket' : imageBucket, 'Name' : imageFilename}},
            Attributes=[attributes])
    return resp['FaceDetails']

def detectLabels(rekognition, imageFilename, imageBucket=defaultBucket, maxLabels=10, minConfidence=80):
    resp = rekognition.detect_labels(
        Image = {"S3Object" : {'Bucket' : imageBucket, 'Name' : imageFilename}},
        MaxLabels = maxLabels, MinConfidence = minConfidence)
    return resp['Labels']

def detectText(rekognition, imageFilename, imageBucket=defaultBucket):
    response = rekognition.detect_text(Image={'S3Object': {'Bucket':imageBucket, 'Name':imageFilename}})
    text = ''
    for t in response['TextDetections']:
        if t['Type'] == 'LINE':
            text = text+t['DetectedText']+' '
    return text
