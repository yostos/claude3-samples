#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tool to generate questions to check Amazon OLP


import boto3
import json
import sys
import os
from dotenv import load_dotenv
import click 


# コマンドライン引数の設定
@click.command()
@click.option('--debug','-D',is_flag=True, help='Debug mode')

def generate(debug):

    """This tool generates questions according to Amazon OLP. """
    load_dotenv()
    access_key = os.environ["AWS_ACCESS_KEY"]
    secret_key = os.environ["AWS_SECRET_KEY"]

    olp = [
        "Customer Obsession",
        "Ownership",
        "Invent and Simplify",
        "Are Right, A Lot",
        "Learn and Be Curious",
        "Hire and Develop the Best",
        "Insist on the Highest Standards",
        "Think Big",
        "Bias for Action",
        "Frugality",
        "Earn Trust",
        "Dive Deep",
        "Have Backbone; Disagree and Commit",
        "Deliver Results",
        "Strive to be Earth’s Best Employer",
        "Success and Scale Bring Broad Responsibility",
    ]

    print("Select the OLP by number for which you wish to generate questions.")
    for i in range(len(olp)):
        print(f"{i+1} : {olp[i]}")
    qano = int(input(">>"))

    qa_olp = olp[qano-1]
    print(f"Generating questions about {qa_olp}.")
    bedrock = boto3.client('bedrock-runtime', 
                           aws_access_key_id = access_key,
                           aws_secret_access_key = secret_key,
                           region_name = "us-west-2")

    question = f"""
    You are an interviewer at Amazon and are conducting a hiring interview. You
    are interviewing for a position at Amazon and have been asked to identify
    your experience with Amazon's Our Leadership Principle {qa_olp}.
    Please provide about five questions. For each question, please add three
    additional questions to go into more depth. Only the generated questions
    should be displayed. The generated questions should be formatted and output
    in Markdown format.
              """

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": question
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
