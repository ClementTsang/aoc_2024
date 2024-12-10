# Day 10

Just grid search. Not too complicated otherwise, though I did trip up because I forgot `frozenset` actually makes a set
out of the `list`; I had to do `frozenset((tuple(my_list), ))` in order to "trick" it into keeping my ordering.
