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

### Limitaciones

Para facilitar la tarea de parseo del archivo, solo se permite que las reglas tengan condiciones logicas unidas con `y`, es decir, `and`. Realmente, esto no es una limitacion, ya que la codicion logica de `o` (`or`) se puede conseguir generando un conjunto de reglas.

Por ejemplo:
Una regla con `o` se podria descomponer en dos reglas:
```
si p o q, entonces s
```
Se reemplazaria por el conjunto de reglas:
```
si p, entonces s
si q entonces s
```

Tampoco se permiten las condiciones anidadas ya que estas tambien se podrian escribirse mediante el uso de varias reglas.

Ejemplo:
```
si (p o q) y r, entonces s
```
Se reemplazaria por el siguiente conjunto de reglas:
```
si p y r, entonces s
si q y r, entonces s
```

## Ejemplo de ejecucion

### Forward chaining

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

### Backward chaining

Base de conocimientos:
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
```

Ejecucion:
```
$ ./target/debug/motor_inferencia -b caso.bc
Archivo de entrada: caso.bc
Introduce hipotesis => v
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
Hipotesis: v
 => s
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
Hipotesis: s
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
Hipotesis: v
 => s
Fin
 => p
Reglas
[ si p y q , entonces s ]
si r , entonces t
si s y t , entonces u
[ si s y r , entonces v ]
Conocimiento
p
q
r
s
v
```
