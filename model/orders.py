from dataclasses import dataclass
from typing import Optional, List


@dataclass
class OrdersRequest:
    bid_requests: Optional[List['BidRequest']] = None


@dataclass
class BidRequest:
    listing_id: Optional[int] = None
    bid_amount: Optional[float] = None
    bid_status: Optional[str] = None


@dataclass
class OrdersList:
    result: Optional[List['OrdersResponse']] = None
    result_count: Optional[int] = None
    total_count: Optional[int] = None


@dataclass
class OrdersResponse:
    order_id: Optional[str] = None
    order_date: Optional[str] = None
    bid_requests: Optional[List['BidRequest']] = None
    order_status: Optional[str] = None
    source: Optional[str] = None
