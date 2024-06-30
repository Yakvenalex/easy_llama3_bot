from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',
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

    response = client.chat.completions.create(
        model="llama3:8b",
        messages=dialog_history,
    )

    # Извлекаем содержимое ответа
    response_content = response.choices[0].message.content
    print("Ответ модели:", response_content)

    # Добавляем ответ модели в историю диалога
    dialog_history.append({
        "role": "assistant",
        "content": response_content,
    })
