#[derive(Clone, Debug)]
pub enum Part {
    Plain { contents: String },
    Highlighted { contents: String },
}

#[derive(Clone, Debug)]
pub struct Item {
    pub parts: Vec<Part>,
}

pub type Index = usize;
