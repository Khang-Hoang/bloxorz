start = (7,4)

board = [
    [0,1,1,1,0,0,0,0,0,0,0,0,1,1,1],
	[0,1,20,1,0,0,0,0,0,0,0,0,1,10,1],
	[0,1,1,1,0,0,0,1,1,1,1,1,1,1,1],
	[0,1,1,1,0,0,0,1,100,1,0,0,1,1,20],
	[1,0,0,0,1,0,0,1,1,1,0,0,0,0,1],
	[10,0,0,0,1,0,0,2,2,2,0,0,0,0,1],
	[1,0,0,1,1,1,2,2,2,2,2,1,1,1,1],
	[0,0,0,1,1,1,2,2,2,2,2,1,30,1,0],
	[0,0,0,1,1,1,2,2,2,2,2,1,1,1,0],
	[0,0,0,1,1,1,1,1,0,0,0,0,0,0,0]
]

buttons = {
	(1,2) : [[1,(3,4)]],
	(1,13) : [[1,(6,1)],[1,(6,2)],[2,(9,8)]],
	(3,14) : [[0,(6,1)],[0,(6,2)],[1,(3,0)]],
	(5,0) : [[0,(2,9)],[0,(2,10)],[0,(6,14)]],
	(7,13) : [(7,13),(2,2)]
}