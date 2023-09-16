pub struct LowercaseString {
    contents: String,
}

pub struct LowercaseChar {
    contents: char,
}

impl LowercaseString {
    pub fn new(s: String) -> Self {
        Self {
            contents: s.to_lowercase(),
        }
    }

    pub fn contents(&self) -> &str {
        &self.contents
    }

    pub fn chars(&self) -> impl Iterator<Item = LowercaseChar> {
        self.chars().map(|c| LowercaseChar { contents: c })
    }
}

impl LowercaseChar {
    pub fn contents(&self) -> char {
        self.contents
    }
}
