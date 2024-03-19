#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tralslation tool between Japanese and English


import boto3
import json
import sys
import os
from dotenv import load_dotenv
import click 


# Definition of command line arguments
@click.command()
@click.option('--debug','-D',is_flag=True, help='Debug mode')

def generate(debug):

    """This tool translates """
    # get API key from .env file
    load_dotenv()
    access_key = os.environ["AWS_ACCESS_KEY"]
    secret_key = os.environ["AWS_SECRET_KEY"]

    source = input("Enter the text you wish to translate: ")

    bedrock = boto3.client('bedrock-runtime', 
                        aws_access_key_id = access_key,
                        aws_secret_access_key = secret_key,
                        region_name = "us-west-2")


    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": 
                        "Please translate the following sentences. If the sentence is in Japanese, translate it into English; if the sentence is in English, translate it into Japanese. Please provide only the translated text in your response."
                },
                {
                    "role": "assistant",
                    "content": 
                        "Now, please enter the text to be translated."
                },
                {
                    "role": "user",
                    "content": source
                },
            ]
        }
    )
    modelId = 'anthropic.claude-3-sonnet-20240229-v1:0'
    accept = 'application/json'
    contentType = 'application/json'
    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    answer = response_body["content"][0]["text"]
    print(answer)


if __name__ == '__main__':
    generate()
