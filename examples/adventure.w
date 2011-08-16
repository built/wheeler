# An Adventure-style game for Wheeler
# Inspiration (but not implementation) drawn from Dennis Merritt's "Adventure in Prolog". Props.

# THIS CODE DOES NOT WORK AS OF YET. This is an ongoing example and exploration. Bear with me.

# Introduce the game:
transition (pattern begin game) (action intro1)

transition (pattern intro1) (action print "Adventure in Wheeler" intro2)
transition (pattern intro2) (action print "-------------------------------" intro3)
transition (pattern intro3) (action print "You are a young detective named Trixie. You are trying to find " intro4)
transition (pattern intro4) (action print "your friend Honey after her mysterious disappearance this morning." intro5)
transition (pattern intro5) (action print "You are standing in the foyer of Honey's house, a modest mansion in " intro6)
transition (pattern intro6) (action print "the countryside. You are facing east.")


# List our rooms
room Conservatory
room Porch
room Foyer
room "Great Hall"
room Study
room Parlor
room "Dining Room"
room "Servant's Quarters"
room Kitchen

# Seems to be a bug where string literals aren't properly being identified as strings
string Conservatory
string Porch
string Foyer
string "Great Hall"
string Study
string Parlor
string "Dining Room"
string "Servant's Quarters"
string Kitchen

# Establish the relationships between any adjoining rooms.
Porch Foyer

"Great Hall" Foyer
"Great Hall" Conservatory
"Great Hall" Parlor
"Great Hall" Kitchen
"Great Hall" "Dining Room"
"Great Hall" "Servant's Quarters"

Parlor Study Conservatory


transition (pattern enter (room)) (action player)
transition (pattern player (room)) (action print "You've entered ")

# Get the party started
begin game

