
class newNode:
	def __init__(self,key):
		self.data = key
		self.left = None
		self.right = None
		self.dist = 0


def topView(root):
	if root==None:
		return
	q = []
	map = dict()
	dist = 0
	root.dist = dist

	q.append(root)

	while len(q):
		root = q[0]
		dist = root.dist

		if dist not in map:
			map[dist] = root.data

		if root.left:
			root.left.dist = dist-1
			q.append(root.left)

		if root.right:
			root.right.dist = dist+1
			q.append(root.right)

		q.pop(0)

	for i in sorted(map):
		print map[i],


if __name__ =='__main__':
	root = newNode(1)
	root.left = newNode(2)
	root.right = newNode(3)
	root.left.left = newNode(4)
	root.left.right = newNode(5)
	root.right.left = newNode(6)
	root.right.right = newNode(7)
	root.left.right.left = newNode(8)
	root.left.right.right = newNode(9)

	topView(root)
