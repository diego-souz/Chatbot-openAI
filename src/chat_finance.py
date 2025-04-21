import yfinance as yf
import json
import openai
from colorama import Fore, Style, init

client = openai.Client()

# Inicializa o colorama
init(autoreset=True)

def get_ticker_data(ticker, period):
    ticker_obj = yf.Ticker(ticker)
    hist = ticker_obj.history(period=period)["Close"]
    hist.index = hist.index.strftime("%Y-%m-%d")
    hist = round(hist, 2)
    #Limitar em 30 resultados
    if len(hist) > 30:
        slice_size = int(len(hist) / 30)
        hist = hist.iloc[::slice_size][::-1]

    return hist.to_json()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_ticker_data",
            "description": "Retorna cotação de ações da Ibovespa.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Ticker da ação a ser consultada com .SA no final. Ex: VALE3.SA, PETR4.SA",
                    },
                    "period": {
                        "type": "string",
                        "description": "Período de tempo para o qual a cotação deve ser consultada. \
                            será informado em dias, meses ou anos. \
                            sendo 1d para 1 dia, 1mo para 1 mês, 2mo para 2 meses, 1y para 1 ano, \
                                 5y para 5 anos e ytd para todos os tempos",
                        "enum": ["1d", "5d", "1mo", "6mo", "1y", "5y", "ytd", "max"],
                    },
                },
                "required": ["ticker", "period"],
            },
        }
    }
]

available_function = {"get_ticker_data": get_ticker_data}

def text_gen(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=message,
        tools=tools,
        tool_choice="auto"
    )

    tool_calls = response.choices[0].message.tool_calls

    if tool_calls:
        message.append(response.choices[0].message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_function[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_return = function_to_call(**function_args)
            
            message.append(
                {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_return
                }
            )

        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages = message
        )
        
        message.append(second_response.choices[0].message)
        print(f"{Fore.CYAN}Assistente IA: {second_response.choices[0].message.content}")

    return message


if __name__ == "__main__":
    print(f"{Fore.GREEN}Bem vindo ao ChatBot Financeiro")
    print(f"{Fore.GREEN}Digite 'sair' para encerrar a conversa")
    print(f"{Fore.GREEN}Iniciando conversa...")
    message = []
    while True:
        user_input = input(f"{Fore.LIGHTYELLOW_EX}Informe a empresa e o período que deseja consultar: {Style.RESET_ALL}")

        # Verificar se usário deseja sair
        if user_input.lower() == "sair":
            break

        message.append({"role":"user", "content":user_input})
        message = text_gen(message)
        
    print(message)