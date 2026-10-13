# 贡献指南 / Contributing

感谢你为 Free APIs 中文精选添砖加瓦！🎉

## 收录标准

- ✅ API 目前**真实可用**（提交前请实际调用验证）
- ✅ 免费：完全免费，或有**对开发者有意义的免费额度**
- ✅ 标注准确：`auth` 字段如实填写 `no`（无需 Key）或 `key`（需注册 Key）
- ❌ 不收需要付费才能用的服务
- ❌ 不收灰色地带或侵犯第三方权益的接口

## 提交格式

在 `apis.json` 的 `apis` 数组中添加：

```json
{
  "name": "API 名称",
  "category": "dev",
  "auth": "no",
  "url": "https://官网或文档地址",
  "example": "https://可直接调用的示例请求（没有则留空字符串）",
  "description": "一句话说明用途和免费额度",
  "note": "可选补充说明（没有则删除此字段）"
}
```

`category` 可选值：`dev` / `data` / `life` / `media` / `text` / `finance` / `ai`

提交后运行 `python build_site.py` 重新生成演示站，一并提交。

## 报告失效

发现接口失效，直接开 Issue 标题格式：`[失效] API名称`，我们会尽快核实下架。
