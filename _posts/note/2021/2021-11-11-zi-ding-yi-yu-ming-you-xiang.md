---
title: 自定义域名邮箱
---

## 自定义域名邮箱 <!-- omit in toc -->

[`#笔记`](https://fangxuetao.com/note)

_2021/11/11_

1. [总结](#总结)
2. [方案一: outlook 个性化电子邮件地址](#方案一-outlook-个性化电子邮件地址)
3. [方案二：iCloud+ 自定电子邮件域名](#方案二icloud-自定电子邮件域名)
4. [方案三：Zoho or Google Workspace](#方案三zoho-or-google-workspace)

自定义域名邮箱，就像 `i@fangxuetao.com` 这样。

首先排除自己搭建邮件服务，可以用，但稳定性我是怀疑的。下面说明几种搭建自定义域名邮箱的方案，以及过程中所遇到的问题。

### 总结

~~最终确定使用 Zoho + gmail 代收此种方案。~~

~~Zoho 有中国版，[好像要提供 xx 材料](http://bv2ex.com/t/326633#:~:text=%E6%B3%A8%E6%84%8F%EF%BC%9A%E5%8F%AA%E6%9C%89%E4%BB%98%E8%B4%B9%E7%94%A8%E6%88%B7%E8%83%BD%E5%A4%9F%E7%BB%91%E5%AE%9A%E8%87%AA%E5%AE%9A%E4%B9%89%E5%9F%9F%E3%80%82%E8%BF%99%E9%A1%B9%E6%9C%8D%E5%8A%A1%E4%B8%8D%E6%8F%90%E4%BE%9B%E7%BB%99%E5%85%8D%E8%B4%B9%E7%94%A8%E6%88%B7%E3%80%82), 我选付费（有免费） Mail Lite 1 USD/month/user，付款支持双币信用卡、PayPal，还有一些细节，可以看 方案三~~

最终的最终选择 iCloud+ 方案，详情见 方案二：iCloud+ 自定电子邮件域名。

### 方案一: outlook 个性化电子邮件地址

如果账户订阅了 Office 365，outlook 设置 高级 个性化电子邮件地址，但仅限 GoDaddy 托管的域名。 

搜索到一篇博客，讲先配置 GoDaddy 域名，再参照生成的 DNS 配置，复刻到其他域名商托管的域名，也是可行的，但是由于我的域名是在 cloudflare 注册，[免费账号不支持更改 NS 服务器,商业计划里的自定义 ns 也只能是在自己的域名下自己搭的 nameserver](https://www.cloudflare.com/zh-cn/registrar-terms/#:~:text=potentially%20valuable%20domains.-,7.2%20nameservers,-Registrant%20agrees%20to)，这种方案我也就没测了。

_2021/11/20_ 更新

测试了 outlook 个性化电子邮件地址，同时给 qq、iCloud、Gmail 发送邮件测试，只有 iCloud 进了垃圾邮箱。[Newsletters spam test by mail-tester.com](https://www.mail-tester.com/) 邮件得分测试 7.2（满分 10），对比 zoho 多了一项 DKIM -1 分。

>Outlook.com 当前不支持域密钥识别邮件 (DKIM) 或基于域的消息身份验证、报告和一致性 (DMARC) -- [在 Microsoft 365 中获取个性化的电子邮件地址](https://support.microsoft.com/zh-cn/office/%E5%9C%A8-microsoft-365-%E4%B8%AD%E8%8E%B7%E5%8F%96%E4%B8%AA%E6%80%A7%E5%8C%96%E7%9A%84%E7%94%B5%E5%AD%90%E9%82%AE%E4%BB%B6%E5%9C%B0%E5%9D%80-75416a58-b225-4c02-8c07-8979403b427b#:~:text=%E5%90%A6%EF%BC%8COutlook.com%20%E5%BD%93%E5%89%8D%E4%B8%8D%E6%94%AF%E6%8C%81%E5%9F%9F%E5%AF%86%E9%92%A5%E8%AF%86%E5%88%AB%E9%82%AE%E4%BB%B6%20(DKIM)%20%E6%88%96%E5%9F%BA%E4%BA%8E%E5%9F%9F%E7%9A%84%E6%B6%88%E6%81%AF%E8%BA%AB%E4%BB%BD%E9%AA%8C%E8%AF%81%E3%80%81%E6%8A%A5%E5%91%8A%E5%92%8C%E4%B8%80%E8%87%B4%E6%80%A7%20(DMARC)%E3%80%82)


### 方案二：iCloud+ 自定电子邮件域名

以我美区 ID 为例，开通最便宜的 0.99 USD/month,可在 iCloud 网页版 账户设置 自定义邮箱域名。并且按照 cloudflare 电子邮件安全配置了 DKIM DMARC。

~~配置好后，我分别给 qq、gamil、iCloud 发送邮件测试，都进了垃圾邮件箱。~~

~~[Newsletters spam test by mail-tester.com](https://www.mail-tester.com/) 邮件得分测试 0.8（满分 10），大失所望，不排除是我配置问题，也可能是刚出不成熟。~~

_2021/11/23_ 更新

iCloud 更新了相关配置，添加 spf 等，按照新配置， 分别给 qq、gamil、iCloud 发送邮件测试，都是正常收件。[Newsletters spam test by mail-tester.com](https://www.mail-tester.com/) 邮件得分测试 9.2（满分 10），厉害厉害。

### 方案三：Zoho or Google Workspace

Google Workspace 最便宜的方案 6 USD/month，排除。

[Zoho](https://www.zoho.com/) 免费方案，最多支持 5 个用户，每个用户邮件发送数量最大为 50，POP、SMTP 功能受限，这意味着只能使用 zoho 官网客户端，或者 web 页面。

我升级到 Mail Lite 1 USD/month/user,邮件数量、附件等等都要提升，就不说具体了，我主要是为了 POP、SMTP 使用 gmial 代收邮件。

Zoho 配置好域名后，再在 gamil 配置好 `查收其他帐号的邮件` `用这个地址发送邮件`,测试向 qq、iCloud、gmail 发送测试邮件，正常收件，都没有进垃圾邮件箱。

[Newsletters spam test by mail-tester.com](https://www.mail-tester.com/) 邮件得分测试 8.2。好奇 gmail 测了下，也是 8.2。
