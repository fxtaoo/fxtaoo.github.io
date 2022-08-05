---
title: GitHub Actions 定期自动构建最新自定义插件 Caddy 版本
---

## GitHub Actions 定期自动构建最新自定义插件 Caddy 版本 <!-- omit in toc -->

1. [第一步，构建镜像](#第一步构建镜像)
2. [第二步，获取 Dockerfile 资源最新版本信息](#第二步获取-dockerfile-资源最新版本信息)
3. [使用 GitHub Actions 自动构建](#使用-github-actions-自动构建)
4. [优化](#优化)

[`#笔记`](https://fangxuetao.com/note) 

*2022/08/06*

介绍见实例 [fxtaoo/caddy](https://github.com/fxtaoo/caddy) 

说说我的想法、遇到的问题，解决方案，建议对照文件看。

### 第一步，构建镜像

要定时自动构建最新版本，[Dockerfile](https://github.com/fxtaoo/caddy/blob/master/Dockerfile) 资源版本信息便不可明文写死，`build` `--build-args` 配合 Dockerfile `ARG`，外部变量可覆盖 Dockerfile 内变量。  
注意 `ARG` 指令有生效范围，如果在 FROM 指令之前指定，那么只能用于 FROM 指令中。

### 第二步，获取 Dockerfile 资源最新版本信息

打包自定义插件 caddy，使用工具 [xcaddy - Custom Caddy Builder](https://github.com/caddyserver/xcaddy) ，GitHub 返回最近 releases 使用如下：

```bash
# XCADDY_VERSION
curl --silent "https://api.github.com/repos/caddyserver/xcaddy/releases/latest" | jq -r .tag_name | sed 's/^v//'
# CADDY_VERSION
curl --silent "https://api.github.com/repos/caddyserver/caddy/releases/latest" | jq -r .tag_name

# 打包命令
docker build --build-arg XCADDY_VERSION=$(curl --silent "https://api.github.com/repos/caddyserver/xcaddy/releases/latest" | jq -r .tag_name | sed 's/^v//') --build-arg CADDY_VERSION=$(curl --silent "https://api.github.com/repos/caddyserver/caddy/releases/latest" | jq -r .tag_name) .
```

到这里，通过 Dockerfile 可以打包最新版本。

### 使用 GitHub Actions 自动构建

结合 [workflows](https://github.com/fxtaoo/caddy/blob/master/.github/workflows/docker-image.yml) 文件看，这里我提下关键点。

```yml
# GitHub Actions 构建时将参数传递至 Dockerfile
      build-args: |
            XCADDY_VERSION=${{ env.XCADDY_VERSION }}
            CADDY_VERSION=${{ env.CADDY_VERSION }}

# 将 CADDY_VERSION 等参数写至 env
 - name: Set env CADDY_VERSION
        run: echo "CADDY_VERSION=$(curl --silent "https://api.github.com/repos/caddyserver/caddy/releases/latest" | jq -r .tag_name)" >> $GITHUB_ENV

# push 与每月定期执行
on:
  push:
    branches: [master]
  pull_request:
    branches: [master]
  schedule:
    - cron: "0 0 1 * *"
```

到这里核心需求，定期自动构建最新已经实现。

### 优化

```yml
# 比较 github caddy 与 docker hub 镜像版本，如果一致，便不执行构建打包动作
    - name: Set env DOCKER_HUB_CADDY_VERSION
        run: echo "DOCKER_HUB_CADDY_VERSION=$(curl --silent https://registry.hub.docker.com/v2/repositories/fxtaoo/caddy/tags | jq -r '.results | .[1] | .name')" >> $GITHUB_ENV
# 从 docker hub 获取的镜像最后版本

if: ${{ env.CADDY_TAG != env.DOCKER_HUB_CADDY_VERSION }}
#  后续操作，只有不一致才执行
# 起先是第一条使用 != 比较，后续使用 ${{ success() }}，不知为何第一条没有执行，后续仍然执行，后面找时间系统学习 GitHub Actions 再研究这个问题。
```






