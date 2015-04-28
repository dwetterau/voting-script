import sys

if len(sys.argv) < 2:
  print "Usage: python vote.py <number_of_voters>"
  sys.exit(1)

totalVoters = int(sys.argv[1])

# Main input loop
# Commands:
# /begin - Resets all voting structures and starts a new vote
# /tally - Calculates the winner by instant-runoff voting
# /score - Ranks the candidates with a majority of support by a linear scale
# /delete - Removes the last added vote
votes = []
maxVoteLength = 0

def begin():
  global votes
  votes = []
  print "-Begin"

def remove():
  global votes
  if votes:
    removed = votes.pop()
    print "-Removed %s" % removed


def getNewMaxVoteLength():
  global votes
  # determine max vote length
  maxVoteLength = 0
  for vote in votes:
    maxVoteLength = max(maxVoteLength, len(vote))
  return maxVoteLength

def tally():
  global votes
  global maxVoteLength
  global totalVoters
  # Vote arrays are arrays of candidate preferences
  votingRound = 0
  eliminated = []
  maxVoteLength = getNewMaxVoteLength()

  # perform all the rounds
  while maxVoteLength > 0:
    voteMap = {}

    # Check the votes at the front of each array
    for vote in votes:
      selection = vote[0]
      if selection not in voteMap:
        voteMap[selection] = 1
      else: 
        voteMap[vote[0]] += 1

    # Check this round for a majority
    winner = [selection for selection, amount in voteMap.iteritems()
        if amount > (totalVoters / 2)]
    if winner:
      print "Winner found! %s" % winner[0]
      return 

    # We didn't have a majority, find minimum candidate and eliminate
    minSelections = []
    minAmount = 1000
    for selection, amount in voteMap.iteritems():
      if amount < minAmount:
        minAmount = amount
        minSelections = [selection]
      elif amount == minAmount:
        minSelections.append(selection)
    
    minSelection = minSelections[0]
    if len(minSelections) > 1:
      # We have a tie for the minimum selection, we will use Irish rules.
      minSelectionsMap = {}
      for m in minSelections:
        minSelectionsMap[m] = 0
        for vote in votes:
          # Look for next place votes for this selection in other votes
          if vote[0] is not m:
            for i in range(1, len(vote)):
              s = vote[i]
              if s is m:
                minSelectionsMap[m] += 1

      # The true min is the min of the mins
      minAmount = 1000
      for m, amount in minSelectionsMap.iteritems():
        if amount < minAmount:
          minSelection = m
          minAmount = amount

    # Iterate through the votes again, if the value at the current round is the
    # minSelection, delete that entry
    newVotes = []
    for vote in votes:
      vote = [s for s in vote if s is not minSelection]
      # Remove votes that are empty now
      if vote:
        newVotes.append(vote)
    
    votes = newVotes

    # Get a new max vote length
    getNewMaxVoteLength()

  # If we never returned from the loop, no candidate ever got a majority
  print "No winner found."

def score():
  global votes
  global totalVoters

  possibleRanks = getNewMaxVoteLength()
  # First populate the map of candidates with votes
  voteMap = {}
  for vote in votes:
    selectionSet = set()
    for selection in vote:
      if selection in selectionSet:
        # Already voted for this candidate
        continue

      if selection not in voteMap:
        voteMap[selection] = 1
      else:
        voteMap[selection] += 1
      
      selectionSet.add(selection)

  # Throw away all candidates with less than a majority of support
  voteMap = {selection: amount for selection, amount in voteMap.iteritems()
      if amount > totalVoters / 2}

  # Calculate the score for each remaining candidate
  totalRankMap = {}
  for selection in voteMap.iterkeys():
    totalRankMap[selection] = 0
    for vote in votes:
      for index, s in enumerate(vote):
        # Filter out selections that don't correspond to the current key
        if s is not selection:
          continue
        score = possibleRanks - (index)
        totalRankMap[selection] += score

  # Sort the results by score order
  results = sorted(totalRankMap.items(), key=lambda i: i[1])[::-1]
  print results

def parseVote(vote):
  vote = list(vote) 
  votes.append(vote)
  print "-Added %s" % vote

commands = {
  'begin': begin, 
  'remove': remove, 
  'tally': tally,
  'score': score
 }

while True:
  line = sys.stdin.readline()
  if not line: 
    break
  line = line.strip()

  if line[0] == '/':
    command = line[1:]
    if command in commands:
      commands[command]()
    else:
      print "-Unrecognized command"
  else:
    parseVote(line)

