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
    None,
    One { item_index: item::Index },
    Multiple { item_indexes: Vec<item::Index> },
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
                    item::Part::Plain { content: _ } => None,
                    item::Part::Highlighted { content } => Some(content.chars()),
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
                        Node::Occupied { item_index: _ } => unsafe {
                            std::hint::unreachable_unchecked()
                        },
                        Node::Free { base } => base,
                    };
                    previous_char = current_char;
                }
            }
        }
        Ok(Self { base })
    }

    pub fn filter(&self, query: &str) -> Output {
        let mut base = &self.base;
        let mut chars = query.chars();
        for c in chars {
            match base.get(&c) {
                None => return Output::None,
                Some(node) => match node {
                    Node::Free { base: next_base } => base = next_base,
                    Node::Occupied { item_index } => {
                        if chars.as_str().is_empty() {
                            return Output::One {
                                item_index: *item_index,
                            };
                        } else {
                            return Output::None;
                        }
                    }
                },
            }
        }
        let mut item_indexes = Vec::new();
        let mut remaining_bases = Vec::from([base]);
        while Some(base) = remaining_bases.pop() {
            for item in base.values() {
                match item {
                    Node::Free { base } => remaining_bases.push(base),
                    Node::Occupied { item_index } => item_indexes.push(*item_index),
                }
            }
        }
        Output::Multiple { item_indexes }
    }
}
