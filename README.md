# Daily Hot

A Dify tool plugin that integrates the [DailyHotApi](https://github.com/imsyy/DailyHotApi) interface, supporting retrieval of trending topics and hot content from 40+ data sources including social media, news, tech platforms, games, and communities.

## Features

- ✨ **Multi-Source Support**: 40+ trending data sources
- 📊 **Flexible Parameters**: Freely choose data sources, control result quantity, enable/disable caching
- 🚀 **Easy Integration**: Seamlessly integrates with Dify workflows
- ⚡ **Smart Caching**: Configurable caching for performance optimization
- 🌍 **No Authentication Required**: Uses public DailyHotApi interface

## Quick Start

### Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Add to Dify:
   - Place the plugin in Dify's plugin directory
   - No credential configuration needed

### Basic Usage

Use in Dify workflows:

```yaml
Tool: Daily Hot
Parameters:
  source: "weibo"        # Data source name
  limit: 30              # Number of results (1-100, default: 30)
  cache: true            # Use cache (default: true)
```

## Supported Data Sources

| Category | Sources |
|----------|---------|
| **Social Media** | weibo, zhihu, douyin, bilibili, xiaohongshu |
| **News** | sina-news, qq-news, netease-news, toutiao, 36kr, thepaper |
| **Tech** | github, hackernews, csdn, juejin, v2ex |
| **Games** | genshin, honkai, lol, gameres |
| **Community** | ngabbs, tieba, acfun, douban-movie, douban-group |
| **Shopping** | smzdm, coolapk, kuaishou |
| **Others** | baidu, sspai, ithome, weread, jianshu, zhihu-daily, huxiu, hellogithub |

## API Response Format

```json
{
  "source": "weibo",
  "source_name": "Weibo",
  "total": 30,
  "data": [
    {
      "id": "unique_id",
      "title": "Trending Topic",
      "hot": 1000,
      "timestamp": 1702790400000,
      "url": "https://..."
    }
  ],
  "success": true
}
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `source` | string | - | **Required**. Data source name |
| `limit` | number | 30 | Number of results to return (1-100) |
| `cache` | boolean | true | Use cached data |

## FAQ

| Question | Solution |
|----------|----------|
| API Timeout | DailyHotApi might be under heavy load, please retry later |
| No Data Returned | Try other data sources, some may be temporarily unavailable |
| Stale Data | Set `cache=false` to force fetch fresh data |
| Rate Limiting | Add delays between multiple requests |

## Documentation

For detailed API documentation, visit [DailyHotApi GitHub](https://github.com/imsyy/DailyHotApi).

## Related Links

- [DailyHotApi Project](https://github.com/imsyy/DailyHotApi)
- [DailyHot Web Version](https://hot.imsyy.top/)
- [Dify Documentation](https://docs.dify.ai/)
- [Privacy Policy](PRIVACY.md)
