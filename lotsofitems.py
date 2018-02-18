from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CategoryItem, User

engine = create_engine('sqlite:///categoryitemswithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

category1 = Category(user_id=1, name="Kitchen")

session.add(category1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, name="Soup Pot", description="Non stick soup pot",
                     price="$10.50", category=category1)

session.add(categoryItem2)
session.commit()


categoryItem1 = CategoryItem(user_id=1, name="Spoons", description="Spoon you can use to eat soup or cereal",
                     price="$2.99", category=category1)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, name="Omlette Pan", description="small convenient pan to make omlettes",
                     price="$5.50", category=category1)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1, name="Dutch Oven", description="Big dutch oven for when guests come over",
                     price="$12.99", category=category1)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=1, name="Colander", description="Made with high quality stainless steel",
                     price="$7.99", category=category1)

session.add(categoryItem4)
session.commit()

categoryItem5 = CategoryItem(user_id=1, name="Glasses", description="16oz of refreshing goodness",
                     price="$5.99", category=category1)

session.add(categoryItem5)
session.commit()

categoryItem6 = CategoryItem(user_id=1, name="Serving bowl", description="Big serving bowl for all occasions",
                     price="$4.99", category=category1)

session.add(categoryItem6)
session.commit()


# Items for Clothing category
category2 = Category(user_id=1, name="Clothing")

session.add(category2)
session.commit()


categoryItem1 = CategoryItem(user_id=1, name="Jeans", description="High quality durable jeans",
                     price="$17.99", category=category2)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, name="Shirts",
                     description="smooth cotton shirts", price="$25", category=category2)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1, name="Skirts", description="Colorful skirts for work and play ",
                     price="$15", category=category2)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=1, name="Sweater", description="High quality wool sweaters",
                     price="$12", category=category2)

session.add(categoryItem4)
session.commit()

categoryItem5 = CategoryItem(user_id=1, name="Gloves", description="Gloves for winter",
                     price="14", category=category2)

session.add(categoryItem5)
session.commit()



#
category1 = Category(user_id=1, name="Toys")

session.add(category1)
session.commit()


categoryItem1 = CategoryItem(user_id=1, name="GI Joe", description="A lifesize GI Joe",
                     price="$28.99", category=category1)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, name="Barbie", description="A entire set of Barbie dolls",
                     price="$36.99", category=category1)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1, name="stuffed panda", description="A high quality talking stuffed panda for your little one",
                     price="$19.95", category=category1)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=1, name="Remote controlled car", description="Remote controlled car with emergency horns",
                     price="$36.99", category=category1)

session.add(categoryItem4)
session.commit()

categoryItem2 = CategoryItem(user_id=1, name="100 piece puzzle", description="fun puzzle to solve with family",
                     price="$10.50", category=category1)

session.add(categoryItem2)
session.commit()


# Items for 'Sports' category
category1 = Category(user_id=1, name="Sports ")

session.add(category1)
session.commit()


categoryItem1 = CategoryItem(user_id=1, name="Roller Blades", description="High quality roller blades with adjustable foot size",
                     price="$52.99", category=category1)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, name="Tennis set", description="Tennis raquets and balls",
                     price="$55.99", category=category1)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1, name="Badminton set",
                     description="badminton raquets and shuttle cock", price="$44.50", category=category1)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=1, name="Snorkeling set", description="Snorkeling gear with earplug",
                     price="$36.95", category=category1)

session.add(categoryItem4)
session.commit()


# Decorative Items
category1 = Category(user_id=1, name="Decorative items")

session.add(category1)
session.commit()


categoryItem1 = CategoryItem(user_id=1, name="Flower Vase", description="Glass vase, metal vase for flowers or to display as themselves",
                     price="$23.95", category=category1)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, name="Painting", description="Oil Painting by a famous artist",
                     price="$64.95", category=category1)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1, name="Decorative bowl", description="decorative bowl made of conch shell",
                     price="$66.95", category=category1)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=1, name="Fridge magnet",
                     description="Customizable fridge magnet", price="$3.95", category=category1)

session.add(categoryItem4)
session.commit()

categoryItem5 = CategoryItem(user_id=1, name="Picture Frames", description="Wooden and glass picture frames",
                     price="$17.95", category=category1)

session.add(categoryItem5)
session.commit()

# Furniture
category1 = Category(user_id=1, name="Furniture")

session.add(category1)
session.commit()


categoryItem1 = CategoryItem(user_id=1, name="Dining Table with 4 chairs", description="Square dining table with 4 chairs made of mahogany",
                     price="$450.95", category=category1)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, name="Book shelf", description="Black wooden book shelf",
                     price="$75.95", category=category1)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1, name="Sofa", description="L shaped sofa for 6 people",
                     price="$890.95", category=category1)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=1, name="Ottoman",
                     description="Ottoman with storage", price="150.95", category=category1)

session.add(categoryItem4)
session.commit()

categoryItem5 = CategoryItem(user_id=1, name="Mobile island for kitchen", description="movable kitchen island with wheels",
                     price="$67.95", category=category1)

session.add(categoryItem5)
session.commit()


print "added menu items!"

