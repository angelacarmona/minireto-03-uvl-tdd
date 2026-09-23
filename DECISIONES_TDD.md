# Diario TDD

## Ciclo 1: caso más pequeño

### Red
- Prueba añadida: `test_one_feature_is_tiny`
- Técnica de diseño de pruebas empleada: prueba mínima del caso base, con un único valor de entrada.
- Motivo de elegir este caso: comenzar por la unidad más pequeña para comprobar que la funcionalidad está ausente y que la prueba detecta ese fallo.
- Fallo observado: `classify_model_size()` lanzaba `NotImplementedError` al ejecutar la prueba del caso con 1 característica.

### Green
- Código mínimo escrito:

```python
def classify_model_size(feature_count: int) -> str:
    return "tiny"
```

- Resultado de las pruebas: el caso con 1 característica pasa. Aunque la implementación es incompleta, TDD nos permite limitar el desarrollo a lo que la prueba exige en ese momento.

### Refactor
- Mejora realizada, o motivo por el que no era necesaria: no se refactoriza todavía porque no hay duplicación ni lógica compleja que justificara cambiar la estructura. El objetivo sigue siendo mantener la solución mínima y legible.

---

## Ciclo 2: validar entradas imposibles

### Red
- Prueba añadida:

```python
def test_zero_features_is_invalid():
    with pytest.raises(ValueError):
        classify_model_size(0)
```

- Técnica de diseño de pruebas empleada: prueba de validación para una condición no válida.
- Motivo de elegir este caso: garantizar que los valores fuera de rango no pasen silenciosamente y que la función sea explícita en las entradas inválidas.
- Fallo observado: la prueba fallaba porque se permitía `0` y la función no lanzaba `ValueError`.

### Green
- Código mínimo escrito:

```python
def classify_model_size(feature_count: int) -> str:
    if feature_count < 1:
        raise ValueError("feature_count debe ser positivo")
    return "tiny"
```

- Resultado de las pruebas: la validación queda reforzada y la prueba del caso inválido pasa.

### Refactor
- Mejora realizada, o motivo por el que no era necesaria: la validación es clara y expresada en una sola condición. No hace falta refactorizar porque la regla es directa y fácil de leer.

---

## Ciclo 3: primer valor límite (5 y 6)

### Red
- Pruebas añadidas:

```python
def test_five_features_is_tiny():
    assert classify_model_size(5) == "tiny"


def test_six_features_is_small():
    assert classify_model_size(6) == "small"
```

- Técnica de diseño de pruebas empleada: prueba de frontera, centrada en el límite entre `tiny` y `small`.
- Motivo de elegir este caso: los valores 5 y 6 marcan el cambio de categoría y sirven para confirmar la regla de bordes.
- Fallo observado: la función no distinguía correctamente entre 5 y 6, por lo que la prueba fallaba en el punto de cambio de límite.

### Green
- Código mínimo escrito:

```python
def classify_model_size(feature_count: int) -> str:
    if feature_count < 1:
        raise ValueError("feature_count debe ser positivo")
    if feature_count <= 5:
        return "tiny"
    return "small"
```

- Resultado de las pruebas: los casos 5 y 6 pasan correctamente. La implementación sigue siendo pequeña y acotada a la regla recién probada.

### Refactor
- Mejora realizada, o motivo por el que no era necesaria: la estructura sigue siendo legible y no requiere más separación. Antes de continuar, se revisa la batería completa para comprobar que no se ha roto nada.

---

## Ciclo 4: límite small/medium (15 y 16)

### Red
- Pruebas añadidas:

```python
def test_fifteen_features_is_small():
    assert classify_model_size(15) == "small"


def test_sixteen_features_is_medium():
    assert classify_model_size(16) == "medium"
```

- Técnica de diseño de pruebas empleada: prueba de frontera entre dos categorías consecutivas.
- Motivo de elegir este caso: comprobar que el cambio de `small` a `medium` ocurre exactamente en 16, con 15 todavía en la categoría anterior.
- Fallo observado: el valor 16 seguía siendo tratado como `small` o no se diferenciaba correctamente.

### Green
- Código mínimo escrito:

```python
def classify_model_size(feature_count: int) -> str:
    if feature_count < 1:
        raise ValueError("feature_count debe ser positivo")
    if feature_count <= 5:
        return "tiny"
    if feature_count <= 15:
        return "small"
    return "medium"
```

- Resultado de las pruebas: los límites 15 y 16 quedan cubiertos y la función sigue respetando el rango de cada categoría.

### Refactor
- Mejora realizada, o motivo por el que no era necesaria: la lógica se mantiene simple mediante condiciones encadenadas. Aunque ya hay varias ramas, la complejidad sigue siendo baja y clara.

---

## Ciclo 5: límite medium/large (30 y 31)

### Red
- Pruebas añadidas:

```python
def test_thirty_features_is_medium():
    assert classify_model_size(30) == "medium"


def test_thirty_one_features_is_large():
    assert classify_model_size(31) == "large"
```

- Técnica de diseño de pruebas empleada: prueba de frontera final, para confirmar el cambio de `medium` a `large`.
- Motivo de elegir este caso: validar el último límite del criterio y completar la clasificación completa del rango definido.
- Fallo observado: la función no separaba 30 de 31 y la prueba mostraba el fallo en el último extremo del dominio válido.

### Green
- Código mínimo escrito:

```python
def classify_model_size(feature_count: int) -> str:
    if feature_count < 1:
        raise ValueError("feature_count debe ser positivo")
    if feature_count <= 5:
        return "tiny"
    if feature_count <= 15:
        return "small"
    if feature_count <= 30:
        return "medium"
    return "large"
```

- Resultado de las pruebas: las fronteras 30 y 31 quedan correctas y la clasificación completa queda implementada.

### Refactor
- Mejora realizada, o motivo por el que no era necesaria: la solución ya está expresada de forma directa y sin duplicación; el refactor se centra en reducir repetición en las pruebas, no en la lógica de producción.

---

## Refactor de las pruebas con parametrización

### Red
- Se comprueba que todas las pruebas de frontera pasan con la lógica actual.
- Motivo: las pruebas de límites comparten la misma estructura y se pueden expresar de forma más compacta sin perder cobertura.

### Green
- Se reescribe la batería para usar `pytest.mark.parametrize`:

```python
@pytest.mark.parametrize(
    ("feature_count", "expected"),
    [
        (1, "tiny"),
        (5, "tiny"),
        (6, "small"),
        (15, "small"),
        (16, "medium"),
        (30, "medium"),
        (31, "large"),
    ],
)
def test_classify_model_size(feature_count, expected):
    assert classify_model_size(feature_count) == expected
```

- Resultado: la parametrización cubre los mismos casos de frontera y mantiene la prueba legible.

### Refactor
- Se eliminan las pruebas específicas redundantes, pero se conserva la prueba de excepción por ser un comportamiento distinto: `test_zero_features_is_invalid()`.
- El conjunto final queda más compacto y más fácil de mantener, sin perder la intención original de cada caso.

---

## Validación final

La función queda con esta versión final:

```python
def classify_model_size(feature_count: int) -> str:
    if feature_count < 1:
        raise ValueError("feature_count debe ser positivo")
    if feature_count <= 5:
        return "tiny"
    if feature_count <= 15:
        return "small"
    if feature_count <= 30:
        return "medium"
    return "large"
```

El proceso sigue el ciclo TDD de forma disciplinada: añadir una prueba pequeña, comprobar el fallo, implementar el mínimo necesario, validar y refactorizar solo si aporta valor. Este diario documenta cada decisión tomada durante la evolución de la función.
