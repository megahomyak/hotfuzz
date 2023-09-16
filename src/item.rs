pub enum Part<Str> {
    Plain(Str),
    Highlighted(Str),
}

pub trait Item<Str> {
    type Parts: Iterator<Item = Part<Str>>;

    fn parts(&self) -> Self::Parts;
}
