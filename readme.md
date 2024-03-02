# CloudPIP Documentation

## Overview

CloudPIP is a dynamic Python package importer that simplifies the process of using Python packages on the fly. Unlike traditional package managers that require installation, CloudPIP downloads packages to a temporary folder and loads them at runtime. This approach is particularly useful for testing, experimenting with different package versions, or running Python scripts in environments where permanent package installation is not feasible.

## Features

- **Dynamic Loading:** CloudPIP downloads and loads Python packages from PyPI or any other URL without installing them permanently.
- **Temporary Usage:** Packages are downloaded to a temporary directory, which can be cleaned up easily.
- **Ease of Use:** Simplifies experimentation with packages and versions without affecting the system's Python environment.

## Installation

CloudPIP does not require installation. Ensure you have the Python file `cloudpip.py` in your project directory or in a location that's accessible to your Python scripts.

## Usage

### Importing from PyPI

To use a package from PyPI, you only need to import CloudPIP's `download_and_load_package` function, use it to load the desired package, and then use the package as usual.

Example:

```python
from cloudpip import download_and_load_package as cloudimport, cleanup as cloudcleanup

# Load 'requests' package from PyPI
cloudimport("requests")

import requests
print(requests.get("https://pastebin.com/raw/MzcMMpxp").text)

# Optional: Clean up the temporary directories created by CloudPIP
cloudcleanup()
```

### Importing from a CDN or Other URLs

CloudPIP can also load packages from other URLs, such as CDNs. Set `is_pypi` to `False` to load packages directly from the specified URL.

Example:

```python
from cloudpip import download_and_load_package as cloudimport, cleanup as cloudcleanup

# Load a package directly from a URL
cloudimport("https://cdn.auth.ink/u/R48I86.gz", is_pypi=False)
# The URL `https://cdn.auth.ink/u/R48I86.gz` points to my CDN, where the `requests` package can be downloaded.
import some_package
# Use the imported package as needed

# Recommended: Clean up after use
cloudcleanup()
```

## Cleanup

It's recommended to call the `cleanup` function after you're done using dynamically loaded packages. This function removes temporary directories and files created by CloudPIP, freeing up disk space.

```python
from cloudpip import cleanup as cloudcleanup

# After using the packages
cloudcleanup()
```

For issues, suggestions, or contributions, please open an issue in the project's GitHub repository.
