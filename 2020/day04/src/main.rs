use std::fs::File;
use std::io::{self, BufRead};
use std::collections::HashMap;

use std::str::FromStr;

use regex::Regex;


fn main() {
    let file = File::open("input").unwrap();
    let passports: Vec<String> = io::BufReader::new(file).lines().map(|l| l.unwrap()).collect();

    let mut iter = passports.iter();

    let height = Regex::new(r"^(\d+)(cm|in)$").unwrap();
    let colour = Regex::new(r"^#[0-9a-f]{6}$").unwrap();
    let pidr = Regex::new(r"^[0-9]{9}$").unwrap();

    let mut valid = 0;
    loop {
        let result: Vec<&String> = iter.by_ref().take_while(|c| !c.is_empty()).collect();
        if result.is_empty() {
            break;
        }

        let tags: HashMap<&str, &str> = result
            .iter()
            .flat_map(|s| s.split_whitespace())
            .map(|f| {
                let fields: Vec<&str> = f.split(':').collect();
                (*fields.first().unwrap(), *fields.last().unwrap())
            })
            .collect();

        let byr: u64 = match tags.get("byr").and_then(|d| Some(d.parse())) {
            Some(Ok(byr)) => byr,
            _ => continue
        };
        let iyr: u64 = match tags.get("iyr").and_then(|d| Some(d.parse())) {
            Some(Ok(d)) => d,
            _ => continue
        };
        let eyr: u64 = match tags.get("eyr").and_then(|d| Some(d.parse())) {
            Some(Ok(d)) => d,
            _ => continue
        };
        let pid: &str = match tags.get("pid") {
            Some(d) => d,
            _ => continue
        };
        let hgt: &str = match tags.get("hgt") {
            Some(d) => d,
            _ => continue
        };
        let hcl: &str = match tags.get("hcl") {
            Some(d) => d,
            _ => continue
        };
        let ecl: &str = match tags.get("ecl") {
            Some(d) => d,
            _ => continue
        };

        if byr < 1920 || byr > 2002 {
            println!("{:?} has invalid byr", result);
            continue;
        }

        if iyr < 2010 || iyr > 2020 {
            println!("{:?} has invalid iyr", result);
            continue;
        }

        if eyr < 2020 || eyr > 2030 {
            println!("{:?} has invalid eyr", result);
            continue;
        }

        let c = height.captures(hgt).and_then(|cap| {
            match &cap[2] {
                "cm" => { 
                    let n: u64 = cap[1].parse().unwrap();
                    Some(n >= 150 && n <= 193)
                },
                "in" => { 
                    let n: u64 = cap[1].parse().unwrap();
                    Some(n >= 59 && n <= 76)
                },
                _ => Some(false),
            }
        });
        match c {
            Some(false) | None => {
                println!("{:?} has invalid hgt", result);
                continue
            },
            _ => ()
        }

       if !colour.is_match(hcl) {
           println!("{:?} has invalid hcl", result);
           continue
       }

       match ecl {
        "amb" | "blu" | "brn" | "gry" | "grn" | "hzl" | "oth" => (),
        _ => {
            println!("{:?} has invalid ecl", result);
            continue
        }
       }

       if !pidr.is_match(pid) {
           println!("{:?} has invalid pid", result);
           continue
       }

        valid += 1;
    }

    println!("{}", valid);
}
