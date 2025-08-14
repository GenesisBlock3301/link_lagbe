class BaseAPIException(Exception):
    """Base exception for all custom API errors."""
    status_code = 400
    default_detail = "A server error occurred."

    def __init__(self, detail=None, status_code=None):
        self.detail = detail or self.default_detail
        if status_code:
            self.status_code = status_code
        super().__init__(self.detail)
