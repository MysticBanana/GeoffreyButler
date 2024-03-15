# Flask extensions must be declared here to avoid circular imports
import sqlalchemy as db
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import relationship, joinedload, subqueryload, Session

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, PrimaryKeyConstraint
# from sqlalchemy

Base = declarative_base()


# models
class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    discord_id = Column(Integer, ForeignKey("userserver.discord_id"), primary_key=True)
    discord_name = Column(String)

    # if someone got a special treatment
    vip = Column(Boolean, default=False)

    servers = relationship("UserServer", cascade="all, delete", back_populates="user",
                                primaryjoin="UserServer.discord_id == User.discord_id")


# guild data
class Server(Base):
    __tablename__ = 'server'
    __table_args__ = {'extend_existing': True}

    server_id = Column(Integer, ForeignKey("userserver.server_id"), primary_key=True)
    server_name = Column(String)

    extensions = Column(JSON, nullable=True, default=dict())
    roles = Column(JSON, nullable=True, default=list())
    permissions = Column(JSON, nullable=True, default=dict())

    server_users = relationship("UserServer", cascade="all, delete", back_populates="server",
                                primaryjoin="UserServer.server_id == Server.server_id")


class UserServer(Base):
    __tablename__ = 'userserver'

    discord_id = Column(Integer, ForeignKey(User.discord_id))
    server_id = Column(Integer, ForeignKey(Server.server_id))

    xp = Column(Integer, default=0)
    money = Column(Integer, default=500)
    extension_data = Column(JSON, nullable=True, default=dict())

    user = relationship("User", cascade="all, delete", foreign_keys=discord_id)
    server = relationship("Server", cascade="all, delete", foreign_keys=server_id)

    __table_args__ = (
        PrimaryKeyConstraint(discord_id, server_id),
        {'extend_existing': True})

