import pytest
from lazebot import report_generator


def test_op_score_report_guild():
    result = report_generator.op_score_report("736645715", True)
    assert result[0] == """\
====  Ops Score Report (RoTE)  ====
Scores reflect how much a guild relies on a player for TB ops. Rare units and higher relics contribute the most.

Score = Estimated crystal cost of replacing ops units"""
    assert result[1] == """\
```Total score for ClanBeroya: 2,192,235

Owio (269812363): 566,731
Δχέ ωΦνέș (242848755): 251,211
Zula Wren (441392819): 108,265
Hero of Narth (839465738): 89,087
Därth Bënji (524218147): 77,299
TwöHearted (385214597): 74,271
Sκγ βεήdέr Unleashed (545547414): 67,266
Cheesecakehunter (113348231): 59,359
Fulcrum Unleashed (173472829): 56,024
DarthTurin (749836178): 55,040
The WerePizza (446346384): 48,839
Laze Bastra (736645715): 45,675
Old Maath (738733632): 45,548
PeJah91 (867284984): 39,244
CatMasters (469438919): 38,752
TajTheRock (989957716): 35,795
Shoiti (699418728): 34,520
Mushima (796382821): 34,006
Benloc0 (673983664): 33,540
Alphaconn (498636777): 29,698
Bao Dur (889253239): 29,507
Papaofmom (559873813): 29,132
DaHa (834194725): 27,229
Jonnovision (428938971): 25,459
theOne X (394849534): 24,119
Elros Elendae (315636959): 23,844
MINIFrothy Walrus (157957918): 22,119
Arcann (138862254): 20,071
Ozzy20 (367558926): 19,857
Xerxo Bodrun (513252419): 19,570
WoSR (244352453): 18,954
SŇydeR (787125778): 18,898
IndySteve (468277145): 16,444
GrandAdmiralWicket (373616324): 16,203
I have iced tea (227854852): 13,617
Caokeo (138488913): 12,932
Bail (945966261): 12,844
This is the way (779751657): 12,145
laitea (152668344): 11,035
Fatesshadow (872319537): 8,627
Mini Bdogg (142711953): 7,587
KeşPanda (124386395): 5,379
The Hermit (129481921): 2,803
Rap Digo (894491986): 1,376
fuzzypickles (463984383): 1,126
Rfox (462362841): 631
E0351 (771747668): 378
Aquafit (317353364): 89
Azrael (734139688): 86
Carl (387674373): 0```"""


def test_op_score_report_guild_max_phase():
    result = report_generator.op_score_report("242848755", True, max_phase=2)
    assert result[0] == """\
====  Ops Score Report (RoTE)  ====
Scores reflect how much a guild relies on a player for TB ops. Rare units and higher relics contribute the most.

Score = Estimated crystal cost of replacing ops units"""
    assert result[1] == """\
```Total score for ClanBeroya: 276,626

Δχέ ωΦνέș (242848755): 35,606
CatMasters (469438919): 26,842
TwöHearted (385214597): 21,905
TajTheRock (989957716): 17,101
Laze Bastra (736645715): 16,396
DaHa (834194725): 15,942
Shoiti (699418728): 11,969
Sκγ βεήdέr Unleashed (545547414): 10,100
Caokeo (138488913): 9,456
Jonnovision (428938971): 9,436
The WerePizza (446346384): 9,031
Xerxo Bodrun (513252419): 8,741
Cheesecakehunter (113348231): 7,743
Ozzy20 (367558926): 6,971
Owio (269812363): 6,835
Zula Wren (441392819): 6,643
Fulcrum Unleashed (173472829): 5,531
SŇydeR (787125778): 4,909
DarthTurin (749836178): 4,506
IndySteve (468277145): 4,167
Fatesshadow (872319537): 4,107
Bao Dur (889253239): 4,094
Därth Bënji (524218147): 3,935
KeşPanda (124386395): 3,654
Mushima (796382821): 3,452
Papaofmom (559873813): 2,771
GrandAdmiralWicket (373616324): 2,771
Hero of Narth (839465738): 2,224
Benloc0 (673983664): 2,148
Alphaconn (498636777): 2,058
Old Maath (738733632): 1,757
Rap Digo (894491986): 1,376
fuzzypickles (463984383): 763
Elros Elendae (315636959): 626
theOne X (394849534): 268
E0351 (771747668): 257
PeJah91 (867284984): 181
This is the way (779751657): 89
Aquafit (317353364): 89
Mini Bdogg (142711953): 89
Azrael (734139688): 86
MINIFrothy Walrus (157957918): 0
I have iced tea (227854852): 0
The Hermit (129481921): 0
Carl (387674373): 0
Bail (945966261): 0
Arcann (138862254): 0
laitea (152668344): 0
Rfox (462362841): 0
WoSR (244352453): 0```"""


