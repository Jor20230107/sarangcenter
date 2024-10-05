from sqlalchemy import Column, Integer, String
from app.database import Base

class PageContent(Base):
    __tablename__ = "pages"
    id = Column(Integer, primary_key=True, index=True)
    page_name = Column(String, index=True)
    content = Column(String)
