import os
import sys
import tempfile
import zipfile
import tarfile
from pathlib import Path
import shutil
import urllib.request
from urllib.error import URLError
from html.parser import HTMLParser
from datetime import datetime

LIGHTBLACK_EX = "\033[90m"
CYAN = "\033[36m"
RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"

def log_positive(txt):
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S")
    print(f"{LIGHTBLACK_EX + dt_string} ({CYAN}+{LIGHTBLACK_EX}){CYAN} {txt}{RESET}")

def log_negative(txt):
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S")
    print(f"{LIGHTBLACK_EX + dt_string} ({RED}-{LIGHTBLACK_EX}){RED} {txt}{RESET}")

def log_normal(txt):
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S")
    print(f"{LIGHTBLACK_EX + dt_string} ({BLUE}~{LIGHTBLACK_EX}){BLUE} {txt}{RESET}")

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == 'href':
                    self.hrefs.append(attr[1])

def get_last_pypi_href(lib_name):
    url = f"https://pypi.org/simple/{lib_name}/"
    try:
        with urllib.request.urlopen(url) as response:
            html_content = response.read().decode('utf-8')
        parser = MyHTMLParser()
        parser.feed(html_content)
        if parser.hrefs:
            last_href = parser.hrefs[-1]
            clean_href = last_href.split('#')[0]
            return clean_href
        else:
            return "No href found."
    except URLError as e:
        log_negative(f"Failed to access {url}: {e}")
        return None
def download_and_load_package(packagename_or_url, is_pypi=True):
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

    url = get_last_pypi_href(packagename_or_url) if is_pypi else packagename_or_url
    if url is None:
        return None

    req = urllib.request.Request(url, headers=hdr)
    try:
        with urllib.request.urlopen(req) as response:
            file_name = url.split('/')[-1]
            temp_file_path = tempfile.mktemp(suffix=file_name)
            with open(temp_file_path, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            package_path = LoadPackage(temp_file_path)
            os.remove(temp_file_path)
            sys.path.append(package_path)
            return package_path
    except URLError as e:
        log_negative(f"Failed to download package: {e}")
        return None



def get_first_dir_name(folder_path):
    for entry in os.listdir(folder_path):
        if os.path.isdir(os.path.join(folder_path, entry)):
            return entry
    return None
def LoadPackage(file_path_str):
    file_path = Path(file_path_str)
    
    if file_path.suffix == '.zip':
        open_archive = zipfile.ZipFile
    elif file_path.suffix in ['.gz', '.bz2', '.tar']:
        open_archive = tarfile.open
    else:
        raise ValueError("Unsupported archive type")

    temp_dir_path = tempfile.mkdtemp(prefix="cloudpip_")

    with open_archive(file_path, 'r') as archive:
        if isinstance(archive, zipfile.ZipFile):
            archive.extractall(path=temp_dir_path)
        elif isinstance(archive, tarfile.TarFile):
            archive.extractall(path=temp_dir_path)
    
    sys.path.append(temp_dir_path)
    
    return temp_dir_path + "\\" + get_first_dir_name(temp_dir_path)

def cleanup():

    temp_dir = tempfile.gettempdir()

    for dir_name in os.listdir(temp_dir):

        full_path = os.path.join(temp_dir, dir_name)

        if os.path.isdir(full_path) and dir_name.startswith("cloudpip_"):

            shutil.rmtree(full_path)