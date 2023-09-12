import hotfuzz
from hotfuzz import Option, HighlightedPart as H, PlainPart as P

print(hotfuzz.run([
    Option(parts=[H("H"), P("ello")], payload=None),
    Option(parts=[P("Hi-"), H("L"), P("o")], payload=None),
    Option(parts=[H("F"), P("ile "), H("M"), P("anager")], payload=None),
    Option(parts=[H("J"), P("oe")], payload=None),
    Option(parts=[P("Minecraft")], payload=None),
    Option(parts=[H("Vim")], payload=None),
]))
