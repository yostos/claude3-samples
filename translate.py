#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Translation tool between Japanese and English
# using Amazon Bedrock and Claude3

import boto3
import json
import os
from dotenv import load_dotenv
import click

@click.command()
def translate_text():
    """This tool translates text using Amazon Bedrock and Claude3."""
    # Load API key and secret key from .env file
    load_dotenv()
    access_key = os.environ["AWS_ACCESS_KEY"]
    secret_key = os.environ["AWS_SECRET_KEY"]

    # Prompt the user for text to translate
    source = input("Enter the text you wish to translate: ")

    # Define the prompt for the translation task
    prompt = (
        "Please translate the following sentences. If the sentence is in Japanese, "
            "translate it into English; if the sentence is in English, translate it into Japanese. "
            "Please provide only the translated text in your response.\n\n"
            f"{source}"
    )
    # Initialize the Bedrock client
    bedrock = boto3.client('bedrock-runtime',
                            aws_access_key_id=access_key,
                            aws_secret_access_key=secret_key,
                            region_name="us-west-2")

    # Define the body for the translation task
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": "You are a bilingual assistant fluent in both English and Japanese."
            },
            {
                "role":"assistant",
                "content":"Now, please enter the text to be translated."
            },
            {
                "role": "user",
                "content": prompt 
            }
        ]
    })

    # Specify the model ID for Claude3
    model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'

    # Invoke the model and get the response
    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )

    # Parse the response and extract the translated text
    response_body = json.loads(response['body'].read())
    translated_text = response_body["content"][0]["text"]
    print(translated_text)

if __name__ == '__main__':
    translate_text()
