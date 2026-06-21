import os
import re
from pathlib import Path

def listar_archivos_carpeta_combo():
    """
    Busca la carpeta 'Combo' en el dispositivo y lista los archivos disponibles
    """
    # Buscar la carpeta Combo en el directorio actual y en el raíz
    posibles_rutas = [
        Path.cwd() / "Combo",  # Carpeta Combo en el directorio actual
        Path("/") / "Combo",   # Carpeta Combo en la raíz
        Path.home() / "Combo", # Carpeta Combo en el home
    ]
    
    # También buscar en todas las unidades disponibles (Windows)
    if os.name == 'nt':  # Windows
        import string
        from string import ascii_uppercase
        for drive in ascii_uppercase:
            ruta = Path(f"{drive}:/Combo")
            if ruta.exists():
                posibles_rutas.append(ruta)
    
    # Encontrar la primera ruta que exista
    for ruta in posibles_rutas:
        if ruta.exists() and ruta.is_dir():
            return ruta
    
    return None

def obtener_archivos_txt(carpeta):
    """
    Obtiene todos los archivos .txt de la carpeta especificada
    """
    archivos = []
    for archivo in carpeta.glob("*.txt"):
        archivos.append(archivo)
    # Ordenar alfabéticamente para consistencia
    archivos.sort()
    return archivos

def mostrar_archivos(archivos):
    """
    Muestra los archivos con números para seleccionar
    """
    print("\n" + "="*50)
    print("ARCHIVOS ENCONTRADOS:")
    print("="*50)
    for i, archivo in enumerate(archivos, 1):
        # Mostrar solo el nombre del archivo
        nombre = archivo.name
        # Obtener tamaño del archivo
        tamaño = archivo.stat().st_size
        print(f"{i}. {nombre} ({tamaño} bytes)")
    print("="*50 + "\n")

def leer_archivo(ruta_archivo):
    """
    Lee un archivo y devuelve sus líneas
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        return lineas
    except UnicodeDecodeError:
        # Intentar con otra codificación
        try:
            with open(ruta_archivo, 'r', encoding='latin-1') as f:
                lineas = f.readlines()
            return lineas
        except Exception as e:
            print(f"Error al leer el archivo {ruta_archivo.name}: {e}")
            return []

def unir_archivos(archivos_seleccionados, nombre_salida):
    """
    Une los archivos seleccionados y elimina duplicados
    """
    todas_las_lineas = []
    
    for archivo in archivos_seleccionados:
        print(f"Leyendo: {archivo.name}")
        lineas = leer_archivo(archivo)
        todas_las_lineas.extend(lineas)
    
    # Eliminar líneas duplicadas preservando el orden
    lineas_unicas = []
    lineas_vistas = set()
    
    for linea in todas_las_lineas:
        # Limpiar la línea para comparación (eliminar espacios al inicio/final)
        linea_limpia = linea.strip()
        if linea_limpia and linea_limpia not in lineas_vistas:
            lineas_unicas.append(linea)
            lineas_vistas.add(linea_limpia)
    
    # Escribir el archivo de salida
    try:
        with open(nombre_salida, 'w', encoding='utf-8') as f:
            f.writelines(lineas_unicas)
        print(f"\n✅ Archivo guardado como: {nombre_salida}")
        print(f"📊 Líneas totales: {len(todas_las_lineas)}")
        print(f"📊 Líneas únicas: {len(lineas_unicas)}")
        print(f"🗑️  Duplicados eliminados: {len(todas_las_lineas) - len(lineas_unicas)}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

def validar_seleccion(seleccion, max_numero):
    """
    Valida que la selección sea válida
    """
    try:
        numeros = [int(x.strip()) for x in seleccion.split(',')]
        for num in numeros:
            if num < 1 or num > max_numero:
                print(f"❌ El número {num} no es válido. Debe estar entre 1 y {max_numero}")
                return None
        return numeros
    except ValueError:
        print("❌ Entrada inválida. Use números separados por comas (ejemplo: 1,3,5)")
        return None

def main():
    print("📁 BUSCADOR DE ARCHIVOS EN CARPETA 'Combo'")
    print("="*50)
    
    # Buscar la carpeta Combo
    carpeta_combo = listar_archivos_carpeta_combo()
    
    if not carpeta_combo:
        print("❌ No se encontró la carpeta 'Combo' en el dispositivo.")
        print("   Buscado en:")
        print("   - Directorio actual")
        print("   - Raíz del disco")
        print("   - Carpeta de usuario")
        return
    
    print(f"✅ Carpeta 'Combo' encontrada en: {carpeta_combo}")
    
    # Obtener archivos .txt
    archivos = obtener_archivos_txt(carpeta_combo)
    
    if not archivos:
        print(f"❌ No se encontraron archivos .txt en {carpeta_combo}")
        return
    
    # Mostrar archivos disponibles
    mostrar_archivos(archivos)
    
    # Solicitar selección de archivos
    while True:
        seleccion = input("🔢 Ingrese los números de los archivos a unir (separados por comas): ")
        numeros_seleccionados = validar_seleccion(seleccion, len(archivos))
        if numeros_seleccionados is not None:
            break
    
    # Obtener los archivos seleccionados
    archivos_seleccionados = [archivos[i-1] for i in numeros_seleccionados]
    
    print("\n📋 Archivos seleccionados:")
    for i, archivo in enumerate(archivos_seleccionados, 1):
        print(f"   {i}. {archivo.name}")
    
    # Solicitar nombre del archivo de salida
    while True:
        nombre_salida = input("\n📝 Ingrese el nombre del archivo de salida (ejemplo: resultado.txt): ").strip()
        if nombre_salida:
            # Asegurar que tenga extensión .txt
            if not nombre_salida.endswith('.txt'):
                nombre_salida += '.txt'
            break
        print("❌ El nombre no puede estar vacío")
    
    # Unir archivos
    print("\n🔄 Procesando archivos...")
    unir_archivos(archivos_seleccionados, nombre_salida)
    
    print("\n✨ ¡Proceso completado!")

if __name__ == "__main__":
    main()