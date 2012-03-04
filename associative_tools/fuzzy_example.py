from fuzzyhash import FuzzyHash

change_score = 20
clarity_score = 20
influence_score = 20


# =------------------------=
# Naive implementation
# =------------------------=
if change_score in range(18, 26): change_factor = "high"
if change_score in range(11, 18): change_factor = "medium"	

if clarity_score in range(18, 26): clarity_factor = "high"
if clarity_score in range(11, 18): clarity_factor = "medium"	

if influence_score in range(18, 26): influence_factor = "high"
if influence_score in range(11, 18): influence_factor = "medium"	


# =------------------------=
# Refactoring. No fuzzy hash yet.
# =------------------------=

medium_range = range(11, 18)
high_range = range(18, 26)

if change_score in high_range: change_factor = "high"
if change_score in medium_range: change_factor = "medium"	

if clarity_score in high_range: clarity_factor = "high"
if clarity_score in medium_range: clarity_factor = "medium"	

if influence_score in high_range: influence_factor = "high"
if influence_score in medium_range: influence_factor = "medium"	


# =------------------------=
# Let's use a FuzzyHash
# =------------------------=
factor = FuzzyHash()

medium_range = range(11, 18)
high_range = range(18, 26)

factor[medium_range] = "medium"
factor[high_range]   = "high"

# Usage. Intermediate variables wouldn't actually be needed. You get the idea.
change_factor = factor[change_score]
clarity_factor =  factor[clarity_score]
influence_factor = factor[influence_score]


# =------------------------=
# Tighten up
# =------------------------=
factor[range(11, 18)] = "medium"
factor[range(18, 26)]   = "high"

# Usage. See above.
change_factor = factor[change_score]
clarity_factor =  factor[clarity_score]
influence_factor = factor[influence_score]























