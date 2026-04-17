import os
import re

files_to_fix = [
    "database/crud_usuario.py",
    "database/crud_brigada.py",
    "database/crud_actividad.py",
    "database/crud_turno.py",
    "database/crud_reporte.py",
    "database/crud_dashboard.py",
    "database/crud_estadisticas.py"
]

tables_to_lower = [
    "Usuario",
    "Institucion_Educativa",
    "Reporte_de_Impacto",
    "Reporte_Actividad",
    "Reporte_Incidente",
    "Brigada",
    "Actividad",
    "Turno",
    "Password_Resets",
    "Configuracion",
    "Indicador_Ambiental"
]

pattern = r"\b(FROM|JOIN|UPDATE|INTO|TABLE)\s+(" + "|".join(tables_to_lower) + r")\b"

for filepath in files_to_fix:
    if not os.path.exists(filepath):
        print(f"MISSING: {filepath}")
        continue
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    def replace_match(m):
        return f"{m.group(1)} {m.group(2).lower()}"
    
    new_content = re.sub(pattern, replace_match, content, flags=re.IGNORECASE)
    
    # Also handle the edge case where table is after a comma: "FROM Brigada b, Usuario u" -> "Usuario" is not preceded by FROM
    # Wait, the codebase almost always uses explicit JOINs: "FROM Brigada b LEFT JOIN Usuario u"
    
    if content != new_content:
        print(f"Changed {filepath}")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
    else:
        print(f"No changes in {filepath}")
