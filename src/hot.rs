use crate::item::{self, Item};
use std::collections::HashMap;

pub enum Node {
    Free { base: HashMap<char, Self> },
    Occupied { item_index: item::Index },
}

pub struct Hot {
    base: HashMap<char, Node>,
}

pub enum CreationError {
    Collision,
}

pub enum Output {
    OneChosen(item::Index),
    MultipleChosen(item::Index),
}

impl Hot {
    pub fn new(items: &[Item]) -> Result<Self, CreationError> {
        let mut base = HashMap::new();
        for (index, item) in items.iter().enumerate() {
            let mut base: *mut _ = &mut base;
            let mut highlighted_chars = item
                .parts
                .iter()
                .filter_map(|part| match part {
                    item::Part::Plain { contents: _ } => None,
                    item::Part::Highlighted { contents } => Some(contents.chars()),
                })
                .flatten();
            if let Some(mut previous_char) = highlighted_chars.next() {
                for current_char in highlighted_chars {
                    match unsafe { *base }.get(&current_char) {
                        None => (),
                        Some(_node) => return Err(CreationError::Collision),
                    }
                    unsafe { *base }.insert(
                        current_char,
                        Node::Free {
                            base: HashMap::new(),
                        },
                    );
                    base = match unsafe { (*base).get_mut(&current_char).unwrap_unchecked() } {
                        Node::Occupied { item_index: _ } => unsafe { std::hint::unreachable_unchecked() },
                        Node::Free { base } => base,
                    };
                    previous_char = current_char;
                }
            }
        }
        Ok(Self { base })
    }

    pub fn filter(&self, query: &str) -> Output {
        for char in query.chars() {

        }
        self.base.get()
    }
}
