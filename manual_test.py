import hotfuzz

items = ["abc", "Abc", "BAB", "01234567890123456789012345678901234567890123456789"]

for i in range(100):
    items.append("o" + str(i))

hotfuzz = hotfuzz.HotFuzz(items, initially_invisible=False)
result = hotfuzz.run()
if result is not None:
    print(items[result])
else:
    print(None)
