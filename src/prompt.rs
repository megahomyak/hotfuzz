#[derive(Debug)]
pub struct Prompt {
    contents: String,
}

pub enum CreationError {
    NewlineEncountered,
}

impl Prompt {
    pub fn new(contents: String) -> Result<Self, CreationError> {
        for char in contents.chars() {
            match char {
                '\n' => return Err(CreationError::NewlineEncountered),
                _ => (),
            }
        }
        Ok(Self { contents })
    }
}
