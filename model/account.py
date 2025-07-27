from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class Account:
    available_cash_balance: Optional[float] = None
    pending_investments_primary_market: Optional[float] = None
    pending_investments_secondary_market: Optional[float] = None
    pending_quick_invest_orders: Optional[float] = None
    total_principal_received_on_active_notes: Optional[float] = None
    total_amount_invested_on_active_notes: Optional[float] = None
    outstanding_principal_on_active_notes: Optional[float] = None
    total_account_value: Optional[float] = None
    pending_deposit: Optional[float] = None
    external_user_id: Optional[str] = None
    prosper_account_digest: Optional[str] = None
    invested_notes: Optional[Dict[str, float]] = None
    pending_bids: Optional[Dict[str, float]] = None
