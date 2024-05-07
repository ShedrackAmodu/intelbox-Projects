from pyamaze import maze,agent
m=maze(10,15)
m.CreateMaze(loopPercent=0)

a=agent(m,footprints=True,filled=True)

m.tracePath({a:m.path},delay=200)
m.run()

# done