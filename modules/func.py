from pathlib import Path
import requests
from clint.textui import progress

def download_data(links: list, folder: str, proxy=False, auth=None):
    BASE_URL = "http://repositorio.dados.gov.br/segrt/"
    for data in links:
        file_exists = False
        link = f"{BASE_URL}{data}"
        dpath = Path(f"{folder}/{data}")
        if dpath.is_file():
                while not file_exists:
                    print("\n")
                    get_info = input(f"O arquivo {data} já foi realizado o download. Deseja refazer o download? Digite S para Sim e N para Não.")
                    if get_info.upper() == "S":
                        file_exists = True
                        if proxy:
                            get_data = requests.get(link, proxies=auth, stream=True)
                        if not proxy:
                            get_data = requests.get(link, stream=True)
                        if get_data.status_code == 200:
                            print(f"Iniciando o download de {link}.")
                            pbar(get_data, dpath)
                        else:
                            print(f"Recurso {link} não disponível.\n")
                    elif get_info.upper() == "N":
                        file_exists = True
                        print(f"O arquivo {link} não será realizado download.\n")
                    else:
                        print("Comando inválido. Digite uma opção válida.")
        else:
            if proxy:
                get_data = requests.get(link, proxies=auth, stream=True)
            if not proxy:
                get_data = requests.get(link, stream=True)
            if get_data.status_code == 200:
                print(f"Iniciando o download de {link}.")
                pbar(get_data, dpath)
            else:
                print(f"Recurso {link} não disponível.")

def pbar(r, path):
    with open(path, "wb") as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()

def create_folder(name):
    foldername = Path(f"./data/{name}/")
    foldername.mkdir(parents=True, exist_ok=True)
    return foldername