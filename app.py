from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

class TuringMachineEncryptor:
    def __init__(self, desplazamiento=3):
        self.desplazamiento = desplazamiento
    
    def encriptar_texto(self, texto, vueltas):
        """Encripta el texto el número de vueltas especificado."""
        resultado = texto
        for _ in range(vueltas):
            resultado = ''.join([self.encriptar_caracter(c) for c in resultado])
        return resultado
    
    def desencriptar_texto(self, texto, vueltas):
        """Desencripta el texto el número de vueltas especificado."""
        resultado = texto
        for _ in range(vueltas):
            resultado = ''.join([self.desencriptar_caracter(c) for c in resultado])
        return resultado

    def encriptar_caracter(self, caracter):
        """Encripta un solo carácter"""
        if caracter.isalpha():
            base = ord('a') if caracter.islower() else ord('A')
            return chr((ord(caracter) - base + self.desplazamiento) % 26 + base)
        return caracter
    
    def desencriptar_caracter(self, caracter):
        """Desencripta un solo carácter"""
        if caracter.isalpha():
            base = ord('a') if caracter.islower() else ord('A')
            return chr((ord(caracter) - base - self.desplazamiento) % 26 + base)
        return caracter

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encriptar', methods=['POST'])
def encriptar_endpoint():
    data = request.json
    texto = data.get('texto', '')
    desplazamiento = data.get('desplazamiento', 3)
    vueltas = data.get('vueltas', 1)
    turing_machine = TuringMachineEncryptor(desplazamiento)
    encriptado = turing_machine.encriptar_texto(texto, vueltas)
    return jsonify({"resultado": encriptado})

@app.route('/desencriptar', methods=['POST'])
def desencriptar_endpoint():
    data = request.json
    texto = data.get('texto', '')
    desplazamiento = data.get('desplazamiento', 3)
    vueltas = data.get('vueltas', 1)
    turing_machine = TuringMachineEncryptor(desplazamiento)
    desencriptado = turing_machine.desencriptar_texto(texto, vueltas)
    return jsonify({"resultado": desencriptado})

# Solo un bloque para iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
