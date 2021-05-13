from slot import VaccineSlot
import json

with open("objects.json", "r") as fp:
    objects = json.load(fp)

email = "uttam@gmail.com"
obj = eval(objects[email])
print(obj.url)
#avl = myslot.get_available_slots()
#print(avl)