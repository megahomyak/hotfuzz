mod item {
    pub enum Part {
        Highlighted(part::Highlighted),
        Plain(part::Plain),
    }

    pub mod part {
        use super::Part;

        pub struct Highlighted {
            pub contents: String,
        }

        pub struct Plain {
            pub contents: String,
        }

        pub struct Iter<Parts> {
            parts: Parts,
        }

        impl<Parts: Iterator<Item = Part>> Iterator for Iter<Parts> {
            type Item = Part;

            fn next(&mut self) -> Option<Self::Item> {
                self.parts.next()
            }
        }

        impl<Parts: Iterator<Item = Part>> Iter<Parts> {
            pub fn highlighted<'a>(&'a mut self) -> impl Iterator<Item = Highlighted> + 'a {
                self.filter_map(|item| match item {
                    Part::Highlighted(part) => Some(part),
                    Part::Plain(_part) => None,
                })
            }

            pub fn plain<'a>(&'a mut self) -> impl Iterator<Item = Plain> + 'a {
                self.filter_map(|item| match item {
                    Part::Highlighted(_part) => None,
                    Part::Plain(part) => Some(part),
                })
            }
        }
    }
}

pub trait Item {
    type Parts: Iterator<Item = item::Part>;

    fn parts(&self) -> item::part::Iter<Self::Parts>;

    fn text(&self) -> String {
        let mut result = String::new();
        for part in self.parts() {
            match part {
                item::Part::Plain(part) => result.push_str(&part.contents),
                item::Part::Highlighted(part) => result.push_str(&part.contents),
            }
        }
        result.shrink_to_fit();
        result
    }
}

pub enum Output<Item, Items> {
    Chosen(Item),
    Various(Items),
    None,
}

pub trait Filter<Item> {
    type Items: IntoIterator<Item = Item>;

    fn get_results(&self, input: &str) -> Output<Item, Self::Items>;
}

mod hot {
    use super::item::Part;
    use std::collections::HashMap;

    enum Node<Item> {
        Occupied(Item),
        Free(HashMap<char, Self>),
    }

    pub struct Hot<Item> {
        nodes: HashMap<char, Node<Item>>,
    }

    pub enum CreationError {
        Collision,
    }

    impl<Item: super::Item> Hot<Item> {
        pub fn new(items: impl Iterator<Item = Item>) -> Result<Self, CreationError> {
            let mut base = HashMap::new();
            for item in items {
                let mut base = &mut base;
                let mut iter = item.parts().highlighted().map();
                let mut last_char = todo!();
                for part in item.parts() {
                    match part {
                        Part::Highlighted { contents } => last_char = (),
                        Part::Plain { contents: _ } => (),
                    }
                }
            }
        }
    }
}
