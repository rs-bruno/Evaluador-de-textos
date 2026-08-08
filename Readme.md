# Clasificador

## Objetivo

El objetivo de la siguiente herramienta es ser capaz de clasificar textos en español por dificultad de lectura. También, dados dos textos, ser capaz de comparar la dificultad relativa entre ellos. Con éste objetivo se definen los conceptos teóricos de _"riqueza sintáctica"_ y _"riqueza semántica"_. Luego se implementa una métrica que es capaz de estimar la _"riqueza semántica"_ de un texto dado (la estimación está lejos de la métrica teórica ideal, pero aún así es suficiente para lograr una buena aproximación al objetivo de comparar la dificultad relativa entre dos textos y clasificarlos por dificultad).

## Casos de prueba v3.0.0

La siguiente es una tabla que muestra la evaluación de las riquezas semántica y sintáctica de cada uno de los textos de prueba, como observación, la tabla se ordenó por riqueza semántica decreciente, pero resultó ser que la riqueza sintáctica también está ordenada de forma decreciente (con la excepción de la Ilíada y la Odisea en cuyo caso la riqueza sintáctica es casi igual), indicando una alta correlación entre riquezas sintáctica y semántica.

|  Nombre obra | Autor | Riqueza sintáctica | Riqueza semántica |
| --- | --- | --- | --- |
| Diccionario de la lengua española (edición del tricentenario) | Real Academia Española | 14.73% (108408 / 735532) | 99.39% (77521 / 77991) |
| 4 3 2 1 | Paul Auster | 2.46% (18163 / 735532) | 11.93% (9309 / 77991) |
| La santa biblia | Anónimo | 2.33% (17146 / 735532) | 8.86% (6912 / 77991) |
| Don Quijote de la Mancha | Miguel de Cervantes | 2.05% (15144 / 735532) | 8.56% (6677 / 77991) |
| Cien años de soledad | Gabriel García Márquez | 1.61% (11852 / 735532) | 8.51% (6638 / 77991) |
| Odisea | Homero | 1.25% (9267 / 735532) | 5.22% (4072 / 77991) |
| Ilíada | Homero | 1.26% (9299 / 735532) | 5.01% (3911 / 77991) |
| Las mil y una Noches | Anónimo | 0.89% (6568 / 735532) | 4.54% (3546 / 77991) |
| El alquimista | Paulo Coelho | 0.53% (3964 / 735532) | 2.67% (2089 / 77991) |
| El principito | Saint-Exúpery | 0.31% (2294 / 735532) | 1.87% (1459 / 77991) |

La siguiente tabla muestra las mismas obras ordenadas por dificultad.

|  Nombre obra | Dificultad |
| --- | --- |
| Diccionario de la lengua española (edición del tricentenario) | 1199.13 |
| La santa biblia | 353.20 |
| 4 3 2 1 | 312.05 |
| Don Quijote de la Mancha | 273.08 |
| Cien años de soledad | 208.91 |
| Ilíada | 162.91 |
| Odisea | 153.89 |
| Las mil y una Noches | 140.67 |
| El alquimista | 103.08 |
| El principito | 75.51 |

## Definiciones 

Dado **S**, el conjunto de todas las palabras que la gramática del idioma español permite generar, y **T** un texto en español, se definen riqueza sintáctica y riqueza semántica de **T** como sigue:

**riqueza_sintáctica(T)** = |**palabras_distintas(T)**| / |**S**|

Notar que si a **T** le agregamos diferentes conjugaciones de un mismo verbo, la cantidad |**palabras_distintas(T)**| aumenta y en consecuencia **riqueza_sintáctica(T)** también. Un verbo regular en el idioma español tiene 52 conjugaciones distintas, por lo que, un texto que usa todas las conjugaciones de dos verbos distintos tendrá una riqueza sintáctica significativamente mayor que uno que usa sólo una conjugacion de 10 verbos diferentes. Lo mismo sucede agregando diferentes formas de un mismo sustantivo o adjetivo, por ejemplo "perro", "perros", "perra" y "perras", las cuatro son palabras distintas y por ende un texto que use las 4 tiene mayor riqueza sintáctica que uno que use solo una de ellas.

Las observaciones anteriores dejan claro que dados dos textos **T1** y **T2**, tales que **riqueza_sintáctica(T1)** > **riqueza_sintáctica(T2)** no necesariamente significa que el texto **T1** sea más rico en vocabulario que **T2**. Menos aún sería posible afirmar algo sobre la _"riqueza semántica"_, intuitivamente definida como la cantidad de ideas y conceptos distintos referenciados por un texto.

Antes de pasar a definir los conceptos utilizados para construir nuestra aproxiación de una métrica para la "riqueza semántica", vale la pena observar que, si existiera una métrica exacta para lo que pretendemos definir, llamémosla **R_SEM(T)**, la misma sería _"invariante por sinónimos"_ e _"invariante por definiciones"_.

