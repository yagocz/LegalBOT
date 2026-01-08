"""
Users API endpoints for LegalBot
"""

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta, datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import (
    get_current_user, 
    get_password_hash, 
    verify_password,
    create_access_token,
    create_refresh_token,
)
from app.core.config import settings
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
    TokenResponse,
    SubscriptionResponse,
    UsageResponse,
)
from app.models.user import User, Subscription, Usage, PlanType

router = APIRouter(prefix="/users", tags=["Users"])

# Plan limits
PLAN_LIMITS = {
    PlanType.FREE: {"queries": 3, "documents": 1},
    PlanType.BASIC: {"queries": 20, "documents": "unlimited"},
    PlanType.PREMIUM: {"queries": "unlimited", "documents": "unlimited"},
    PlanType.ENTERPRISE: {"queries": "unlimited", "documents": "unlimited"},
}


@router.post("/register", response_model=TokenResponse)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user"""
    # Check if email exists
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Create user
    user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=get_password_hash(user_data.password),
        plan=PlanType.FREE,
    )
    db.add(user)
    
    # Create subscription
    subscription = Subscription(
        user_id=user.id,
        plan=PlanType.FREE,
        status="active",
    )
    db.add(subscription)
    
    # Create usage record
    current_month = datetime.utcnow().strftime("%Y-%m")
    usage = Usage(
        user_id=user.id,
        month=current_month,
        queries_count="0",
        documents_count="0",
    )
    db.add(usage)
    
    await db.commit()
    await db.refresh(user)
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    """Login and get access token"""
    result = await db.execute(
        select(User).where(User.email == credentials.email)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cuenta desactivada"
        )
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user profile"""
    user_id = UUID(current_user["user_id"])
    
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return UserResponse.model_validate(user)


@router.put("/me", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user profile"""
    user_id = UUID(current_user["user_id"])
    
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Update fields
    if update_data.name is not None:
        user.name = update_data.name
    if update_data.avatar is not None:
        user.avatar = update_data.avatar
    
    await db.commit()
    await db.refresh(user)
    
    return UserResponse.model_validate(user)


@router.get("/subscription", response_model=SubscriptionResponse)
async def get_subscription(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's subscription"""
    user_id = UUID(current_user["user_id"])
    
    result = await db.execute(
        select(Subscription).where(Subscription.user_id == user_id)
    )
    subscription = result.scalar_one_or_none()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Suscripción no encontrada"
        )
    
    return SubscriptionResponse.model_validate(subscription)


@router.get("/usage", response_model=UsageResponse)
async def get_usage(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current month's usage"""
    user_id = UUID(current_user["user_id"])
    current_month = datetime.utcnow().strftime("%Y-%m")
    
    # Get user for plan info
    user_result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Get or create usage record
    result = await db.execute(
        select(Usage).where(
            Usage.user_id == user_id,
            Usage.month == current_month
        )
    )
    usage = result.scalar_one_or_none()
    
    if not usage:
        usage = Usage(
            user_id=user_id,
            month=current_month,
            queries_count="0",
            documents_count="0",
        )
        db.add(usage)
        await db.commit()
        await db.refresh(usage)
    
    # Get limits based on plan
    limits = PLAN_LIMITS.get(user.plan, PLAN_LIMITS[PlanType.FREE])
    
    return UsageResponse(
        queries_count=int(usage.queries_count),
        queries_limit=limits["queries"],
        documents_count=int(usage.documents_count),
        documents_limit=limits["documents"],
        month=current_month,
    )