def test_op_score_report_player():
    result = report_generator.op_score_report("242848755", False)
    assert result[0] == """\
====  Ops Score Report (RoTE)  ====
Scores reflect how much a guild relies on a player for TB ops. Rare units and higher relics contribute the most.

Score = Estimated crystal cost of replacing ops units"""
    assert result[1] == """\
```Total score for Δχέ ωΦνέș: 251,211

Units:
Darth Malgus: 16,488
  11 req in P6 @ R9
  backups = R8, R8, R8, R7, R7
General Kenobi: 15,510
  4 req in P6 @ R9
  backups = R8, R8, R8, R8, R8
Krrsantan: 15,510
  1 req in P6 @ R9
  backups = R8, R8, R8, R8, R8
Lord Vader: 15,510
  10 req in P6 @ R9
  backups = R8, R8, R8, R8, R8
Chirrut Îmwe: 13,125
  3 req in P3 @ R7
  backups = R2, R0, G12, G12, G12
Royal Guard: 12,392
  1 req in P6 @ R9
  backups = R9, R7, R7, R7, R7
Nightsister Acolyte: 10,745
  1 req in P3 @ R7
  backups = R7, G12, G12, G12, G12
Teebo: 10,745
  1 req in P3 @ R7
  backups = R7, G12, G12, G12, G12
Boba Fett, Scion of Jango: 10,220
  6 req in P4 @ R8
  backups = R7, R7, R7, R7, R6
Ki-Adi-Mundi: 10,099
  2 req in P4 @ R8
  backups = R7, R7, R7, R7, R7
Starkiller: 10,099
  13 req in P4 @ R8
  backups = R7, R7, R7, R7, R7
Kylo Ren (Unmasked): 9,785
  1 req in P5 @ R9
  backups = R9, R8, R7, R7, R7
Luminara Unduli: 7,831
  1 req in P3 @ R7
  backups = R7, R1, G12, G12, G12
Jolee Bindo: 6,521
  3 req in P3 @ R7
  backups = R5, R5, R5, R5, R5
Kyle Katarn: 6,521
  3 req in P3 @ R7
  backups = R5, R5, R5, R5, R5
Ben Solo: 4,887
  6 req in P4 @ R8
  backups = R8, R7, R7, R7, R7
Wampa: 4,887
  1 req in P4 @ R8
  backups = R9, R7, R7, R7, R7
Young Han Solo: 4,673
  1 req in P3 @ R7
  backups = R7, R5, R5, G12, G12
Logray: 4,301
  5 req in P3 @ R7
  backups = R7, R6, R3, G12, G12
Imperial Probe Droid: 4,112
  4 req in P2 @ R6
  backups = R6, R3, R1, G12, G12
Paploo: 3,919
  1 req in P1 @ R5
  backups = R3, R3, R3, G12, G12
Hoth Rebel Soldier: 3,558
  1 req in P3 @ R7
  backups = R8, R7, R1, G12, G12
Rey: 3,502
  11 req in P6 @ R9
  backups = R9, R9, R8, R8, R8
Sith Assassin: 3,502
  1 req in P5 @ R9
  backups = R9, R9, R8, R8, R8
Ewok Elder: 3,464
  1 req in P3 @ R7
  backups = R7, R7, R2, G12, G12
Dark Trooper: 2,280
  1 req in P4 @ R8
  backups = R8, R8, R7, R7, R7
Darth Vader: 2,280
  1 req in P4 @ R8
  backups = R8, R8, R7, R7, R7
Maul: 2,280
  6 req in P4 @ R8
  backups = R8, R8, R7, R7, R7
Clone Sergeant - Phase I: 2,082
  3 req in P3 @ R7
  backups = R7, R6, R6, R5, R5
Jawa Engineer: 1,992
  1 req in P1 @ R5
  backups = R5, R5, R2, G12, G12
Hoth Rebel Scout: 1,730
  2 req in P3 @ R7
  backups = R7, R7, R5, R3, R3
Zaalbar: 1,598
  1 req in P2 @ R6
  backups = R6, R5, R5, R3, R3
Plo Koon: 1,520
  1 req in P3 @ R7
  backups = R7, R7, R5, R5, R4
Barriss Offee: 1,472
  1 req in P3 @ R7
  backups = R7, R7, R5, R5, R5
Tusken Raider: 1,472
  2 req in P3 @ R7
  backups = R7, R7, R5, R5, R5
Darth Traya: 1,472
  1 req in P3 @ R7
  backups = R8, R7, R5, R5, R5
Enfys Nest: 1,472
  1 req in P3 @ R7
  backups = R7, R7, R5, R5, R5
Vandor Chewbacca: 1,341
  1 req in P2 @ R6
  backups = R6, R5, R5, R5, R5
Kuiil: 1,341
  1 req in P2 @ R6
  backups = R6, R5, R5, R5, R5
Resistance Hero Poe: 1,115
  1 req in P3 @ R7
  backups = R7, R7, R6, R5, R5
Resistance Hero Finn: 1,115
  1 req in P3 @ R7
  backups = R7, R7, R6, R5, R5
The Mandalorian (Beskar Armor): 977
  1 req in P4 @ R8
  backups = R9, R8, R8, R7, R7
Jedi Knight Luke Skywalker: 977
  4 req in P4 @ R8
  backups = R8, R8, R8, R7, R7
Pao: 807
  1 req in P2 @ R6
  backups = R6, R6, R5, R4, R3
Admiral Ackbar: 711
  1 req in P2 @ R6
  backups = R8, R6, R5, R5, R3
Ezra Bridger: 711
  1 req in P2 @ R6
  backups = R7, R6, R5, R5, R3
Hunter: 631
  1 req in P3 @ R7
  backups = R7, R7, R7, R5, R5
Cara Dune: 631
  1 req in P3 @ R7
  backups = R7, R7, R7, R5, R5
Obi-Wan Kenobi (Old Ben): 631
  2 req in P3 @ R7
  backups = R7, R7, R7, R5, R5
Wrecker: 631
  1 req in P3 @ R7
  backups = R9, R7, R7, R5, R5
Mother Talzin: 631
  1 req in P3 @ R7
  backups = R7, R7, R7, R5, R5
Greef Karga: 626
  2 req in P2 @ R6
  backups = R6, R6, R5, R5, R5
L3-37: 626
  2 req in P2 @ R6
  backups = R7, R6, R5, R5, R5
Veteran Smuggler Chewbacca: 626
  1 req in P2 @ R6
  backups = R6, R6, R5, R5, R5
Death Trooper: 626
  2 req in P2 @ R6
  backups = R7, R6, R5, R5, R5
Talia: 506
  1 req in P1 @ R5
  backups = R7, R7, R5, R5, G12
B1 Battle Droid: 363
  1 req in P3 @ R7
  backups
---------- truncated ----------```"""


