from typing import Any

import requests
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class DailyHotProvider(ToolProvider):
    """
    Provider for DailyHot tool.
    This provider validates credentials (if any) for the DailyHot API.
    It provides configuration validation and health checks for the DailyHot service.
    """

    BASE_URL = "https://api.hot.imsyy.top"
    DEFAULT_TIMEOUT = 10

    def __init__(self):
        """Initialize the provider with default configuration."""
        super().__init__()
        self.api_base_url = self.BASE_URL
        self.timeout = self.DEFAULT_TIMEOUT

    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        Validate provider credentials and API connectivity.

        The DailyHot API is public and doesn't require authentication,
        but we perform a health check to ensure the service is accessible.

        Args:
            credentials: Dictionary of credentials to validate (may be empty)

        Raises:
            ToolProviderCredentialValidationError: If validation fails
        """
        try:
            # Extract custom configuration if provided, use defaults otherwise
            if credentials:
                api_base_url = str(
                    credentials.get("daily_hot_url", self.BASE_URL)
                ).strip()
                if not api_base_url:
                    api_base_url = self.BASE_URL

                timeout_val = credentials.get("timeout", self.DEFAULT_TIMEOUT)
                try:
                    timeout = int(timeout_val) if timeout_val else self.DEFAULT_TIMEOUT
                except (ValueError, TypeError):
                    timeout = self.DEFAULT_TIMEOUT
            else:
                api_base_url = self.BASE_URL
                timeout = self.DEFAULT_TIMEOUT

            # Validate timeout value
            if timeout < 1 or timeout > 120:
                timeout = self.DEFAULT_TIMEOUT

            # Store validated configuration
            self.api_base_url = api_base_url
            self.timeout = timeout

            # Perform health check on the API endpoint
            self._health_check()
        except ToolProviderCredentialValidationError:
            raise
        except Exception as e:
            raise ToolProviderCredentialValidationError(
                f"Failed to validate DailyHot service: {str(e)}"
            )

    def _health_check(self) -> bool:
        """
        Check if the DailyHot API is accessible.

        Returns:
            bool: True if API is accessible

        Raises:
            Exception: If API is not accessible
        """
        try:
            # Use configured URL or default
            api_url = getattr(self, "api_base_url", self.BASE_URL)
            timeout = getattr(self, "timeout", 10)

            # Remove trailing slash if present for consistent URL building
            api_url = api_url.rstrip("/")

            # Use /all endpoint to check if API is accessible
            # This endpoint returns available routes and doesn't require specific parameters
            endpoint = f"{api_url}/all"

            try:
                response = requests.get(endpoint, timeout=timeout)
                response.raise_for_status()

                # Check if response is valid JSON
                data = response.json()

                # Check for success: code == 200 and has routes
                if isinstance(data, dict) and data.get("code") == 200:
                    # Verify response has expected structure
                    if "routes" in data or "count" in data:
                        return True

                raise Exception(f"Unexpected API response format: {data}")

            except requests.exceptions.Timeout:
                raise Exception("API request timeout - service may be unavailable")
            except requests.exceptions.ConnectionError:
                raise Exception("Cannot connect to DailyHot API service")
            except requests.exceptions.RequestException as e:
                raise Exception(f"API request failed: {str(e)}")

        except Exception as e:
            raise Exception(f"Health check failed: {str(e)}")
