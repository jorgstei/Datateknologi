//Printing stuff
pub fn run() {
    // Basic printout with variables
    println!("Hey, my name is {} and I'm {} years old", "Jørgen", 2021-1999);
    // Basic printout with reused variables (brackets are marked with the index of the value you want to replace them with)
    println!("Hey, my name is {0} and I'm {1} years old. I think {0} is a great name!", "Jørgen", 2021-1999);
    // Named arguments
    println!("Hey, my name is {name} and I'm {age} years old", age = 2021-1999, name = "Jørgen");
    // Placeholder traits, essentially what you want your variable to be interpreted as.
    /*
    - ``, which uses the `Display` trait
    - `?`, which uses the `Debug` trait
    - `e`, which uses the `LowerExp` trait
    - `E`, which uses the `UpperExp` trait
    - `o`, which uses the `Octal` trait
    - `p`, which uses the `Pointer` trait
    - `b`, which uses the `Binary` trait
    - `x`, which uses the `LowerHex` trait
    - `X`, which uses the `UpperHex` trait
    */
    println!("Binary {:b}, Hex:{:x}, Octal: {:o}", 10,10,10);


    // We can also put a question mark in the brackets to make it print whatever the fk we want.
    let (x,y,z,asd) = (10,4.3,232323, "hello");
    println!("{:?}", (x,y,z,asd));
}