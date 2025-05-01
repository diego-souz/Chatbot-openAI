import yfinance as yf
import json
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

client = openai.Client()

def get_ticker_data(ticker, period):
    ticker_obj = yf.Ticker(ticker)
    hist = ticker_obj.history(period=period)["Close"]
    hist.index = hist.index.map(lambda x: x.strftime("%Y-%m-%d"))
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
        message.append(response.choices[0].message.to_dict())
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
        
        message.append(second_response.choices[0].message.to_dict())
        print(message)

    return message
