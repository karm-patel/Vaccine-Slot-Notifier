from app import db, data, permanent_data
records = data.query.all()
db.create_all()
for ind,each in enumerate(records):
    print(ind+1,end="\t")
    print(f"{str(each.timestamp):10s}",end="\t")
    print(f"{each.email:30s}",end="\t")
    print(f"{each.min_age:10s}",end="\t")
    if each.by == "Area":
        print(f"{each.state:20s}",end="\t")
        print(f"{each.district}",end="\t")
    else:
        print(f"{each.pin}",end="\t")
    print()
