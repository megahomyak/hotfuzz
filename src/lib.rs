mod filters;
mod item;
mod lowercase_string;

pub enum Mode {
    Hot,
    Fuzz,
}

pub struct HotFuzz<Item> {
    mode: Mode,
    hot: filters::hot::Hot<Item>,
    fuzz: filters::fuzz::Fuzz<Item>,
}

pub enum CreationError {
    Collision,
}

impl<Item> HotFuzz<Item> {
    pub fn new(mode: Mode, items: impl IntoIterator<Item = Item>) -> Result<Self, CreationError> {}
}
