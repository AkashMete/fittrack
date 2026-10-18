"""Offset-based pagination (API_DESIGN.md) — returns (items, meta)."""
from flask import request


def get_page_args(default_per_page: int = 20, max_per_page: int = 100):
    try:
        page = max(int(request.args.get("page", 1)), 1)
        per_page = min(max(int(request.args.get("per_page", default_per_page)), 1), max_per_page)
    except ValueError:
        page, per_page = 1, default_per_page
    return page, per_page


def paginate(queryset, page: int, per_page: int):
    total = queryset.count()
    items = list(queryset.skip((page - 1) * per_page).limit(per_page))
    pages = max((total + per_page - 1) // per_page, 1)
    meta = {
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pages,
        "has_next": page < pages,
        "has_prev": page > 1,
    }
    return items, meta
