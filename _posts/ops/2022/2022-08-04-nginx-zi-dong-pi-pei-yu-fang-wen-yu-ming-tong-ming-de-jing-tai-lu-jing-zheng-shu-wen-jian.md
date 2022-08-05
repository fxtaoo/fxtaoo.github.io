---
title: nginx 自动匹配与访问域名同名的静态路径、证书文件
---

## nginx 自动匹配与访问域名同名的静态路径、证书文件 <!-- omit in toc -->

[`#Ops`](https://fangxuetao.com/ops) 

*2022/08/04*

工作上遇到一个需求，一台机器上将要有许多页面站点，做备案用。  
域名不一样，也没有域名管理权限。  
最原始的办法，新添一个站点，nginx 加一个 server 配置。  
我就想，能不能访问 `a.com` 就资源路径自动到 `/data/a.com`，证书也是自动选择 `/data/a.com/a.com.crt`。  
这样新添一个站点，只需要把相关静态资源放置 `/data/域名` 即可。

最终实现这个需求，自动匹配与访问域名同名的静态路径、证书文件。  
这种实现对性能有影响，不过这些站点几乎无访问量，也就无所谓了。

nginx 配置如下
{% capture details %}

```bash
user  nginx;
worker_processes  auto;

# error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include mime.types;

    server{
        listen 80;
        server_name ~^(www\.)?(?<domain>.+)$;

        location / {
            root /data/$domain;
        }
    }

    map $ssl_server_name $cert {
        default $ssl_server_name;
        ~*www.(.*) $1;
    }

    server{
        listen 443 ssl;
        server_name ~^(www\.)?(?<domain>.+)$;

        ssl_certificate     /data/$cert/$cert.crt;
        ssl_certificate_key /data/$cert/$cert.key;

        location / {
            root /data/$domain;
        }
    }
    access_log /dev/null;
    error_log /dev/null;
}
```
{% endcapture %}
{% capture summary %}nginx.conf{% endcapture %}{% include details.html %}
