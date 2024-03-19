#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Generate CDK TypeScript definitions from AWS architecture diagrams

import boto3
import json
import base64
import sys
import os
from dotenv import load_dotenv
import click 


@click.command()
@click.option('--debug','-D',is_flag=True, help='Debug mode')
@click.option('--file', '-f',prompt='AWS Architecture Image Filename',help='Input Image Filename')

def generate(debug,file):

    """This tool generate Typescript from AWS figure"""
    load_dotenv()
    access_key = os.environ["AWS_ACCESS_KEY"]
    secret_key = os.environ["AWS_SECRET_KEY"]

    image = open(file, "rb").read()
    b64 = base64.b64encode(image).decode("utf-8")

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
                    "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": b64
                        }
                    },
                    {
                        "type": "text",
                        "text": "Please write and present the AWS CDK code in TypeScript that will realize the image composition."
                    }
                ]
                }
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
