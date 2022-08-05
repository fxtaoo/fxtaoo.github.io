---
title: 越过长城，走向世界。
---

## 越过长城，走向世界！<!-- omit in toc -->

[`#笔记`](https://fangxuetao.com/note) 

*2021/11/23*

1. [服务器](#服务器)
2. [域名](#域名)
3. [服务端](#服务端)
   1. [安装 docker 相关](#安装-docker-相关)
   2. [shadowsocks-rust](#shadowsocks-rust)
      1. [haproxy 代理](#haproxy-代理)
   3. [VLESS-GRPC](#vless-grpc)
      1. [使用 cloudflare CDN](#使用-cloudflare-cdn)
4. [客户端](#客户端)
5. [最后](#最后)

>Across the Great Wall we can reach every corner in the world.（越过长城，走向世界）

简单的说一下自己目前的翻墙方案以及使用的相关工具。  

### 服务器

```bash
echo "hello shell"
echo "hello python"
```
  
```bash
echo "hello shell"
echo "hello python"
```

首先要有一台不受长城防火墙管制的服务器，我使用的是搬瓦工的 [CN2 GIA-E 限量版](https://stock.bwg.net/) 日本机房，测试请看 [搬瓦工 DC6 CN2 GIA-ECOMMERCE 演示站点](https://dc6.bwg.net/) 这里就不多做赘述。

### 域名
可有可无的一个域名。没有域名直接用 ip 也行，但有域名在配置变更 ip 后，只需要配置一次 dns 指向即可，直接用 ip 则需要在每一个客户端更改 ip。还有在一些如 xray 等一些方案中，流量伪装需要一个域名。  
我的域名注册、托管在 cloudflare。这里打一波自来水广告，cloudflare 域名注册续费无促销打折活动的日常情况下，最便宜。具体请看 [Cloudflare注册商介绍：你可能会喜欢的域名注册](https://blog.cloudflare.com/zh-cn/cloudflare-registrar-zh-cn/)。

### 服务端

#### 安装 docker 相关

debian 11 docker 安装脚本

```bash
# 需要 sudo 权限
bash -c "$(wget -O- https://raw.fxtaoo.dev/fxtaoo/cmd/main/install/debian-docker.sh)"

# docker ps 使用该命令 docker 是否可用
```

安装 docker-compose


```bash
sudo apt install -y python3-pip

pip docker-compose

# 检查是否可用
docker-compose version
```


#### [shadowsocks-rust](https://github.com/shadowsocks/shadowsocks-rust)


安装 shadowsocks-rust

新建一个文件夹，该文件夹下新建 `docker-compose.yml` 文件，该文件如下：

```yml
version: '3'
services:
  ss-rust:
    image: ghcr.io/shadowsocks/ssserver-rust:latest
    container_name: ss-rust
    restart: always
    ports:
      - prot:prot
      - prot:prot/udp
    volumes:
      - ./ssserver-rust.json:/etc/shadowsocks-rust/config.json:ro
```

该文件夹下新建文件 `ssserver-rust.json`，该文件如下：


```json
{
  "server": "0.0.0.0",
  "server_port": prot,
  "password": "密码",
  "mode": "tcp_and_udp",
  "method": "chacha20-ietf-poly1305",
  "udp_timeout": 60,
  "dns": "google",
  "no_delay": true,
  "keep_alive": 15,
  "nofile": 10240
}
```

在该文件夹下执行命令：


```bash
# 启动
docker-compose up -d

# 检查是否运行
docker ps

# 检查服务是否正常
# 可在自己电脑端 cmd 或终端，检查端口
telnet ip|域名 9527
```

##### haproxy 代理

*2021/3/29*

腾讯云活动，入手了一台。尝试配置 tcp、grpc 代理。

tcp 代理如下：

```cfg
global
    daemon
    maxconn 256

defaults
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend ss-in
    mode tcp
    bind *:port
    default_backend ss-out

backend ss-out
    server s1 f2.fxtaoo.dev:port maxconn 32
```

docker-compose.yml  

```yml
  haproxy:
    image: haproxy
    container_name: haproxy
    restart: always
    ports:
      - "prot:prot"
    volumes:
      - ./haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro
```

grpc 尝试了下，没用成功，没深入研究。

#### VLESS-GRPC

这种方案需要域名

[VLESS-GRPC README.md](https://github.com/XTLS/Xray-examples/tree/main/VLESS-GRPC)

参考 shadowsocks-rust 部分，这里只贴上配置部分。

`docker-compose.yml` docker 服务配置


```yml
version: '3'
  caddy:
    image: caddy:alpine
    container_name: caddy
    restart: always
    ports:
      - 443:443
      - 80:80
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - /data/caddy:/data
      - ./www:/var/www:ro

  xray:
    image: teddysun/xray
    container_name: xray
    restart: always
    volumes:
      - ./xray-server.json:/etc/xray/config.json:ro
```

`Caddyfile` caddy 前端代理配置


```bash
xxx.com {
    @grpc {
        protocol grpc
        path /path/*
    }
    reverse_proxy @grpc h2c://xray:prot
    root * /var/www
    file_server
}
```

`xray-server.json` xray 服务配置

```json
{
  "log": {
    "loglevel": "warning"
  },
  "inbounds": [
    {
      "port": prot,
      "protocol": "vless",
      "settings": {
        "clients": [
          {
            "id": "xx-xx-xx-xx-xx"
          }
        ],
        "decryption": "none"
      },
      "streamSettings": {
        "network": "grpc",
        "grpcSettings": {
          "serviceName": "path",
          "multiMode": true
        }
      }
    }
  ],
  "outbounds": [
    {
      "tag": "direct",
      "protocol": "freedom",
      "settings": {}
    },
    {
      "tag": "blocked",
      "protocol": "blackhole",
      "settings": {}
    }
  ],
  "routing": {
    "domainStrategy": "AsIs",
    "rules": [
      {
        "type": "field",
        "ip": [
          "geoip:private"
        ],
        "outboundTag": "blocked"
      }
    ]
  }
}
```


PC 客户端我使用 [v2rayN](https://github.com/2dust/v2rayN)

![fangxuetao.com-2021-11-23-zi-ding-yi-yu-ming-you-xiang-0.webp](/assets/images/note/2021-11-23-yue-guo-chang-cheng-zou-xiang-shi-jie/fangxuetao.com-2021-11-23-zi-ding-yi-yu-ming-you-xiang-0.webp)


##### 使用 cloudflare CDN
*2022/12/16*   
我的方案是配置一个 A 记录，不开启代理日常使用。    
再配置一个 CNAME 到上面配置的 A 记录，并开启代理。  
使用 cloudflare CDN 速度远慢于不使用，不过白嫖还要啥自行车呢？我只有在严重不稳定时才切换到 cloudflare CDN 线路。  

### 客户端

移动端我使用 `Shadowrocket` 俗称 `小火箭`，ios 端国区以下架，可在淘宝购买临时账号，在 App store 登录下载。此种方法缺点是购买账号随时可能失效，无法保证长期更新。  
长期方案美区 ID 账号，应用购买付款可使用双币信用卡购买礼物卡充值，或者绑定 PayPal 绑定双币信用卡付款。  
PC 端我使用 [shadowsocks-windows](https://github.com/shadowsocks/shadowsocks-windows) 配合 chrome 插件 [SwitchyOmega](https://chrome.google.com/webstore/detail/proxy-switchyomega/padekgcemlokbadohgkifijomclgjgif?hl=zh-CN) 使用。

### 最后

墙高一尺，梯高一杖。后续要换了新方案，会更新维护这篇文章。祝大家能够畅游互联网。




