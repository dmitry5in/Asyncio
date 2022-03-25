from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import sqlalchemy as db


engine = create_engine('postgresql://demodb:123456@localhost:5432/demodb')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True)
    sw_id = db.Column(db.Integer)
    birth_year = db.Column(db.String)
    eye_color = db.Column(db.String)
    gender = db.Column(db.String)
    hair_color = db.Column(db.String)
    height = db.Column(db.String)
    name = db.Column(db.String)
    mass = db.Column(db.String)
    skin_color = db.Column(db.Text)
    homeworld = db.Column(db.Text)
    starships = db.Column(db.ARRAY(db.Text)) #text[]
    vehicles = db.Column(db.ARRAY(db.Text)) #text[]
    species = db.Column(db.ARRAY(db.Text)) #text[]
    films = db.Column(db.ARRAY(db.Text)) #text[]


    def __str__(self):
        return f'{self.name}'


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session.commit()