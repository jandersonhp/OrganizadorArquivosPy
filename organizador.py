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

# ------------------------------
# Função para aplicar o tema
# ------------------------------
def aplicar_tema(tema):
    if tema == "dark":
        root.configure(bg="#1e1e1e")
        lbl.config(bg="#1e1e1e", fg="#ffffff")
        frame_caminho.config(bg="#1e1e1e")
        entry_caminho.config(bg="#252526", fg="#d4d4d4", insertbackground="white")
        btn_browse.config(bg="#0e639c", fg="white")
        btn_organizar.config(bg="#007acc", fg="white")
        txt_saida.config(bg="#252526", fg="#d4d4d4", insertbackground="white")
        btn_tema.config(bg="#444444", fg="white", text="🌞 Modo Claro")
    else:  # light
        root.configure(bg="#f0f0f0")
        lbl.config(bg="#f0f0f0", fg="#333333")
        frame_caminho.config(bg="#f0f0f0")
        entry_caminho.config(bg="white", fg="black", insertbackground="black")
        btn_browse.config(bg="#4CAF50", fg="white")
        btn_organizar.config(bg="#2196F3", fg="white")
        txt_saida.config(bg="white", fg="black", insertbackground="black")
        btn_tema.config(bg="#dddddd", fg="black", text="🌙 Modo Escuro")

    global tema_atual
    tema_atual = tema

# Alternar tema
def alternar_tema():
    if tema_atual == "dark":
        aplicar_tema("light")
    else:
        aplicar_tema("dark")

# Criando a janela principal
root = tk.Tk()
root.title("Organizador de Arquivos")
root.geometry("400x400")

# Label inicial
lbl = tk.Label(root, text="Selecione a pasta que deseja organizar:",
               font=("Arial", 12, "bold"))
lbl.pack(pady=10)

# Frame para entrada e botão de selecionar
frame_caminho = tk.Frame(root)
frame_caminho.pack(pady=5, padx=10, fill="x")

entry_caminho = tk.Entry(frame_caminho, font=("Consolas", 11),
                         relief="flat")
entry_caminho.pack(side="left", fill="x", expand=True, padx=(5,5), ipady=4)

btn_browse = tk.Button(frame_caminho, text="📂 Procurar", command=selecionar_pasta,
                       font=("Segoe UI", 8, "bold"),
                       relief="flat", padx=5, pady=5)
btn_browse.pack(side="right")

# Botão organizar
btn_organizar = tk.Button(root, text="⚡ Organizar Arquivos", command=organizar,
                          font=("Segoe UI", 12, "bold"),
                          relief="flat", padx=10, pady=5)
btn_organizar.pack(pady=10)

# Botão alternar tema
btn_tema = tk.Button(command=alternar_tema)
menu_bar = tk.Menu(root)
tema_menu = tk.Menu(menu_bar, tearoff=0)
tema_menu.add_command(label="🌙 Dark", command=lambda: aplicar_tema("dark"))
tema_menu.add_command(label="☀️ Light", command=lambda: aplicar_tema("light"))
menu_bar.add_cascade(label="Tema", menu=tema_menu)
root.config(menu=menu_bar)

# Caixa de saída
txt_saida = scrolledtext.ScrolledText(root, width=70, height=20,
                                      font=("Courier New", 10), relief="sunken", bd=2)
txt_saida.pack(padx=10, pady=5)

# Tema inicial = dark
tema_atual = "dark"
aplicar_tema(tema_atual)


root.mainloop()
