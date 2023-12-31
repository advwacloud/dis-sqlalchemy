from dis_sqlalchemy import ForeignKey
from dis_sqlalchemy import func
from dis_sqlalchemy import Integer
from dis_sqlalchemy import select
from dis_sqlalchemy import String
from dis_sqlalchemy.orm import relationship
from dis_sqlalchemy.testing import eq_
from dis_sqlalchemy.testing import fixtures
from dis_sqlalchemy.testing.fixtures import fixture_session
from dis_sqlalchemy.testing.schema import Column
from dis_sqlalchemy.testing.schema import Table


class AssociationTest(fixtures.MappedTest):
    run_setup_classes = "once"
    run_setup_mappers = "once"

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "items",
            metadata,
            Column(
                "item_id",
                Integer,
                primary_key=True,
                test_needs_autoincrement=True,
            ),
            Column("name", String(40)),
        )
        Table(
            "item_keywords",
            metadata,
            Column("item_id", Integer, ForeignKey("items.item_id")),
            Column("keyword_id", Integer, ForeignKey("keywords.keyword_id")),
            Column("data", String(40)),
        )
        Table(
            "keywords",
            metadata,
            Column(
                "keyword_id",
                Integer,
                primary_key=True,
                test_needs_autoincrement=True,
            ),
            Column("name", String(40)),
        )

    @classmethod
    def setup_classes(cls):
        class Item(cls.Basic):
            def __init__(self, name):
                self.name = name

            def __repr__(self):
                return "Item id=%d name=%s keywordassoc=%r" % (
                    self.item_id,
                    self.name,
                    self.keywords,
                )

        class Keyword(cls.Basic):
            def __init__(self, name):
                self.name = name

            def __repr__(self):
                return "Keyword id=%d name=%s" % (self.keyword_id, self.name)

        class KeywordAssociation(cls.Basic):
            def __init__(self, keyword, data):
                self.keyword = keyword
                self.data = data

            def __repr__(self):
                return "KeywordAssociation itemid=%d keyword=%r data=%s" % (
                    self.item_id,
                    self.keyword,
                    self.data,
                )

    @classmethod
    def setup_mappers(cls):
        KeywordAssociation, Item, Keyword = (
            cls.classes.KeywordAssociation,
            cls.classes.Item,
            cls.classes.Keyword,
        )

        items, item_keywords, keywords = cls.tables.get_all(
            "items", "item_keywords", "keywords"
        )

        cls.mapper_registry.map_imperatively(Keyword, keywords)
        cls.mapper_registry.map_imperatively(
            KeywordAssociation,
            item_keywords,
            properties={"keyword": relationship(Keyword, lazy="joined")},
            primary_key=[item_keywords.c.item_id, item_keywords.c.keyword_id],
        )

        cls.mapper_registry.map_imperatively(
            Item,
            items,
            properties={
                "keywords": relationship(
                    KeywordAssociation,
                    order_by=item_keywords.c.data,
                    cascade="all, delete-orphan",
                )
            },
        )

    def test_insert(self):
        KeywordAssociation, Item, Keyword = (
            self.classes.KeywordAssociation,
            self.classes.Item,
            self.classes.Keyword,
        )

        sess = fixture_session()
        item1 = Item("item1")
        item2 = Item("item2")
        item1.keywords.append(
            KeywordAssociation(Keyword("blue"), "blue_assoc")
        )
        item1.keywords.append(KeywordAssociation(Keyword("red"), "red_assoc"))
        item2.keywords.append(
            KeywordAssociation(Keyword("green"), "green_assoc")
        )
        sess.add_all((item1, item2))
        sess.flush()
        saved = repr([item1, item2])
        sess.expunge_all()
        result = sess.query(Item).all()
        loaded = repr(result)
        eq_(saved, loaded)

    def test_replace(self):
        KeywordAssociation, Item, Keyword = (
            self.classes.KeywordAssociation,
            self.classes.Item,
            self.classes.Keyword,
        )

        sess = fixture_session()
        item1 = Item("item1")
        item1.keywords.append(
            KeywordAssociation(Keyword("blue"), "blue_assoc")
        )
        item1.keywords.append(KeywordAssociation(Keyword("red"), "red_assoc"))
        sess.add(item1)
        sess.flush()

        red_keyword = item1.keywords[1].keyword
        del item1.keywords[1]
        item1.keywords.append(KeywordAssociation(red_keyword, "new_red_assoc"))
        sess.flush()
        saved = repr([item1])
        sess.expunge_all()
        result = sess.query(Item).all()
        loaded = repr(result)
        eq_(saved, loaded)

    def test_modify(self):
        KeywordAssociation, Item, Keyword = (
            self.classes.KeywordAssociation,
            self.classes.Item,
            self.classes.Keyword,
        )

        sess = fixture_session()
        item1 = Item("item1")
        item2 = Item("item2")
        item1.keywords.append(
            KeywordAssociation(Keyword("blue"), "blue_assoc")
        )
        item1.keywords.append(KeywordAssociation(Keyword("red"), "red_assoc"))
        item2.keywords.append(
            KeywordAssociation(Keyword("green"), "green_assoc")
        )
        sess.add_all((item1, item2))
        sess.flush()

        red_keyword = item1.keywords[1].keyword
        del item1.keywords[0]
        del item1.keywords[0]
        purple_keyword = Keyword("purple")
        item1.keywords.append(KeywordAssociation(red_keyword, "new_red_assoc"))
        item2.keywords.append(
            KeywordAssociation(purple_keyword, "purple_item2_assoc")
        )
        item1.keywords.append(
            KeywordAssociation(purple_keyword, "purple_item1_assoc")
        )
        item1.keywords.append(
            KeywordAssociation(Keyword("yellow"), "yellow_assoc")
        )

        sess.flush()
        saved = repr([item1, item2])
        sess.expunge_all()
        result = sess.query(Item).all()
        loaded = repr(result)
        eq_(saved, loaded)

    def test_delete(self):
        KeywordAssociation = self.classes.KeywordAssociation
        Item = self.classes.Item
        item_keywords = self.tables.item_keywords
        Keyword = self.classes.Keyword

        sess = fixture_session()
        item1 = Item("item1")
        item2 = Item("item2")
        item1.keywords.append(
            KeywordAssociation(Keyword("blue"), "blue_assoc")
        )
        item1.keywords.append(KeywordAssociation(Keyword("red"), "red_assoc"))
        item2.keywords.append(
            KeywordAssociation(Keyword("green"), "green_assoc")
        )
        sess.add_all((item1, item2))
        sess.flush()
        eq_(
            sess.connection().scalar(
                select(func.count("*")).select_from(item_keywords)
            ),
            3,
        )

        sess.delete(item1)
        sess.delete(item2)
        sess.flush()
        eq_(
            sess.connection().scalar(
                select(func.count("*")).select_from(item_keywords)
            ),
            0,
        )
