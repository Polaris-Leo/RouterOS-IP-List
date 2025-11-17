# scripts/generate_rsc.py
import os

DATA_DIR = "data"
OUTPUT_DIR = "output"

ISP_MAP = {
    "cernet": "cernet.txt",
    "cmcc": "cmcc.txt",
    "telecom": "telecom.txt",
    "unicom": "unicom.txt",
    "cn": "all_cn.txt",
    "cn6": "all_cn_ipv6.txt"
}

def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_ros_script(provider_name, input_txt_file, output_rsc_file):
    try:
        with open(input_txt_file, 'r', encoding='utf-8') as f_in:
            ip_list = [line.strip() for line in f_in if line.strip()]

        with open(output_rsc_file, 'w', encoding='utf-8') as f_out:
            f_out.write(f"/ip firewall address-list remove [/ip firewall address-list find list={provider_name}]\n")
            f_out.write("/ip firewall address-list\n")

            for ip in ip_list:
                f_out.write(f"add address={ip} list={provider_name}\n")

        print(f"生成: {output_rsc_file}")

    except FileNotFoundError:
        print(f"找不到文件: {input_txt_file}")

def main():
    ensure_folder(OUTPUT_DIR)

    for isp, file_name in ISP_MAP.items():
        input_path = os.path.join(DATA_DIR, file_name)
        output_path = os.path.join(OUTPUT_DIR, f"chnroutes-{isp}.rsc")
        create_ros_script(isp, input_path, output_path)


if __name__ == "__main__":
    main()
