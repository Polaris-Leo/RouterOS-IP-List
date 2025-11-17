# scripts/fetch_ip_lists.py
import requests
import os

DOWNLOAD_LIST = {
    "all_cn.txt": "https://ispip.clang.cn/all_cn.txt",
    "all_cn_ipv6.txt": "https://ispip.clang.cn/all_cn_ipv6.html",
    "cernet.txt": "https://ispip.clang.cn/cernet.txt",
    "cmcc.txt": "https://ispip.clang.cn/cmcc.txt",
    "telecom.txt": "https://ispip.clang.cn/chinatelecom.txt",
    "unicom.txt": "https://ispip.clang.cn/unicom_cnc.txt"
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
        resp.encoding = resp.apparent_encoding

        # IPv6 页面里有 HTML，需要过滤出纯 IPv6 CIDR
        if filename == "all_cn_ipv6.txt":
            lines = []
            for line in resp.text.splitlines():
                line = line.strip()
                if ":" in line and "/" in line:
                    lines.append(line)
            resp_text = "\n".join(lines)
        else:
            resp_text = resp.text

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(resp_text)

        print(f"Saved: {filepath}")


if __name__ == "__main__":
    download_files()
