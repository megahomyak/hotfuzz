use std::collections::HashMap;

use crate::lowercase_string::LowercaseChar;

pub enum Node<Item> {
    Occupied(Item),
    Free(HashMap<LowercaseChar, Self>),
}

pub struct Hot<Item> {
    base: HashMap<LowercaseChar, Item>,
}

pub enum CreationError {
    Collision,
}

impl<'a, Item: crate::item::Item> Hot<Item> {
    pub fn new(items: impl Iterator<Item = &'a Item>) -> Result<Self, CreationError> {
        use crate::item::Part;

        let mut base = HashMap::new();
        for item in items {
            let mut highlighted_chars = item
                .parts()
                .filter_map(|part| match part {
                    Part::Plain(_contents) => None,
                    Part::Highlighted(contents) => Some(contents.chars()),
                })
                .flatten();
            let base = &mut base as *mut _;
            if let Some(previous_char) = highlighted_chars.next() {
                for current_char in highlighted_chars {
                    let mut new_base = HashMap::new();
                    base.entry();
                }
            }
        }
    }
}
