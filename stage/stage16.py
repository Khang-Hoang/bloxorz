start = (6,3)

board = [
    [0,30,0,0,0,0,0,0,0,0,1,1,1],
	[30,1,30,0,0,20,20,1,0,0,1,100,1],
	[0,30,0,0,0,0,0,0,0,0,1,1,1],
	[0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,0,1,1,1,0,0,0,1,1,1,0,0],
	[0,0,1,1,1,1,1,1,1,30,1,0,0],
	[0,0,1,1,1,0,0,0,1,1,1,0,0]
]

buttons = {
	(6,9) : [(0,1),(1,0)],
	(0,1) : [(1,7),(1,5)],
	(1,0) : [(1,2),(0,1)],
	(1,2) : [(1,0),(1,2)],
	(2,1) : [(2,1),(1,0)],
	(1,5) : [[1,(1,3)],[1,(1,4)]],
	(1,6) : [[1,(1,8)],[1,(1,9)]]  
}