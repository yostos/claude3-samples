#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tralslation tool between Japanese and English
# using OpenAI API


from openai import OpenAI

import os
import json
import sys
from dotenv import load_dotenv
import click 


# Definition of command line arguments
@click.command()

def translate_text():

    """This tool translates """
    # get API key from .env file
    load_dotenv()

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    source = input("Enter the text you wish to translate: ")

    # Define the prompt for the translation task
    prompt = (
        "Please translate the following sentences. If the sentence is in Japanese, "
            "translate it into English; if the sentence is in English, translate it into Japanese. "
            "Please provide only the translated text in your response.\n\n"
            f"{source}"
    )
    # Call the OpenAI API to generate the translation
    response = client.chat.completions.create(model = "gpt-4",
                                              messages = [
                                              {"role": "system","content": "You are a bilingual assistant fluent in both English and Japanese."},
                                              {"role": "user","content": prompt}
                                              ])

    # Extract and print the translated text
    translated_text = response.choices[0].message.content.strip()
    print(translated_text)


if __name__ == '__main__':
    translate_text()
