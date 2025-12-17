import json
from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class DailyHotTool(Tool):
    """
    Tool for fetching hot topics from DailyHotApi
    Supports multiple data sources: weibo, zhihu, douyin, bilibili, news, tech, gaming, etc.
    """

    # Base URL for DailyHotApi (default)
    BASE_URL = "https://api.hot.imsyy.top"
    DEFAULT_TIMEOUT = 10

    # Available sources
    SOURCES = {
        "weibo": "微博",
        "zhihu": "知乎",
        "douyin": "抖音",
        "bilibili": "哔哩哔哩",
        "36kr": "36氪",
        "baidu": "百度",
        "toutiao": "今日头条",
        "tieba": "百度贴吧",
        "juejin": "稀土掘金",
        "github": "GitHub",
        "hackernews": "Hacker News",
        "v2ex": "V2EX",
        "csdn": "CSDN",
        "sina-news": "新浪新闻",
        "qq-news": "腾讯新闻",
        "netease-news": "网易新闻",
        "sspai": "少数派",
        "ithome": "IT之家",
        "thepaper": "澎湃新闻",
        "genshin": "原神",
        "honkai": "崩坏：星穹铁道",
        "lol": "LOL",
        "ngabbs": "NGA",
        "smzdm": "什么值得买",
        "acfun": "AcFun",
        "douban-movie": "豆瓣电影",
        "douban-group": "豆瓣讨论小组",
        "weread": "微信读书",
        "jianshu": "简书",
        "zhihu-daily": "知乎日报",
        "huxiu": "虎嗅",
        "techcrunch": "TechCrunch",
        "coolapk": "酷安",
        "kuaishou": "快手",
        "emoji": "Emoji排行",
        "earthquake": "地震信息",
        "gameres": "游研社",
        "hellogithub": "HelloGitHub",
    }

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """
        Main invoke method for the tool
        Parameters:
            - source: str, the data source (required)
            - limit: int, number of items to return (default: 30)
            - cache: bool, whether to use cache (default: True)
        """
        try:
            # Get API configuration from provider credentials
            api_base_url = self._get_api_url()
            timeout = self._get_timeout()

            source = tool_parameters.get("source", "").strip()
            limit = int(tool_parameters.get("limit", 30))
            cache = tool_parameters.get("cache", True)

            # Validate source
            if not source:
                yield self.create_json_message(
                    {
                        "error": "Missing required parameter: source",
                        "available_sources": list(self.SOURCES.keys()),
                    }
                )
                return

            if source not in self.SOURCES:
                yield self.create_json_message(
                    {
                        "error": f"Unknown source: {source}",
                        "available_sources": list(self.SOURCES.keys()),
                    }
                )
                return

            # Validate limit
            if limit < 1 or limit > 100:
                limit = 30

            # Fetch data from API
            result = self._fetch_hot_data(source, limit, cache, api_base_url, timeout)

            yield self.create_json_message(result)

        except Exception as e:
            yield self.create_json_message(
                {"error": f"Failed to fetch hot data: {str(e)}"}
            )

    def _get_api_url(self) -> str:
        """
        Get the API URL from provider credentials or use default.

        Returns:
            str: The configured API URL
        """
        try:
            # Access provider credentials if available
            if hasattr(self, "runtime") and self.runtime:
                credentials = self.runtime.credentials
                if credentials and isinstance(credentials, dict):
                    custom_url = credentials.get("daily_hot_url", "").strip()
                    if custom_url:
                        return custom_url
        except Exception:
            pass

        # Return default URL if no custom configuration
        return self.BASE_URL

    def _get_timeout(self) -> int:
        """
        Get the timeout value from provider credentials or use default.

        Returns:
            int: The configured timeout value
        """
        try:
            # Access provider credentials if available
            if hasattr(self, "runtime") and self.runtime:
                credentials = self.runtime.credentials
                if credentials and isinstance(credentials, dict):
                    timeout_val = credentials.get("timeout", "")
                    if timeout_val:
                        try:
                            timeout = int(timeout_val)
                            if 1 <= timeout <= 120:
                                return timeout
                        except (ValueError, TypeError):
                            pass
        except Exception:
            pass

        # Return default timeout if no valid custom configuration
        return self.DEFAULT_TIMEOUT

    def _fetch_hot_data(
        self,
        source: str,
        limit: int = 30,
        cache: bool = True,
        api_base_url: str = None,
        timeout: int = None,
    ) -> dict[str, Any]:
        """
        Fetch hot data from DailyHotApi

        Args:
            source: Data source name (e.g., 'weibo', 'zhihu')
            limit: Number of items to return
            cache: Whether to use cache
            api_base_url: Custom API base URL (if not provided, uses default)
            timeout: Request timeout in seconds

        Returns:
            dict with hot data or error information
        """
        if api_base_url is None:
            api_base_url = self.BASE_URL
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        try:
            # Build query parameters
            params = {
                "limit": limit,
            }
            if not cache:
                params["cache"] = "false"

            # Make API request using the new route format: /{source}
            url = f"{api_base_url.rstrip('/')}/{source}"

            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()

            data = response.json()

            # Process and return data
            if data.get("code") == 200 and data.get("data"):
                return {
                    "source": source,
                    "source_name": self.SOURCES.get(source, source),
                    "total": len(data.get("data", [])),
                    "data": data.get("data", []),
                    "success": True,
                }
            else:
                return {
                    "source": source,
                    "error": "No data returned from API",
                    "success": False,
                }

        except requests.exceptions.Timeout:
            return {"error": "API request timeout", "source": source, "success": False}
        except requests.exceptions.RequestException as e:
            return {
                "error": f"API request failed: {str(e)}",
                "source": source,
                "success": False,
            }
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse API response",
                "source": source,
                "success": False,
            }
