import hotfuzz

hotfuzz = hotfuzz.HotFuzz(["abc", "Abc", "BAB", "01234567890123456789012345678901234567890123456789"])
print(hotfuzz.run())
