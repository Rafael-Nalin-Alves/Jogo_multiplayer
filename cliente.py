import socket
import pickle
import time

# Classe que gerencia a comunicação de rede do cliente
class ClienteRede:
    def __init__(self):
        # Cria um socket UDP
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Solicita o endereço IP do servidor ao usuário
        self.server = input("Digite o endereço IP do servidor (ex: 127.0.0.1): ").strip()
        self.port = 5555  # Porta padrão do servidor
        self.addr = (self.server, self.port)  # Tupla com endereço do servidor
        self.player_id = None  # ID do jogador (definido pelo servidor)
        self.ultimo_envio = 0  # Timestamp do último envio
        self.ultima_resposta = 0  # Timestamp da última resposta
        self.latencia = 0  # Latência da comunicação (em ms)
        
        # Define um timeout de 0.5 segundos para recebimento de dados
        self.cliente.settimeout(0.5)
        
        # Inicia a conexão com o servidor
        self.connect()

    # Método para conectar ao servidor
    def connect(self):
        try:
            # Envia uma mensagem inicial para se registrar no servidor
            self.cliente.sendto(pickle.dumps({"conectar": True}), self.addr)
            
            # Aguarda a resposta do servidor com o ID do jogador
            data, addr = self.cliente.recvfrom(2048)
            initial_data = pickle.loads(data)
            self.player_id = initial_data["player_id"]
            print(f"Conectado como jogador {self.player_id + 1}")
            return self.player_id
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return None

    # Método para enviar dados ao servidor e receber resposta
    def enviar(self, data):
        try:
            tempo_inicio = time.time()
            
            # Adiciona um timestamp aos dados enviados
            data["timestamp"] = tempo_inicio
            
            # Serializa e envia os dados
            dados_compactados = pickle.dumps(data)
            self.cliente.sendto(dados_compactados, self.addr)
            
            # Tenta receber a resposta do servidor
            try:
                resposta, addr = self.cliente.recvfrom(2048)
                if not resposta:
                    return None
                    
                # Desserializa a resposta
                dados_resposta = pickle.loads(resposta)
                # Calcula a latência (em milissegundos)
                self.latencia = int((time.time() - tempo_inicio) * 1000)
                self.ultima_resposta = time.time()
                return dados_resposta
            except socket.timeout:
                return None  # Retorna None se o recebimento expirar
                
        except socket.error as e:
            print(f"Erro de rede: {e}")
            return None
        except pickle.PickleError as e:
            print(f"Erro de serialização: {e}")
            return None

    # Método para fechar o socket do cliente
    def fechar(self):
        try:
            self.cliente.close()
        except:
            pass  # Ignora erros ao fechar