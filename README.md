LAN Election Voting
====================

## Operation:

Run the script with:

``` python vote.py <number_of_voters> ```

Once running, you have access to the following commands:

- /begin This resets all voting structures for a new vote
- /delete This removes the most recently added vote, useful for mess ups
- /score This computes the ranking of candidates based off the score approach
  below
- /tally this computes the winner with Instant-Runoff Voting

To add a vote, simply type in a string of characters denoting the ranking of a
vote.  If four candidates (A, B, C, and D) are running and a person ranks A
first, C second, and D third, the vote would be input as "ACD".  This infers
that the candidate votes "no confidence" for candidate D.

### Tally Function: 
This computes the winner of the election according to
Instant-Runoff Voting.  Ties in the candidate to eliminate are broken by Irish
rules.

### Score Function: 
This computes a ranking of the candidates. It operates as
follows:

First it eliminates all candidates that received less than a majority of the
vote (i.e. candidates that were ranked by less than half of all voters).

It then computes each candidates 'score' which is determined by the number of
candidates running and the rank they were assigned in each vote.

If there are 4 candidates running and a vote is "ABC", then A receives 4
points, B receives 3 points, and C receives 2 points.

The candidates are then sorted and returned to the terminal.
