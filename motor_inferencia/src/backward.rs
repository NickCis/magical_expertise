use base_conocimientos;

// XXX: Se podria hacer un trait de chaining para que lo implementen tanto forward como backward

pub struct BackwardChaining {
    bc : Vec<base_conocimientos::BaseConocimientos>,
    hipotesis : Vec<String>,
    end : bool,
}

impl BackwardChaining {
    pub fn new(path: &str, hipotesis: &str) -> Result<BackwardChaining, &'static str> {
        let bc = BackwardChaining {
            bc : vec![ match base_conocimientos::BaseConocimientos::open(path) {
                Ok(bc) => bc,
                Err(s) => return Err(s),
            }],
            hipotesis : vec![ hipotesis.to_string() ],
            end : false,
        };

        Ok(bc)
    }

    pub fn next(&mut self) {
        if self.has_ended() {
            return;
        }

        let mut bc_new = base_conocimientos::BaseConocimientos::from(self.bc.last().unwrap());

        // Compruebo si la hipotesis esta en la base de conocimiento
        let h = self.hipotesis.last().unwrap().clone();
        match bc_new.variables.iter().position(|v| v.to_string() == h) {
            None => {
                // Busco que regla tiene
                for rule in bc_new.rules.iter_mut() {
                    if rule.includes(&h) {
                        if rule.trigger(&bc_new.variables) {
                            match bc_new.variables.iter().position(|var| var.to_string() == h){
                                None => bc_new.variables.push(h.to_string()),
                                _ => {},
                            };

                            match self.hipotesis.len() {
                                0 => self.end = true,
                                _ => {
                                    let prev_hipo = self.hipotesis[self.hipotesis.len()-2].clone();
                                    match bc_new.variables.iter().position(|var| var.to_string() == prev_hipo.to_string()) {
                                        None => self.hipotesis.push(prev_hipo), 
                                        _ => self.end = true,
                                    };
                                },
                            };
                        } else {
                            for cond in rule.condition.iter_mut() {
                                match self.hipotesis.iter().position(|var| var.to_string() == cond.to_string()) {
                                    None => {
                                        self.hipotesis.push(cond.clone());
                                        break;
                                    },
                                    _ => {},
                                };
                            }
                        }
                        break;
                    }
                }
            },
            _ => {
            }
        };

        self.bc.push(bc_new);
    }

    pub fn prev(&mut self) {
        // Ignoramos las cosas malas
        match self.bc.len() {
            1 => {},
            _ => {
                match self.bc.pop() {
                    _ => {},
                };

                match self.hipotesis.pop() {
                    _ => {},
                };
            },
        };
    }

    pub fn print(&self){
        println!("{}", match self.bc.last() {
            Some(b) => b.to_string(),
            None => "".to_string(),
        });
        if ! self.has_ended() {
            println!("Hipotesis: {}", match self.hipotesis.last() {
                Some(h) => h.to_string(),
                None => "".to_string(),
            });
        }
    }

    pub fn has_ended(&self) -> bool {
        self.end
    }
}
