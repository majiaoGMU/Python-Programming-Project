from Tkinter import *
from Map import *
import time

starttime = 0
map = Map(800, 600)
starttime = time.clock()
map.addLayer('US_states-49','wheat')
map.addLayer('US_major_rivers-49', 'blue')
map.addLayer('US_freeways-49','coral')

#print str(time.clock() - starttime) + ' seconds is needed for adding layers'

map.vis()
print str(time.clock() - starttime) + ' seconds is needed for visulization'
map.root.mainloop()
