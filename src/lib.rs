use item::Item;

mod fuzz;
mod hot;
mod item;
pub mod prompt;
pub use prompt::Prompt;

enum Mode {
    Hot,
    Fuzz,
}

pub struct HotFuzz<'a> {
    hot: hot::Hot,
    fuzz: fuzz::Fuzz,
    mode: Mode,
    items: &'a [Item],
}

#[derive(Debug)]
pub enum CreationError {
    Collision,
}

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
pub enum Output {
    Choice(item::Index),
    Exit,
}

impl<'a> HotFuzz<'a> {
    pub fn new(items: &'a [Item]) -> Result<Self, CreationError> {
        let hot = match hot::Hot::new(items) {
            Err(error) => {
                return Err(match error {
                    hot::CreationError::Collision => CreationError::Collision,
                })
            }
            Ok(hot) => hot,
        };
        let fuzz = fuzz::Fuzz::new(items);
        Ok(Self {
            items,
            hot,
            fuzz,
            mode: Mode::Hot,
        })
    }

    pub fn run(&self, mut prompt: Prompt) -> Output {
        self.hot
    }
}
