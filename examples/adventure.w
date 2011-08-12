# An Adventure-style game for Wheeler
# Inspiration (but not implementation) drawn from Dennis Merritt's "Adventure in Prolog". Props.

transition (pattern begin game) (action intro1)

transition (pattern intro1) (action print "Adventure in Wheeler" intro2)
transition (pattern intro2) (action print "-------------------------------" intro3)
transition (pattern intro3) (action print "You are a young detective named Trixie. You are trying to find " intro4)
transition (pattern intro4) (action print "your friend Honey after her mysterious disappearance this morning." intro5)
transition (pattern intro5) (action print "You are standing in the foyer of Honey's house, a modest mansion in " intro6)
transition (pattern intro6) (action print "the countryside. You are facing east.")

# Get the party started
begin game

