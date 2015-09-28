
use base_conocimientos;

// XXX: Se podria hacer un trait de chaining para que lo implementen tanto forward como backward

pub struct ForwardChaining {
    bc : Vec<base_conocimientos::BaseConocimientos>,
    end : bool,
}

impl ForwardChaining {
    pub fn new(path: &str) -> Result<ForwardChaining, &'static str> {
        let fc = ForwardChaining {
            bc : vec![ match base_conocimientos::BaseConocimientos::open(path) {
                Ok(bc) => bc,
                Err(s) => return Err(s),
            }],
            end : false,
        };

        Ok(fc)
    }

    pub fn next(&mut self) {
        if self.has_ended() {
            return;
        }

        let mut bc_new = base_conocimientos::BaseConocimientos::from(self.bc.last().unwrap());
        let mut has_triggered = false;

        // XXX: esto es un asco
        for rule in bc_new.rules.iter_mut() {
            if rule.is_triggered() {
                continue;
            }

            if rule.trigger(&bc_new.variables) {
                has_triggered = true;
                for result in rule.result.iter() {
                    match bc_new.variables.iter().position(|var| var == result){
                        None => bc_new.variables.push(result.clone()),
                        _ => {},
                    };
                }

                break;
            }
        }

        if has_triggered {
            self.bc.push(bc_new);
        } else {
            self.end = true;
        }
    }

    pub fn prev(&mut self) {
        // Ignoramos las cosas malas
        match self.bc.len() {
            1 => {},
            _ => match self.bc.pop() {
                _ => {},
            },
        };
    }

    pub fn print(&self){
        println!("{}", match self.bc.last() {
            Some(b) => b.to_string(),
            None => "".to_string(),
        });
    }

    pub fn has_ended(&self) -> bool {
        self.end
    }
}