Más precisamente, sea **T2** un texto que resulta de concatenarle a **T1** sinónimos de alguna de las palabras ya existentes en **T1**, entonces **R_SEM(T2)** = **R_SEM(T1)** ya que ambos textos referencian las mismas ideas y conceptos (en **T2** sólo agregamos sinónimos de palabras existentes en **T1**). También dado **T3**, un texto que resulta de sustituir en **T1** una de sus palabras por su definición, se tiene **R_SEM(T3)** = **R_SEM(T1)**, ya que de nuevo, una palabra y su definición son una misma idea.

De esas dos propiedades se pueden derivar otras como que concatenarle a un texto la definición de una de sus palabras no varía su riqueza semántica, lo cual se debe a que podemos primero concatenarle una palabra ya existente (es sinónima de si misma) y luego sustituirla por su definición, ambos pasos sin variar la riqueza semántica original del texto. La aproximación que construiremos no tendrá en cuenta estas dos propiedades y por lo tanto se parecerá más a una métrica de _"riqueza de vocabulario"_.

Con el fin de definir una métrica que aproxime el concepto de riqueza semántica mejor que la ya definida _"riqueza sintáctica"_, utilizaremos la idea de _"palabra derivada"_.
Ejemplos de palabras derivadas serían:
- Todas las conjugaciones de un verbo en infinitivo, ej: amar -> amo, amaste, amamos, amabais.
- Plurales masculinos y formas femeninas de sustantivos y adjetivos, ej: oso -> osos, osa, osas.
- Adverbios derivados de adjetivos, los cuales a su vez se derivan de sustantivos, ej: velocidad -> veloz -> velozmente.
- Diminutivos, ej: perro -> perrito.

Una palabra **p** es derivada inmediata de otra **b** si existe en la gramática española una regla de construcción de palabras que permita construir **p** a partir de **b**.

Denotamos **b**->**p** al hecho de que **p** es derivada inmediata de **b**.

La lista de criterios de derivación dada anteriormente no es exhaustiva. En lo que sigue asumimos que se conocen todos los criterios de derivación y que para toda palabra **p** de **S**, existe a lo sumo una derivación inmediata que construye a **p** (puede no existir ninguna en cuyo caso decimos que **p** es una palabra primitiva).

Una palabra **p** es derivada de **b**, si se cumple una de las siguientes condiciones: 

1. **p** == **b**.

2. Existe una secuencia finita y no vacía de derivaciones inmediatas tales que:
	- La primera derivación tiene como palabra base a **b**.
	- La ultima como palabra derivada a **p**.
	- Y para toda derivación posterior a la primera, la palabra base es la palabra derivada en la derivación anterior.

Denotamos **b**-->**p** el hecho de que exista una derivación de **p** a partir de **b**.

Definimos largo de una derivacion como:
- len(**p1**-->**p2**) = 0, si **p1** == **p2**.
- len(**p1**-->**p2**) = cantidad de derivaciones inmediatas que forman la secuencia si **p1** != **p2**.

Definimos la relación de "equivalencia semántica" **=SEM** entre dos palabras **p1** y **p2** de S como:

**p1 =SEM p2** <=> (existe **p3**: **p3**-->**p1** y **p3**-->**p2**)

La relación **=SEM**, así definida, es en efecto una relación de equivalencia. 

<details>

<summary> Ver demostración </summary>

