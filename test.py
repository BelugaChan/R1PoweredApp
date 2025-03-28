import PyPDF2
import os, os.path
from openai import OpenAI
import time

directory = r'D:\UchebPlans'
finalCount = len([entry for entry in os.listdir(directory) if os.path.isfile(os.path.join(directory, entry))])

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

def extract_technologies(directory: str, client: OpenAI) -> set:
    """Extract IT technologies from PDF files in a directory"""
    technologies = set()
    text = ""
    counter = 0

    for file in os.scandir(directory):
        if not file.is_file():
            continue

        try:
            with open(file.path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    text += page.extract_text() + ' '
        except Exception as e:
            print(f"Error processing file: {file.path}")
            continue

        counter += 1
        if(counter % 5 == 0 or counter == finalCount):
            print(f"processed {counter} PDFs")
            technologies = makeAPICall(text, technologies, client)
            text = ""
        
        time.sleep(10)
        # technologies = makeAPICall(text, technologies, client)
    return technologies

def makeAPICall(text: str, technologies: set, client: OpenAI) -> set:
    if(text.strip()):
        try:
            completion = client.chat.completions.create(
                        model="deepseek/deepseek-chat-v3-0324:free",
                        messages=[{
                            "role": "user",
                            "content": f"""Найди IT технологии в данном тексте. НЕ ДОБАВЛЯЙ в список длинные выражения. 
                            Выведи ТОЛЬКО результат поиска через запятую без пояснений.
                            Примеры для ориентира: Базы данных, SQL, Hadoop, SPARK, (Apache Kafka), ETL, MySQL, С++, 
                            чат-бот, Python, криптография, Data Science, ERP, MES, APS, VR, AR, ИИ, MathCad, Arduino IDE, 
                            САПР, 3D моделирование, Unity, NLP, AutoCAD, ML, .NET, мобильная разработка, C#, Blender.
                            
                            Текст для обработки: {text}"""
                        }]
                    )
            new_techs = [t.strip().lower().replace('\n','').replace('*','') for t in completion.choices[0].message.content.split(',') if t.strip()]
            technologies.update(new_techs)
        except Exception as e:
            print(f"Error while calling API {e}")
    return technologies

res = extract_technologies(directory,client)
print(res)

