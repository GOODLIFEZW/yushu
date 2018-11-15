from flask import current_app
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)   # 默认这本书没被赠送出去

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    """
        只显示一定数量（30）
        按时间排序，最新的显示在前面
        去重，同一本书籍的礼物不重复出现(mysql去重需先分组)
    """
    @classmethod
    def recent(cls):
        # 链式调用
        recent_gifts = Gift.query.filter_by(launched=False).group_by(Gift.isbn).order_by(
                    desc(Gift.create_time)).limit(current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gifts

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_user_gifts(cls, uid):
        # 单纯查这个模型的话，使用filter_by比较快
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish    # 避免循环导入
        # 根据传入的一组isbn，到Wish表算出某个礼物的心愿数量
        # 查询比较复杂的话或者跨模型查询使用filter比较好
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(Wish.isbn).all()
        # 直接返回count_list不是很友好
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list
