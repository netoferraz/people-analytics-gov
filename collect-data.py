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
#create a folder for GSISTE data
giste_folder = Path("./data/gsiste")
giste_folder.mkdir(parents=True, exist_ok=True)
#create a folder for das data
das_folder = Path("./data/das")
das_folder.mkdir(parents=True, exist_ok=True)
#create a folder for abono data
abono_folder = Path("./data/abono")
abono_folder.mkdir(parents=True, exist_ok=True)
#create a pdv folder
pdv_folder = Path("./data/pdv")
pdv_folder.mkdir(parents=True, exist_ok=True)
#create a licenses folder
license_folder = Path("./data/licenses")
license_folder.mkdir(parents=True, exist_ok=True)
#available positions data
availpos_folder = Path("./data/availpos")
availpos_folder.mkdir(parents=True, exist_ok=True)
#download datasets
if args.proxy:
    #retired people
    download_data(retired_ppl_links, retired_ppl_folder, proxy=True, auth=PROXIES)
    #carrer data.
    download_data(carrer_ppl_links, carrer_folder, proxy=True, auth=PROXIES)
    #GSISTE data
    download_data(temporary_grat, giste_folder, proxy=True, auth=PROXIES)
    #DAS data
    download_data(das_data, das_folder, proxy=True, auth=PROXIES)
    #abono data 
    download_data(abono_data, abono_folder, proxy=True, auth=PROXIES)
    #pdv data
    download_data(pdv_data, pdv_folder, proxy=True, auth=PROXIES)
    #licenses data
    download_data(licenses_data, license_folder, proxy=True, auth=PROXIES)
    #available position data
    download_data(available_position_data, availpos_folder, proxy=True, auth=PROXIES)
if args.normal:
    #retired people
    download_data(retired_ppl_links, retired_ppl_folder)
    #carrer data
    download_data(carrer_ppl_links, carrer_folder)
    #GSISTE data
    download_data(temporary_grat, giste_folder)
    #DAS data
    download_data(das_data, das_folder)
    #abono data 
    download_data(abono_data, abono_folder)
    #pdv data
    download_data(pdv_data, pdv_folder)
    #licenses data
    download_data(licenses_data, license_folder)
    #available position data
    download_data(available_position_data, availpos_folder)