""";; This buffer is for notes you don't want to save, and for Lisp evaluation.
;; If you want to create a file, visit that file with C-x C-f,
;; then enter the text in that file's own buffer."""
import re, mmap

#opens the file to read 
def reg_exp(pgn, color):
  with open(pgn, 'r+') as f:
    data = mmap.mmap(f.fileno(), 0)
    #searches for the specified string combination 
    reg1 = re.search('WhiteElo (.*)', data)
    #grabs the string right after the flag and stores it in a variable
    final_string1 = reg1.group(1)
    reg2 = re.search('BlackElo (.*)', data)
    final_string2 = reg2.group(1)
    reg3 = re.search('Result (.*)', data)
    final_string3 = reg3.group(1)
    
    #strips the quotation marks and ending bracket and returns an int
    if color == 'w':
      WhiteElo = int(final_string1[1:-3])
      #displays who won the game
      if int(final_string3[1]) == 0:
        winner = 'l'
      elif int(final_string3[3]) == 2:
        winner = 't'
      else:
        winner = 'w'
      return (WhiteElo, winner)
    else:
      BlackElo = int(final_string2[1:-3])
      #displays who won the game
      if int(final_string3[1]) == 0:
        winner = 'w'
      elif int(final_string3[3]) == 2:
        winner = 't'
      else:
        winner = 'l'
      return (BlackElo, winner)
    
  f.close()


