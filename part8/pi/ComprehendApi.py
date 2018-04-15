#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3

defaultRegion = 'eu-west-1'
defaultUrl = 'https://comprehend.'+defaultRegion+'.amazonaws.com'
defaultBucket = "jsimon-public"

languages = {'en':'English', 'fr':'French', 'de':'German', 'es':'Spanish'}

def connectToComprehend(regionName=defaultRegion, endpointUrl=defaultUrl):
    return boto3.client('comprehend', region_name=regionName, endpoint_url=endpointUrl)

def detectLanguage(client,text):
        resp = client.detect_dominant_language(Text=text)
        language_code = resp['Languages'][0]['LanguageCode']
	return language_code, languages[language_code]