def test_op_score_report_player_max_phase():
    result = report_generator.op_score_report("242848755", False, max_phase=2)
    assert result[0] == """\
====  Ops Score Report (RoTE)  ====
Scores reflect how much a guild relies on a player for TB ops. Rare units and higher relics contribute the most.

Score = Estimated crystal cost of replacing ops units"""
    assert result[1] == """\
```Total score for Δχέ ωΦνέș: 35,606

Units:
Teebo: 8,930
  1 req in P2 @ R6
  backups = R7, G12, G12, G12, G12
Imperial Probe Droid: 4,112
  4 req in P2 @ R6
  backups = R6, R3, R1, G12, G12
Paploo: 3,919
  1 req in P1 @ R5
  backups = R3, R3, R3, G12, G12
Young Han Solo: 2,859
  1 req in P2 @ R6
  backups = R7, R5, R5, G12, G12
Boba Fett, Scion of Jango: 2,771
  12 req in P2 @ R6
  backups = R5, R5, R5, R5, R5
Jawa Engineer: 1,992
  1 req in P1 @ R5
  backups = R5, R5, R2, G12, G12
Zaalbar: 1,598
  1 req in P2 @ R6
  backups = R6, R5, R5, R3, R3
Vandor Chewbacca: 1,341
  1 req in P2 @ R6
  backups = R6, R5, R5, R5, R5
Kuiil: 1,341
  1 req in P2 @ R6
  backups = R6, R5, R5, R5, R5
Pao: 807
  1 req in P2 @ R6
  backups = R6, R6, R5, R4, R3
Admiral Ackbar: 711
  1 req in P2 @ R6
  backups = R8, R6, R5, R5, R3
Ezra Bridger: 711
  1 req in P2 @ R6
  backups = R7, R6, R5, R5, R3
Greef Karga: 626
  2 req in P2 @ R6
  backups = R6, R6, R5, R5, R5
L3-37: 626
  2 req in P2 @ R6
  backups = R7, R6, R5, R5, R5
Veteran Smuggler Chewbacca: 626
  1 req in P2 @ R6
  backups = R6, R6, R5, R5, R5
Enfys Nest: 626
  1 req in P2 @ R6
  backups = R7, R7, R5, R5, R5
Death Trooper: 626
  2 req in P2 @ R6
  backups = R7, R6, R5, R5, R5
Talia: 506
  1 req in P1 @ R5
  backups = R7, R7, R5, R5, G12
Mon Mothma: 268
  1 req in P2 @ R6
  backups = R7, R6, R6, R5, R5
Sabine Wren: 257
  1 req in P1 @ R5
  backups = R5, R5, R5, R3, R3
Droideka: 89
  1 req in P2 @ R6
  backups = R7, R7, R6, R6, R5
B2 Super Battle Droid: 89
  2 req in P2 @ R6
  backups = R6, R6, R6, R6, R5
The Mandalorian: 89
  1 req in P2 @ R6
  backups = R8, R8, R7, R6, R5
Logray: 86
  3 req in P1 @ R5
  backups = R7, R7, R7, R6, R3```"""


