from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog_database_setup import Base, Category, CategoryItem, User

engine = create_engine('postgresql://catalog:password@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com", picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()  

category1 = Category(name="Soccer", user_id=1)

session.add(category1)
session.commit()

item1 = CategoryItem(user_id=1, name = "Soccer Ball", description = "A black and white ball used for Soccer", category = category1)

session.add(item1)
session.commit()

item2 = CategoryItem(user_id=1, name = "Shin Gards", description = "Gards to protect shins from kicks and soccer balls", category = category1)

session.add(item2)
session.commit()

item3 = CategoryItem(user_id=1, name = "Goalie Gloves", description = "Gloves to help with grip as a goalie", category = category1)

session.add(item3)
session.commit()

category2 = Category(user_id=1, name = "Basketball")

session.add(category2)
session.commit()

item1 = CategoryItem(user_id=1, name = "Basketall", description = "Orange ball used to play Basketball", category = category2)

session.add(item1)
session.commit()

item2 = CategoryItem(user_id=1, name = "Hoop", description = "Rim, net and backboard in order to score in Basketball", category = category2)

session.add(item2)
session.commit()

category3 = Category(user_id=1, name = 'Baseball')

session.add(category3)
session.commit()

item1 = CategoryItem(user_id=1, name = "Baseball", description = "White ball with red stitching used to play baseball", category = category3)

session.add(item1)
session.commit()

item2 = CategoryItem(user_id=1, name = "Bat", description = "Wooden club used to hit baseballs and score runs while playing", category = category3)

session.add(item2)
session.commit()

item3 = CategoryItem(user_id=1, name = "Baseball Glove", description = "Leather glove used to catch baseball while playing defense", category = category3)

session.add(item3)
session.commit()

item4 = CategoryItem(user_id=1, name = "Cap", description = "Cap used to block out sun and indicate team when playing baseball", category = category3)

session.add(item4)
session.commit()

category4 = Category(user_id=1, name="Football")

session.add(category4)
session.commit()

item1 = CategoryItem(user_id=1, name = "Football", description = "Leather oval shaped ball used to play football", category = category4)

session.add(item1)
session.commit()

item2 = CategoryItem(user_id=1, name = "Football Helmet", description = "Used to protect head from injury in the contact sport of Football", category = category4)

session.add(item2)
session.commit()

item3 = CategoryItem(user_id=1, name = "Pads", description = "Used to protect the body from injury in the contact sport of Football", category = category4)

session.add(item3)
session.commit()

item4 = CategoryItem(user_id=1, name = "Mouth Gaurd", description = "Gaurd to protect the teeth from damage and injury during the contact sport of Football", category = category4)

session.add(item4)
session.commit()

category5 = Category(user_id=1, name = 'Hockey')

session.add(category5)
session.commit()

item1 = CategoryItem(user_id=1, name = "Stick", description = "Stick to move, pass, and score in Hockey", category = category5)

session.add(item1)
session.commit()

item2 = CategoryItem(user_id=1, name = "Puck", description = "Round rubber disk used to score in Hockey", category = category5)

session.add(item2)
session.commit()

item3 = CategoryItem(user_id=1, name = "Hockey Helmet", description = "Used to protect head from injury during the contact sport of Hockey", category = category5)

session.add(item3)
session.commit()

item4 = CategoryItem(user_id=1, name = "Hockey Gloves", description = "Used to protect hands from injury during the contact sport of Hockey", category = category5)

session.add(item4)
session.commit()

item5 = CategoryItem(user_id=1, name = "Skates", description = "Ice Skates used to move around on the ice while playing Hockey", category = category5)

session.add(item5)
session.commit()


































