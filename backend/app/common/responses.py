"""Success envelope helpers so every endpoint returns the same shape."""


def success(data, meta: dict | None = None, status_code: int = 200):
    body = {"status": "success", "data": data}
    if meta is not None:
        body["meta"] = meta
    return body, status_code
