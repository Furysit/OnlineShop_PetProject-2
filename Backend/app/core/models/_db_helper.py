from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession
from asyncio import current_task


from app.core.config import settings

class DataBaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url = settings.db_URL,
            echo = settings.db_echo
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush = False,
            autocommit = False,
            expire_on_commit = False,
        )
    def get_scoped_session(self):
        session = async_scoped_session(
            self.session_factory,
            scopefunc=current_task
        )
        return session
    
    # async def session_dependecy(self):
    #     async with self.session_factory() as session:
    #         yield session
    #         await session.close()

    async def scoprd_session_dependecy(self):
        session =  self.get_scoped_session()
        yield session
        await session.remove()



db_helper = DataBaseHelper(
    url=settings.db_URL, 
    echo=settings.db_echo,
)