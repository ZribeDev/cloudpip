from cloudpip import download_and_load_package as cloudimport, cleanup as cloudcleanup
cloudimport("requests") # Importing Requests via PyPi

import requests
print(requests.get("https://pastebin.com/raw/MzcMMpxp").text)

# cloudcleanup() is used to delete temporary folders and libraries created by CloudPIP, freeing up storage. (Recommended)
cloudcleanup()