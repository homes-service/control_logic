from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from settings import settings

router = APIRouter(
    prefix=f"{settings.V1}/auth",
    tags=["Authentication"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register")
def register(user, db: AsyncSession = Depends(get_session)):
    # db_user = db.query(models.User).filter(
    #     models.User.telegram_id == user.telegram_id).first()
    # if db_user:
    #     raise HTTPException(status_code=400,
    #     detail="User already registered")
    # hashed_password = auth.get_password_hash(
    #     user.password) if user.password else None
    # db_user = models.User(
    #     telegram_id=user.telegram_id,
    #     username=user.username,
    #     email=user.email,
    #     hashed_password=hashed_password
    # )
    # db.add(db_user)
    # db.commit()
    # return {"message": "User registered"}
    pass


@router.post("/token")
def login(telegram_id: int, db: AsyncSession = Depends(get_session)):
    # user = db.query(models.User).filter(
    #     models.User.telegram_id == telegram_id).first()
    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")
    #
    # access_token = auth.create_access_token(
    #     data={"sub": str(user.telegram_id)})
    # return {"access_token": access_token, "token_type": "bearer"}
    pass


@router.get("/me")
def read_current_user(token: str = Depends(oauth2_scheme),
                      db: AsyncSession = Depends(get_session)):
    # try:
    #     payload = jwt.decode(token, auth.SECRET_KEY,
    #                          algorithms=[auth.ALGORITHM])
    #     telegram_id = int(payload.get("sub"))
    #     user = db.query(models.User).filter(
    #         models.User.telegram_id == telegram_id).first()
    #     if not user:
    #         raise HTTPException(status_code=404, detail="User not found")
    #     return user
    # except JWTError:
    #     raise HTTPException(status_code=401, detail="Invalid token")
    pass
