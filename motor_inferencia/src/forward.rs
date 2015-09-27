
use base_conocimientos;

// XXX: Se podria hacer un trait de chaining para que lo implementen tanto forward como backward

pub struct ForwardChaining {
    bc : Vec<base_conocimientos::BaseConocimientos>,
}

impl ForwardChaining {
    pub fn new(path: &str) -> Result<ForwardChaining, &'static str> {
        let fc = ForwardChaining {
            bc : vec![ match base_conocimientos::BaseConocimientos::open(path) {
                Ok(bc) => bc,
                Err(s) => return Err(s),
            }],
        };

        Ok(fc)
    }

    pub fn next(&mut self) {
        let mut bc_new = base_conocimientos::BaseConocimientos::from(self.bc.last().unwrap());

        // XXX: esto es un asco
        for v in &bc_new.rules {
            if v.is_triggered() {
                continue;
            }

            if(v.trigger(&bc_new.variables)){
                for r in v.result {
                    bc_new.variables.push(r);
                }
            }
        }

        self.bc.push(bc_new);
    }

    pub fn prev(&self) {
    }

    pub fn print(&self){
        println!("{}", match self.bc.last() {
            Some(b) => b.to_string(),
            None => "".to_string(),
        });
    }
}
