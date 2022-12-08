use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashSet;
use std::iter::Iterator;


fn main() {
    let file = File::open("input").unwrap();
    let forms: Vec<String> = io::BufReader::new(file).lines().map(|l| l.unwrap()).collect();

    let mut iter = forms.iter();

    let mut sum = 0;
    loop {
        let result: Vec<&String> = iter.by_ref().take_while(|c| !c.is_empty()).collect();
        if result.is_empty() {
            break;
        }

        let all: HashSet<char> = result.iter().flat_map(|l| l.chars()).collect();
        let yes: Vec<HashSet<char>> = result.iter().map(|l| l.chars().collect()).collect();
        let alll = yes.iter().fold(all, |a, b| a.intersection(&b).map(|&c| c).collect());

        sum += alll.len();
    }

    println!("{}", sum);
}

