import json

def serializar_plan(plan_data: dict) -> str:
    """
    Toma un diccionario con la estructura de un plan (objetivos, hitos, recursos, estatus, etc)
    y lo serializa a JSON seguro para almacenamiento en BD.
    """
    try:
        return json.dumps(plan_data, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        print(f"Error serializando plan: {e}")
        return "{}"

def deserializar_plan(plan_json_str: str) -> dict:
    """
    Toma un string JSON de la BD y lo convierte a dict.
    Si está vacío o es inválido, devuelve la estructura base.
    """
    estructura_base = {
        "momento_escolar": "",
        "origen_actividad": "",
        "efemeride": "",
        "necesidad_detectada": "",
        "objetivo_plan": "",
        "nivel_educativo": "",
        "resultado_esperado": "",
        "resultado_obtenido": ""
    }
    
    # Si viene nulo o puramente en blanco
    if not plan_json_str or not str(plan_json_str).strip():
        return estructura_base
        
    try:
        data = json.loads(plan_json_str)
        if isinstance(data, dict):
            # Nos aseguramos de inicializar las claves mínimas si faltan
            for clave, valor_defecto in estructura_base.items():
                if clave not in data:
                    data[clave] = valor_defecto
            return data
        else:
            # Si era un JSON array válido pero no un dict
            return estructura_base
    except json.JSONDecodeError:
        # RETROCOMPATIBILIDAD: Era texto plano viejo, lo inyectamos al objetivo
        resultado = estructura_base.copy()
        resultado["objetivo_plan"] = str(plan_json_str).strip()
        return resultado
