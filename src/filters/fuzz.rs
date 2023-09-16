pub struct Fuzz<Item> {
    items: Vec<Item>,
}

impl<Item> Fuzz<Item> {
    pub fn new(items: impl Iterator<Item = Item>) -> Self {

    }
}
