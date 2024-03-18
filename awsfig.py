#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AWS のアーキテクチャー図から CDKのTypeScript定義を生成する


import boto3
import json
import base64
import sys
import os
from dotenv import load_dotenv
import click 


# コマンドライン引数の設定
@click.command()
@click.option('--debug','-D',is_flag=True, help='Debug mode')
@click.option('--file', '-f',prompt='AWS Architecture Image Filename',help='Input Image Filename')

def generate(debug,file):

    """This tool generate Typescript from AWS figure"""
    # .envからAPIキーを取得する。
    # .envファイルには、DEEPL_API_KEY="APIキー"のように記載する。
    load_dotenv()
    access_key = os.environ["AWS_ACCESS_KEY"]
    secret_key = os.environ["AWS_SECRET_KEY"]

    image = open(file, "rb").read()
    b64 = base64.b64encode(image).decode("utf-8")

    # 指定可能なリージョンはバージニア北部（us-east-1）またはオレゴン（us-west-2）
    # デフォルトリージョンで良い場合はリージョン指定省略可
    # サンプルのため認証情報が直接書き込まれています。適切な方法で取得するようにしてください。
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
                        "text": "画像の構成を実現するAWS CDKのコードをTypeScriptで書いて提示してください。"
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
