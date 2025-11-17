# scripts/fetch_ip_lists.py
import requests
import os

DOWNLOAD_LIST = {
    "all_cn.txt":          "https://ispip.clang.cn/all_cn.txt",
    "all_cn_ipv6.txt":     "https://ispip.clang.cn/all_cn_ipv6.txt",
    "cernet.txt":          "https://ispip.clang.cn/cernet.txt",
    "cmcc.txt":            "https://ispip.clang.cn/cmcc.txt",
    "telecom.txt":         "https://ispip.clang.cn/chinatelecom.txt",
    "unicom.txt":          "https://ispip.clang.cn/unicom_cnc.txt"
}

DATA_DIR = "data"

def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_files():
    ensure_folder(DATA_DIR)

    for filename, url in DOWNLOAD_LIST.items():
        filepath = os.path.join(DATA_DIR, filename)
        print(f"Downloading {filename} ...")

        resp = requests.get(url, timeout=30)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(resp.text)

        print(f"Saved: {filepath}")

if __name__ == "__main__":
    download_files()
