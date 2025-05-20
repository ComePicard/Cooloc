from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.auth import get_current_user
from app.schemas.auth import TokenData, Token
from app.schemas.users import UserCreate
from app.services.auth import create_access_token, create_refresh_token, authenticate_user
from app.services.users import create_user, fetch_user_by_email

router = APIRouter()


@router.get("/me")
def read_me(current_user: TokenData = Depends(get_current_user)):
    return {"email": current_user.email}


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # OAuth2PasswordRequestForm uses username field, but we're using it for email
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: TokenData = Depends(get_current_user)):
    # Create new access and refresh tokens
    access_token = create_access_token({"sub": current_user.email})
    refresh_token = create_refresh_token({"sub": current_user.email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/signup", response_model=Token)
async def signup(user_data: UserCreate):
    """
    Register a new user and return access and refresh tokens.
    """
    # Check if user with this email already exists
    existing_user = await fetch_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    try:
        # Create the user in the database
        user = await create_user(user_data)

        # Generate tokens for the new user
        access_token = create_access_token({"sub": user.email})
        refresh_token = create_refresh_token({"sub": user.email})

        # Return tokens for immediate authentication
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except Exception as e:
        # Handle any other errors during user creation
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )
