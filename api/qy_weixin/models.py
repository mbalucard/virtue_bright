from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, SmallInteger, String, Text, func, text, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def _dt_iso(v: datetime | None) -> str | None:
    """时间戳转 ISO 格式"""
    return v.isoformat() if v else None


class Base(DeclarativeBase):
    pass


class QyWeixinCalendar(Base):
    """企业微信日历表"""
    __tablename__ = "qy_weixin_calendar"

    cal_id: Mapped[str] = mapped_column(
        String(64), primary_key=True, comment="日历ID"
    )
    summary: Mapped[str | None] = mapped_column(String(255), comment="日历标题")
    description: Mapped[str | None] = mapped_column(Text, comment="日历描述")
    is_public: Mapped[int | None] = mapped_column(
        Integer, server_default=text("0"), comment="是否公共日历"
    )
    is_corp_calendar: Mapped[int | None] = mapped_column(
        Integer, server_default=text("0"), comment="是否企业日历"
    )
    admin: Mapped[str | None] = mapped_column(String(64), comment="日历管理员用户ID")
    is_delete: Mapped[int | None] = mapped_column(
        SmallInteger,
        server_default=text("0"),
        comment="是否删除日历 0: 否, 1: 是",
    )
    create_time: Mapped[datetime | None] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间"
    )
    last_updated_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        comment="最后更新时间",
    )

    def to_dict(self) -> dict:
        return {
            "cal_id": self.cal_id,
            "summary": self.summary,
            "description": self.description,
            "is_public": self.is_public,
            "is_corp_calendar": self.is_corp_calendar,
            "admin": self.admin,
            "is_delete": self.is_delete,
            "create_time": _dt_iso(self.create_time),
            "last_updated_time": _dt_iso(self.last_updated_time),
        }


class QyWeixinDepartment(Base):
    """企业微信部门表"""
    __tablename__ = "qy_weixin_department"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="部门ID")
    name: Mapped[str | None] = mapped_column(String(128), comment="部门名称")
    parentid: Mapped[int | None] = mapped_column(Integer, comment="父部门ID")
    order: Mapped[int | None] = mapped_column(
        "order", BigInteger, comment="部门排序")
    department_leader: Mapped[str | None] = mapped_column(
        String(64), comment="部门负责人ID"
    )
    is_delete: Mapped[int | None] = mapped_column(
        SmallInteger, server_default=text("0"), comment="是否删除部门 0: 否, 1: 是"
    )
    create_time: Mapped[datetime | None] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间"
    )
    last_updated_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        comment="最后更新时间",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "parentid": self.parentid,
            "order": self.order,
            "department_leader": self.department_leader,
            "is_delete": self.is_delete,
            "create_time": _dt_iso(self.create_time),
            "last_updated_time": _dt_iso(self.last_updated_time),
        }


class QyWeixinUser(Base):
    """企业微信用户表"""
    __tablename__ = "qy_weixin_user"

    userid: Mapped[str] = mapped_column(
        String(128), primary_key=True, comment="用户ID")
    name: Mapped[str | None] = mapped_column(String(255), comment="姓名")
    position: Mapped[str | None] = mapped_column(String(255), comment="职位")
    status: Mapped[int | None] = mapped_column(SmallInteger, comment="人员状态")
    enable: Mapped[int | None] = mapped_column(
        SmallInteger, comment="是否启用 0: 否, 1: 是"
    )
    isleader: Mapped[int | None] = mapped_column(
        SmallInteger, comment="是否为部门负责人 0: 否, 1: 是"
    )
    hide_mobile: Mapped[int | None] = mapped_column(
        SmallInteger, comment="是否隐藏手机号 0: 否, 1: 是"
    )
    telephone: Mapped[str | None] = mapped_column(String(64), comment="座机号")
    main_department: Mapped[int | None] = mapped_column(
        Integer, comment="主部门ID")
    alias: Mapped[str | None] = mapped_column(String(128), comment="别名")
    external_position: Mapped[str | None] = mapped_column(
        String(128), comment="对外职务")
    direct_leader: Mapped[str | None] = mapped_column(
        String(128), comment="直接负责人列表")
    is_delete: Mapped[int | None] = mapped_column(
        SmallInteger, server_default=text("0"), comment="是否删除用户 0: 否, 1: 是"
    )
    create_time: Mapped[datetime | None] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间"
    )
    last_updated_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        comment="最后更新时间",
    )

    def to_dict(self) -> dict:
        return {
            "userid": self.userid,
            "name": self.name,
            "position": self.position,
            "status": self.status,
            "enable": self.enable,
            "isleader": self.isleader,
            "hide_mobile": self.hide_mobile,
            "telephone": self.telephone,
            "main_department": self.main_department,
            "alias": self.alias,
            "external_position": self.external_position,
            "direct_leader": self.direct_leader,
            "is_delete": self.is_delete,
            "create_time": _dt_iso(self.create_time),
            "last_updated_time": _dt_iso(self.last_updated_time),
        }


class QyWeixinUserDepartment(Base):
    """企业微信用户-部门关系表"""
    __tablename__ = "qy_weixin_user_department"

    userid: Mapped[str] = mapped_column(
        String(128), primary_key=True, comment="用户ID")
    department_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, comment="所属部门ID"
    )
    is_leader_in_dept: Mapped[int | None] = mapped_column(
        SmallInteger, comment="是否为部门负责人 0: 否, 1: 是"
    )
    is_delete: Mapped[int | None] = mapped_column(
        SmallInteger, server_default=text("0"), comment="是否删除关系 0: 否, 1: 是"
    )
    create_time: Mapped[datetime | None] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间"
    )
    last_updated_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        comment="最后更新时间",
    )

    def to_dict(self) -> dict:
        return {
            "userid": self.userid,
            "department_id": self.department_id,
            "is_leader_in_dept": self.is_leader_in_dept,
            "is_delete": self.is_delete,
            "create_time": _dt_iso(self.create_time),
            "last_updated_time": _dt_iso(self.last_updated_time),
        }


# class UserTest(Base):
#     __tablename__ = "user_test"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)
#     email = Column(String(100), unique=True, nullable=True)

#     def __repr__(self):
#         return f"<User(id={self.id}, name={self.name}, email={self.email})>"
