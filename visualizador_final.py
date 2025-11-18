import random
import colorsys
import tkinter as tk
from tkinter import ttk

# --- Variável Global para a Paleta Atual ---
# Usada para saber qual paleta salvar como favorita
paleta_atual = []
paleta_em_uso = "Complementar"


# --- Funções de Conversão ---
def hsv_para_rgb_255(h, s, v):
    """Converte HSV (0.0-1.0) para RGB (0-255)."""
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)


def rgb_para_hex(r, g, b):
    """Converte valores RGB (0-255) para o código hexadecimal."""
    return f'#{r:02x}{g:02x}{b:02x}'.upper()


# --- Funções de Geração de Paletas ---
def gerar_paleta_complementar():
    """Gera 2 cores: Base e Oposta (180 graus)."""
    h_base = random.random();
    s = 0.8;
    v = 0.9
    h_complementar = (h_base + 0.5) % 1.0

    r_base, g_base, b_base = hsv_para_rgb_255(h_base, s, v)
    r_comp, g_comp, b_comp = hsv_para_rgb_255(h_complementar, s, v)

    return [
        {'nome': 'Base', 'hex': rgb_para_hex(r_base, g_base, b_base)},
        {'nome': 'Comp.', 'hex': rgb_para_hex(r_comp, g_comp, b_comp)}
    ]


def gerar_paleta_triadica():
    """Gera 3 cores igualmente espaçadas (120 graus)."""
    h_base = random.random();
    s = 0.8;
    v = 0.9
    distancia = 1.0 / 3.0

    h2 = (h_base + distancia) % 1.0
    h3 = (h_base + (2 * distancia)) % 1.0

    r_base, g_base, b_base = hsv_para_rgb_255(h_base, s, v)
    r2, g2, b2 = hsv_para_rgb_255(h2, s, v)
    r3, g3, b3 = hsv_para_rgb_255(h3, s, v)

    return [
        {'nome': 'Base', 'hex': rgb_para_hex(r_base, g_base, b_base)},
        {'nome': 'Cor 2', 'hex': rgb_para_hex(r2, g2, b2)},
        {'nome': 'Cor 3', 'hex': rgb_para_hex(r3, g3, b3)}
    ]


def gerar_paleta_analoga():
    """Gera 3 cores vizinhas (30 graus de distância)."""
    h_base = random.random();
    s = 0.8;
    v = 0.9
    distancia = 30 / 360

    h1 = (h_base - distancia) % 1.0
    h3 = (h_base + distancia) % 1.0

    r1, g1, b1 = hsv_para_rgb_255(h1, s, v)
    r_base, g_base, b_base = hsv_para_rgb_255(h_base, s, v)
    r3, g3, b3 = hsv_para_rgb_255(h3, s, v)

    return [
        {'nome': 'Cor 1', 'hex': rgb_para_hex(r1, g1, b1)},
        {'nome': 'Base', 'hex': rgb_para_hex(r_base, g_base, b_base)},
        {'nome': 'Cor 3', 'hex': rgb_para_hex(r3, g3, b3)}
    ]


# --- Funções de Visualização ---
root = None
content_frame = None
status_label = None  # Novo label para status


def gerar_nova_paleta():
    """Gera uma nova paleta baseada no tipo que está sendo visualizado."""
    global paleta_em_uso

    if paleta_em_uso == "Complementar":
        desenhar_paleta(gerar_paleta_complementar(), "Paleta Complementar")
    elif paleta_em_uso == "Triádica":
        desenhar_paleta(gerar_paleta_triadica(), "Paleta Triádica")
    elif paleta_em_uso == "Análoga":
        desenhar_paleta(gerar_paleta_analoga(), "Paleta Análoga")


