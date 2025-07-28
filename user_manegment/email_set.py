from exception import InvalidResetTokenError
from fastapi import  HTTPException, Request
from fastapi import Depends
from email.message import EmailMessage
import smtplib
from service import get_user_by_email
from tokens import  create_access_token, decode_access_token
from fastapi.security import OAuth2PasswordBearer

ACCESS_TOKEN_EXPIRE_MINUTES = 60  
SECRET = "your-secret-key"
ALGO = "HS256"


#oauth2 = OAuth2PasswordBearer(tokenUrl="/forgotpassword")

def generate_reset_link(email: str, request: Request):
    base_url = str(request.base_url).rstrip("/")
    # Simulate token or ID encoding here
    token = create_access_token(email,ACCESS_TOKEN_EXPIRE_MINUTES)
    return f"{base_url}/reset-password?token={token}&email={email}"



def send_reset_email(to_email: str, reset_link: str):
    from_email = "molamantithirupathirao@gmail.com"
    app_password = "vakg iylc jgsq vfim"  # Use Gmail app password

    msg = EmailMessage()
    msg["Subject"] = "Password Reset Request"
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(f"Click the link below to reset your password:\n\n{reset_link}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(from_email, app_password)
            smtp.send_message(msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")
    

async def get_current_user2(token: str):
   
    data = decode_access_token(token)
    #     if await is_token_blacklisted(token):
    #         raise HTTPException(401, "Token has been revoked.")
    # except JWTError:
    #     raise HTTPException(401, "Invalid token")
    
    user = await get_user_by_email(data.get("sub"))
    if not user:
        raise InvalidResetTokenError()
    # if not user or not user.get("active"):
    #     raise HTTPException(403, "User is inactive.")
    return user

# async def find_by_reset_token(token: str):
#     from utils.security import decode_access_token
#     try:
#         data = decode_access_token(token)
#     except:
#         raise HTTPException(400, "Invalid token.")
#     if data.get("type") != "reset":
#         raise HTTPException(400, "Wrong token type.")
#     return await users.find_one({"email": data.get("sub")})