from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

class TuringMachineEncryptor:
    def __init__(self, desplazamiento=3):
        self.desplazamiento = desplazamiento
        self.cinta = []
        self.cabezal = 0
        self.estado = "encriptar"
    
    def cargar_texto(self, texto):
        """Carga el texto en la cinta como una lista de caracteres"""
        self.cinta = list(texto)
        self.cabezal = 0
    
    def avanzar(self):
        """Avanza el cabezal al siguiente carácter"""
        self.cabezal += 1

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
    
    def procesar(self, modo="encriptar"):
        """Procesa la cinta para encriptar o desencriptar"""
        self.estado = modo
        resultado = []
        
        while self.cabezal < len(self.cinta):
            caracter_actual = self.cinta[self.cabezal]
            
            if self.estado == "encriptar":
                nuevo_caracter = self.encriptar_caracter(caracter_actual)
            elif self.estado == "desencriptar":
                nuevo_caracter = self.desencriptar_caracter(caracter_actual)
            
            resultado.append(nuevo_caracter)
            self.avanzar()
        
        return ''.join(resultado)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encriptar', methods=['POST'])
def encriptar_endpoint():
    data = request.json
    texto = data.get('texto', '')
    desplazamiento = data.get('desplazamiento', 3)
    turing_machine = TuringMachineEncryptor(desplazamiento)
    turing_machine.cargar_texto(texto)
    encriptado = turing_machine.procesar(modo="encriptar")
    return jsonify({"resultado": encriptado})

@app.route('/desencriptar', methods=['POST'])
def desencriptar_endpoint():
    data = request.json
    texto = data.get('texto', '')
    desplazamiento = data.get('desplazamiento', 3)
    turing_machine = TuringMachineEncryptor(desplazamiento)
    turing_machine.cargar_texto(texto)
    desencriptado = turing_machine.procesar(modo="desencriptar")
    return jsonify({"resultado": desencriptado})

if __name__ == '__main__':
    app.run(debug=True)
