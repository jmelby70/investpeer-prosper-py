# model/filterset.py
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class FilterSet:
    grades: Optional[str] = None
    employment_length_over: Optional[int] = None
    inquiries_under: Optional[int] = None
    delinquencies_under: Optional[int] = None
    payment_income_ratio_under: Optional[float] = None
    loan_count_over: Optional[int] = None


@dataclass
class FilterSetProperties:
    filter_set_list: List[FilterSet] = field(default_factory=list)


def check_grade(filter_set, grade: str) -> bool:
    if filter_set.grades is None:
        return False
    accepted_grades = [g.strip() for g in filter_set.grades.split(",")]
    return grade in accepted_grades


def check_employment_length(filter_set, months_employed: float) -> bool:
    if filter_set.employment_length_over is None:
        return False
    return months_employed >= filter_set.employment_length_over * 12


def check_inquiries(filter_set, inquiries: float) -> bool:
    if filter_set.inquiries_under is None:
        return False
    return inquiries <= filter_set.inquiries_under


def check_delinquencies(filter_set, delinquencies: float) -> bool:
    if filter_set.delinquencies_under is None:
        return False
    return delinquencies <= filter_set.delinquencies_under


def check_payment_income_ratio(filter_set, payment: float, monthly_income: float) -> bool:
    if filter_set.payment_income_ratio_under is None or monthly_income == 0:
        return False
    return (payment / monthly_income) <= filter_set.payment_income_ratio_under
