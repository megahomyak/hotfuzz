# HotFuzz

HotFuzz is a new way of interaction with a computer. It is quick, convenient and easy to learn. Essentially, it is about picking an item from a list.

* Easy for beginners
* Efficient for masters
* Easy to become a master

## Installation

* `pip install hotfuzz`

## Features

Two modes: "Hot" and "Fuzz".

In any mode what you do is you narrow the amount of items in the list by filtering the unwanted ones out with your input.

* "Hot": a mode where you can access an item of the list by typing out big letters from its name. If you typed out all the big letters from a certain item in the correct order, this item is considered your choice (HotFuzz is closed, the item is returned)
* "Fuzz": it's just a [fuzzy search](https://en.m.wikipedia.org/wiki/Approximate_string_matching) implementation that excludes items that don't match the query

Thanks to the "Fuzz" mode, you can find whatever you need if you don't remember the big letters. And if you do remember, you can access the item easily by simply typing out these letters.

Since you always see the name of the item in the "Fuzz" mode, overtime you remember it, and thus you remember the big letters from it, which allows you to access the item in the "Hot" mode.

The default mode is "Hot", so you can pick an item with the minimal amount of key presses, and those key presses will always be the same every time.

Since hotkeys are tied to big letters, user interface creators will be forced to make at least somewhat semantic hotkeys.

And since the big letters are needed to be pressed sequentially, you can use such an interface with one finger.

## Comparison to some other approaches

* **Vim**: Vim does not have a convenient way to find a command by its name, nor does it have semantic hotkeys, which creates an insanely high barrier of entry for the editor. Its hotkeys are also sometimes time-based or require holding multiple buttons at the same time, which is not convenient.
* **VSCode**: it does indeed have a "command palette", but that command palette has hotkeys that are not required to be semantic, and they are also usually invoked by pressing multiple buttons at the same time.
* **Graphical user interfaces**: you are limited by the amount of space on your screen, the precision of your mouse and the fact that you only have one mouse with usually two buttons and a wheel. Searching through long lists of menus, submenus and their items can be tedious. From my experience, GUIs are very slow to use compared to keyboard-based interfaces.

## How to use the graphical interface

* Switch modes by pressing "/"
* In any mode, you can move the item selection using arrow keys and return the selected item by pressing the "Return" key or the "Enter" key
* In any mode, you can delete the last character from the input field by pressing Backspace. You can also hold it to delete multiple characters or use it with Ctrl to delete words
* The "Hot" mode: type out the big characters in the name of the element you want
* The "Fuzz" mode: narrow the list by typing out the name of the element you want (imprecisely), then return the wanted element
* Exit HotFuzz by pressing the "Escape" key (this will indicate that you haven't chosen an item)
* Be aware that items that cannot be accessed in the "Hot" mode won't be displayed in the "Hot" mode. The "Fuzz" mode is guaranteed to display all items when the input field is empty

## How to invoke HotFuzz from your program

Create a `HotFuzz` instance with the items that you need:

```python
from hotfuzz import HotFuzz

items = ["Some Thing", "Some Other Thing"]

hotfuzz = HotFuzz(items, initially_invisible=False)
```

Then invoke the `.run()` method of the `HotFuzz` instance to allow the user to interact with HotFuzz:

```python
result_index = hotfuzz.run()
```

The returned value may be `None` if the user closed the HotFuzz window without choosing an item:

```python
if result_index is None:
    print("Nothing was selected")
else:
    print(items[result_index] + " was selected")
```

You can change `initially_invisible` to `True` if you want the HotFuzz window to be invisible when the user is in the "Hot" mode and the input field is empty. This can help if in your program the user needs to be looking at something while taking actions.

Be aware that when passing a list of arguments where at least one sequence of big letters matches the beginning of another sequence of big letters (of a different item), a `HotCollision` will be raised (when creating a `HotFuzz` instance) because the item with the longer sequence will be inaccessible, which should not happen.
