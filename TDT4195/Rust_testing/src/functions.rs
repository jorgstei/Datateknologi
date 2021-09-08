pub fn run(){
    let res = multiply(6,7);
    println!("{}", res);

    // Nice shorthand for functions that also allow us to use outside variables.
    let n3 = 10;
    let add_nums = |n1: i32, n2: i32| n1+n2+n3;
    println!("Add two numbers and add ten: {}", add_nums(1,3));
}

// need to specify type of parameters (in brackets) and type of return val (after ->)
// Disgusting syntax: You return shit by not adding a ; to the end of the line.
fn multiply(n1: i32, n2:i32) -> i32{
    n1 + n2;
    n1 * n2
}



