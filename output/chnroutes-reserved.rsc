# ============================================================
# RouterOS 默认保留 IPv4 地址列表
# List Name: reserved
# ============================================================

/ip firewall address-list

# 清理旧版本，保证脚本可重复导入
remove [find where list="reserved" comment="chnroutes-reserved"]

# 当前网络
add list="reserved" address=0.0.0.0/8 \
    comment="chnroutes-reserved"

# RFC1918 私有地址
add list="reserved" address=10.0.0.0/8 \
    comment="chnroutes-reserved"
add list="reserved" address=172.16.0.0/12 \
    comment="chnroutes-reserved"
add list="reserved" address=192.168.0.0/16 \
    comment="chnroutes-reserved"

# RFC6598 运营商级 NAT 地址
add list="reserved" address=100.64.0.0/10 \
    comment="chnroutes-reserved"

# 环回地址
add list="reserved" address=127.0.0.0/8 \
    comment="chnroutes-reserved"

# IPv4 链路本地地址
add list="reserved" address=169.254.0.0/16 \
    comment="chnroutes-reserved"

# IETF 协议分配地址
add list="reserved" address=192.0.0.0/24 \
    comment="chnroutes-reserved"

# 文档及示例地址
add list="reserved" address=192.0.2.0/24 \
    comment="chnroutes-reserved"
add list="reserved" address=198.51.100.0/24 \
    comment="chnroutes-reserved"
add list="reserved" address=203.0.113.0/24 \
    comment="chnroutes-reserved"

# 已弃用的 6to4 Relay Anycast
add list="reserved" address=192.88.99.0/24 \
    comment="chnroutes-reserved"

# 网络设备基准测试地址
add list="reserved" address=198.18.0.0/15 \
    comment="chnroutes-reserved"

# IPv4 组播地址
add list="reserved" address=224.0.0.0/4 \
    comment="chnroutes-reserved"

# 保留用于未来用途
add list="reserved" address=240.0.0.0/4 \
    comment="chnroutes-reserved"
