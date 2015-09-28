# Motor de inferencia

```
$ cargo build
 ...

$ cargo run
     Running `target/debug/motor_inferencia`
Usage: target/debug/motor_inferencia FILE [options]

Options:
    -b, --backward      backward chaining
    -h, --help          imprime esta ayuda
```

Ejemplo de archivo de base de conocimiento:

```
# Reglas
si p y q, entonces s
si r, entonces t
si s y t, entonces u
si s y r, entonces v

# Conocimiento
p
q
r
s
```


## Archivos de base de conocimiento

Se toma como regla todo lo que comience con `si` seguido de condiciones logicas, que podrian ser unidas con `y` finalizadas las condiciones con una `,`, seguida de la palabra `entonces` y despues el resultado.

```
si <cond1> y <cond2> y <...>, entonces <resultado>
```


Se toma como conocimiento inicial todas las lineas que no sean reglas.

Se debe escribir una regla o un conocimiento por linea.

Se ignoran las lineas vacias o las que comiencen con el caracter numeral `#`.


## Ejemplo de ejecucion
Archivo de base de conocimiento:

```
$ cat caso.bc
# Reglas
si p y q, entonces s
si r, entonces t
si s y t, entonces u
si s y r, entonces v

# Conocimiento
p
q
r
s

```

Ejecucion:
```
$ cargo run caso.bc
     Running `target/debug/motor_inferencia caso1.bc`
Archivo de entrada: caso1.bc
Opciones:
        s: siguiente paso
        a: anterior paso
        p: imprimir informacion
        q: salir
 => p
Reglas
si p y q , entonces s
si r , entonces t
si s y t , entonces u
si s y r , entonces v
Conocimiento
p
q
r
s
 => s
 => p
Reglas
[ si p y q , entonces s ]
si r , entonces t
si s y t , entonces u
si s y r , entonces v
Conocimiento
p
q
r
s
 => s
 => p
Reglas
[ si p y q , entonces s ]
[ si r , entonces t ]
si s y t , entonces u
si s y r , entonces v
Conocimiento
p
q
r
s
t
 => s
 => p
Reglas
[ si p y q , entonces s ]
[ si r , entonces t ]
[ si s y t , entonces u ]
si s y r , entonces v
Conocimiento
p
q
r
s
t
u
 => s
 => p
Reglas
[ si p y q , entonces s ]
[ si r , entonces t ]
[ si s y t , entonces u ]
[ si s y r , entonces v ]
Conocimiento
p
q
r
s
t
u
v
 => s
Fin
=> q
```
