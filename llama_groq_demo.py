from groq import Groq
from decouple import config

client = Groq(
    api_key=config("GROQ_API_KEY"),
)

dialog_history = []

while True:
    user_input = input("Введите ваше сообщение ('stop' для завершения): ")

    if user_input.lower() == "stop":
        break

    # Добавляем сообщение пользователя в историю диалога
    dialog_history.append({
        "role": "user",
        "content": user_input,
    })

    models = ["gemma-7b-it", "llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"]
    chat_completion = client.chat.completions.create(
        messages=dialog_history,
        model=models[1],
    )

    response = chat_completion.choices[0].message.content
    print("Ответ модели:", response)

    # Добавляем ответ модели в историю диалога
    dialog_history.append({
        "role": "assistant",
        "content": response,
    })
