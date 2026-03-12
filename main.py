import requests
import pandas as pd
from bs4 import BeautifulSoup


def clean_html(raw_html):
    """Убирает HTML-теги (типа <div>), оставляя только чистый текст."""
    if not raw_html:
        return "Описание отсутствует"
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ").strip()


URL = "https://api.hh.ru/vacancies"
PARAMS = {
    "text": "Повар",
    "experience": "between1And3",  
    "per_page": 5,                
    "page": 0
}


response = requests.get(URL, params=PARAMS)
data = response.json()

vacancies = []

for item in data["items"]:
    vacancy_id = item["id"]
    
    
    detail = requests.get(f"{URL}/{vacancy_id}").json()
    
    
    title = item.get("name", "Не указано")
    
    
    salary = "Не указана"
    if item.get("salary"):
        salary_from = item["salary"]["from"]
        salary_to = item["salary"]["to"]
        salary = f"{salary_from} - {salary_to}" if salary_from or salary_to else "Не указана"
    
    
    description_html = detail.get("description", "")
    description = clean_html(description_html)
    
    
    skills = [s["name"] for s in detail.get("key_skills", [])]
    skills_text = ", ".join(skills) if skills else "Не указано"
    
    
    vacancies.append({
        "Название вакансии": title,
        "Краткое описание": description,
        "Заработная плата": salary,
        "Ключевые навыки": skills_text
    })


df = pd.DataFrame(vacancies)
df.to_excel("jobs.xlsx", index=False)

print("Файл jobs.xlsx успешно создан!")
