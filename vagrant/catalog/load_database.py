from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_database import ArmorType, WeaponType, Armor, Weapon, Base

engine = create_engine('sqlite:///pathofexile.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

bow = WeaponType(name="Bow")
session.add(bow)
session.commit()

claw = WeaponType(name="Claw")
session.add(bow)
session.commit()

dagger = WeaponType(name="Dagger")
session.add(bow)
session.commit()

bodyArmor = ArmorType(name="Body Armor")
session.add(bow)
session.commit()

boots = ArmorType(name="Boots")
session.add(bow)
session.commit()

gloves = ArmorType(name="Gloves")
session.add(bow)
session.commit()

plateVest = Armor(name="Plate Vest", armorType=bodyArmor, reqLevel=1, armorAmount=14, evasionRating=0,
                  energyShield=0, reqStrength=12, reqDexterity=0, reqIntelligence=0)
session.add(plateVest)
session.commit()

ironGreaves = Armor(name="Iron Greaves", armorType=boots, reqLevel=1, armorAmount=6, evasionRating=0,
                  energyShield=0, reqStrength=8, reqDexterity=0, reqIntelligence=0)
session.add(ironGreaves)
session.commit()

ironGauntlets = Armor(name="Iron Gauntlets", armorType=gloves, reqLevel=1, armorAmount=6, evasionRating=0,
                  energyShield=0, reqStrength=6, reqDexterity=0, reqIntelligence=0)
session.add(plateVest)
session.commit()

crudeBow = Weapon(name="Crude Bow", weaponType=bow, reqLevel=1, minDamage=5, maxDamage=13, attacksPerSecond=1.4,
                  damagePerSecond=12.6, reqStrength=0, reqDexterity=14, reqIntelligence=0)
session.add(crudeBow)
session.commit()

nailedFist = Weapon(name="Nailed Fist", weaponType=claw, reqLevel=1, minDamage=4, maxDamage=11, attacksPerSecond=1.6,
                    damagePerSecond=12.0, reqStrength=0, reqDexterity=11, reqIntelligence=11)
session.add(nailedFist)
session.commit()

glassShank = Weapon(name="Glass Shank", weaponType=dagger, reqLevel=1, minDamage=6, maxDamage=10, attacksPerSecond=1.5,
                    damagePerSecond=12.0, reqStrength=0, reqDexterity=9, reqIntelligence=6)
session.add(crudeBow)
session.commit()
