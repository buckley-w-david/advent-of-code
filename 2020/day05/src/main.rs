use std::fs::File;
use std::io::{self, BufRead};


fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file = File::open("input")?;
    let passes: Vec<String> = io::BufReader::new(file).lines().map(|l| l.unwrap()).collect();

    let mut seats = Vec::new();
    for pass in passes {
        let mut chars = pass.chars();
        let mut row_t = 128;
        let mut row_b = 0;
        for _ in 0..7 {
            match chars.next() {
                Some('F') => row_t -= (row_t - row_b) / 2,
                Some('B') => row_b += (row_t - row_b) / 2,
                _ => (),
            }
        }
        let row = row_b;

        let mut col_t = 8;
        let mut col_b = 0;
        for _ in 0..3 {
            match chars.next() {
                Some('L') => col_t -= (col_t - col_b) / 2,
                Some('R') => col_b += (col_t - col_b) / 2,
                _ => (),
            }
        }

        let col = col_b;

        let seat_id = row*8 + col;
        seats.push((row, col, seat_id));
    }

    seats.sort();

    for window in seats.windows(3) {
        let mut win = window.iter();
        let (l, m, r) = (win.next().unwrap(), win.next().unwrap(), win.next().unwrap());
        if l.2+1 != m.2 {
            println!("{}", l.2+1);
            break;
        } else if m.2+1 != r.2 {
            println!("{}", m.2+1);
            break;
        }
    }

    Ok(())
}