def test_op_score_report_player_non_verbose():
    result = report_generator.op_score_report("242848755", False, verbose=False)
    assert result[0] == """\
====  Ops Score Report (RoTE)  ====
Scores reflect how much a guild relies on a player for TB ops. Rare units and higher relics contribute the most.

Score = Estimated crystal cost of replacing ops units"""
    assert result[1] == """\
```Total score for Δχέ ωΦνέș: 251,211

Units:
Darth Malgus: 16,488
General Kenobi: 15,510
Krrsantan: 15,510
Lord Vader: 15,510
Chirrut Îmwe: 13,125
Royal Guard: 12,392
Nightsister Acolyte: 10,745
Teebo: 10,745
Boba Fett, Scion of Jango: 10,220
Ki-Adi-Mundi: 10,099
Starkiller: 10,099
Kylo Ren (Unmasked): 9,785
Luminara Unduli: 7,831
Jolee Bindo: 6,521
Kyle Katarn: 6,521
Ben Solo: 4,887
Wampa: 4,887
Young Han Solo: 4,673
Logray: 4,301
Imperial Probe Droid: 4,112
Paploo: 3,919
Hoth Rebel Soldier: 3,558
Rey: 3,502
Sith Assassin: 3,502
Ewok Elder: 3,464
Dark Trooper: 2,280
Darth Vader: 2,280
Maul: 2,280
Clone Sergeant - Phase I: 2,082
Jawa Engineer: 1,992
Hoth Rebel Scout: 1,730
Zaalbar: 1,598
Plo Koon: 1,520
Barriss Offee: 1,472
Tusken Raider: 1,472
Darth Traya: 1,472
Enfys Nest: 1,472
Vandor Chewbacca: 1,341
Kuiil: 1,341
Resistance Hero Poe: 1,115
Resistance Hero Finn: 1,115
The Mandalorian (Beskar Armor): 977
Jedi Knight Luke Skywalker: 977
Pao: 807
Admiral Ackbar: 711
Ezra Bridger: 711
Hunter: 631
Cara Dune: 631
Obi-Wan Kenobi (Old Ben): 631
Wrecker: 631
Mother Talzin: 631
Greef Karga: 626
L3-37: 626
Veteran Smuggler Chewbacca: 626
Death Trooper: 626
Talia: 506
B1 Battle Droid: 363
Aurra Sing: 363
Mon Mothma: 268
Sabine Wren: 257
First Order SF TIE Pilot: 210
0-0-0: 210
Savage Opress: 210
Grand Admiral Thrawn: 121
Bastila Shan (Fallen): 121
Droideka: 89
B2 Super Battle Droid: 89
The Mandalorian: 89```"""
