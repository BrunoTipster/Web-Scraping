import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
import logging

# Configura o logging
logging.basicConfig(filename='erros.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

def fetch_lotofacil_results():
    try:
        url = 'https://noticias.uol.com.br/loterias/lotofacil/'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        site = requests.get(url, headers=headers)
        site.raise_for_status()  # Levanta um erro para códigos de status HTTP ruins

        soup = BeautifulSoup(site.content, 'html.parser')
        
        # Encontra a div com a classe 'lottery-wrapper-content' e obtém o atributo 'data-info'
        info_div = soup.find('div', class_='lottery-wrapper-content')
        concurso_info = info_div['data-info'] if info_div else "Informação do concurso não encontrada"

        # Encontra todas as divs que têm a classe 'lt-result'
        placas = soup.find_all('div', class_='lt-result')

        if placas:
            for placa in placas:
                numeros = placa.find_all('div', class_='lt-number')
                if numeros:
                    numeros_sorteados = [num.get_text() for num in numeros]
                    return concurso_info, numeros_sorteados
        return concurso_info, []
    except Exception as e:
        logging.error("Erro ao buscar resultados da Lotofacil", exc_info=True)
        return "Erro ao obter informações do concurso", []

def display_results():
    try:
        concurso_info, numeros_sorteados = fetch_lotofacil_results()
        
        if numeros_sorteados:
            concurso_label.config(text=concurso_info)
            for widget in numbers_frame.winfo_children():
                widget.destroy()
            for i, num in enumerate(numeros_sorteados):
                num_label = ttk.Label(numbers_frame, text=num, style="Number.TLabel")
                num_label.grid(row=i // 5, column=i % 5, padx=5, pady=5)
        else:
            concurso_label.config(text=concurso_info)
            for widget in numbers_frame.winfo_children():
                widget.destroy()
            error_label = ttk.Label(numbers_frame, text="Não foi possível obter os números sorteados.", style="TLabel")
            error_label.grid(row=0, column=0, columnspan=5, pady=5)
    except Exception as e:
        logging.error("Erro ao exibir resultados", exc_info=True)
        concurso_label.config(text="Ocorreu um erro ao tentar exibir os resultados.")
        for widget in numbers_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    try:
        # Cria a janela principal
        root = tk.Tk()
        root.title("Resultados da Lotofácil")

        # Define o estilo personalizado
        style = ttk.Style()
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff", font=("Arial", 12))
        style.configure("Header.TLabel", font=("Arial", 18, "bold"), foreground="#ffffff", background="#800080")
        style.configure("Concurso.TLabel", font=("Arial", 12), foreground="#ffffff", background="#800080")
        style.configure("Number.TLabel", font=("Arial", 14), foreground="#800080", borderwidth=2, relief="solid", anchor="center", width=3)
        style.map("Number.TLabel", background=[('active', '#f0f0f0')])

        # Cria um frame para centralizar os widgets
        frame = ttk.Frame(root, padding="10", style="TFrame")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Cria um label de cabeçalho
        header_label = ttk.Label(frame, text="LOTOFÁCIL", style="Header.TLabel")
        header_label.grid(row=0, column=0, columnspan=5, pady=(0, 10), sticky="ew")

        # Cria um label para exibir o número do concurso e data
        concurso_label = ttk.Label(frame, text="", style="Concurso.TLabel")
        concurso_label.grid(row=1, column=0, columnspan=5, pady=(0, 10), sticky="ew")

        # Cria um botão para buscar os resultados
        fetch_button = ttk.Button(frame, text="Buscar Resultados", command=display_results)
        fetch_button.grid(row=2, column=0, columnspan=5, pady=(0, 10))

        # Cria um frame para mostrar os números sorteados
        numbers_frame = ttk.Frame(frame, style="TFrame")
        numbers_frame.grid(row=3, column=0, columnspan=5, pady=(0, 10))

        # Inicia o loop principal
        root.mainloop()
    except Exception as e:
        logging.error("Erro no loop principal", exc_info=True)
