---
title: 代理 raw.githubusercontent.com
---

## 代理 raw.githubusercontent.com <!-- omit in toc -->

[`#笔记`](https://fangxuetao.com/note) 

*2022/07/21*

https://github.com/fxtaoo/cmd 放了些 shell 脚本，国内拉取时不时 404，为了解决这个问题，我的最终方案海外 vps 使用 caddy 代理请求，为保护 vps 启用了 Cloudflare CDN。

以 [golang 安装最新版本](https://proxy.fxtaoo.dev/raw/fxtaoo/cmd/master/install/golang.sh) shell 脚本为例，地址为 [https://proxy.fxtaoo.dev/raw/fxtaoo/cmd/master/install/golang.sh](https://proxy.fxtaoo.dev/raw/fxtaoo/cmd/master/install/golang.sh)

caddy 配置文件 Caddyfile

```bash
(BASE) {
  encode zstd gzip
  log {
    output discard
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

proxy.fxtaoo.dev {
    import BASE
    tls /etc/caddy/tls/fxtaoo.dev.pem /etc/caddy/tls/fxtaoo.dev.key
    handle_path /raw/* {
        import PATHRP fxtaoo raw.githubusercontent.com
    }
}
```

`proxy.fxtaoo.dev` 代理域名  
`tls` 我使用 Cloudflare 免费提供的源证书（源证书仅对 Cloudflare 与源服务器之间的加密有效）  
`handle_path` 去除匹配的路径前缀，例如我请求 `/raw/fxtaoo/cmd/master/install/golang.sh`，向源请求 `/fxtaoo/cmd/master/install/golang.sh`  
`import PATHRP fxtaoo raw.githubusercontent.com`，`route` 只代理 `fxtaoo`