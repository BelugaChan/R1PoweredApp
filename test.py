from openai import OpenAI
import PyPDF2
import os

directory = r'some-path'

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="api-key-from-open-router",
)

res = ""
counter = 0
answer = ""
for entry in os.scandir(directory):  
    if entry.is_file():
        counter += 1
        with open(entry.path,'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                res += page.extract_text() + ' '
    if counter % 5 == 0:
        print('Done with reading pdfs')
        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[
                {
                "role": "user",
                "content": f"""Найди IT технологии в данном тексте. НЕ ДОБАВЛЯЙ в список длинные выражения. Выведи ТОЛЬКО результат поиска через запятую без пояснений.
                Примеры для ориентира: Базы данных, SQL,Hadoop,SPARK,(Apache Kafka),ETL,MySQL,С++, чат-бот,Python, криптография, 
                Data Science, ERP, MES, APS, VR,AR, ИИ, MathCad, Arduino IDE, САПР, 3D моделирование,Unity, NLP, AutoCAD, ML,.NET, 
                мобильная разработка,C#,Blender.

                Текст для обработки: {res}"""
                }
            ]
        )
        answer += completion.choices[0].message.content + ','
        res=""
        print(f"done: {counter}\n" )

myList = answer.lower().split(',')
for i in range (len(myList)):
    myList[i] = myList[i].strip().replace('\n','').replace('*','')

new_list = list(filter(None, myList))
print(set(new_list))
