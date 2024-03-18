#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AWS のアーキテクチャー図から CDKのTypeScript定義を生成する


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
    # .envからAPIキーを取得する。
    # .envファイルには、DEEPL_API_KEY="APIキー"のように記載する。
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

    print("質問を生成したいOLPを番号で選択してください。")
    for i in range(len(olp)):
        print(f"{i+1} : {olp[i]}")
    qano = int(input(">>"))

    qa_olp = olp[qano-1]
    print(f"{qa_olp}についての質問を生成します。")
    # 指定可能なリージョンはバージニア北部（us-east-1）またはオレゴン（us-west-2）
    # デフォルトリージョンで良い場合はリージョン指定省略可
    # サンプルのため認証情報が直接書き込まれています。適切な方法で取得するようにしてください。
    bedrock = boto3.client('bedrock-runtime', 
                           aws_access_key_id = access_key,
                           aws_secret_access_key = secret_key,
                           region_name = "us-west-2")

    question = f"""
                あなたはアマゾンの面接官で採用面接を行っています。
                アマゾンのOur Leadership Principleの{qa_olp}についての経験を確認するための
                質問を使用としています。5パターンぐらい質問を提示してください。
                それぞれの質問について深堀するための質問を3つづつ追加してください。
                提示は生成した質問のみ表示してください。
                生成した質問はMarkdown形式で整形して出力してください。
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
