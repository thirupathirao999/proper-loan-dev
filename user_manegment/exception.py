from fastapi import HTTPException

class UserAlreadyExitsError(HTTPException):
    def __init__(self):
        super().__init__(409, "User already exists. Go to login page")

class InvalidCredentialsError(HTTPException):
    def __init__(self):
        super().__init__(401, "Invalid credentials.")


class PhoneNumberError(HTTPException):
    def __init__(self):
        super().__init__(400, "enter a valid phone number it must have a 10 digits")


class PasswordPolicyError(HTTPException):
    def __init__(self):
        super().__init__(400, "Password does not meet policy requirements.password must cotaine  one[A-Z],one[a-z],one digit,one special charector and at least contain 8 letters")

class PasswordReuseError(HTTPException):
    def __init__(self):
        super().__init__(400, "Cannot reuse old password.")

class PasswordExpiredError(HTTPException):
    def __init__(self):
        super().__init__(403, "Password expired; please change now.")

class TooManyResetRequestsError(HTTPException):
    def __init__(self):
        super().__init__(429, "Too many password reset requests; try later.")

class InvalidResetTokenError(HTTPException):
    def __init__(self):
        super().__init__(400, "Invalid or expired password reset token.")

class UserInactiveError(HTTPException):
    def __init__(self):
        super().__init__(403, "User is inactive.")
