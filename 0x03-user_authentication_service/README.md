from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker

uName = 'root'
pwd = '33606399'
db_name = 'test_db'

Base = declarative_base()
engine = create_engine(
    'mysql+mysqldb://{}:{}@localhost:3306/{}'.format(
        uName, pwd, db_name
    )
)

Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))

    def __init__(self, name, fullname, nickname):
        self.name = name
        self.fullname = fullname
        self.nickname = nickname

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name, self.fullname, self.nickname)


users = session.query(User).filter(User.name.in_(['ali', 'ahmed'])).all()

for user in users:
    print(user)