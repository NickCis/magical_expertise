extern crate regex;
use self::regex::Regex;

use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;
use std::path::Path;

pub struct Rule {
    triggered: bool,
    pub condition: Vec<String>,
    pub result: Vec<String>,
}

impl Rule {
    fn new(line: &String) -> Result<Rule, &'static str> {
        let mut r = Rule {
            triggered: false,
            result: Vec::new(),
            condition: Vec::new(),
        };

        let syntax_regex = Regex::new(r"^\s*si\s*(.*?),\s*entonces\s*(.*?)$").unwrap();
        if !syntax_regex.is_match(line) {
            return Err("Sintaxis de regla invalida");
        }

        let captures = syntax_regex.captures(line).unwrap();
        r.result.push(String::from(captures.at(2).unwrap_or("")));

        let cond_regex = Regex::new(r"([^\s]*)\s*y?").unwrap();
        for cap in cond_regex.captures_iter(captures.at(1).unwrap_or("")){
            let cond = String::from(cap.at(1).unwrap_or(""));
            if !cond.is_empty() {
                r.condition.push(cond);
            }
        }

        return Ok(r);
    }

    pub fn is_triggered(&self) -> bool {
        self.triggered
    }

    pub fn trigger(&mut self, variables : &Vec<String>) -> bool{
        for v in &self.condition {
            match variables.iter().position(|r| r.to_string() == v.to_string()) {
                None => return false,
                _ => {}
            };
        }
        self.triggered = true;
        return true;
    }

    fn is_rule(line: &String) -> bool {
        let rule_regex = Regex::new(r"^\s*si[^,]*,\s*entonces").unwrap();
        return rule_regex.is_match(line);
    }

    pub fn to_string(&self) -> String {
        let mut ret = [
            "si".to_string(),
            self.condition.join(" y "),
            ", entonces".to_string(),
            self.result.join(" ")
        ].join(" ");
        if self.is_triggered() {
            ret = format!("[ {} ]", ret);
        }

        return ret;
    }
}

impl Clone for Rule {
    fn clone(&self) -> Rule {
        Rule {
            triggered: self.triggered,
            condition: self.condition.clone(),
            result: self.result.clone(),
        }
    }
}

pub struct BaseConocimientos {
    pub rules: Vec<Rule>,
    pub variables: Vec<String>,
}

impl BaseConocimientos {
    pub fn new() -> BaseConocimientos {
        BaseConocimientos {
            rules: Vec::new(),
            variables: Vec::new(),
        }
    }

    pub fn from(bc : &BaseConocimientos) -> BaseConocimientos {
        BaseConocimientos {
            variables: bc.variables.clone(),
            rules: bc.rules.clone(),
        }
    }

    pub fn open(path : &str) -> Result<BaseConocimientos, &'static str> {
        let mut bc = BaseConocimientos::new();

        let path = Path::new(&path);
        let file = match File::open(&path){
            Err(_) => return Err("No se pudo abrir el archivo"),
            Ok(file) => file,
        };

        let file = BufReader::new(file);

        for line in file.lines() {
            let line = match line {
                Ok(l) => l,
                Err(_) => continue
            };

            bc.parse_line(&line);
        }

        return Ok(bc);
    }

    fn parse_line(&mut self, line: &String) {
        let comment_regex = Regex::new(r"^\s*#|^\s*$").unwrap();

        if comment_regex.is_match(line){
            return;
        }

        if Rule::is_rule(line){
            match Rule::new(line) {
                Ok(rule) => self.rules.push(rule),
                Err(r) => println!("Regla invalida: {}", r),
            }
        }else{
            self.variables.push(line.to_string());
        }
    }

    pub fn to_string(&self) -> String{
        let rules : Vec<String> = self.rules.iter().map(|r| {
            r.to_string()
        }).collect();
        [
            "Reglas".to_string(),
            rules.join("\n"),
            "Conocimiento".to_string(),
            self.variables.join("\n")
        ].join("\n")
    }
}
