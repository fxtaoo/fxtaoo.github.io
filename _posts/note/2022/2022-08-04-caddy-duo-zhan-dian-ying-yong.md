---
title: caddy 多站点应用
---

## caddy 多站点应用 <!-- omit in toc -->

[`#笔记`](https://fangxuetao.com/note) 

*2022/08/04*

列下我的搬瓦工机器 caddy 上的站点：  
+ [方学涛](https://fangxuetao.com/)，这个是我的博客，一个 [jekyll github-pages](https://github.com/fxtaoo/fxtaoo.github.io)，caddy 作用 fangxuetao.com 代理到 fxtaoo.github.io。  
+ proxy.fxtaoo.dev 一些代理，通过路径区分代理 raw.githubusercontent.com、git.githubusercontent.com等，参数 `route` 做一些限制，例如代理 raw 只允许 raw.githubusercontent.com/fxtaoo/。  
+ 配合 VLESS-GRPC 使用，caddy 通过 path 前置分流。

说说遇到的一些问题。  

站点使用 CDN，访问不到真实 IP，caddy 无法自动生成证书。  
最初的我的解决方法是，使用了 cloudflare CDN 的二级域名站点，手动配置 cloudflare 提供的源证书，caddy 一个二级域名使用了通配符证书，其他的二级域名就不再自动申请，这种情况需要添加参数 `auto_https ignore_loaded_certs` 即使存在通配符证书，也自动申请证书。  
后面了解到 caddy 有个非官方模块 [Cloudflare module for Caddy](https://github.com/caddy-dns/cloudflare),可以通过 DNS 与验证域名归属。这个是非官方模块，于是我自己手动打包了一个。  
[fxtaoo/caddy](https://hub.docker.com/r/fxtaoo/caddy) ， github actions 自动打包推送到 docker hub，尝试使用了一下，很不错。

打包有个印象深刻的点，更改可执行文件的权限，docker 新建一层，镜像大小直接翻了一倍！  

![fangxuetao.com-2022-08-04-caddy-duo-zhan-dian-ying-yong-0.webp](/assets/images/note/2022-08-04-caddy-duo-zhan-dian-ying-yong/fangxuetao.com-2022-08-04-caddy-duo-zhan-dian-ying-yong-0.webp)

正确的做法是 `COPY --chmod=0755 --from=0 /tmp/xcaddy/caddy /usr/bin/caddy` 复制时便配置好权限。
  
![fangxuetao.com-2022-08-04-caddy-duo-zhan-dian-ying-yong-1.webp](/assets/images/note/2022-08-04-caddy-duo-zhan-dian-ying-yong/fangxuetao.com-2022-08-04-caddy-duo-zhan-dian-ying-yong-1.webp)

最后贴上 caddy 的配置

{% capture details %}
```bash
{
 log {
    output discard
  }
}

(BASE) {
  encode zstd gzip
  tls {
    dns cloudflare xxxxx
    resolvers 1.0.0.1
  }
}

(RP) {
  reverse_proxy https://{args.0} {
      header_up Host {args.0}
      header_down Access-Control-Allow-Origin *
      header_down Access-Control-Allow-Methods *
      header_down Access-Control-Allow-Headers *
    }
}

(PATHRP) {
  route /{args.0}/* {
    import RP {args.1}
  }
}

fangxuetao.com {
    import BASE
    import RP fxtaoo.github.io
}

proxy.fxtaoo.dev {
    import BASE
    handle_path /raw/* {
        import PATHRP fxtaoo raw.githubusercontent.com
    }
    handle_path /git/* {
        import PATHRP fxtaoo git.githubusercontent.com
    }
    handle_path /go/* {
        route /VERSION{"m":["text"]} {
        import RP go.dev
      }
    }
}

f2.fxtaoo.dev {
    import BASE
    @grpc {
        protocol grpc
        path /f2/*
    }
    reverse_proxy @grpc h2c://127.0.0.1:34573
    root * /var/www
    file_server
}
```
{% endcapture %}
{% capture summary %}Caddyfile{% endcapture %}{% include details.html %}