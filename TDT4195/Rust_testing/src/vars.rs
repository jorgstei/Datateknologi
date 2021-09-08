// Variables hold primitive data or references to data
// Variables are by default immutable, solved my mut keyword
// Block scoped

pub fn run() {
    let name = "Jørgen";
    let mut avgSmashGSP = 8000000;
    // i got better wohoo
    avgSmashGSP = 8000002;
    println!("Hey my smash gsp is currently {}", avgSmashGSP);

    // Assign multiple vars in a tuple
    let (person, gsp) = ("erkos", 10000000);
    println!("Holy moly {}'s gsp is {}", person, gsp);

    // Types
    /*
    Integers: u for unsigned (not + -), i for normal signed integers u8-128, i8-128
    Floats: f32, f64
    Boolean: bool
    Characters: char, intialized with ''
    Tuples: ()
    Arrays: Fixed length in rust (like java), vectors are scalable (like arraylist)
    */

    // Rust is statically typed and therefore needs to know the type of every variable, but it infers this at compile time. 
    // For example the default for integers like this is i32
    let x = 1;
    
    // Default is f64
    let y = 2.5;

    // Add explicit type
    let z: i64 = 893219818;

    // Find max size of int like this:
    println!("Max i32: {}", std::i32::MAX);
    println!("Max i64: {}", std::i64::MAX);

    // Print emoji for the memes (emojis are unicode so they count as chars):

    let shit = '\u{1F4A9}';
    println!("{}", shit);

    // Strings are immutable
    let str1 = "Hey";

    // Mutable if we construct them like this, because hehe good language
    let mut str2 = String::from("Hello");
    // Mutate them by adding or removing chars:
    str2.push('W');
    // Or adding / removing strings
    str2.push_str("orld");
    // They have props like .len(), .capacity(), .is_empty(), .contains(), .replace("World", "There"), .split_whitespace()
    println!("{:?}", (str1, str2));

    // Assertion testing, can do it normally aswell to get a bool, but this is some funky rust stuff you can do aswell
    //assert_eq!(5, str1.len());

    

}