import openai
from colorama import Fore, Style, init

client = openai.Client()

# Inicializa o colorama
init(autoreset=True)

def text_gen(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=message,
        temperature=0,
        max_tokens=1000,
        stream=True
    )
    print(f"{Fore.CYAN}Assitente IA: ", end="")
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
    print(f"{Fore.GREEN}Bem vindo ao ChatBot")
    print(f"{Fore.GREEN}Digite 'sair' para encerrar a conversa")
    print(f"{Fore.GREEN}Iniciando conversa...")
    message = []
    while True:
        user_input = input(f"{Fore.LIGHTYELLOW_EX}Informe sua mensagem: {Style.RESET_ALL}")

        # Verificar se usário deseja sair
        if user_input.lower() == "sair":
            break

        message.append({"role":"user", "content":user_input})
        message = text_gen(message)
        
        
        
    
