# An Adventure-style game for Wheeler
# Inspiration (but not implementation) drawn from Dennis Merritt's "Adventure in Prolog". Read it.

# This is an ongoing example and exploration, and not a full game.

# Introduce the game:
begin game -> intro1

intro1 -> print "Adventure in Wheeler" intro2
intro2 -> print "-------------------------------" intro3
intro3 -> print "You are a young detective named Trixie. You are trying to find " intro4
intro4 -> print "your friend Honey after her mysterious disappearance this morning." intro5
intro5 -> print "You are standing in the foyer of Honey's house, a modest mansion in " intro6
intro6 -> print "the countryside. You are facing east."


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


enter (room) -> player
player (room) -> print "You've entered "


# Get the party started
begin game



