class Item():
    def __init__(self,cursor, itemID):
        self.cursor = cursor
        self.itemID = itemID


    def itemProfile(self,itemID):
        # return image, title, priceType, saleStatus, postTime
        # need for view item action

        print()

    def searchItem(self,keywords):
        # look through all items' title, compare with all capitalize letters
        # if found return list of itemProfile, call self.itemProfile(itemID)
        # if not found, add to notification DB
        pass

