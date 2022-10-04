# Используя SQLAlchemy, составить запрос выборки магазинов, продающих целевого издателя.
# Напишите Python скрипт, который:
# Подключается к БД любого типа на ваш выбор (например, к PostgreSQL).
# Импортирует необходимые модели данных.
# # Выводит издателя (publisher), имя или идентификатор которого принимается через input()

import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

def import_models_query(login_path, id_publisher):

    DSN = login_path
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    with open('tests_data.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()
    subq1 = session.query(Book.id).join(Publisher.book).filter(Publisher.id == id_publisher).subquery()
    subq2 = session.query(Stock.id).join(subq1, Stock.id_book == subq1.c.id).subquery()
    q = session.query(Shop).join(subq2, Shop.id == subq2.c.id)
    # print(q)
    for s in q.all():
        print(s.id, s.name)
    session.close()

if __name__ == "__main__":
    db_type = input('Write database type ')
    db_user = input('Write database user name ')
    db_password = input('Write database password ')
    db_location = input('Write database location ')
    db_connection = input('Write database connection code ')
    db_name = input('Write database name ')
    # db_type = 'postgresql'
    # db_user = 'postgres'
    # db_password = 'postgres'
    # db_location = 'localhost'
    # db_connection = '5432'
    # db_name = 'shops_db'
    login_path = f"{db_type}://{db_user}:{db_password}@{db_location}:{db_connection}/{db_name}"
    # login_path = "postgresql://postgres:postgres@localhost:5432/shops_db"
    id_publisher = int(input('Write publisher id for the query '))
    import_models_query(login_path, id_publisher)

