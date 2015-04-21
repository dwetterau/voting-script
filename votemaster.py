import sys

# Main input loop
# Commands:
# /begin - Resets all voting structures and starts a new vote
# /tally - Calculates the winner
# /delete - Removes the last added vote
votes = []

def begin():
  votes = []
  print "-Begin"

def remove():
  if votes:
    removed = votes.pop()
    print "-Removed %s" % removed

def tally():
  # TODO: run the tallying procedure
  pass

def parseVote(vote):
  vote = list(vote) 
  votes.append(vote)
  print "-Added %s" % vote

commands = {
  'begin': begin, 
  'remove': remove, 
  'tally': tally
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

