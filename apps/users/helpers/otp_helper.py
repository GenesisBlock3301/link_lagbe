class OTPConstants:
    VERIFICATION_EXPIRY_SECONDS = 600   # Time to verify OTP
    STORE_EXPIRY_SECONDS = 120         # Time to store OTP in DB/cache
    RESEND_EXPIRY_SECONDS = 120        # Time before allowing resend

    @classmethod
    def get(cls, name):
        """
        Dynamically get any constant by name.
        Example: OTPConstants.get('VERIFICATION_EXPIRY_SECONDS')
        """
        return getattr(cls, name)

    @classmethod
    def verification_expiry(cls):
        return cls.VERIFICATION_EXPIRY_SECONDS

    @classmethod
    def store_expiry(cls):
        return cls.STORE_EXPIRY_SECONDS

    @classmethod
    def resend_expiry(cls):
        return cls.RESEND_EXPIRY_SECONDS
