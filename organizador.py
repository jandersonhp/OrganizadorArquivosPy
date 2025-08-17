import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Categorias e extensões
categorias = {
    "Imagens": [".jpg",".png",".gif",".jpeg"],
    "Documentos": [".pdf", ".docx", ".txt", ".xlsx", ".odt", ".odp", ".odb", ".odg"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Musicas": [".mp3", ".wav"],
    "Programas": [".exe"],
    "Compactados": [".rar", ".zip", ".7z", ".tar", ".gz", ".bz2", ".xz"]
}

# Função para mover arquivos sem sobrescrever
def mover_arquivo(origem, destino_pasta):
    nome_arquivo = os.path.basename(origem)
    destino = os.path.join(destino_pasta, nome_arquivo)
    contador = 1
    nome_sem_ext, ext = os.path.splitext(nome_arquivo)
    while os.path.exists(destino):
        destino = os.path.join(destino_pasta, f"{nome_sem_ext} ({contador}){ext}")
        contador += 1
    shutil.move(origem, destino)
    return os.path.basename(destino_pasta)

# Função para organizar arquivos
def organizar():
    pasta = entry_caminho.get()
    if not os.path.exists(pasta):
        messagebox.showerror("Erro", "Pasta não encontrada!")
        return

    arquivos = os.listdir(pasta)

    # Criar pastas das categorias
    for categoria in categorias:
        caminho_nova_pasta = os.path.join(pasta, categoria)
        if not os.path.exists(caminho_nova_pasta):
            os.makedirs(caminho_nova_pasta)

    # Contadores
    contador_categoria = {categoria: 0 for categoria in categorias}
    contador_categoria["Outros"] = 0

    # Limpa a saída
    txt_saida.delete(1.0, tk.END)

    for arquivo in arquivos:
        caminho_arquivo = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho_arquivo):
            movido = False
            for categoria, extensoes in categorias.items():
                if arquivo.lower().endswith(tuple(extensoes)):
                    destino_pasta = os.path.join(pasta, categoria)
                    mover_arquivo(caminho_arquivo, destino_pasta)
                    contador_categoria[categoria] += 1
                    movido = True
                    break
            if not movido:
                pasta_outros = os.path.join(pasta, "Outros")
                if not os.path.exists(pasta_outros):
                    os.makedirs(pasta_outros)
                mover_arquivo(caminho_arquivo, pasta_outros)
                contador_categoria["Outros"] += 1

    # Exibe o resumo
    txt_saida.insert(tk.END, "Resumo da organização:\n")
    for categoria, qtd in contador_categoria.items():
        txt_saida.insert(tk.END, f"{categoria}: {qtd} arquivo(s)\n")
    messagebox.showinfo("Sucesso", "Arquivos organizados com sucesso!")

# Função para selecionar pasta
def selecionar_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        entry_caminho.delete(0, tk.END)
        entry_caminho.insert(0, pasta)

# Criando a janela principal
root = tk.Tk()
root.title("Organizador de Arquivos")
root.configure(bg="#f0f0f0")
root.geometry("400x400")

# Label inicial
tk.Label(root, text="Selecione a pasta que deseja organizar:",
         bg="#f0f0f0", fg="#333333", font=("Arial", 12, "bold")).pack(pady=10)

# Frame para entrada e botão de selecionar
frame_caminho = tk.Frame(root, bg="#f0f0f0")
frame_caminho.pack(pady=5, padx=10, fill="x")
entry_caminho = tk.Entry(frame_caminho, font=("Arial", 11))
entry_caminho.pack(side="left", fill="x", expand=True, padx=(0,5))
btn_browse = tk.Button(frame_caminho, text="Selecionar", command=selecionar_pasta,
                       bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=12)
btn_browse.pack(side="left")

# Botão organizar
btn_organizar = tk.Button(root, text="Organizar", command=organizar,
                          bg="#2196F3", fg="white", font=("Arial", 12, "bold"), width=20)
btn_organizar.pack(pady=10)

# Caixa de saída
txt_saida = scrolledtext.ScrolledText(root, width=70, height=20, bg="#ffffff", fg="#000000",
                                      font=("Courier New", 10), relief="sunken", bd=2)
txt_saida.pack(padx=10, pady=5)

root.mainloop()
