class TokenConstants:
    ACCESS_TOKEN_EXPIRY_MINUTES = 1440
    ACCESS_TOKEN_EXPIRY_MINUTES_REMEMBER_ME = 43200
    REFRESH_TOKEN_EXPIRY_DAYS = 7
    REFRESH_TOKEN_EXPIRY_DAYS_REMEMBER_ME = 60
    ALGORITHM = 'HS256'

    @classmethod
    def get(cls, name):
        return getattr(cls, name)

    @classmethod
    def access_token_expiry(cls, remember_me=False):
        return cls.ACCESS_TOKEN_EXPIRY_MINUTES_REMEMBER_ME if remember_me else cls.ACCESS_TOKEN_EXPIRY_MINUTES

    @classmethod
    def refresh_token_expiry(cls, remember_me=False):
        return cls.REFRESH_TOKEN_EXPIRY_DAYS_REMEMBER_ME if remember_me else cls.REFRESH_TOKEN_EXPIRY_DAYS

    @classmethod
    def algorithm(cls):
        return cls.ALGORITHM