def desenhar_paleta(paleta_dados, titulo):
    """Limpa a tela e desenha os novos blocos de cores."""
    global content_frame, paleta_atual, paleta_em_uso, status_label

    paleta_atual = paleta_dados
    paleta_em_uso = titulo.split()[1]  # Extrai "Complementar", "Triádica" ou "Análoga"

    # Limpa o Frame anterior
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Título
    title_label = ttk.Label(content_frame, text=titulo, font=('Helvetica', 14, 'bold'))
    title_label.pack(pady=10)

    # Frame para as caixas de cor
    color_frame = ttk.Frame(content_frame)
    color_frame.pack(fill=tk.X, padx=10)

    # Desenha cada cor
    for item in paleta_dados:
        label = ttk.Label(
            color_frame,
            text=f"{item['nome']}\n{item['hex']}",
            background=item['hex'],
            foreground="#000000",
            width=15,
            anchor='center'
        )
        label.pack(padx=5, side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Limpa a mensagem de status
    status_label.config(text="")


# --- FUNÇÃO DE SALVAMENTO ATUALIZADA (Salva em arquivo .txt) ---

def salvar_favorito_e_feedback():
    """
    Formata a paleta atual e salva em um arquivo de texto local
    chamado 'paletas_favoritas.txt'.
    """
    global paleta_atual, paleta_em_uso, status_label

    if not paleta_atual:
        status_label.config(text="Erro: Nenhuma paleta para salvar.", foreground="red")
        return

    # 1. Formata o item a ser salvo
    codigos_hex = ", ".join([item['hex'] for item in paleta_atual])
    item_para_salvar = f"[{paleta_em_uso}] - {codigos_hex}"

    # 2. SALVA EM UM ARQUIVO LOCAL
    try:
        # 'a' significa "append" (adicionar ao final do arquivo, sem apagar o que já existe)
        with open("paletas_favoritas.txt", "a") as arquivo:
            arquivo.write(item_para_salvar + "\n")

        # 3. Feedback visual na tela
        status_label.config(text=f"Salvo! Paleta {paleta_em_uso} adicionada ao arquivo.", foreground="green")

    except Exception as e:
        # Caso haja algum erro de permissão ou escrita no disco
        status_label.config(text=f"Erro ao salvar em arquivo: {e}", foreground="red")

def exibir_visualizador_completo():
    """Configura a janela principal e os botões de controle."""
    global root, content_frame, status_label

    root = tk.Tk()
    root.title("Gerador de Harmonias de Cores")
    root.geometry("600x350")

    # Frame de Controles Principais (Tipo de Paleta e Gerar)
    control_frame = ttk.Frame(root)
    control_frame.pack(pady=10)

    # Botões para alternar as paletas
    ttk.Button(control_frame, text="Complementar (2)",
               command=lambda: desenhar_paleta(gerar_paleta_complementar(), "Paleta Complementar")).pack(side=tk.LEFT,
                                                                                                         padx=5)

    ttk.Button(control_frame, text="Triádica (3)",
               command=lambda: desenhar_paleta(gerar_paleta_triadica(), "Paleta Triádica")).pack(side=tk.LEFT, padx=5)

    ttk.Button(control_frame, text="Análoga (3)",
               command=lambda: desenhar_paleta(gerar_paleta_analoga(), "Paleta Análoga")).pack(side=tk.LEFT, padx=5)

    # Botão de Geração (Novo)
    ttk.Button(control_frame, text="🔄 Gerar Novo",
               command=gerar_nova_paleta).pack(side=tk.LEFT, padx=15)

    # Botão de Salvar (Favorito)
    ttk.Button(control_frame, text="⭐ Salvar como Favorito",
               command=salvar_favorito_e_feedback).pack(side=tk.LEFT, padx=5)

    # Frame para o Conteúdo (cores)
    content_frame = ttk.Frame(root)
    content_frame.pack(fill=tk.BOTH, expand=True)

    # Label de Status (para feedback de salvamento)
    status_label = ttk.Label(root, text="", foreground="black")
    status_label.pack(pady=10)

    # Desenha a Complementar por padrão ao iniciar
    desenhar_paleta(gerar_paleta_complementar(), "Paleta Complementar")

    root.mainloop()


# --- Bloco de Inicialização (Execução) ---
if __name__ == '__main__':
    exibir_visualizador_completo()