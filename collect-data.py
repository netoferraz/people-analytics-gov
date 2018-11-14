from pathlib import Path
import requests
from lxml import html
import argparse
from modules.func import download_data, create_folder

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
retired_ppl_folder = create_folder("retired-employees")
#create a folder for carrer data
carrer_folder = create_folder("carrer")
#create a folder for GSISTE data
giste_folder = create_folder("gsiste")
#create a folder for das data
das_folder = create_folder("das")
#create a folder for abono data
abono_folder = create_folder("abono")
#create a pdv folder
pdv_folder = create_folder("pdv")
#create a licenses folder
license_folder = create_folder("licenses")
#available positions data
availpos_folder = create_folder("availpos")

#list of all links
list_of_links = [retired_ppl_links, carrer_ppl_links, temporary_grat, das_data, abono_data, pdv_data, licenses_data, available_position_data]
#list of all folders
list_of_folders = [retired_ppl_folder, carrer_folder, giste_folder, das_folder, abono_folder, pdv_folder, license_folder, availpos_folder]

#download datasets
if args.proxy:
    for links, folder in zip(list_of_links, list_of_folders):
        download_data(links, folder)
if args.normal:
    for links, folder in zip(list_of_links, list_of_folders):
        download_data(links, folder)