1.	**p1 =SEM p1**: ya que **p1**-->**p1** por ser **p1** == **p1**.
2.	Si **p1 =SEM p2**, existe **p3**: **p3**-->**p1** y **p3**-->**p2**, entonces, para el mismo **p3**: **p3**-->**p2** y **p3**-->**p1**, es decir **p2 =SEM p1**.
3.	Si **p1 =SEM p2** y **p2 =SEM p3**, existen **p4** y **p5** tales que:
	- **p4**-->**p1** y **p4**-->**p2**
	- **p5**-->**p2** y **p5**-->**p3**
	
	Por inducción en los largos de **p4**-->**p2** y **p5**-->**p2** demostraremos que hay un ancestro común a **p3** y **p1**.
	
	- Largos 0 y 0: **p4** == **p2**, **p5** == **p2**, entonces **p5** == **p4**, entonces el ancestro común a **p3** y **p1** es **p4**.
	- Largos 0 y n+1, asumiendo cierto 0 y n: **p4** == **p2**, entonces hay una derivación **p5**-->**p4**, concatenandole la derivación **p4**-->**p1** tenemos que **p5**-->**p1**, por lo tanto **p5** es un ancestro común a **p1** y **p3** (no  usamos la hipótesis inductiva).
	- Largos n+1 y 0, asumiendo ciertto n y 0: **p5** == **p2**, entonces hay una derivación **p4**-->**p5**, concatenandole la derivacion **p5**-->**p3** tenemos que **p4**-->**p3**, por lo tanto **p4** es un ancestro común a **p1** y **p3** (no usamos la hipótesis inductiva).
	- Largos m+1 y n asumiendo cierto m y n: len(**p4**-->**p2**) = m+1, len(**p5**-->**p2**) = n, separando en casos:
	
		1. m+1 == n: m+1 > 0, entonces tanto **p4**-->**p2** como **p5**-->**p2** son secuencias de al menos una derivación inmediata. Entonces la última derivación inmediata de ambas secuencias es la misma ya que existe una única tal que deriva **p2**. Llamémosla **p_x**->**p2**, entonces existen derivaciones **p4**-->**p_x** y **p5**-->**p_x** del mismo largo tales que su última derivación  inmediata es la misma, de nuevo debido a que existe una única tal que p_x es la palabra derivada, y por ende se puede asegurar la existencia de un par de derivaciones del mismo largo **p4**-->**p_y**, **p5**-->**p_y**, con largo menor a len(**p4**-->**p_x**), debido a que las derivaciones originales son de largo finito, el proceso se puede repetir hasta hayar que existen derivaciones de largo 1, es decir derivaciones inmediatas **p4**->**p_z**, **p5**->**p_z** para un **p_z** de S, lo cual implica que **p4** es igual a **p5**.Entonces **p4** == **p5**, es ancestro común a **p1** y **p3**.
		2. m+1 > n: n > 0 (el caso n = 0 ya lo cubrimos en un paso inductivo anterior), entonces tanto **p4**-->**p2** como **p5**-->**p2** son secuencias de al menos una derivación inmediata. Entonces la última derivación inmediata de ambas secuencias es la misma ya que existe una única tal que deriva **p2**. Mediante el mismo proceso descrito en el caso anterior, que consiste en encontrar nuevos pares de derivaciones con uno menos de longitud en cada paso, y cuya palabra derivada coincide, se llega a que existen derivaciones **p4**-->**p_z** y **p5**-->**p_z**, tales que:
			- len(**p4**-->**p_z**) > 1
			- len(**p5**-->**p_z**) = 1, **p5**-->**p_z** es en realidad una derivacion inmediata **p5**->**p_z**, que coincide con la última derivación inmediata de **p4**-->**p_z**. 
		
			Luego, existe una derivación **p4**-->**p5** tal que:
		
			- len(**p4**-->**p5**) >= 1 y **p4**-->**p5** concatenado con **p5**->**p_z** es igual a la derivacion completa **p4**-->**p_z**.
		
			Dado que existe **p4**-->**p5**, concatenándole **p5**-->**p3**, se tiene que **p4**-->**p3**, por lo tanto **p4** es ancestro común de **p1** y **p3**.
		3. n > m+1: m+1 > 0, este caso es simétrico al anterior y llegamos a que existe una derivacion **p5**-->**p4**, y por lo tanto concatenandole **p4**-->**p1** se tiene que **p5**-->**p1**, por lo tanto **p5** es ancestro común de **p1** y **p3**.
			
	En todos los casos existe un **p** tal que **p**-->**p2** y **p**-->**p3**, por lo tanto se concluye que **p2 =SEM p3**.
4.	Los tres puntos anteriores muestran que **=SEM** es una relación reflexiva, simétrica y transitiva, es decir, de equivalencia.

</details>

La idea intuitiva de ésta relacion es que todas las palabras que deriven una misma palabra primitiva pertenecerán a la misma clase de equivalencia. Entonces dados los conceptos de palabra primitiva y palabra derivada, otra propiedad que debería cumplir la métrica **R_SEM(T)** es que sea _"invariante por palabras equivalentes bajo **=SEM**"_. Ésta será la propiedad principal que tratará de cumplir nuestra estimación de **R_SEM**.

Definimos entonces, dado un texto **T**, un conjunto de palabras **P**, una palabra arbitraria **s** ∈ **S**  y **eq(S)** el conjunto de clases de equivalencia de **=SEM**:

**clase_semántica(s)** = **x** ∈ **eq(S)**: **s** ∈ **x** (**s** debe de pertenecer a uno y solo un **x** ya que **eq(S)** es una partición de **S**, lo que asegura que **clase_semántica(s)** sea una función bien definida sobre **S**)

**clases_semánticas(P)**: { **clase_semántica(p)**: **p** ∈ **P** }

**clases_abarcadas(T)** = **clases_semánticas(palabras_distintas(T))**

**riqueza_semántica(T)** = |**clases_abarcadas(T)**| / |**eq(S)**|

Luego definimos dificultad de un texto como:

**dificultad(T)** = |**clases_abarcadas(T)**| / |**palabras_distintas(T)**|

Como justificación intuitiva, pensamos en la dificultad de un texto como _"cantidad de ideas sobre cantidad de palabras que se usan para describirlas"_, a dicho factor le llamaremos **factor de dificultad**. Cuanto más palabras usamos para expresar una idea mas fácil resulta su comprensión por lo tanto cuando el promedio de palabras por idea (|**palabras_distintas(T)**| / |**clases_abarcadas(T)**|) aumenta, la dificultad debe disminuir, lo que sugiere que la dificultad sea inversamente proporcional al promedio de palabras por idea (|**palabras_distintas(T)**| / |**clases_abarcadas(T)**|)^(-1) = |**clases_abarcadas(T)**| / |**palabras_distintas(T)**|.

Por último definimos esfuerzo requerido de un texto de la siguiente manera:

**esfuerzo(T)** = **dificultad(T)** * **|largo(T)|**

Es decir como el producto de la dificultad y el largo del texto (puede ser medido en palabras o en caracteres).

## Implementación
Descripción de la implementación.
WIP...
