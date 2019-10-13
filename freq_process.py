import time
file = open('note_freq.txt', 'r')
a = {}
for line in file:
    line = ' '.join(line.split())
    line = line[2:]
    line = line.strip()
    line.replace(' ','')
    line = ''.join(line.split())
    b = line[1] == '#'
    if(b):
        note = line[0:3]
        freq = float(line[3:])
        a[note] = freq
    else:
        note = line[0:2]
        freq = float(line[2:])
        a[note] = freq
print(a)