from pathlib import Path
import requests
from lxml import html
import argparse
from modules.func import download_data

parser = argparse.ArgumentParser()
parser.add_argument("--proxy", action="store_true")
parser.add_argument("--normal", action="store_true")
args = parser.parse_args()

BASE_URL = "http://repositorio.dados.gov.br/segrt/"
if args.proxy:
    from env_variables import PROXIES
    get_all_links = requests.get(BASE_URL, proxies=PROXIES)
if args.normal:
   get_all_links = requests.get(BASE_URL)
#download all data available for people in federal governmnet
if get_all_links.status_code == 200:
    content = html.fromstring(get_all_links.text)
    filter_only_a_tags = content.xpath('//a/@href')
    #get links for retired employees data
    #example of url http://repositorio.dados.gov.br/segrt/APOSENTADOS-102018.CSV
    retired_ppl_links = [link for link in filter_only_a_tags if 'APOSENTADOS' in link.upper() and '.CSV' in link.upper() and 'PDF' not in link.upper()]
    #get links for carrer in federal government
    #example of url http://repositorio.dados.gov.br/segrt/CARREIRA-012017.TXT
    carrer_ppl_links = [link for link in filter_only_a_tags if 'CARREIRA' in link.upper() and 'PDF' not in link.upper()]
    #get links for temporary gratification (GSISTE)
    #example of url  http://repositorio.dados.gov.br/segrt/GSISTE_102018.CSV
    temporary_grat = [link for link in filter_only_a_tags if 'GSISTE' in link.upper() and 'PDF' not in link.upper()]
    #get links for DAS data
    #example of url http://repositorio.dados.gov.br/segrt/CARGODAS_102018.csv
    das_data = [link for link in filter_only_a_tags if 'CARGODAS' in link.upper() and 'PDF' not in link.upper()]
    #get links for "abono permanencia"
    #example of url http://repositorio.dados.gov.br/segrt/ABONOP_112017.csv
    abono_data = [link for link in filter_only_a_tags if 'ABONOP' in link.upper() and 'PDF' not in link.upper()]
    #get links for PDV
    #example of url http://repositorio.dados.gov.br/segrt/Programa%20de%20Desligamento%20Vonlutario%20-%20PDV-201808.xlsx
    pdv_data = [link for link in filter_only_a_tags if 'DESLIGAMENTO' in link.upper() and 'PDF' not in link.upper()]
    #get links for licenses 
    #example of url http://repositorio.dados.gov.br/segrt/AFASTREM_092018.CSV
    licenses_data = [link for link in filter_only_a_tags if 'AFASTREM' in link.upper() and 'PDF' not in link.upper()]
    #get links for available positions
    #example of url http://repositorio.dados.gov.br/segrt/LotOrgao_DistOcupVagas%20-%20201803.xlsx
    available_position_data = [link for link in filter_only_a_tags if 'DISTOCUP' in link.upper() and 'PDF' not in link.upper()]

#create a folder for retired employees
retired_ppl_folder = Path("./data/retired-employees/")
retired_ppl_folder.mkdir(parents=True, exist_ok=True)
#create a folder for carrer data
carrer_folder = Path("./data/carrer")
carrer_folder.mkdir(parents=True, exist_ok=True)

#download datasets
#retired people
if args.proxy:
    download_data(retired_ppl_links, retired_ppl_folder, proxy=True, auth=PROXIES)
if args.normal:
    download_data(retired_ppl_links, retired_ppl_folder)

#carrer data
if args.proxy:
    download_data(carrer_ppl_links, carrer_folder, proxy=True, auth=PROXIES)
if args.normal:
    download_data(carrer_ppl_links, carrer_folder)
"""
for data in retired_ppl_links:
    file_exists = False
    link = f"{BASE_URL}{data}"
    #retired ppl
    dpath = Path(f"{retired_ppl_folder}/{data}")
    if dpath.is_file():
        while not file_exists:
            get_info = input(f"O arquivo {data} já foi realizado o download. Deseja refazer o download? Digite S para Sim e N para Não.")
            if get_info.upper() == "S":
                file_exists = True
                if args.proxy:
                    get_data = requests.get(link, proxies=PROXIES, stream=True)
                if args.normal:
                    get_data = requests.get(link, stream=True)
                if get_data.status_code == 200:
                   with open(f"{retired_ppl_folder}/{data}", "wb") as f:
                       print(f"Iniciando o download de {link}.")
                       file = f.write(get_data.content)
                else:
                    print(f"Recurso {link} não disponível.")
            elif get_info.upper() == "N":
                file_exists = True
                print(f"O arquivo {link} não será realizado download.")
            else:
                print("Comando inválido. Digite uma opção válida.")
    else:
        if args.proxy:
            get_data = requests.get(link, proxies=PROXIES, stream=True)
        if args.normal:
            get_data = requests.get(link, stream=True)
        if get_data.status_code == 200:
            with open(f"{retired_ppl_folder}/{data}", "wb") as f:
                print(f"Iniciando o download de {link}.")
                file = f.write(get_data.content)
        else:
            print(f"Recurso {link} não disponível.")
"""