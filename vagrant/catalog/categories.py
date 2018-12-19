from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog_database_setup import Base, Category, CategoryItem

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


    

category1 = Category(name="Soccer")

session.add(category1)
session.commit()

item1 = CategoryItem(name = "Soccer Ball", description = "A black and white ball used for Soccer", category = category1)

session.add(item1)
session.commit()

item2 = CategoryItem(name = "Shin Gards", description = "Gards to protect shins from kicks and soccer balls", category = category1)

session.add(item2)
session.commit()

item3 = CategoryItem(name = "Gloves", description = "Gloves to help with grip as a goalie", category = category1)

session.add(item3)
session.commit()

category2 = Category(name = "Basketball")

session.add(category2)
session.commit()

item1 = CategoryItem(name = "Basketall", description = "Orange ball used to play Basketball", category = category2)

session.add(item1)
session.commit()

item2 = CategoryItem(name = "Hoop", description = "Rim, net and backboard in order to score in Basketball", category = category2)

session.add(item2)
session.commit()

category3 = Category(name = 'Baseball')

session.add(category3)
session.commit()

item1 = CategoryItem(name = "Baseball", description = "White ball with red stitching used to play baseball", category = category3)

session.add(item1)
session.commit()

item2 = CategoryItem(name = "Bat", description = "Wooden club used to hit baseballs and score runs while playing", category = category3)

session.add(item2)
session.commit()

item3 = CategoryItem(name = "Glove", description = "Leather glove used to catch baseball while playing defense", category = category3)

session.add(item3)
session.commit()

item4 = CategoryItem(name = "Cap", description = "Cap used to block out sun and indicate team when playing baseball", category = category3)

session.add(item4)
session.commit()

category4 = Category(name="Football")

session.add(category4)
session.commit()

item1 = CategoryItem(name = "Football", description = "Leather oval shaped ball used to play football", category = category4)

session.add(item1)
session.commit()

item2 = CategoryItem(name = "Helmet", description = "Used to protect head from injury in the contact sport of Football", category = category4)

session.add(item2)
session.commit()

item3 = CategoryItem(name = "Pads", description = "Used to protect the body from injury in the contact sport of Football", category = category4)

session.add(item3)
session.commit()

item4 = CategoryItem(name = "Mouth Gaurd", description = "Gaurd to protect the teeth from damage and injury during the contact sport of Football", category = category4)

session.add(item4)
session.commit()

category5 = Category(name = 'Hockey')

session.add(category5)
session.commit()

item1 = CategoryItem(name = "Stick", description = "Stick to move, pass, and score in Hockey", category = category5)

session.add(item1)
session.commit()

item2 = CategoryItem(name = "Puck", description = "Round rubber disk used to score in Hockey", category = category5)

session.add(item2)
session.commit()

item3 = CategoryItem(name = "Helmet", description = "Used to protect head from injury during the contact sport of Hockey", category = category5)

session.add(item3)
session.commit()

item4 = CategoryItem(name = "Gloves", description = "Used to protect hands from injury during the contact sport of Hockey", category = category5)

session.add(item4)
session.commit()

item5 = CategoryItem(name = "Skates", description = "Ice Skates used to move around on the ice while playing Hockey", category = category5)

session.add(item5)
session.commit()


































