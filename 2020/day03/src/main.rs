use std::fs::File;
use std::io::{self, BufRead};


fn main() {
    let file = File::open("input").unwrap();
    let hill: Vec<Vec<bool>> = io::BufReader::new(file).lines().map(|l| l.unwrap().chars().map(|c| c == '#').collect()).collect();
    let length = hill.iter().count();
    let width = hill.first().unwrap().iter().count();

    let slopes = &[
        (1, 1),
        (1, 3),
        (1, 5),
        (1, 7),
        (2, 1),
    ];

    let product: usize = slopes.map(|(step_y, step_x)| {
        let y_steps = (0..length).step_by(step_y);
        let x_steps = (0..width).cycle().step_by(step_x);
        y_steps.zip(x_steps).filter(|&(y, x)| hill[y][x]).count()
    }).iter().product();
    println!("{}", product);
}
