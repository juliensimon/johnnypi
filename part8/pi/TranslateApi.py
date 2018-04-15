#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3

defaultRegion = 'eu-west-1'
defaultUrl = 'https://translate.'+defaultRegion+'.amazonaws.com'
defaultBucket = "jsimon-public"

def connectToTranslate(regionName=defaultRegion, endpointUrl=defaultUrl):
    return boto3.client('translate', region_name=regionName, endpoint_url=endpointUrl)

def translateText(translate, text, source, target):
        response = translate.translate_text(Text=text, SourceLanguageCode=source, TargetLanguageCode=target)
        return response['TranslatedText']
