from dataclasses import dataclass
from typing import List
from typing import Optional


@dataclass
class Listings:
    result: List['Listing']
    result_count: int
    total_count: int


@dataclass
class Listing:
    credit_bureau_values_transunion_indexed: Optional['CreditBureauValues'] = None
    listing_start_date: Optional[str] = None
    listing_status: Optional[int] = None
    listing_status_reason: Optional[str] = None
    verification_stage: Optional[int] = None
    listing_amount: Optional[float] = None
    amount_funded: Optional[float] = None
    amount_remaining: Optional[float] = None
    percent_funded: Optional[float] = None
    partial_funding_indicator: Optional[bool] = None
    funding_threshold: Optional[float] = None
    prosper_rating: Optional[str] = None
    lender_yield: Optional[float] = None
    borrower_rate: Optional[float] = None
    borrower_apr: Optional[float] = None
    listing_term: Optional[int] = None
    listing_monthly_payment: Optional[float] = None
    prosper_score: Optional[int] = None
    listing_category_id: Optional[int] = None
    listing_title: Optional[str] = None
    income_range: Optional[int] = None
    income_range_description: Optional[str] = None
    stated_monthly_income: Optional[float] = None
    income_verifiable: Optional[bool] = None
    dti_wprosper_loan: Optional[float] = None
    employment_status_description: Optional[str] = None
    occupation: Optional[str] = None
    borrower_state: Optional[str] = None
    prior_prosper_loans_active: Optional[int] = None
    prior_prosper_loans: Optional[int] = None
    prior_prosper_loans_principal_borrowed: Optional[float] = None
    prior_prosper_loans_principal_outstanding: Optional[float] = None
    prior_prosper_loans_balance_outstanding: Optional[float] = None
    prior_prosper_loans_cycles_billed: Optional[int] = None
    prior_prosper_loans_ontime_payments: Optional[int] = None
    prior_prosper_loans_late_cycles: Optional[int] = None
    prior_prosper_loans_late_payments_one_month_plus: Optional[int] = None
    max_prior_prosper_loan: Optional[float] = None
    min_prior_prosper_loan: Optional[float] = None
    prior_prosper_loan_earliest_pay_off: Optional[int] = None
    lender_indicator: Optional[int] = None
    channel_code: Optional[str] = None
    amount_participation: Optional[float] = None
    investment_typeid: Optional[int] = None
    investment_type_description: Optional[str] = None
    last_updated_date: Optional[str] = None
    invested: Optional[bool] = None
    biddable: Optional[bool] = None
    has_mortgage: Optional[bool] = None
    historical_return: Optional[float] = None
    historical_return_10th_pctl: Optional[float] = None
    historical_return_90th_pctl: Optional[float] = None
    estimated_monthly_housing_expense: Optional[float] = None
    co_borrower_application: Optional[bool] = None
    months_employed: Optional[float] = None
    listing_number: Optional[int] = None
    investment_product_id: Optional[int] = None
    decision_bureau: Optional[str] = None
    member_key: Optional[str] = None
    listing_creation_date: Optional[str] = None


@dataclass
class CreditBureauValues:
    credit_report_date: Optional[str] = None
    at02s_open_accounts: Optional[float] = None
    g041s_accounts_30_or_more_days_past_due_ever: Optional[float] = None
    g093s_number_of_public_records: Optional[float] = None
    g094s_number_of_public_record_bankruptcies: Optional[float] = None
    g095s_months_since_most_recent_public_record: Optional[float] = None
    g218b_number_of_delinquent_accounts: Optional[float] = None
    g980s_inquiries_in_the_last_6_months: Optional[float] = None
    re20s_age_of_oldest_revolving_account_in_months: Optional[float] = None
    s207s_months_since_most_recent_public_record_bankruptcy: Optional[float] = None
    re33s_balance_owed_on_all_revolving_accounts: Optional[float] = None
    at57s_amount_delinquent: Optional[float] = None
    g099s_public_records_last_24_months: Optional[float] = None
    at20s_oldest_trade_open_date: Optional[float] = None
    at03s_current_credit_lines: Optional[float] = None
    re101s_revolving_balance: Optional[float] = None
    bc34s_bankcard_utilization: Optional[float] = None
    at01s_credit_lines: Optional[float] = None
    g102s_months_since_most_recent_inquiry: Optional[float] = None
    fico_score: Optional[str] = None
