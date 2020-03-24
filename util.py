import io

class TCGUser:
    all_users = []
    def __init__(self, name):
        self.collected = {}
        self.name = name
        TCGUser.all_users.append(self)

class TCGCollection:
    all_collections = []
    def __init__(self, collection_name, items, img_size, width, preview=None):
        self.width = width
        self.name = collection_name
        self.img_size = img_size
        self.size = len(items)
        self.items = []
        self.preview = preview
        for i in items:
            self.items.append(i)
        TCGCollection.all_collections.append(self)


def getTCGUser(name):
    for user in TCGUser.all_users:
        if user.name == name:
            return user
    new_user = TCGUser(name)
    return new_user

def getCollection(collection_name):
    for collection in TCGCollection.all_collections:
        if collection.name == collection_name:
            return collection
    return None

# https://stackoverflow.com/questions/60006794/send-image-from-memory
def ImageToByteStream(image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format='JPEG')
    imgByteArr.seek(0)
    return imgByteArr