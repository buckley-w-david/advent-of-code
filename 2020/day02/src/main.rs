use std::fs::File;
use std::num::ParseIntError;
use std::char::ParseCharError;
use std::io::{self, BufRead};

use regex::Regex;
use lazy_static::lazy_static;
use std::str::FromStr;
use thiserror::Error;

#[derive(Debug)]
struct PasswordEntry {
    lower_bound: usize,
    upper_bound: usize,
    letter: char,
    password: String
}

#[derive(Error, Debug)]
pub enum ParsePasswordError {
    #[error("Integers is wrong")]
    Int(#[from] ParseIntError),
    #[error("Char is wrong")]
    Char(#[from] ParseCharError),
    #[error("Files!")]
    File(#[from] io::Error),
    #[error("Everything is wrong")]
    Structure,
}


// 1-3 x: xbfmxxfxxf
const PASSWORD_REGEX: &str = r"(\d+)-(\d+) ([a-zA-Z]): (.+)";

impl FromStr for PasswordEntry {
    type Err = ParsePasswordError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        lazy_static! {
            static ref REGEX: Regex = Regex::new(PASSWORD_REGEX).unwrap();
        }

        REGEX.captures(s)
            .ok_or(ParsePasswordError::Structure)
            .and_then(|cap| Ok(PasswordEntry {
                lower_bound: cap[1].parse()?,
                upper_bound: cap[2].parse()?,
                letter: cap[3].parse()?,
                password: cap[4].parse().unwrap(),
            }))
    }
}

impl PasswordEntry {
    pub fn valid(&self) -> bool {
        let mut chars = self.password.chars();
        let first = chars.nth(self.lower_bound-1).unwrap();
        let second = chars.nth(self.upper_bound - self.lower_bound-1).unwrap();
        (self.letter == first || self.letter == second) && first != second
    }

    // This is the validation function for the first of the two challenges
    // pub fn valid(&self) -> bool {
    //     let count = self.password.chars().filter(|&c| c == self.letter).count();
    //     count >= self.lower_bound && count <= self.upper_bound
    // }
}


fn main() -> Result<(), ParsePasswordError> {
    let file = File::open("input")?;
    let pdb: Vec<PasswordEntry> = io::BufReader::new(file).lines().map(|l| l.unwrap().parse().unwrap()).collect();
    println!("{}", pdb.iter().filter(|p| p.valid()).count());
    Ok(())
}
