# Proyecto de Comparación: HyperLogLog vs HashSets para Conteo Único

## Descripción

Este proyecto realiza una comparación entre el algoritmo **HyperLogLog** y las estructuras **HashSet** tradicionales para el conteo de elementos únicos en grandes volúmenes de datos. El enfoque principal es analizar el consumo de memoria de ambas aproximaciones bajo diferentes escenarios de datos.

El proyecto simula el conteo de direcciones IPv4 (representadas como números enteros) y permite configurar parámetros como el volumen total de datos y el porcentaje de elementos únicos, midiendo sistemáticamente el uso de memoria mientras se escalan estos parámetros.

## Características

- **Generación de datos controlada**: Produce datasets con un porcentaje predefinido de elementos únicos
- **Comparación de algoritmos**:
  - **HyperLogLog**: Algoritmo probabilístico para estimar cardinalidad
  - **HashSet**: Enfoque tradicional con conteo exacto
- **Medición de memoria**: Monitorea el consumo de memoria en tiempo real
- **Escalabilidad**: Pruebas iterativas desde volúmenes pequeños hasta grandes conjuntos de datos
- **Métricas detalladas**: Compara precisión vs eficiencia de memoria

## Requisitos

- Python 3.7+
- Bibliotecas requeridas:
  - `datasketch` (para HyperLogLog)
  - `Pympler` (para medición de memoria)
  - `matplotlib` (para visualización)

## Instalación

1. Clonar o descargar el proyecto
2. Crear un entorno virtual de python
```bash
python3 -m venv .venv
```
3. Activar entorno virtual
- En Windows
```commandline
source .venv\bin\Scripts\activate.bat
```
- En sistemas Linux
```bash
source ./.venv/bin/activate
```
4. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Estructura del Proyecto

```
proyecto-conteo/
├── main.py                 # Script principal de comparación
├── data_generator.py       # Generador de datos sintéticos
├── memory_tests.py         # Pruebas de memoria de los algoritmos
└── README.md
```

## Uso

Ejecuta el script principal:

```bash
python main.py
```

### Configuración de Parámetros

En el archivo `main.py`, puedes modificar los siguientes parámetros:

```python
# Configuración de la prueba
INITIAL_MAX_REGISTER_COUNT = 200_000  # Tamaño inicial del dataset
END_MAX_REGISTER_COUNT = 2_000_000    # Tamaño máximo del dataset
LOOP_STEP = 200_000                   # Incremento por iteración
UNIQUE_VALUES_PERCENT = 0.5           # Porcentaje de unicidad en total de datos
HYPERLOGLOG_p = 12                    # Precisión del HyperLogLog (afecta memoria/accuracy)
```

## Métodos de Conteo Comparados

### 1. HyperLogLog
- **Tipo**: Algoritmo probabilístico
- **Ventaja**: Memoria constante independiente del número de elementos únicos
- **Desventaja**: Estimación aproximada (error ~1.04/√m)
- **Uso de memoria**: ~1.5 KB para precisión estándar

### 2. HashSet (Conjunto tradicional)
- **Tipo**: Estructura de datos exacta
- **Ventaja**: Conteo 100% preciso
- **Desventaja**: Memoria lineal con el número de elementos únicos
- **Uso de memoria**: ~20-30 MB por millón de elementos únicos

## Ejemplo de Salida

```
=== LOOP 1 ===
Datos totales: 1,000,000 | Unicos: 100,000 (10.0%)
HyperLogLog:
  - Elementos estimados: 99,850
  - Memoria utilizada: 1.54 KB
HashSet:
  - Elementos contados: 100,000
  - Memoria utilizada: 25.67 MB
Ratio memoria: 17,058x (HashSet/HyperLogLog)
```

## Resultados Esperados

El proyecto generará comparativas que demuestran:

1. **Memoria constante** de HyperLogLog vs **crecimiento lineal** de HashSet
2. **Trade-off** entre precisión y eficiencia de memoria
3. **Puntos de quiebre** donde HyperLogLog se vuelve más conveniente
4. **Impacto** del porcentaje de unicidad en la eficiencia

## Aplicaciones Prácticas

- Análisis de tráfico de red (conteo de IPs únicas)
- Métricas de usuarios únicos en plataformas web
- Análisis de logs a gran escala
- Sistemas de monitorización con restricciones de memoria

## Limitaciones

- HyperLogLog proporciona estimaciones, no conteos exactos
- La generación de datos es sintética (basada en números aleatorios)
- Las mediciones de memoria pueden variar según el entorno de ejecución

## Personalización

Puedes extender el proyecto para:
- Probar con diferentes tipos de datos (strings, UUIDs, etc.)
- Implementar otros algoritmos probabilísticos (Count-Min Sketch, Bloom Filter)
- Agregar visualizaciones gráficas de los resultados
- Probar con datasets reales en lugar de sintéticos

## Licencia

Este proyecto es para fines educativos y de investigación.