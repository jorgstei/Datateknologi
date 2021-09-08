
use std::mem;
pub fn run(){
    // Tuples can contain max 12 elements, and they can all be of different types
    // Basically objects
    let tuple: (&str, &str, u16, char) = ("Jørgen", "NTNU", 22, '\u{1F4A9}');
    println!("{} goes to {} and is {} years old. His emoji is {}", tuple.0, tuple.1, tuple.2, tuple.3);

    // Arrays are of static length and type
    let mut arr: [i32; 5] = [1,2,3,4,5];
    println!("{:?}", arr);
    // Even though they are static in len and type, they are NOT immutable if we include the mut keyword
    arr[0] = 3;
    println!("{:?}", arr);
    // Check amount of memory used by arr (needs to be a reference, &). Can include "use std::mem" to not have to write std::mem every time. Still need mem tho.
    println!("Array occupies {} bytes", mem::size_of_val(&arr));
    // Get portion of array
    let slice: &[i32] = &arr[0..2];
    println!("Slice: {:?}", slice);

    // Now static arrays are shit so lets use vectors instead
    let mut vect: Vec<i32> = vec![1,2,3,4,5];
    // Same operations as arrays, but we can now push

    vect.push(6);
    println!("After push {:?}", vect);
    vect.pop();
    println!("After pop {:?}", vect);

    // Loop through vect

    for n in vect.iter() {
        println!("Number: {}", n);
    }
    // We can also mutate the vector at the same time
    for n in vect.iter_mut() {
        *n += 2;
    }
    println!("After +2 {:?}", vect);

    // If else bla bla same shit as everywhere else, except it complains if you use parentheses around the if, still runs tho

    // We also have other loops, loop is essentially just a (better i think for compiler reasons) while true. while loop is the same as everywhere else
    let mut count = 0;
    loop{
        count += 1;
        println!("Num: {}", count);
        if(count == 4){
            break;
        }
    }

    // For range, basically same as python. inclusive..exclusive
    for n in 0..10 {
        if n % 2 == 0 {
            println!("{} is an even number", n);
        }
    }

}