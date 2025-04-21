#Execute com o comando:
# streamlit run main.py
 
import sys
import os

# Obtém o diretório do script main.py
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")

# Adiciona o diretório src ao sys.path se não estiver lá
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import interface

# Main function to run the Streamlit app
if __name__ == "__main__":

    interface.streamlit_interface()

