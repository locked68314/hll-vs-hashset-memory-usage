from matplotlib import pyplot as plt

def format_bytes_size(bytes):
    """Convierte bytes a un formato legible."""
    for unidad in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unidad}"
        bytes /= 1024
    return f"{bytes:.2f} PB"

def transpose_data(data: dict):
    columns = [key for key in data.keys()]
    values = [value for value in data.values()]

    transposed_data = []
    sample_column = values[0]
    for index, _ in enumerate(sample_column):
        temp_list = []
        for column in values:
            temp_list.append(column[index])
        transposed_data.append(temp_list)

    return {"columns": columns, "values": transposed_data}

def tabla_comparativa(columns, data, image_name):
    # Configurar la figura y eje
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('tight')
    ax.axis('off')

    # Crear la tabla
    tabla = ax.table(
        cellText=data,
        colLabels=columns,
        cellLoc='center',
        loc='center'
    )

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.auto_set_column_width([i for i in range(len(columns))])  # Ajuste automático
    tabla.scale(1.2, 1.5)

    plt.savefig(image_name,
                dpi=300,
                bbox_inches='tight',
                facecolor='white',
                edgecolor='none')

