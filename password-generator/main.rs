use rand::seq::SliceRandom;
use rand::Rng;
use std::io;

fn main() {
    let mut rng = rand::thread_rng();
    
    println!("Length (min 4): ");
    let mut length = String::new();
    io::stdin().read_line(&mut length).unwrap();
    let mut length: usize = length.trim().parse().unwrap_or(4);
    length = length.max(4);
    
    println!("Use special chars? (y/n): ");
    let mut use_special = String::new();
    io::stdin().read_line(&mut use_special).unwrap();
    let use_special = use_special.trim().to_lowercase() == "y";
    
    let lower = "abcdefghijklmnopqrstuvwxyz";
    let upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    let digits = "0123456789";
    let special = "!@#$%^&*()_+-=";
    
    let mut password: Vec<char> = vec![
        lower.chars().nth(rng.gen_range(0..lower.len())).unwrap(),
        upper.chars().nth(rng.gen_range(0..upper.len())).unwrap(),
        digits.chars().nth(rng.gen_range(0..digits.len())).unwrap(),
    ];
    
    if use_special {
        password.push(special.chars().nth(rng.gen_range(0..special.len())).unwrap());
    }
    
    let all: String = format!("{}{}{}{}", 
        lower, upper, digits, 
        if use_special { special } else { "" }
    );
    
    while password.len() < length {
        password.push(all.chars().nth(rng.gen_range(0..all.len())).unwrap());
    }
    
    password.shuffle(&mut rng);
    println!("Password: {}", password.iter().collect::<String>());
}