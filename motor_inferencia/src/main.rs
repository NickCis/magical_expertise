//mod base_conocimientos;
extern crate getopts;

use std::env;
use getopts::Options;
use std::io;

mod base_conocimientos;
mod forward;


fn do_backward(inp: &str){
    // Aca tenes que implementar el back

}

fn do_forward(inp: &str){
    let f = match forward::ForwardChaining::new(inp) {
        Err(e) => panic!("Error: {}", e),
        Ok(f) => f,
    };

    println!("Opciones:\n\ts: siguiente paso\n\ta: anterior paso\n\tp: imprimir informacion\n\te: salir");

    loop {
        let mut opt = String::new();
        io::stdin().read_line(&mut opt)
            .ok()
            .expect("Error leyendo opcion");

        match opt.trim() {
            "s" => f.next(),
            "a" => f.prev(),
            "p" => f.print(),
            "e" => break,
            _ => {
                println!("'{}' : opcion invalida", opt);
                continue;
            },
        };
    }
}

fn print_usage(program: &str, opts: Options){
    let brief = format!("Usage: {} FILE [options]", program);
    print!("{}", opts.usage(&brief));
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let program = args[0].clone();

    let mut opts = Options::new();
    //opts.optopt("o", "output", "archivo de salida", "PATH");
    //opts.optflag("d", "debug", "activa modo debug");
    opts.optflag("b", "backward", "backward chaining");
    opts.optflag("h", "help", "imprime esta ayuda");

    let matches = match opts.parse(&args[1..]) {
        Ok(m) => { m }
        Err(f) => { panic!(f.to_string()) }
    };

    if matches.opt_present("h") {
        print_usage(&program, opts);
        return;
    }

    let input = if !matches.free.is_empty() {
        matches.free[0].clone()
    } else {
        print_usage(&program, opts);
        return;
    };

    println!("Archivo de entrada: {}", input);

    if matches.opt_present("b") {
        do_backward(&input);
    }else{
        do_forward(&input);
    }
}
