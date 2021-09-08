// Imports the other files, accessed by filename::function();
// For this to work the function in the file will need to have the "pub" keyword before it
mod printouts;
mod vars;
mod arrays;
mod functions;

fn main() {
    println!("Hello, world!");
    //printouts::run();
    //vars::run();
    //arrays::run();
    functions::run();
}
