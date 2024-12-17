use rayon::iter::{IntoParallelIterator, ParallelIterator};

fn combo(a: u64, b: u64, c: u64, operand: u64) -> u64 {
    match operand {
        0 | 1 | 2 | 3 => operand,
        4 => a,
        5 => b,
        6 => c,
        _ => panic!("uhhhh"),
    }
}

fn main() {
    // let program = vec![0, 3, 5, 4, 3, 0];
    let program = vec![2, 4, 1, 1, 7, 5, 1, 5, 4, 0, 5, 5, 0, 3, 3, 0];
    let range = 100000000000000..1000000000000000;
    println!("The range is {range:?}");

    let max_length = 2_u64.pow(program.len() as u32 - 1);

    range.into_par_iter().for_each(|i| {
        let mut a = i;
        let mut b = 0;
        let mut c = 0;

        let mut pc = 0;
        let mut out: Vec<u64> = vec![];
        let mut steps: u64 = 0;

        while pc < program.len() {
            steps += 1;

            if steps > max_length {
                break;
            }

            let opcode = program[pc];
            let operand = program[pc + 1];

            match opcode {
                0 => {
                    a = a / 2_u64.pow(combo(a, b, c, operand) as u32);
                }
                1 => {
                    b = b ^ operand;
                }
                2 => {
                    b = combo(a, b, c, operand) % 8;
                }
                3 => {
                    if a != 0 {
                        pc = operand as usize;
                        continue;
                    }
                }
                4 => {
                    b = b ^ c;
                }
                5 => {
                    out.push(combo(a, b, c, operand) % 8);
                    if out.len() == program.len() {
                        println!("possible length match: {i}");
                    }

                    let mut bad = false;
                    for (o, p) in out.iter().zip(&program) {
                        if o != p {
                            bad = true;
                            break;
                        }
                    }

                    if bad {
                        break;
                    }
                }
                6 => {
                    b = a / 2_u64.pow(combo(a, b, c, operand) as u32);
                }
                7 => {
                    c = a / 2_u64.pow(combo(a, b, c, operand) as u32);
                }
                _ => {}
            }

            pc += 2;
        }

        if out == program {
            println!("Part 2: {i}");
        }
    });
}
