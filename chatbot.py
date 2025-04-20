import openai

client = openai.Client()

def text_gen(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=message,
        temperature=0,
        max_tokens=1000,
        stream=True
    )
    print("Bot: ", end="")
    fulltext = ""
    for response_stream in response:
        text= response_stream.choices[0].delta.content
        if text:
            fulltext += text
            print(text, end="")
    print()
    message.append({"role":"assistant", "content":fulltext})
    return message



if __name__ == "__main__":
    print("Bem vindo ao ChatBot")
    print("Digite 'sair' para encerrar a conversa")
    print("Iniciando conversa...")
    message = []
    while True:
        user_input = input("Informe sua mensagem: ")

        # Verificar se usário deseja sair
        if user_input.lower() == "sair":
            break

        message.append({"role":"user", "content":user_input})
        message = text_gen(message)
        
        
        
    
