from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# Naming convention for foreign keys
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

# Base class for models
Base = declarative_base(metadata=metadata)


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    def __repr__(self):
        return f"<Company {self.name}>"

    @property
    def devs(self):
        return list({freebie.dev for freebie in self.freebies})

    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        return freebie

    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()


class Dev(Base):
    __tablename__ = "devs"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<Dev {self.name}>"

    @property
    def companies(self):
        return list({freebie.company for freebie in self.freebies})

    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, other_dev, freebie):
        if freebie in self.freebies:
            freebie.dev = other_dev


class Freebie(Base):
    __tablename__ = "freebies"

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)
    dev_id = Column(Integer, ForeignKey("devs.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))

    dev = relationship("Dev", backref=backref("freebies", cascade="all, delete-orphan"))
    company = relationship(
        "Company", backref=backref("freebies", cascade="all, delete-orphan")
    )

    def __repr__(self):
        return f"<Freebie {self.item_name} (${self.value})>"

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
