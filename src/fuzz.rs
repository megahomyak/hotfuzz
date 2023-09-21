use std::cmp::Reverse;

use crate::item::{self, Item};

pub struct Fuzz {
    items: Vec<String>,
}

impl Fuzz {
    pub fn new(items: &[Item]) -> Self {
        let mut processed_items = Vec::new();
        for item in items {
            let mut item_text = String::new();
            for part in item.parts {
                item_text.push_str(match part {
                    item::Part::Highlighted { contents } => &contents,
                    item::Part::Plain { contents } => &contents,
                });
            }
            item_text.shrink_to_fit();
            processed_items.push(item_text);
        }
        processed_items.shrink_to_fit();
        Self { items: processed_items }
    }

    pub fn filter(&self, query: &str) -> impl Iterator<Item = item::Index> {
        let mut matches = Vec::new();
        for (index, item_text) in self.items.iter().enumerate() {
            let searcher = sublime_fuzzy::FuzzySearch::new(query, item_text).case_insensitive();
            if let Some(match_) = searcher.best_match() {
                matches.push((index, match_));
            }
        }
        matches.sort_unstable_by_key(|(_index, match_)| Reverse(match_.score()));
        matches.into_iter().map(|(index, _match)| index)
    }
}
