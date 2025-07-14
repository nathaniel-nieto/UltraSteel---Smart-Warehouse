from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import qrcode
import mysql.connector
import os

app = Flask(__name__)

def determinar_turno(hora):
    if 6 <= hora < 14:
        return "Matutino"
    elif 14 <= hora < 22:
        return "Vespertino"
    else:
        return "Nocturno"

@app.route('/api/kit', methods=['POST'])
def registrar_kit():
    data = request.json
    operador = data['Operador']
    tipo = data['Tipo']
    if not str(tipo).isdigit() or int(tipo) not in [1, 2, 3, 4, 5]:
        return jsonify({"status": "error", "message": "Tipo de kit inválido (solo 1, 2, 3, 4 o 5)"}), 400

    # Fecha y hora actual
    ahora = datetime.now()
    fecha = ahora.strftime("%Y-%m-%d")
    hora = ahora.strftime("%H:%M")
    turno = determinar_turno(ahora.hour)
    id_kit = str(uuid.uuid4())[:8]

    # Información completa
    item = {
        'id': id_kit,
        'Tipo': tipo,
        'Operador': operador,
        'Fecha': fecha,
        'Hora': hora,
        'Turno': turno
    }

    # Guardar en base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="********",
        database="ultrasteeldata"
    )
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO almacen (id, tipo, operador, fecha, hora, turno, estatus)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        item['id'], item['Tipo'], item['Operador'],
        item['Fecha'], item['Hora'], item['Turno'], 'En almacén'
    ))
    conn.commit()
    cursor.close()
    conn.close()
    
  # Crear carpeta si no existe
    carpeta = "qrs_generados"
    os.makedirs(carpeta, exist_ok=True)

    # Generar QR personalizado
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=5,  # tamaño del cuadrado (ajustar aquí para reducir el tamaño físico)
        border=2     # margen en cuadros
    )
    qr.add_data(str(item))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Guardar QR en carpeta
    img.save(os.path.join(carpeta, f"kit_{tipo}_{id_kit}.png"))
    

    return jsonify({"status": "success", "id": id_kit})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
