#[derive(Clone, Debug)]
pub enum Part {
    Plain { content: String },
    Highlighted { content: String },
}

#[derive(Clone, Debug)]
pub struct Item {
    pub parts: Vec<Part>,
}

pub type Index = usize;
