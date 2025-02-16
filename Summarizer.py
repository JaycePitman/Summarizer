from openai import OpenAI
from PyPDF2 import PdfReader
import os
import time
import io

client = OpenAI(
    api_key='<OpenAI_api_key>'
    )

def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def get_text(file):
    pdf_data = open(file, "rb")
    reader = PdfReader(pdf_data)
    num_pages = len(reader.pages)
    text = ""

    for page in range(num_pages):
        current_page = reader.pages[page]
        text += current_page.extract_text()
    return text

file_path = input("Enter the path to the file: ")
text = get_text(file_path)
gpt_prompt = "Summarize the following text: " + text
chat = chat_gpt(gpt_prompt)
print(chat)
