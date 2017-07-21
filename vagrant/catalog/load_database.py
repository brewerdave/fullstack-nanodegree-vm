#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_database import Base, CharacterClass, GameVersion, Build, User

engine = create_engine('sqlite:///pathofexile.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

marauder = CharacterClass(name="Marauder")
session.add(marauder)
session.commit()

duelist = CharacterClass(name="Duelist")
session.add(duelist)
session.commit()

ranger = CharacterClass(name="Ranger")
session.add(ranger)
session.commit()

shadow = CharacterClass(name="Shadow")
session.add(shadow)
session.commit()

witch = CharacterClass(name="Witch")
session.add(witch)
session.commit()

templar = CharacterClass(name="Templar")
session.add(templar)
session.commit()

scion = CharacterClass(name="Scion")
session.add(scion)
session.commit()

version1 = GameVersion(name="1.0")
session.add(version1)
session.commit()

version2 = GameVersion(name="1.1")
session.add(version2)
session.commit()

version3 = GameVersion(name="1.2")
session.add(version3)
session.commit()

version4 = GameVersion(name="1.3")
session.add(version4)
session.commit()

version5 = GameVersion(name="2.0")
session.add(version5)
session.commit()

version6 = GameVersion(name="2.1")
session.add(version6)
session.commit()

version7 = GameVersion(name="2.2")
session.add(version7)
session.commit()

version8 = GameVersion(name="2.3")
session.add(version8)
session.commit()

version9 = GameVersion(name="2.4")
session.add(version9)
session.commit()

version10 = GameVersion(name="2.5")
session.add(version10)
session.commit()

version11 = GameVersion(name="2.6")
session.add(version11)
session.commit()

version12 = GameVersion(name="3.0")
session.add(version12)
session.commit()

user1 = User(name="David Brewer", email="brewerdavidalan@gmail.com",
             picture="https://lh4.googleusercontent.com/-YgQaZfQ_l28/AAAAAAAAAAI/AAAAAAAAABw/43vQlNZ2-Uw/photo.jpg")
session.add(user1)
session.commit()

build1 = Build(title="Sarang's Endgame TS/LA/Barrage Archer | Pathfinder | Crit Bow | Videos | Budget Version",
               author="_Saranghaeyo_",
               character_class_name="Ranger",
               short_description="Fun lightning bow build ",
               long_description="""Hello everyone, I'm _Saranghaeyo_.

This is my Endgame TS/LA/Barrage Archer. I've been playing since Torment League (Patch 1.3) where I started as a Tornado Shot/Puncture Ranger and I've loved the build ever since. Since then I've put countless hours into Bow Attack builds with various classes and gear sets over Standard and many challenge leagues. It is my favorite character archetype in Path of Exile.

I have no claims that this is a must-follow optimal gear/tree configuration, as your style and preferences may differ. Many of the concepts here are slowly becoming general knowledge.

This guide is intended for experienced users who are comfortable with playing as a Pathfinder, mainly the Flask-management playstyle but also life-based. The budget is not intended to include Legacy items. If you aren't a fan of any of those aspects, then this guide may not be for you. Instead, here are some very strong alternatives:

https://www.pathofexile.com/forum/view-thread/1745340 >>> blasting_cap's SignalShot (CI Pathfinder)

https://www.pathofexile.com/forum/view-thread/1744275 >>> Dzz1rt's Crit Archer (Life Pathfinder, Expensive & Min-Max'ed)

https://www.pathofexile.com/forum/view-thread/1782214 >>> Nephalim's LA Ghost Raider (Life Raider, Very Strong Endgame Raider)


xeTiW0H

Archers gained some amazing offensive weapons in Patch 2.6, although on the defensive front, especially Life Pool, there wasn't a lot of help given. In the current state, CI/ES builds reign supreme with their ability to create a very large EHP pool. I am hoping for some changes and looking forward to Patch 3.0 and/or the beta.

There was no hindrance to the 100% Elemental Damage Conversion strategy, and in fact with the new Primeval Force Cluster this strategy becomes even stronger:

c6d496f306

We also gained an incredibly powerful weapon in terms of Flasks:

Verified


Rewarding the juggling of resistances to pay off in a big way, with more Elemental Damage penetration. Other major changes to the tree was changing Blood Drinker to "Attack Damage" instead of "Physical Attack Damage," allowing us to not path as awkwardly to the newly changed Duelist Leech area. These changes are reflected in the tree updates.


Y5C30yh

If you do not feel like reading further, my current Gear, Flasks, and Jewels are posted. This section is always being refined.

WGCESAA

Standard Gear, Updated 4/8/2017



o91gLSj

What an amazing tool for us to use here: https://www.pathofexile.com/forum/view-thread/1716360

This allows us to take a more in-depth look at this style of character, including what the actual DPS numbers are. The number of arrows granted in this build through items like a Barrage Helm Enchant, Dying Sun, +1 Quiver, are huge multipliers for our damage that Tooltip DPS in-game does not represent. It is also the primary reason Death's Opus is so underrated, along with its +150% Crit Multiplier.

This Path of Building loadout includes:

    All the example gear you see above
    The example Passive Tree provided
    Well-rolled Chin Sol, Well-rolled Lioneye's Glare, Dummy 370 pDPS bow is 8.7% Crit Base



You can tweak the mods in each of the gear pieces, or even input your own items to see what the best upgrades would be for you. Remember to activate in the configurations things like Power Charges, Range = 0 if you are using Chin Sol, and so forth.

Pastebin Code



H4uFO8z

The following are Gameplay Videos from Patch 2.6.
I upload videos to my Plays.tv Channel here: http://plays.tv/u/SarangPOE


The Shaper

https://plays.tv/s/LD_qEJ9yVsil >>> Deathless Shaper Run


Guardian Fights

https://plays.tv/s/LD_qbyaaS7Ox >>> Lair of the Hydra

https://plays.tv/s/LD_qfkspCYXV >>> Maze of the Minotaur (Good speed run, ~1:40 from entering map to kill)

https://plays.tv/s/LD_qjN7sKabI >>> Forge of the Phoenix

https://plays.tv/s/LD_qnV4Vf1Cj >>> Pit of the Chimera (Bad fog RNG, had to portal one time)


fyBACjV

    Maximize Critical Strike Chance
    100% Conversion of Physical Damage to Elemental & Scaling



To me, these are the two core things we can focus on to maximize our damage output. Maximizing Critical Strike Chance seems like a no-brainer but from my experience it is the #1 thing that people just ignore. If you take so many passives in a tree for Critical Strike Chance/Critical Strike Multiplier, you are doing yourself a disservice by failing to optimize for it. Do what you have to in order to reach the Critical Strike Chance Cap. See the spoiler for how your Crit Chance is affected by a Diamond Flask.

Verified
Verified


Diamond Flask Augmentation Table


How to scale damage? It is now moreso becoming common knowledge but in the current state of the game we have excellent opportunities to take Physical Damage, convert it all to Elemental Damage, and scale it hard with Multipliers, especially the WED Gem + Frenzy Charges. That is how we get a large portion of our end-game level of damage. Elemental Damage Penetration from sources such as Boot Enchantments or the Lightning Penetration version of Vessel of Vinktar are also able to augment our damage in ways tooltip DPS does not show.

Verified


We were already familiar with PTL + WED, just add in a Signal Fire and you'll be doing all Elemental Damage, which takes advantage of all of your Increased Physical Damage, Projectile Damage, Elemental Damage modifiers, and so forth. With Pathfinder offering ways to reduce Utility Flask usage, we replace those Utility Flasks with more offensive ones:




Offensive Screenshots



l22IDAq

    Layered Defenses
    Instant Leech
    Life Pool



Survive with Layered Defenses. With current Gear/Tree & Flasks,

    6.8K Life Pool with non-Legacy Kaom's Heart, 6K Life with Belly of the Beast
    20K+ Evasion w/ Jade Flask
    Acrobatics + Phase Acrobatics Keystones
    Arrow Dancing Keystone
    Movement Speed
    Life/Mana on Kill with Assassin's Mark Curse on Hit
    Flasks uptime grants us Resistances, more damage, and more to instantly leech.



Speaking of Instant Leech...



Convert damage to Lightning, get a massive leech amount from Lightning Damage. The Non-Legacy versions of this Flask may not have full uptime, but the effect is very strong when you do. Having these defenses, as well as Instant Leech at such a ridiculous amount, protects us from Reflect. I don't recommend doing a Reflect Map, but you can survive through any instant where you may encounter Reflect monsters.



We do NOT use an Evasion Chest. I believe that Evasion stacking on gear is pretty dead in the current state of the game. You can stack as much as you want, but it will never have the same effect as truly increasing your life pool. There are enough secondary forms of damage which cannot be Evaded or Dodged, that pure evasion will never save you from. Also, as Flasks become more powerful, a single Jade Flask of Reflexes is able to emulate an entire body of Evasion:




dRVdOcq

Several trees are included below.

Bandits


Ascendancy



Default Tree - With Lioneye's Fall Jewel

Conditions: Have Atziri's Acuity, Have Lioneye's Fall Jewel

Spoiler



End-Game Tree w/ Vaal Pact

Conditions: Does not have Atziri's Acuity

Spoiler



End-Game "Traditional" Style Tree

Conditions: Have Atziri's Acuity, feels comfortable with lower life total

Spoiler



End-Game "Traditional" Style Tree v2

Conditions: Have Atziri's Acuity, farms content where Frenzy/Power charges are not always up, such as Shaper, Uber Lab, etc

Spoiler
☆ 2.6 Endgame TS/LA/Barrage Archer (Pathfinder) ☆ /// 1711388 (ACTIVE)

IRL Stuff, waiting for 3.0
Last edited by _Saranghaeyo_ on Apr 23, 2017 9:41:49 PM
Last bumped on Jul 10, 2017 7:48:21 PM
	
Avatar
Posted by Completed 40 Challenges_Saranghaeyo_
on Aug 13, 2016 11:56:55 PM
Quote
UXWoUCE

A budget gear set for this build can be put together. It can be a very good budget option and/or League starter. While testing this setup, I found Raider to be pretty strong here. You can start as either class, and switch Ascendancy later. Raider has an advantage on a low budget because your only source of Instant Leech is either Vaal Pact or Atziri's Acuity, and Vaal Pact + Blood Rage creates very uncomfortable gameplay. Raider's automatic Frenzy Charge generation bypasses this weakness.

As a budget character, consider this a transition phase between upgrades and the ability to reach all end-game content. It's unlikely to take on Guardians or Shaper with this gear, but to help you farm to get there.

This is what you should expect to do with budget gears:

    Up to T13 Maps Comfortably
    T14 & T15 Maps with some kiting/manual dodging
    Uber Labyrinth with certain Modifiers (NOT a dedicated Uber Lab farmer)
    Normal Atziri
    Other lower level boss instances, such as Normal Rigwald & The Pale Court




Example Gear - 5L Death Opus


Cost Breakdown


Example Videos - Budget Gear



Just like most bow builds, use your Flasks, attack with your Lightning Arrow or Tornado Shot (Links are both shown in the sample gear) to clear trash, and use Barrage as a strong Single Target skill.

Curse on Hit with Assassin's Mark will allow us to keep our Power Charges up. I dislike manual cursing or Frenzy Charge generation (with the skill itself). In the time that it takes you to fire your Frenzy with Curse on Hit and GMP, you could just fire 2 attacks and kill the targets in the same amount of time. The Raider Ascendancy allows us to bypass manual generation of Frenzy charges; with Way of the Poacher, this is free as well, so no need to risk using Blood Rage and having your health dip in between packs.

Gearing wise, I found it much more successful to go for Rare, Tri-Resist Gloves/Belt/Boots than seeing most beginning players go for items like Atziri's Step, and so forth. The biggest reason for me is that Jewelry with Flat Physical Damage and WED can provide so much damage for even the poorest of builds, and when you are struggling to cap your resistances, Jewelry options with both DPS mods and Resistances aren't cheap.


XCzzd4K

For leveling, get raw damage and life first, and Crit comes much later on. Gearing requires some stats, so if you follow this rule, we need to prioritize STR/DEX first, and then INT later. So starting in Ranger, moving to Duelist, and finishing off in Shadow is my preferred way to level.

First 29 Passive Points Used


Next 18 Passive Points, 47 Points Used


Next 22 Passive Points, 69 Points Used


Next 23 Passive Points, 92 Points Used


When you get Atziri's Acuity, you can connect to Shadow via the right side of the skill tree (saves points). My personal preference for the last things to pick up are Point Blank (when you progress into higher content or commit to boss killing), Frenzy Charges, and Jewel Sockets that take 3 points to travel to.


JTnOvk0

Video Archive - Patch 2.4

Spoiler


Video Archive - Patch 2.4 Testing

Spoiler


Video Archive - Patch 2.3

Spoiler



Old Research Topic from Patch 2.0

Spoiler


Post always WIP.""",
               url="https://www.pathofexile.com/forum/view-thread/1711388",
               game_version="2.6",
               user_id=1)
session.add(build1)
session.commit()

build2 = Build(title="Pizza Sticks: Flameblast Totem Inquisitor/Hierophant",
               author="viperesque",
               character_class_name="Templar",
               short_description="Good build for HC SSF ",
               long_description="""1. BUILD CONCEPT

Flameblast charges up while you channel it, increasing in damage and AoE the longer you hold it before releasing. Traditional Flameblast builds have struggled with the awkwardness of standing still for such a long period of time. This build does away with that by having totems do it for us, letting us run around at our leisure while our totems blow up the whole screen.

Flameblast also faces issues with reflect due to its high damage per hit. Again, totems deal with this by tanking the reflected damage for us. This also allows us to go crit with no fear.

Totems pretty much solve all of Flameblast's problems. It's a match made in heaven.


2. WHY PLAY THE BUILD? (PROS AND CONS)

Pros:

    Very high damage. Current statistics: ~110k DPS per totem with Increased AoE, ~175k per totem with Conc. Effect for single target. Most bosses die in under five seconds, most other things get one-shot.
    Large area of effect, enough to one-shot entire packs of monsters.
    Whirling Blades access + Inquis attack speed for zippy clearing.
    Can do literally all map mods.
    Confirmed sub-5-minute Atziri, haven't been able to test harder endgame boss fights yet but they should in theory be fine.
    Totems are naturally safe - you're reflect immune, don't have to stand still to deal damage, and have extreme range (even more extreme for Flameblast because the totem will cast if the edge of a blast centred at its max range will hit a mob).
    No unique items required or even particularly recommended.
    Straightforward, hardcore viable, beginner friendly, self-found friendly build. If you're new to Path of Exile and have any extra questions or don't really follow anything in this guide, PM me and I'll do my best to help!


Cons:

    Very, very dependent on cast speed due to needing to hit 10 Flameblast stacks before the totem will release. Can feel quite clunky without sufficiently increased cast speed (pretty much anything under 100%).
    Requires CI to do the hardest endgame content safely - life-based version is much cheaper but can't achieve the same levels of tankiness, although the natural safety of totems offsets this to a large extent.
    Totem playstyle is offputting to many people. Hopefully I can win a few of you over with this build!




3. ASCENDANCY CHOICE, SKILL TREE AND BANDITS

Inquisitor or Hierophant? Elementalist???

Inquisitor has massive damage thanks to resistance penetration, extra crit, a bunch of cast speed and the more damage aura. For killing bosses, Inquisitor is unquestionably the best choice.

Hierophant has slightly better clear speed (4 totems lends itself to a much more fire and forget playstyle) and is slightly more defensive thanks to mini-MoM and the extra totems providing distractions to mobs. I personally prefer Inquisitor even for lower content, but that's just me. If you want to Hiero, go ahead.

Couple of (imperfect) Inquis vs Hiero comparison videos: Gorge run, T15 Daresso kill

RaizQT published a video explaining at some length why he prefers noncrit Elementalist to Inquisitor. He makes some poor assumptions (e.g. that this build can't reach 95% crit chance, or sacrifices defenses compared to his), but has some very good points. He avoided the maths in his video, but let me lay it all out here (huge shout-outs to Openarl for making Path of Building and letting us theorycrafters do stuff like this with ease).

Inquis damage stats (6L in real conditions, against a boss, with all buffs active):

E2dPcDl

Elementalist damage stats (6L in real conditions, against a boss, with all buffs active):

LqRx7CK

Remember that the initial hit DPS is multiplied by 2 thanks to dual totems.

Sum all that and you get that Inquis deals ~510k DPS vs Elementalist's ~271k. The damage is MUCH closer against regular mobs but the inbuilt resistance and curse effect reduction of bosses kind of wrecks the Elementalist version. However, that is not an entirely fair comparison because of Shaper of Desolation. If you assume that the Elementalist version is consistently shocking (a pretty reasonable assumption against all but the biggest and meanest bosses), then:

6Gegx79

490k total DPS, very comparable. Just not reliable against anything with over 1.5 million life, or ignite immunity.

Other than that, Elementalist gets free prolif and occasional AoE (both very strong, though not asstrong as in most builds due to Flameblast's already massive AoE), Inquis gets faster movement, quality of life from higher cast speed and ele damage reduction, and everything else is almost identical (at least for the respective CI versions). I'll let you decide which you prefer based on this information.

Life or CI?

CI can be thought of as the final form of the build. It has more survivability and more damage (although Tukohama's Fortress can actually let the life version outstrip CI in damage). However, CI is expensive. If you're starting a league or don't intend to accumulate large amounts of currency, go for life. If you're serious about getting to red maps and Shaper, aim for CI. You can always swap from one to the other for a middling amount of regrets.

Trees

This section only shows final skill trees. For advice on what to prioritise while levelling, see section 6: "Levelling Tips".

Life-Based (Hybrid) Skill Tree

Level 90 skill tree (or Tukohama's Fortress version)

Normal: Help Oak (+40 maximum life)
Cruel: Help Alira (5% increased cast speed)
Merciless: Help Alira (+1 maximum power charge)

Energy Shield-Based (CI) Skill Tree

Level 90 skill tree

Normal: Kill all (+1 skill point)
Cruel: Help Alira (5% increased cast speed)
Merciless: Help Alira (+1 maximum power charge)


4. GEARING RECOMMENDATIONS

Life-Based


Energy Shield-Based (CI)



5. GEMS

Flameblast - Spell Totem - Faster Casting - Increased Area of Effect(/Concentrated Effect) - Increased Critical Strikes - Controlled Destruction(/Elemental Proliferation)

Primary damage setup. Gems are listed in order of importance, e.g. drop Controlled Destruction if you only have a 5L. Concentrated Effect should be kept handy for high-life bosses, although you won't need it for most boss fights. Elemental Proliferation is an option if you want to improve your clear speed, although you definitely want to swap off it for boss fights. I personally find it unnecessary but many swear by it, and it's particularly good for huge swarms of mobs such as breaches.

Anger - Discipline - Summon Lightning Golem

Auras and buffs. Clarity is not necessary due to the extremely low mana cost of Flameblast totems, but feel free to run it if you really want to. The life version can replace Discipline with whatever 35% or less aura you like (e.g. Blasphemy Enfeeble), but it's still good.

Whirling Blades/Shield Charge - Faster Attacks - Fortify(/Blood Magic)

Primary movement. Blood Magic is helpful if you don't run Clarity (but please don't try to use it if you're CI!). You can also run this in a 4L and use both Blood Magic and Fortify.

Flame Dash - Faster Casting

Something to get over walls. Can use Lightning Warp - Less Duration - Fasting Casting if preferred.

Orb of Storms - Power Charge on Critical - Curse on Hit - Temporal Chains

Amazing power charge generation and free curse application. Feel free to swap out the curse to whatever you fancy.

There are some leftover slots here. Fill them with whatever takes your fancy (e.g. a CwDT setup, Vaal Haste, Vaal Discipline). No other gems are particularly important to this build.



6. LEVELLING TIPS

Life-Based


Energy Shield-Based (CI)




7. PLAYSTYLE

This is just a few general tips on how to play the build. To get a better impression of what it feels like overall, head to the videos section.

    Hang back and drop totems if you're scared. In low level content you can whirl along without care, but when in doubt let your totems scout out for you.
    One totem is sufficient to kill packs. Don't waste time dropping both for a single pack.
    While waiting for your totems to kill everything, you can curse mobs or spam Ice Spears to generate power charges.
    Without Clarity, mana may be a small issue despite the low cost of your totems. Mana regen on gear is nice.
    Map mods of note: Reduced/no regen (bring a mana flask and be wary of long ES recharge times), elemental reflect (your totems will one-shot themselves so be ready to recast them constantly).




8. REPRESENTATIVE STATS

Life-Based (Slightly Outdated)


Energy Shield-Based (CI)



9. VIDEOS

Many excellent videos courtesy of blajo (linked with permission):

Shaper Run

Uber Atziri Run

Phoenix Run
Minotaur Run
Hydra Run
Chimera Run

Chayula's Domain Run
Normal Atziri Run
Uber Lab Run

Inquis/Hiero comparions videos (mine):


Inquis vs Hiero: T13 Gorge Run

Inquis vs Hiero: T15 Daresso kill


Thanks for reading, and I hope this guide has been useful to you!
Have you done something awesome with Sire of Shards? PM me and tell me all about it!
Last edited by viperesque on Jul 10, 2017 12:06:58 AM
Last bumped on Jul 16, 2017 10:31:34 PM""",
               url="https://www.pathofexile.com/forum/view-thread/1730745",
               game_version="2.6",
               user_id=1)
session.add(build2)
session.commit()
