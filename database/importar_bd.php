<?php
/**
 * Script para importar la base de datos automáticamente
 * Ejecuta este archivo desde el navegador: http://localhost/maqueta/bd/importar_bd.php
 */

// Configuración
$host = 'localhost';
$user = 'root';
$pass = '@Juan253688910';
$db_name = 'db_brigadas_maracaibo';
$sql_file = __DIR__ . '/db_brigadas_fixed.sql';

header('Content-Type: text/html; charset=utf-8');
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Importar Base de Datos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        .success {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            border: 1px solid #c3e6cb;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            border: 1px solid #f5c6cb;
        }
        .info {
            background: #d1ecf1;
            color: #0c5460;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            border: 1px solid #bee5eb;
        }
        pre {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 Importar Base de Datos</h1>
        
        <?php
        try {
            // Conectar a MySQL (sin seleccionar base de datos)
            $conexion = new mysqli($host, $user, $pass);
            
            if ($conexion->connect_error) {
                throw new Exception("Error de conexión: " . $conexion->connect_error);
            }
            
            echo '<div class="success">✓ Conexión a MySQL exitosa</div>';
            
            // Crear base de datos si no existe
            $conexion->query("CREATE DATABASE IF NOT EXISTS `$db_name` CHARACTER SET utf8 COLLATE utf8_general_ci");
            echo '<div class="info">✓ Base de datos "' . $db_name . '" verificada/creada</div>';
            
            // Seleccionar la base de datos
            $conexion->select_db($db_name);
            
            // Leer el archivo SQL
            if (!file_exists($sql_file)) {
                throw new Exception("El archivo SQL no existe: $sql_file");
            }
            
            $sql = file_get_contents($sql_file);
            
            if (empty($sql)) {
                throw new Exception("El archivo SQL está vacío");
            }
            
            echo '<div class="info">✓ Archivo SQL leído correctamente</div>';
            
            // Ejecutar el SQL
            // Dividir en múltiples consultas
            $queries = array_filter(
                array_map('trim', explode(';', $sql)),
                function($query) {
                    return !empty($query) && 
                           !preg_match('/^--/', $query) && 
                           !preg_match('/^SET\s+@/', $query);
                }
            );
            
            $success_count = 0;
            $error_count = 0;
            $errors = [];
            
            foreach ($queries as $query) {
                if (empty(trim($query))) continue;
                
                // Saltar comentarios y configuraciones SET
                if (preg_match('/^(--|SET\s+@|CREATE\s+SCHEMA|USE)/i', trim($query))) {
                    continue;
                }
                
                if ($conexion->query($query)) {
                    $success_count++;
                } else {
                    $error_count++;
                    $errors[] = $conexion->error . " (Query: " . substr($query, 0, 50) . "...)";
                }
            }
            
            echo '<div class="success">✓ Consultas ejecutadas: ' . $success_count . '</div>';
            
            if ($error_count > 0) {
                echo '<div class="error">✗ Errores: ' . $error_count . '</div>';
                foreach ($errors as $error) {
                    echo '<div class="error">' . htmlspecialchars($error) . '</div>';
                }
            }
            
            // Verificar tablas creadas
            $resultado = $conexion->query("SHOW TABLES");
            $tablas = [];
            if ($resultado) {
                while ($fila = $resultado->fetch_array()) {
                    $tablas[] = $fila[0];
                }
            }
            
            if (count($tablas) > 0) {
                echo '<div class="success">✓ Tablas creadas: ' . count($tablas) . '</div>';
                echo '<ul>';
                foreach ($tablas as $tabla) {
                    echo '<li>' . htmlspecialchars($tabla) . '</li>';
                }
                echo '</ul>';
            }
            
            $conexion->close();
            
            echo '<div class="success"><strong>✓ Importación completada!</strong></div>';
            echo '<p><a href="../verificar_conexion.php">Verificar conexión</a> | <a href="../index.html">Ir al formulario</a></p>';
            
        } catch (Exception $e) {
            echo '<div class="error"><strong>✗ Error:</strong> ' . htmlspecialchars($e->getMessage()) . '</div>';
        }
        ?>
    </div>
</body>
</html>
