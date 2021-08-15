import requests
from pprint import pprint

import json
from datetime import datetime, timedelta, timezone

UTC = timezone.utc
JST = timezone(timedelta(hours=+9), 'JST')

def convert_jst(datetime_obj):
    if datetime_obj.tzinfo is None:
        datetime_obj = datetime_obj.replace(tzinfo=UTC)
    return datetime_obj.astimezone(JST)

def send_to_notion(title, get_question, get_answer, get_question_author, get_answer_author, get_question_date):
    page_title = title
    question = get_question
    answer = get_answer
    question_author = get_question_author
    answer_author = get_answer_author
    question_date = get_question_date
    question_date_jst = convert_jst(question_date)
    print(question_date)

    def get_request_url(end_point):
        return f'https://api.notion.com/v1/{end_point}'

    notion_api_key = ''
    databases_id = ''
    headers = {"Authorization": f"Bearer {notion_api_key}",
               "Content-Type": "application/json",
               "Notion-Version": "2021-07-27",
               }

    property_name = {"title": [{"text": {"content": page_title}}]}
    property_date = {"date": {"start": question_date_jst.isoformat()}}
    property_question_author = {"select": {"name": question_author}}
    property_question = {
        "type": "rich_text",
        "rich_text": [{"text": {"content": question}}], }
    property_answer_author = {"select": {"name": answer_author}}
    property_answer = {
        "type": "rich_text",
        "rich_text": [{"text": {"content": answer}}], }

    body = {
        "parent": {
            "database_id": databases_id},
        "properties": {
            "Q&A": property_name,
            "質問日": property_date,
            "質問者": property_question_author,
            "Question": property_question,
            "解答者": property_answer_author,
            "Answer": property_answer
        }}

    response = requests.request('POST', url=get_request_url(
        'pages'), headers=headers, data=json.dumps(body))
    pprint(response.json())