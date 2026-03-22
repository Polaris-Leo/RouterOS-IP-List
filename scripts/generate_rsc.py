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

# 所有内网/保留IP子网（RFC 1918 及其他不可路由地址段）
PRIVATE_NETWORKS = [
    "0.0.0.0/8",        # "This" Network
    "10.0.0.0/8",       # RFC 1918 私有网络
    "100.64.0.0/10",    # Shared Address Space (CGNAT)
    "127.0.0.0/8",      # 本地回环
    "169.254.0.0/16",   # 链路本地
    "172.16.0.0/12",    # RFC 1918 私有网络
    "192.0.0.0/24",     # IETF 协议保留
    "192.168.0.0/16",   # RFC 1918 私有网络
    "198.18.0.0/15",    # 网络基准测试
    "224.0.0.0/4",      # 组播
    "240.0.0.0/4",      # 保留
    "255.255.255.255/32", # 广播
]

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


def create_novpn_script(output_file, checksum_file):
    """生成 novpn 列表：CN IP + 所有内网/保留地址段"""
    try:
        cn_path = os.path.join(DATA_DIR, "all_cn.txt")
        with open(cn_path, "r", encoding="utf-8") as f:
            raw_lines = f.readlines()

        cn_lines = validate_cidr_list(raw_lines)

        if len(cn_lines) < 1:
            raise Exception("all_cn.txt 内容为空，疑似下载失败。")

        all_lines = cn_lines + PRIVATE_NETWORKS

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("/ip firewall address-list remove [/ip firewall address-list find list=novpn]\n")
            f.write("/ip firewall address-list\n")
            for ip in all_lines:
                f.write(f"add address={ip} list=novpn\n")

        write_checksum(output_file, checksum_file)
        print(f"[OK] 生成 {output_file}")

    except Exception as e:
        print(f"[ERROR] 生成 novpn 失败：{e}")
        raise e


def main():
    ensure_folder(OUTPUT_DIR)
    ensure_folder(CHECKSUM_DIR)

    for isp, fname in ISP_MAP.items():
        input_path = os.path.join(DATA_DIR, fname)
        output_path = os.path.join(OUTPUT_DIR, f"chnroutes-{isp}.rsc")
        checksum_path = os.path.join(CHECKSUM_DIR, f"chnroutes-{isp}.sha256")

        create_ros_script(isp, input_path, output_path, checksum_path)

    # 生成 novpn 列表（CN IP + 内网保留地址）
    create_novpn_script(
        os.path.join(OUTPUT_DIR, "chnroutes-novpn.rsc"),
        os.path.join(CHECKSUM_DIR, "chnroutes-novpn.sha256")
    )

if __name__ == "__main__":
    main()
