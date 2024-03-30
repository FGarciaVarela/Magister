from openai import Client

api_key = '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'

client = Client(api_key=api_key)

def consultar_chatgpt(prompt, max_tokens=2048):
    response = client.completions.create(
        model ="gpt-3.5-turbo",
        prompt= prompt,
        max_tokens = max_tokens
    )
    return response.choices[0].text


while True:

    prompt = input("¿Wich is the prompt? \n")
    consultar_chatgpt(prompt, 2048)

    if prompt == "exit":
        break
