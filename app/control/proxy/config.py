"""Proxy clearance config helpers shared by control and dataplane code."""

from dataclasses import dataclass
from typing import Any

from app.platform.config.snapshot import get_config


@dataclass(frozen=True)
class ClearanceConfig:
    cf_cookies: str = ""
    user_agent: str = ""
    cf_clearance: str = ""
    browser: str = ""


@dataclass(frozen=True)
class EgressConfig:
    mode: str = "direct"
    proxy_url: str = ""
    resource_proxy_url: str = ""
    proxy_pool: list[str] | None = None
    resource_proxy_pool: list[str] | None = None
    skip_ssl_verify: bool = False


def _cfg_str(cfg: Any, key: str) -> str:
    value = cfg.get_str(key, "")
    return value if value.strip() else ""


def first_config_str(cfg: Any, *keys: str) -> str:
    for key in keys:
        value = _cfg_str(cfg, key)
        if value:
            return value
    return ""


def resolve_clearance_config(cfg: Any | None = None) -> ClearanceConfig:
    cfg = cfg or get_config()
    return ClearanceConfig(
        cf_cookies=first_config_str(
            cfg,
            "proxy.cf_cookies",
            "proxy.clearance.cf_cookies",
        ),
        user_agent=first_config_str(
            cfg,
            "proxy.user_agent",
            "proxy.clearance.user_agent",
        ),
        cf_clearance=first_config_str(
            cfg,
            "proxy.cf_clearance",
            "proxy.clearance.cf_clearance",
        ),
        browser=first_config_str(
            cfg,
            "proxy.browser",
            "proxy.clearance.browser",
        ),
    )


def resolve_egress_config(cfg: Any | None = None) -> EgressConfig:
    cfg = cfg or get_config()
    mode = cfg.get_str("proxy.egress.mode", "direct").strip().lower() or "direct"
    proxy_url = first_config_str(cfg, "proxy.egress.proxy_url", "proxy.base_proxy_url")
    resource_proxy_url = first_config_str(
        cfg, "proxy.egress.resource_proxy_url", "proxy.asset_proxy_url"
    )
    proxy_pool = cfg.get_list("proxy.egress.proxy_pool", [])
    resource_proxy_pool = cfg.get_list("proxy.egress.resource_proxy_pool", [])

    if mode == "direct" and (proxy_url or proxy_pool or cfg.get_bool("proxy.enabled", False)):
        if proxy_pool:
            mode = "proxy_pool"
        elif proxy_url:
            mode = "single_proxy"

    return EgressConfig(
        mode=mode,
        proxy_url=proxy_url,
        resource_proxy_url=resource_proxy_url,
        proxy_pool=proxy_pool,
        resource_proxy_pool=resource_proxy_pool,
        skip_ssl_verify=cfg.get_bool(
            "proxy.egress.skip_ssl_verify",
            cfg.get_bool("proxy.skip_proxy_ssl_verify", False),
        ),
    )


__all__ = [
    "ClearanceConfig",
    "EgressConfig",
    "first_config_str",
    "resolve_clearance_config",
    "resolve_egress_config",
]
