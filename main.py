# filename: main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# 1) Session middleware for storing user info in a secure, signed cookie.
#    Use a truly random & persistent secret in production (e.g. from env vars).
app.add_middleware(SessionMiddleware, secret_key=os.urandom(24))

# 2) Configure OAuth with Authlib for FastAPI/Starlette
oauth = OAuth()


oauth.register(
    name='oidc',
    authority='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_8tJV5czrl',
    client_id='64ig6tpoi467ncg2b4me9gkvi1',
    client_secret='iggav30qn30n71cmss1ain46sts3lupoqsc07h97ndq2easm48f',
    server_metadata_url='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_8tJV5czrl/.well-known/openid-configuration',
    client_kwargs={'scope': 'phone openid email'}
)

# 3) Home route: checks if we're storing user info in the session
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    user = request.session.get("user")
    if user:
        return f"""
        <h1>Hello, {user['email']}</h1>
        <p><a href="/logout">Logout</a></p>
        """
    else:
        return """
        <h1>Welcome!</h1>
        <p>Please <a href="/login">Login</a>.</p>
        """

# 4) Login route: triggers an OAuth 2.0 "authorize" redirect
@app.get("/login")
async def login(request: Request):
    # Option A: Hard-code the redirect URI
    return await oauth.oidc.authorize_redirect(
        request,
        redirect_uri="http://localhost:8000/authorize"
    )
#this doesn't work
# @app.get("/login")
# async def login(request: Request):
#     redirect_uri = request.url_for("authorize")
#     return await oauth.oidc.authorize_redirect(request, redirect_uri)

# 5) Authorize route: Cognito redirects here after a successful login.
@app.get("/authorize")
async def authorize(request: Request):
    # Authlib exchanges the "code" for tokens and fetches user info from Cognito
    token = await oauth.oidc.authorize_access_token(request)
    user = token["userinfo"]
    
    # We store the user info (claims) in the server-side session
    request.session["user"] = user
    return RedirectResponse(url="/")

# 6) Logout route: clears the user from the session
@app.get("/logout")
def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")
