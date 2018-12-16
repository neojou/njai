import shop

def shopSmart(orderList, fruitShops):
	minShop = None
	minCost = -1
	for shop in fruitShops:
		cost = shop.getPriceOfOrder(orderList)
		if minCost == -1 or cost < minCost:
			minShop = shop
			minCost = cost
	return minShop
    
if __name__ == '__main__':
  "This code runs when you invoke the script from the command line"
  orders = [('apples',1.0), ('oranges',3.0)]
  dir1 = {'apples': 2.0, 'oranges':1.0}
  shop1 =  shop.FruitShop('shop1',dir1)
  dir2 = {'apples': 1.0, 'oranges': 5.0}
  shop2 = shop.FruitShop('shop2',dir2)
  shops = [shop1, shop2]
  print("For orders %s , the best shop is %s" % (orders,  shopSmart(orders, shops).getName()))
  orders = [('apples',3.0)]
  print("For orders %s , the best shop is %s" % (orders,  shopSmart(orders, shops).getName()))

