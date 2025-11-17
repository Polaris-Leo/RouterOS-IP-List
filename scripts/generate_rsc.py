import os
import hashlib
import ipaddress

DATA_DIR = "data"
OUTPUT_DIR = "output"
CHECKSUM_DIR = "checksum"

ISP_MAP = {
    "cernet":  "cernet.txt",
    "cmcc":    "cmcc.txt",
    "telecom": "telecom.txt",
    "unicom":  "unicom.txt",
    "cn":      "all_cn.txt",
    "cn6":     "all_cn_ipv6.txt"   # IPv6
}

def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def validate_cidr_list(lines):
    """确保内容全部是合法的 IP/CIDR"""
    valid = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            ipaddress.ip_network(line, strict=False)
            valid.append(line)
        except Exception:
            print(f"[WARN] 非法行已忽略: {line}")
    return valid

def write_checksum(file_path, checksum_path):
    """生成 SHA256 校验值"""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        sha256.update(f.read())
    with open(checksum_path, "w") as f:
        f.write(sha256.hexdigest())

def create_ros_script(provider_name, input_file, output_file, checksum_file):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            raw_lines = f.readlines()

        lines = validate_cidr_list(raw_lines)

        if len(lines) < 1:
            raise Exception(f"{provider_name} 内容为空，疑似下载失败。")

        # ------- 生成 RouterOS 脚本 -------
        with open(output_file, "w", encoding="utf-8") as f:

            # IPv4 vs IPv6
            if provider_name == "cn6":
                f.write(f"/ipv6 firewall address-list remove [/ipv6 firewall address-list find list={provider_name}]\n")
                f.write("/ipv6 firewall address-list\n")
            else:
                f.write(f"/ip firewall address-list remove [/ip firewall address-list find list={provider_name}]\n")
                f.write("/ip firewall address-list\n")

            # 写入 CIDR
            for ip in lines:
                f.write(f"add address={ip} list={provider_name}\n")

        write_checksum(output_file, checksum_file)
        print(f"[OK] 生成 {output_file}")

    except Exception as e:
        print(f"[ERROR] 生成 {provider_name} 失败：{e}")
        raise e


def main():
    ensure_folder(OUTPUT_DIR)
    ensure_folder(CHECKSUM_DIR)

    for isp, fname in ISP_MAP.items():
        input_path = os.path.join(DATA_DIR, fname)
        output_path = os.path.join(OUTPUT_DIR, f"chnroutes-{isp}.rsc")
        checksum_path = os.path.join(CHECKSUM_DIR, f"chnroutes-{isp}.sha256")

        create_ros_script(isp, input_path, output_path, checksum_path)

if __name__ == "__main__":
    main()
