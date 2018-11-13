from pathlib import Path
import requests
def download_data(links: list, folder: str, proxy=False, auth=None):
    BASE_URL = "http://repositorio.dados.gov.br/segrt/"
    for data in links:
        file_exists = False
        link = f"{BASE_URL}{data}"
        dpath = Path(f"{folder}/{data}")
        if dpath.is_file():
                while not file_exists:
                    get_info = input(f"O arquivo {data} já foi realizado o download. Deseja refazer o download? Digite S para Sim e N para Não.")
                    if get_info.upper() == "S":
                        file_exists = True
                        if proxy:
                            get_data = requests.get(link, proxies=auth, stream=True)
                        if not proxy:
                            get_data = requests.get(link, stream=True)
                        if get_data.status_code == 200:
                            with open(dpath, "wb") as f:
                                print(f"Iniciando o download de {link}.")
                                _ = f.write(get_data.content)
                        else:
                            print(f"Recurso {link} não disponível.")
                    elif get_info.upper() == "N":
                        file_exists = True
                        print(f"O arquivo {link} não será realizado download.")
                    else:
                        print("Comando inválido. Digite uma opção válida.")
        else:
            if proxy:
                get_data = requests.get(link, proxies=auth, stream=True)
            if not proxy:
                get_data = requests.get(link, stream=True)
            if get_data.status_code == 200:
                with open(dpath, "wb") as f:
                    print(f"Iniciando o download de {link}.")
                    _ = f.write(get_data.content)
            else:
                print(f"Recurso {link} não disponível.")
