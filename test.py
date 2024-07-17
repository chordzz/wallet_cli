import json

fr = open("data/users.json", 'r')

data = json.load(fr)
# print(f.read())
print(data)
print(type(data))

new_data = {
      "id": ["00", "00", "00"],
      "name": ["00", "00"],
      "department": ["00", "00"]
    }

data.append(new_data)
print(data)

fw = open("data/users.json", 'w')
fw.write(json.dumps(data, indent=4))
fw.close()
