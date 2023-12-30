import openai
from setts import GPT_TOKEN
from prompts import prompts


def gpt(type_: str) -> str:
    openai.api_key = GPT_TOKEN

    print("start generating")
    print("Type:", type_)

    if str(type_) == "none" or str(type_) == "None":
        return False

    try:
        # Используйте параметр data вместо messages
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": type_}
            ]
        )

        # Получаем текст из массива choices
        if 'choices' in response and response['choices']:
            return response.get("choices")[0].get("message").get("content")
        else:
            print(2)
            return False

    except openai.error.OpenAIError as e:
        print(e)
        return False