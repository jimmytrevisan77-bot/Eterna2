"""Commerce integration scaffolding for Shopify, Printify and Etsy."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

try:  # pragma: no cover - optional dependency
    import shopify
except ImportError:  # pragma: no cover
    shopify = None  # type: ignore

try:  # pragma: no cover - optional dependency
    import printify
except ImportError:  # pragma: no cover
    printify = None  # type: ignore

try:  # pragma: no cover - optional dependency
    from etsyv3 import EtsyV3
except ImportError:  # pragma: no cover
    EtsyV3 = None  # type: ignore


@dataclass
class CommerceStatus:
    shopify_connected: bool
    printify_connected: bool
    etsy_connected: bool


class CommerceManager:
    """Coordinate product publishing across partner platforms."""

    def __init__(self, config: Optional[Dict[str, str]] = None) -> None:
        self.config = config or {}
        self.shopify_session = None
        self.printify_client = None
        self.etsy_client = None
        self._bootstrap_clients()

    def _bootstrap_clients(self) -> None:
        if shopify is not None and {"SHOPIFY_API_KEY", "SHOPIFY_PASSWORD", "SHOPIFY_SHOP_NAME"} <= self.config.keys():
            shop_url = f"https://{self.config['SHOPIFY_API_KEY']}:{self.config['SHOPIFY_PASSWORD']}@{self.config['SHOPIFY_SHOP_NAME']}.myshopify.com/admin"
            shopify.ShopifyResource.set_site(shop_url)
            self.shopify_session = shopify

        if printify is not None and "PRINTIFY_API_TOKEN" in self.config:
            self.printify_client = printify.Client(self.config["PRINTIFY_API_TOKEN"])

        if EtsyV3 is not None and {"ETSY_API_KEY", "ETSY_SHOP_ID"} <= self.config.keys():
            self.etsy_client = EtsyV3(api_key=self.config["ETSY_API_KEY"])

    def status(self) -> CommerceStatus:
        return CommerceStatus(
            shopify_connected=self.shopify_session is not None,
            printify_connected=self.printify_client is not None,
            etsy_connected=self.etsy_client is not None,
        )

    def publish_listing(self, payload: Dict[str, str]) -> bool:
        """Publish a product across all configured stores."""

        success = True
        if self.shopify_session is not None:
            try:  # pragma: no cover - requires credentials
                product = shopify.Product()
                product.title = payload.get("title")
                product.body_html = payload.get("description")
                success &= bool(product.save())
            except Exception:
                success = False

        if self.printify_client is not None:
            try:
                self.printify_client.blueprints.list()
            except Exception:
                success = False

        if self.etsy_client is not None:
            try:
                self.etsy_client.listings.getListingsByShop(shop_id=self.config.get("ETSY_SHOP_ID"))
            except Exception:
                success = False

        return success


__all__ = ["CommerceManager", "CommerceStatus"]
