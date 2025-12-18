# Daily Hot

一个 Dify 工具插件，集成 [DailyHotApi](https://github.com/imsyy/DailyHotApi) 接口，支持从 40+ 个数据源获取热门话题和热点内容，包括社交媒体、新闻、科技平台、游戏和社区。

## 功能特性

- ✨ **多源支持**: 40+ 个热点数据源
- 📊 **灵活参数**: 自由选择数据源、控制结果数量、开关缓存
- 🚀 **易于集成**: 与 Dify 工作流无缝融合
- ⚡ **智能缓存**: 可配置缓存，性能优化
- 🌍 **无需认证**: 使用公开的 DailyHotApi 接口

## 快速开始

### 安装

1. 安装依赖:

```bash
pip install -r requirements.txt
```

2. 添加到 Dify:
   - 将插件放入 Dify 插件目录
   - 无需配置凭证

### 基础用法

在 Dify 工作流中使用:

```yaml
工具: Daily Hot
参数:
  source: "weibo"        # 数据源名称
  limit: 30              # 返回结果数 (1-100, 默认: 30)
  cache: true            # 是否使用缓存 (默认: true)
```

## 支持的数据源

| 分类 | 数据源 |
|------|--------|
| **社交媒体** | weibo, zhihu, douyin, bilibili, xiaohongshu |
| **新闻资讯** | sina-news, qq-news, netease-news, toutiao, 36kr, thepaper |
| **科技** | github, hackernews, csdn, juejin, v2ex |
| **游戏** | genshin, honkai, lol, gameres |
| **社区** | ngabbs, tieba, acfun, douban-movie, douban-group |
| **购物** | smzdm, coolapk, kuaishou |
| **其他** | baidu, sspai, ithome, weread, jianshu, zhihu-daily, huxiu, hellogithub |

## API 响应格式

```json
{
  "source": "weibo",
  "source_name": "微博",
  "total": 30,
  "data": [
    {
      "id": "unique_id",
      "title": "热门话题",
      "hot": 1000,
      "timestamp": 1702790400000,
      "url": "https://..."
    }
  ],
  "success": true
}
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `source` | string | - | **必需**. 数据源名称 |
| `limit` | number | 30 | 返回结果数量 (1-100) |
| `cache` | boolean | true | 是否使用缓存数据 |

## 常见问题

| 问题 | 解决方案 |
|------|--------|
| API 超时 | DailyHotApi 可能负载过高，请稍后重试 |
| 无数据返回 | 尝试其他数据源，某些源可能暂时无数据 |
| 数据过旧 | 设置 `cache=false` 强制获取最新数据 |
| 请求频率限制 | 多次请求时添加延迟间隔 |

## 文档

详细的 API 文档请访问 [DailyHotApi GitHub](https://github.com/imsyy/DailyHotApi)。

## 相关链接

- [DailyHotApi 项目](https://github.com/imsyy/DailyHotApi)
- [DailyHot 网页版](https://hot.imsyy.top/)
- [Dify 文档](https://docs.dify.ai/)
- [隐私政策](../PRIVACY.md)
