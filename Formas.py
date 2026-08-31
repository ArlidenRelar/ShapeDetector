
import cv2

# Abrir la cámara
camara = cv2.VideoCapture(0)

while True:

    # Capturar imagen
    _, imagen = camara.read()

    # Convertir a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Convertir a blanco y negro
    _, negro = cv2.threshold(gris, 100, 255, cv2.THRESH_BINARY)

    # Buscar contornos
    contornos, _ = cv2.findContours(
        negro,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # Analizar cada contorno
    for contorno in contornos:

        # Ignorar objetos muy pequeños
        area = cv2.contourArea(contorno)

        if area < 500:
            continue

        # Aproximar la forma
        perimetro = cv2.arcLength(contorno, True)

        vertices = cv2.approxPolyDP(
            contorno,
            0.04 * perimetro,
            True
        )

        # Número de vértices
        lados = len(vertices)

        # Obtener posición
        x, y, w, h = cv2.boundingRect(contorno)

        # Reconocer forma
        if lados == 3:
            forma = "Triangulo"

        elif lados == 4:

            # Comprobar si es cuadrado
            proporcion = w / float(h)

            if 0.9 <= proporcion <= 1.1:
                forma = "Cuadrado"
            else:
                forma = "Rectangulo"

        else:
            forma = "Circulo"

        # Dibujar contorno
        cv2.drawContours(imagen, [contorno], -1, (0, 255, 0), 2)

        # Escribir nombre
        cv2.putText(
            imagen,
            forma,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    # Mostrar cámara
    cv2.imshow("Reconocimiento de formas", imagen)

    # Presionar Q para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cerrar todo
camara.release()
cv2.destroyAllWindows()