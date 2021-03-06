start = (2,8)

board = [
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
	[0,0,1,1,1,1,1,1,1,1,0,0,1,1,1],
	[0,0,1,1,1,0,0,10,1,1,0,0,1,1,1],
	[0,0,1,1,1,0,0,1,1,1,0,0,0,0,0],
	[0,0,1,10,1,0,0,30,1,10,0,0,0,0,0],
	[0,0,1,1,1,0,0,1,1,1,0,0,0,0,0],
	[1,1,1,1,0,0,0,1,1,1,0,0,10,1,1],
	[1,10,0,0,0,0,0,0,0,0,0,0,1,1,1],
	[0,0,0,0,0,0,0,0,0,0,0,0,1,100,1],
	[0,0,0,0,0,0,0,0,0,0,0,0,1,1,1]
]

buttons = {
	(2,7)  : [[0,(1,5)],[0,(1,6)]],
	(4,3)  : [[0,(1,5)],[0,(1,6)]],
	(4,7)  : [(1,13),(7,13)],
	(4,9)  : [[0,(1,5)],[0,(1,6)]],
	(7,1)  : [[2,(1,10)],[2,(1,11)]],
	(6,12) : [[2,(6,10)],[2,(6,11)]]
}