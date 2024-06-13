import os
import subprocess

def solicitar_caminho_pasta():
    caminho = input("Digite o caminho da pasta: ")
    while not os.path.isdir(caminho):
        print("Caminho inválido. Por favor, tente novamente.")
        caminho = input("Digite o caminho da pasta: ")
    return caminho

def listar_arquivos(caminho_pasta):
    extensoes_interesse = ['.docx', '.pdf', '.mp4', '.avi', '.mkv', '.jpg', '.jpeg', '.png', '.mp3']
    arquivos = []
    for root, _, files in os.walk(caminho_pasta):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensoes_interesse):
                arquivos.append(os.path.join(root, file))
    return arquivos

def extrair_metadados(arquivo):
    resultado = subprocess.run(['exiftool', '-all:all', '-json', arquivo], capture_output=True, text=True)
    if resultado.returncode == 0:
        return resultado.stdout
    else:
        print(f"Erro ao extrair metadados de {arquivo}: {resultado.stderr}")
        return None

def gerar_arquivo_metadados(caminho_pasta):
    arquivos = listar_arquivos(caminho_pasta)
    dados_para_salvar = []

    for arquivo in arquivos:
        print(f"Extraindo metadados de: {arquivo}")
        metadados = extrair_metadados(arquivo)
        if metadados:
            dados_para_salvar.append(f"Metadados de: {arquivo}\n{metadados}\n")

    with open('metadados.txt', 'w', encoding='utf-8') as f:
        for linha in dados_para_salvar:
            f.write(linha + '\n')
    print("Metadados salvos em 'metadados.txt'")

if __name__ == "__main__":
    caminho_pasta = solicitar_caminho_pasta()
    gerar_arquivo_metadados(caminho_pasta)
