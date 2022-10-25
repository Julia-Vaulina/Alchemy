import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from alchemy import create_tables, Publisher, Shop, Sale, Stock, Book

DSN = ''


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
session.close()

query = session.query(Publisher, Book, Shop, Stock)
query = query.join(Publisher, Publisher.id == Book.id_publisher)
query = query.join(Stock, Book.id == Stock.id_book)
query = query.join(Shop, Stock.id_shop == Shop.id)

records = query.all()

idpublisher = input('Введите id издалеля: ')

for Publisher, Book, Shop, Stock in records:
    if Publisher.id == int(idpublisher):
        print(Publisher.name)
        break

for Publisher, Book, Shop, Stock in records:
    if Publisher.name == 'Microsoft Press':
        print(f'Издатель {Publisher.name} имеется в продаже в {Shop.name}')
