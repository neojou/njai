
fruitPrices = {'apples':2.00, 'oranges':1.50, 'pears': 1.75,
	       'limes':0.75, 'strawberries':1.00}

def buyLotsOfFruit(orderList):
	totalCost = 0
	for (fruit, numPounds) in orderList:
		if fruit not in fruitPrices:
			print("We don't have %s" % fruit)
			return "None"
		else:
			totalCost += fruitPrices[fruit] * numPounds
	return totalCost
	

if __name__ == '__main__':
	orderList = [('apples', 2.0), ('pears', 3.0), ('limes', 4.0)]
	print("Cost of %s is %.2f" % (orderList, buyLotsOfFruit(orderList)))

