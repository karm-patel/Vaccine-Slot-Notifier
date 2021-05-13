import pickle

objects = pickle.load(open("user_groups", "rb"))
# objects["162:18"]["emails"].remove("karmasmart216@gmail.com")
user_count = 0
for obj in objects:
    print(obj)
    print(objects[obj])
    user_count += len(objects[obj]["emails"])
    print()


# keys = ["4:18","370110:18","108:18"]
# for key in keys:
#     del objects[key]

print("Users:",user_count)
print("Objects:",len(objects))

# pickle.dump(objects,open("user_groups", "wb"))