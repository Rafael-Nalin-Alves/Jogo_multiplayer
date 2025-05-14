import pyxel
from cliente import ClienteRede
from constantes import Consts, TILES_SOLIDOS, TILES_MORTAIS, TILES_PORTAO, tiles_em_linha

def verifica_colisao_mapa(x, y):
    pontos = [
        (x + 2, y + 15),    # Ponto inferior esquerdo
        (x + 13, y + 15),   # Ponto inferior direito
        (x + 2, y + 8),     # Ponto médio esquerdo
        (x + 13, y + 8),    # Ponto médio direito
        (x + 7, y + 1),     # Ponto superior central
    ]
    
    portao_detectado = False
    
    for px, py in pontos:
        tile_x = px // 8
        tile_y = py // 8
        
        # Verificar se a posição está dentro dos limites do tilemap
        if tile_x < 0 or tile_y < 0:
            continue
            
        try:
            tile = pyxel.tilemaps[0].pget(tile_x, tile_y)
        except:
            continue
        
        # Verificar colisão com tiles sólidos
        if (tile[0], tile[1]) in TILES_SOLIDOS:
            return True
            
        # Verificar colisão com tiles mortais
        if (tile[0], tile[1]) in TILES_MORTAIS:
            return "die"
            
        # Verificar colisão com tiles do portão
        if (tile[0], tile[1]) in TILES_PORTAO:
            portao_detectado = True
    
    return "portao" if portao_detectado else False

def verifica_colisao_pixel(hitbox1, hitbox2):
    x1, y1, w1, h1 = hitbox1
    x2, y2, w2, h2 = hitbox2
    return not (x1 >= x2 + w2 or x2 >= x1 + w1 or
                y1 >= y2 + h2 or y2 >= y1 + h1)

def debug_draw_hitbox(x, y, width, height, color):
    pyxel.rectb(x, y, width, height, color)

class Personagem:
    def __init__(self, x, y, inimigo=False, jogador2=False):
        self.x = x
        self.y = y
        self.direcao = "direita" if not inimigo else "esquerda"
        self.andando = False
        self.walk_frame = 0
        self.vida_maxima = 3
        self.vida = self.vida_maxima
        self.morte = False
        self.dano = False
        self.dano_frame = 0
        self.morte_frame = 0
        self.inimigo = inimigo
        self.jogador2 = jogador2
        self.vel_y = 0
        self.no_chao = False
        self.imune = False
        self.tempo_imunidade = 30
        self.animacao_morte_completa = False
        self.acao = "idle"

    def update(self):
        if self.imune:
            self.tempo_imunidade -= 1
            if self.tempo_imunidade <= 0:
                self.imune = False
                self.tempo_imunidade = 30
        
        if self.dano:
            self.dano_frame += 1
        if self.dano_frame >= len(Consts.DANO_FRAMES) * 5:
            self.dano = False
            self.dano_frame = 0
        
        if self.morte:
            self.morte_frame += 0.5
            if self.morte_frame >= len(Consts.MORTE_FRAMES) - 1:
                self.morte_frame = len(Consts.MORTE_FRAMES) - 1
                self.animacao_morte_completa = True

    def desenhar(self, cam_x=0, cam_y=0):
        x = self.x - cam_x
        y = self.y - cam_y
        
        if self.morte:
            frame = int(self.morte_frame)
            if self.jogador2:
                frames = Consts.MORTE_FRAMES_P2
            else:
                frames = Consts.MORTE_FRAMES
                
            if frame < len(frames):
                if self.direcao == "direita":
                    pyxel.blt(x, y, 0, *frames[frame], 16, 16, 11)
                else:
                    pyxel.blt(x, y, 0, frames[frame][0], frames[frame][1], -16, 16, 11)
                    
        elif self.dano:
            frame = (self.dano_frame // 5) % len(Consts.DANO_FRAMES)
            if self.jogador2:
                frames = Consts.DANO_FRAMES_P2
            else:
                frames = Consts.DANO_FRAMES
                
            if frame < len(frames):
                if self.direcao == "direita":
                    pyxel.blt(x, y, 0, *frames[frame], 16, 16, 11)
                else:
                    pyxel.blt(x, y, 0, frames[frame][0], frames[frame][1], -16, 16, 11)
                    
        elif self.andando:
            if self.jogador2:
                frames = Consts.ANDANDO_P2
                sprite_x = (self.walk_frame % len(frames)) * 16
                if self.direcao == "direita":
                    pyxel.blt(x, y, 0, sprite_x, 144, 16, 16, 11)
                else:
                    pyxel.blt(x, y, 0, sprite_x, 144, -16, 16, 11)
            else:
                frames = Consts.ANDANDO
                sprite_x = (self.walk_frame % len(frames)) * 16
                if self.direcao == "direita":
                    pyxel.blt(x, y, 0, sprite_x, 16, 16, 16, 11)
                else:
                    pyxel.blt(x, y, 0, sprite_x, 16, -16, 16, 11)
        else:
            if self.jogador2:
                frame = (pyxel.frame_count // 20) % len(Consts.PARADO_P2)
                u, v = Consts.PARADO_P2[frame]
                if self.direcao == "direita":
                    pyxel.blt(x, y, 0, u, v, 16, 16, 11)
                else:
                    pyxel.blt(x, y, 0, u, v, -16, 16, 11)
            else:
                if self.direcao == "direita":
                    pyxel.blt(x, y, 0, 0, 0, 16, 16, 11)
                else:
                    pyxel.blt(x, y, 0, 0, 0, -16, 16, 11)
         
        if not self.inimigo:
            self.desenhar_coracoes_de_vida()

    def tomar_dano(self):
        if not self.imune and not self.morte and not self.dano:
            self.vida -= 1
            self.dano = True
            self.dano_frame = 0
            self.imune = True
            print(f"Personagem levou dano. Vida restante: {self.vida}")
            
            if self.vida <= 0:
                self.morte = True
                self.morte_frame = 0

    def get_hitbox(self):
        hitbox_width = 10
        hitbox_height = 14
        hitbox_x_offset = 3
        hitbox_y_offset = 1
        
        hitbox_x = self.x + hitbox_x_offset
        hitbox_y = self.y + hitbox_y_offset

        return (hitbox_x, hitbox_y, hitbox_width, hitbox_height)

    def desenhar_coracoes_de_vida(self):
        if self.inimigo:
            return
            
        x_base = 5 if not self.jogador2 else 220
        y_base = 5

        for i in range(self.vida_maxima):
            x = x_base + i * (12 if not self.jogador2 else -12)
            color = pyxel.COLOR_RED if i < self.vida else pyxel.COLOR_DARK_BLUE
            
            pyxel.rect(x - 1, y_base - 1, 10, 10, pyxel.COLOR_YELLOW)
            pyxel.rect(x, y_base, 8, 8, pyxel.COLOR_WHITE)
            
            pyxel.pset(x + 2, y_base + 1, color)
            pyxel.pset(x + 5, y_base + 1, color)
            pyxel.pset(x + 1, y_base + 2, color)
            pyxel.pset(x + 3, y_base + 2, color)
            pyxel.pset(x + 4, y_base + 2, color)
            pyxel.pset(x + 6, y_base + 2, color)
            pyxel.pset(x + 2, y_base + 3, color)
            pyxel.pset(x + 5, y_base + 3, color)
            pyxel.pset(x + 3, y_base + 4, color)
            pyxel.pset(x + 4, y_base + 4, color)
            pyxel.pset(x + 3, y_base + 5, color)

class Jogador(Personagem):
    def __init__(self, x, y, jogador2=False):
        super().__init__(x, y, jogador2=jogador2)
        self.ataque1 = False
        self.ataque2 = False
        self.velocidade_ataque = 0
        self.ataque_x = 0
        self.ataque_y = 0
        self.proximo_ataque = 1
        self.acao = "idle"

    def iniciar_ataque(self):
        if self.morte or self.dano:
            return
            
        if not self.ataque1 and not self.ataque2:
            if self.proximo_ataque == 1:
                self.ataque1 = True
                self.proximo_ataque = 2
                self.ataque_x = self.x
                self.ataque_y = self.y - 16
            else:
                self.ataque2 = True
                self.proximo_ataque = 1
                self.ataque_x = self.x
                self.ataque_y = self.y
            self.velocidade_ataque = 0
            self.acao = "ataque"

    def desenhar_ataque(self, cam_x=0, cam_y=0):
        if self.ataque1:
            self.desenhar_ataque1(cam_x, cam_y)
        elif self.ataque2:
            self.desenhar_ataque2(cam_x, cam_y)

    def desenhar_ataque1(self, cam_x=0, cam_y=0):
        f = self.velocidade_ataque
        x = self.ataque_x - cam_x
        y = self.ataque_y - cam_y
        
        if self.jogador2:
            frames = [
                Consts.ATAQUE_FRAME1_P2,
                Consts.ATAQUE_FRAME2_P2,
                Consts.ATAQUE_FRAME3_P2,
                Consts.ATAQUE_FRAME4_P2,
                Consts.ATAQUE_FRAME5_P2
            ]
            # Dimensões específicas para cada frame do jogador 2
            dimensoes = [
                (32, 32),  # Frame 1
                (32, 32),  # Frame 2
                (35, 32),  # Frame 3
                (35, 32),  # Frame 4
                (35, 32)   # Frame 5
            ]
        else:
            frames = [
                Consts.ATAQUE_FRAME1,
                Consts.ATAQUE_FRAME2,
                Consts.ATAQUE_FRAME3,
                Consts.ATAQUE_FRAME4,
                Consts.ATAQUE_FRAME5
            ]
            # Dimensões específicas para cada frame do jogador 1
            dimensoes = [
                (32, 32),  # Frame 1
                (32, 32),  # Frame 2
                (35, 32),  # Frame 3
                (35, 32),  # Frame 4
                (35, 32)   # Frame 5
            ]
        
        frame_idx = min(f // 3, 4)
        if frame_idx < len(frames):
            width, height = dimensoes[frame_idx]
            y_offset = 0
            
            # Ajuste especial para os frames maiores (3, 4 e 5)
            if frame_idx >= 2:  # Frames 3, 4 e 5
                y_offset = 8  # Ajuste para compensar a altura diferente
                
            if self.direcao == "direita":
                pyxel.blt(x, y + y_offset, 0, *frames[frame_idx], width, height, 11)
            else:
                # Para sprites virados para esquerda, ajustamos a posição x também
                x_offset = width - 16  # Compensar a largura diferente
                pyxel.blt(x - x_offset, y + y_offset, 0, 
                        frames[frame_idx][0], frames[frame_idx][1], -width, height, 11)

    def desenhar_ataque2(self, cam_x=0, cam_y=0):
        f = self.velocidade_ataque
        x = self.x - cam_x
        y = self.y - cam_y
        
        if self.jogador2:
            frames = [
                Consts.ATAQUE2_FRAME1_P2,
                Consts.ATAQUE2_FRAME2_P2,
                Consts.ATAQUE2_FRAME3_P2,
                Consts.ATAQUE2_FRAME4_P2,
                Consts.ATAQUE2_FRAME5_P2
            ]
        else:
            frames = [
                Consts.ATAQUE2_FRAME1,
                Consts.ATAQUE2_FRAME2,
                Consts.ATAQUE2_FRAME3,
                Consts.ATAQUE2_FRAME4,
                Consts.ATAQUE2_FRAME5
            ]
        
        frame_idx = min(f // 3, 4)
        if frame_idx < len(frames):
            if self.direcao == "direita":
                y_offset = -17 if f < 3 else (-15 if 6 <= f < 9 else -16)
                pyxel.blt(x, y + y_offset, 0, *frames[frame_idx], 32, 32, 11)
            else:
                offset = 16
                y_offset = -17 if f < 3 else (-15 if 6 <= f < 9 else -16)
                pyxel.blt(x - offset, y + y_offset, 0, 
                         frames[frame_idx][0], frames[frame_idx][1], -32, 32, 11)

    def get_ataque_hitbox(self):
        frame_index = min(self.velocidade_ataque // 3, 4)
        
        if self.ataque1:
            hitbox_list = Consts.ATAQUE1_HITBOXES_P2 if self.jogador2 else Consts.ATAQUE1_HITBOXES
        elif self.ataque2:
            hitbox_list = Consts.ATAQUE2_HITBOXES_P2 if self.jogador2 else Consts.ATAQUE2_HITBOXES
        else:
            return None

        if frame_index >= len(hitbox_list):
            return None
            
        x_offset, y_offset, width, height = hitbox_list[frame_index]

        # Aplicar o mesmo ajuste de posição Y usado no desenho
        y_adjust = 0
        if self.ataque1 and frame_index in [3, 4]:  # Frames 4 e 5 do ataque 1
            y_adjust = 8

        if self.direcao == "direita":
            hitbox_x = self.ataque_x + x_offset
            hitbox_y = self.ataque_y + y_offset + y_adjust
        else:
            hitbox_x = self.ataque_x - x_offset - width
            hitbox_y = self.ataque_y + y_offset + y_adjust

        return (hitbox_x, hitbox_y, width, height)
    
    def get_ataque_data(self):
        return {
            "ataque1": self.ataque1,
            "ataque2": self.ataque2,
            "velocidade_ataque": self.velocidade_ataque,
            "ataque_x": self.ataque_x,
            "ataque_y": self.ataque_y,
            "direcao": self.direcao,
            "hitbox": self.get_ataque_hitbox()
        }

    def atualizar_ataque(self, inimigos):
        if self.morte:
            return
            
        if self.ataque1 or self.ataque2:
            self.velocidade_ataque += 1
            if self.velocidade_ataque == 1:
                ataque_hitbox = self.get_ataque_hitbox()
                if ataque_hitbox:
                    for inimigo in inimigos:
                        if not inimigo.morte and verifica_colisao_pixel(ataque_hitbox, inimigo.get_hitbox()):
                            inimigo.tomar_dano()
            if self.velocidade_ataque >= 15:
                self.ataque1 = False
                self.ataque2 = False
                self.walk_frame = 0
                self.acao = "idle"

class Inimigo(Personagem):
    def __init__(self, x, y):
        super().__init__(x, y, inimigo=True)
        self.ataque1 = False
        self.velocidade_ataque = 0
        self.ataque_frames_total = 15
        self.cooldown_ataque = 90
        self.ultimo_ataque = 0
        self.vel_atq = 0.8
        self.vel_normal = 0.5
        self.andando = False
        self.walk_frame = 0
        self.vida = 2
        self.morte_frame = 0
        self.dano_frame = 0

    def update_fisica(self):
        if self.morte:
            return
            
        self.vel_y += 0.5
        nova_y = self.y + self.vel_y
        
        colisao = verifica_colisao_mapa(self.x, nova_y)
        
        if colisao == "die":
            self.vida = 0
            self.tomar_dano()
        elif not colisao:
            self.y = nova_y
            self.no_chao = False
        else:
            self.no_chao = self.vel_y > 0
            self.vel_y = 0

    def update_ia(self, jogador):
        if self.morte or self.ataque1 or jogador.morte:
            return

        distancia = abs(jogador.x - self.x)
        pode_atacar = (pyxel.frame_count - self.ultimo_ataque) > self.cooldown_ataque
        
        velocidade = self.vel_atq if (distancia < 40 and pode_atacar) else self.vel_normal
        
        # Move apenas se estiver fora do alcance de ataque
        if distancia > 40 and distancia < 80:
            if jogador.x > self.x:
                self.x += velocidade
                self.direcao = "direita"
            else:
                self.x -= velocidade
                self.direcao = "esquerda"
            self.andando = True
            
            if pyxel.frame_count % 6 == 0:
                self.walk_frame = (self.walk_frame + 1) % len(Consts.INIMIGO_ANDANDO)
        else:
            self.andando = False

        if distancia < 40 and pode_atacar and not self.ataque1:
            self.ataque1 = True
            self.velocidade_ataque = 0
            self.ultimo_ataque = pyxel.frame_count

    def tomar_dano(self):
        if not self.morte:
            self.vida -= 1
            self.dano = True
            self.dano_frame = 0
            print(f"Inimigo levou dano. Vida restante: {self.vida}")
            
            if self.vida <= 0:
                self.morte = True
                self.morte_frame = 0

    def desenhar(self, cam_x=0, cam_y=0):
        x = int(self.x - cam_x)
        y = int(self.y - cam_y)

        if self.morte:
            frame = int(self.morte_frame)
            if self.direcao == "direita":
                pyxel.blt(x, y, 1, *Consts.INIMIGO_MORTE_FRAMES[frame], 32, 16, 11)
            else:
                pyxel.blt(x, y, 1, Consts.INIMIGO_MORTE_FRAMES[frame][0], Consts.INIMIGO_MORTE_FRAMES[frame][1], -32, 16, 11)
            return

        elif self.ataque1:
            self.desenhar_ataque1(cam_x, cam_y)
            return

        elif self.dano:
            frame = self.dano_frame % len(Consts.INIMIGO_DANO_FRAMES)
            u, v = Consts.INIMIGO_DANO_FRAMES[frame]
            largura = 24
            
            if self.direcao == "direita":
                pyxel.blt(x, y, 1, u, v, largura, 16, 11)
            else:
                pyxel.blt(x, y, 1, u + largura, v, -largura, 16, 11)
                
            self.dano_frame += 1
            if self.dano_frame > 10:
                self.dano = False
            return

        elif self.andando:
            frame = self.walk_frame % len(Consts.INIMIGO_ANDANDO)
            u, v = Consts.INIMIGO_ANDANDO[frame]
            largura = 24
            
            if self.direcao == "direita":
                pyxel.blt(x, y, 1, u, v, largura, 16, 11)
            else:
                pyxel.blt(x, y, 1, u + largura, v, -largura, 16, 11)
                
        else:
            frame = (pyxel.frame_count // 10) % len(Consts.Inimigo_Idle)
            u, v = Consts.Inimigo_Idle[frame]
            largura = 24  # Ajustado para corresponder ao estado de andar
            
            if self.direcao == "direita":
                pyxel.blt(x, y, 1, u, v, largura, 16, 11)
            else:
                x_ajustado = x - (largura - 16)  # Ajuste para evitar corte
                pyxel.blt(x_ajustado, y, 1, u, v, -largura, 16, 11)

    def get_ataque_hitbox(self):
        frame_idx = min(self.velocidade_ataque // 3, len(Consts.INIMIGO_ATAQUE1) - 1)
        
        hitboxes = [
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (5, -5, 20, 20),
            (10, -10, 25, 25),
            (0, 0, 0, 0),
            (0, 0, 0, 0)
        ]
        
        x_offset, y_offset, width, height = hitboxes[frame_idx]
        
        if self.direcao == "direita":
            hitbox_x = self.x + x_offset
        else:
            hitbox_x = self.x - x_offset - width
            
        hitbox_y = self.y + y_offset
        
        return (hitbox_x, hitbox_y, width, height)

    def desenhar_ataque1(self, cam_x=0, cam_y=0):
        f = self.velocidade_ataque
        x = int(self.x - cam_x)
        y = int(self.y - cam_y)
        
        frame_dims = [
            (24, 16),
            (19, 19),
            (24, 24),
            (33, 32),
            (32, 22),
            (28, 21)
        ]
        
        frame_idx = min(f // 3, len(Consts.INIMIGO_ATAQUE1) - 1)
        width, height = frame_dims[frame_idx]
        u, v = Consts.INIMIGO_ATAQUE1[frame_idx]

        if frame_idx in [2, 3] and f % 3 == 0:
            ataque_hitbox = self.get_ataque_hitbox()
            if ataque_hitbox:
                jogador_hitbox = self.jogador.get_hitbox()
                if verifica_colisao_pixel(ataque_hitbox, jogador_hitbox):
                    self.jogador.tomar_dano()
        
        x_ajustado = x - (width - 24) // 2
        y_ajustado = y - (height - 16)
        
        if self.direcao == "direita":
            pyxel.blt(x_ajustado, y_ajustado, 1, u, v, width, height, 11)
        else:
            pyxel.blt(x_ajustado, y_ajustado, 1, u, v, -width, height, 11)

        self.velocidade_ataque += 1
        if self.velocidade_ataque >= self.ataque_frames_total:
            self.ataque1 = False
            self.velocidade_ataque = 0
                
class ChevalierGame:
    def __init__(self):
        pyxel.init(256, 192, title="CHEVALIER")
        pyxel.load("tileset.pyxres")
        pyxel.tilemaps[0].imgsrc = 2

        self.mapa_largura = 864 * 2  # 54 tiles (54 * 16 = 864)
        self.mapa_altura = 320 * 2   # 20 tiles (20 * 16 = 320)
        self.cam_x = 0
        self.cam_y = 0

        self.tela_inicial = True
        self.game_over = False
        self.vitoria = False
        self.dados_outro_jogador = None

        try:
            self.cliente = ClienteRede()
            self.player_id = self.cliente.player_id
            
            if self.player_id == 0:
                self.jogador = Jogador(72, 64)
                self.inimigo = Personagem(200, 64, inimigo=True, jogador2=True)
            else:
                self.jogador = Jogador(1632, 480, jogador2=True)
                self.inimigo = Personagem(72, 64, inimigo=True)

        except Exception as e:
            print(f"Falha crítica na conexão: {str(e)}")
            print("Este jogo requer conexão com o servidor. Encerrando...")
            pyxel.quit()
            exit()

        self.debug_mode = False
        self.inimigos = [
            Inimigo(200, 280), Inimigo(39*8, 62*8), 
            Inimigo(48*8, 42*8), Inimigo(65*8, 61*8),
            Inimigo(175*8, 62*8), Inimigo(145*8, 50*8),
            Inimigo(152*8, 35*8), Inimigo(193*8, 37*8)
        ]
        for inimigo in self.inimigos:
            inimigo.jogador = self.jogador

        # Definir canais de som
        self.CH_ATTACK = 0
        self.CH_JUMP = 1
        self.CH_GAMEOVER = 2
        self.CH_WIN = 3

        # Configurar sons
        self.setup_sounds()

        pyxel.run(self.update, self.draw)

    def setup_sounds(self):
        """Configura todos os sons do jogo"""
        # Ataque (som de golpe com descida rápida para simular swoosh)
        pyxel.sounds[0].set(
            notes="G4E4C4",
            tones="nnn",
            volumes="754",
            effects="fff",
            speed=30
        )
        
        # Game Over
        pyxel.sounds[2].set(
            notes="C3B2A2G2F2E2D2C2",
            tones="tttttttt",
            volumes="76543210",
            effects="ffffffff",
            speed=12
        )
        
        # Vitória
        pyxel.sounds[3].set(
            notes="E3G3C4E4G3C4E4G4",
            tones="ssssssss",
            volumes="77777777",
            effects="ffffffff",
            speed=22
        )

    def play_attack(self):
        pyxel.play(self.CH_ATTACK, 0)

    def play_jump(self):
        pyxel.play(self.CH_JUMP, 1)

    def play_gameover(self):
        pyxel.play(self.CH_GAMEOVER, 2)

    def play_win(self):
        pyxel.play(self.CH_WIN, 3)

    def reviver_jogador(self):
        self.jogador.vida = self.jogador.vida_maxima
        self.jogador.morte = False
        self.jogador.dano = False
        self.jogador.imune = False
        self.jogador.morte_frame = 0
        self.jogador.dano_frame = 0
        self.jogador.animacao_morte_completa = False
        
        if hasattr(self, 'player_id') and self.player_id == 1:
            self.jogador.x = 1632
            self.jogador.y = 480
        else:
            self.jogador.x = 72
            self.jogador.y = 64

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Verifica se o jogador morreu e ativa a tela de game over
        if self.jogador.morte and self.jogador.animacao_morte_completa and not self.game_over:
            self.game_over = True
            self.play_gameover()

        # Verifica condição de vitória
        if not self.vitoria and not self.game_over:
            colisao_jogador = verifica_colisao_mapa(self.jogador.x, self.jogador.y)
            colisao_inimigo = verifica_colisao_mapa(self.inimigo.x, self.inimigo.y)
            if colisao_jogador == "portao" and colisao_inimigo == "portao":
                self.vitoria = True
                self.play_win()

        # Se estiver em game over ou vitória, permite reiniciar com R
        if (self.game_over) and pyxel.btnp(pyxel.KEY_R):
            self.reviver_jogador()
            self.game_over = False

        if self.game_over or self.vitoria:
            return  # Não atualiza o jogo enquanto estiver em game over ou vitória

        if self.tela_inicial:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.tela_inicial = False
            return

        self.jogador.update()
        
        if not self.jogador.morte:
            # Verifica colisão com tiles mortais
            colisao = verifica_colisao_mapa(self.jogador.x, self.jogador.y)
            if colisao == "die":
                self.jogador.vida = 0
                self.jogador.tomar_dano()
            
            self.jogador.andando = False

            if not self.jogador.ataque1 and not self.jogador.ataque2:
                if pyxel.btn(pyxel.KEY_D):
                    nova_x = self.jogador.x + 2
                    colisao = verifica_colisao_mapa(nova_x, self.jogador.y)
                    if colisao != True:  # Permite movimento mesmo em tiles mortais
                        self.jogador.x = nova_x
                    self.jogador.direcao = "direita"
                    self.jogador.andando = True
                elif pyxel.btn(pyxel.KEY_A):
                    nova_x = self.jogador.x - 2
                    colisao = verifica_colisao_mapa(nova_x, self.jogador.y)
                    if colisao != True:
                        self.jogador.x = nova_x
                    self.jogador.direcao = "esquerda"
                    self.jogador.andando = True

                if pyxel.btnp(pyxel.KEY_W) and self.jogador.no_chao:
                    self.jogador.vel_y = -6
                    self.jogador.no_chao = False
                    self.play_jump()

            self.jogador.vel_y += 0.5
            nova_y = self.jogador.y + self.jogador.vel_y
            
            colisao = verifica_colisao_mapa(self.jogador.x, nova_y)
            if colisao == "die":
                self.jogador.vida = 0
                self.jogador.tomar_dano()
            elif not colisao:
                self.jogador.y = nova_y
                self.jogador.no_chao = False
            else:
                if self.jogador.vel_y > 0:
                    self.jogador.no_chao = True
                self.jogador.vel_y = 0

            if pyxel.btnp(pyxel.KEY_SPACE):
                self.jogador.iniciar_ataque()
                self.play_attack()

            self.jogador.atualizar_ataque(self.inimigos)

        if self.jogador.andando:
            self.jogador.walk_frame = (self.jogador.walk_frame + 1) % len(Consts.ANDANDO)

        for inimigo in self.inimigos:
            inimigo.update()
            inimigo.update_fisica()
            if not self.jogador.morte:
                inimigo.update_ia(self.jogador)
            if inimigo.ataque1:
                inimigo.velocidade_ataque += 1
            if inimigo.dano:
                inimigo.dano_frame += 1
                if inimigo.dano_frame > 10:
                    inimigo.dano = False

        self.inimigo.update()
        if self.inimigo.dano:
            self.inimigo.dano_frame += 1
            if self.inimigo.dano_frame > 5:
                self.inimigo.dano = False
        if self.inimigo.morte:
            self.inimigo.morte_frame = min(self.inimigo.morte_frame + 1, len(Consts.MORTE_FRAMES) - 1)

        self.update_camera()

        if hasattr(self, 'cliente') and self.cliente:
            try:
                dados = {
                    "x": self.jogador.x,
                    "y": self.jogador.y,
                    "direcao": self.jogador.direcao,
                    "acao": self.jogador.acao,
                    "vida": self.jogador.vida,
                    "morte": self.jogador.morte,
                    "dano": self.jogador.dano,
                    "hitbox": self.jogador.get_hitbox(),
                    "ataque": self.jogador.get_ataque_data()
                }
                
                self.dados_outro_jogador = self.cliente.enviar(dados)
                
                if self.dados_outro_jogador:
                    self.atualizar_inimigo_com_dados()
                    
            except Exception as e:
                print(f"Erro de rede: {e}")
                self.dados_outro_jogador = None

    def atualizar_inimigo_com_dados(self):
        if self.dados_outro_jogador is None:
            return
            
        self.inimigo.x = self.dados_outro_jogador.get("x", self.inimigo.x)
        self.inimigo.y = self.dados_outro_jogador.get("y", self.inimigo.y)
        self.inimigo.direcao = self.dados_outro_jogador.get("direcao", self.inimigo.direcao)
        self.inimigo.acao = self.dados_outro_jogador.get("acao", self.inimigo.acao)
        self.inimigo.vida = self.dados_outro_jogador.get("vida", self.inimigo.vida)
        self.inimigo.morte = self.dados_outro_jogador.get("morte", self.inimigo.morte)
        self.inimigo.dano = self.dados_outro_jogador.get("dano", self.inimigo.dano)
        
        ataque_data = self.dados_outro_jogador.get("ataque", {})
        if ataque_data and (ataque_data.get("ataque1", False) or ataque_data.get("ataque2", False)):
            ataque_hitbox = self.calcular_hitbox_ataque(ataque_data)
            if ataque_hitbox and verifica_colisao_pixel(ataque_hitbox, self.jogador.get_hitbox()):
                self.jogador.tomar_dano()

    def calcular_hitbox_ataque(self, ataque_data):
        frame_index = min(ataque_data.get("velocidade_ataque", 0) // 3, 4)
        
        if ataque_data.get("ataque1", False):
            hitbox_list = Consts.ATAQUE1_HITBOXES_P2 if hasattr(self.inimigo, 'jogador2') and self.inimigo.jogador2 else Consts.ATAQUE1_HITBOXES
        elif ataque_data.get("ataque2", False):
            hitbox_list = Consts.ATAQUE2_HITBOXES_P2 if hasattr(self.inimigo, 'jogador2') and self.inimigo.jogador2 else Consts.ATAQUE2_HITBOXES
        else:
            return None

        if frame_index >= len(hitbox_list):
            return None
            
        x_offset, y_offset, width, height = hitbox_list[frame_index]

        if ataque_data.get("direcao", "direita") == "direita":
            hitbox_x = ataque_data.get("ataque_x", 0) + x_offset
            hitbox_y = ataque_data.get("ataque_y", 0) + y_offset
        else:
            hitbox_x = ataque_data.get("ataque_x", 0) - x_offset - width
            hitbox_y = ataque_data.get("ataque_y", 0) + y_offset

        return (hitbox_x, hitbox_y, width, height)

    def desenhar_ataque_outro_jogador(self, ataque_data):
        f = ataque_data.get("velocidade_ataque", 0)
        x = ataque_data.get("ataque_x", 0) - self.cam_x
        y = ataque_data.get("ataque_y", 0) - self.cam_y
        
        is_jogador2 = hasattr(self.inimigo, 'jogador2') and self.inimigo.jogador2
        
        if ataque_data.get("ataque1", False):
            if is_jogador2:
                frames = [
                    Consts.ATAQUE_FRAME1_P2,
                    Consts.ATAQUE_FRAME2_P2,
                    Consts.ATAQUE_FRAME3_P2,
                    Consts.ATAQUE_FRAME4_P2,
                    Consts.ATAQUE_FRAME5_P2
                ]
            else:
                frames = [
                    Consts.ATAQUE_FRAME1,
                    Consts.ATAQUE_FRAME2,
                    Consts.ATAQUE_FRAME3,
                    Consts.ATAQUE_FRAME4,
                    Consts.ATAQUE_FRAME5
                ]
            
            frame_idx = min(f // 3, 4)
            if frame_idx < len(frames):
                y_offset = 8 if frame_idx in [3, 4] else 0
                
                if ataque_data.get("direcao", "direita") == "direita":
                    pyxel.blt(x, y + y_offset, 0, *frames[frame_idx], 32, 32, 11)
                else:
                    offset = 16
                    pyxel.blt(x - offset, y + y_offset, 0, 
                            frames[frame_idx][0], frames[frame_idx][1], -32, 32, 11)
            
        elif ataque_data.get("ataque2", False):
            if is_jogador2:
                frames = [
                    Consts.ATAQUE2_FRAME1_P2,
                    Consts.ATAQUE2_FRAME2_P2,
                    Consts.ATAQUE2_FRAME3_P2,
                    Consts.ATAQUE2_FRAME4_P2,
                    Consts.ATAQUE2_FRAME5_P2
                ]
            else:
                frames = [
                    Consts.ATAQUE2_FRAME1,
                    Consts.ATAQUE2_FRAME2,
                    Consts.ATAQUE2_FRAME3,
                    Consts.ATAQUE2_FRAME4,
                    Consts.ATAQUE2_FRAME5
                ]
            
            frame_idx = min(f // 3, 4)
            if frame_idx < len(frames):
                y_offset = -17 if f < 3 else (-15 if 6 <= f < 9 else -16)
                if ataque_data.get("direcao", "direita") == "direita":
                    pyxel.blt(x, y + y_offset, 0, *frames[frame_idx], 32, 32, 11)
                else:
                    offset = 16
                    pyxel.blt(x - offset, y + y_offset, 0, 
                             frames[frame_idx][0], frames[frame_idx][1], -32, 32, 11)

    def draw(self):
        pyxel.cls(0)

        if self.tela_inicial:
            pyxel.rectb(0, 0, 256, 192, pyxel.COLOR_YELLOW)
            
            title = "CHEVALIER"
            title_width = len(title) * 5
            x_center = 5 + ((256 - 10 - title_width) // 2)  
            y_center = 70  
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    pyxel.text(x_center + dx, y_center + dy, title, pyxel.COLOR_BLACK)
            pyxel.text(x_center, y_center, title, pyxel.COLOR_RED)
            
            start_message = "Aperte ENTER para comecar"
            start_width = len(start_message) * 5
            x_start = 5 + ((256 - 10 - start_width) // 2) 
            pyxel.text(x_start, y_center + 10, start_message, pyxel.COLOR_WHITE)
            
            pyxel.text(5, 120, "Controles:", pyxel.COLOR_WHITE)
            pyxel.text(5, 130, "A / D: Mover", pyxel.COLOR_WHITE)
            pyxel.text(5, 140, "W: Pular", pyxel.COLOR_WHITE)
            pyxel.text(5, 150, "SPACE: Atacar", pyxel.COLOR_WHITE)
            pyxel.text(5, 160, "R: Reviver/Reiniciar", pyxel.COLOR_WHITE)
            pyxel.text(5, 170, "Q: Sair", pyxel.COLOR_WHITE)
            
            return

        if self.game_over:
            # Fundo opaco
            pyxel.rect(0, 0, 256, 192, pyxel.COLOR_BLACK)
            pyxel.rectb(0, 0, 256, 192, 8)
            
            # Texto de game over
            pyxel.text(85, 70, "GAME OVER", pyxel.COLOR_RED)
            pyxel.text(60, 90, "Pressione R para reviver", pyxel.COLOR_WHITE)
            
            # Desenha o personagem morto no centro
            frame = len(Consts.MORTE_FRAMES) - 1
            if hasattr(self.jogador, 'jogador2') and self.jogador.jogador2:
                frames = Consts.MORTE_FRAMES_P2
            else:
                frames = Consts.MORTE_FRAMES
            
            if frame < len(frames):
                pyxel.blt(120, 100, 0, *frames[frame], 16, 16, 11)
            return

        if self.vitoria:
            # Fundo opaco
            pyxel.rect(0, 0, 256, 192, pyxel.COLOR_BLACK)
            pyxel.rectb(0, 0, 256, 192, 8)
            
            # Texto de vitória
            pyxel.text(85, 70, "VITORIA!", pyxel.COLOR_YELLOW)
            pyxel.text(60, 90, "Pressione q para sair", pyxel.COLOR_WHITE)
            
            # Desenha ambos os personagens
            frame = 0  # Frame parado
            if hasattr(self.jogador, 'jogador2') and self.jogador.jogador2:
                pyxel.blt(100, 100, 0, 16, 0, 16, 16, 11)
            else:
                pyxel.blt(100, 100, 0, 0, 0, 16, 16, 11)
                
            if hasattr(self.inimigo, 'jogador2') and self.inimigo.jogador2:
                pyxel.blt(140, 100, 0, 16, 0, 16, 16, 11)
            else:
                pyxel.blt(140, 100, 0, 0, 0, 16, 16, 11)
            return

        # Desenha o jogo
        pyxel.bltm(-self.cam_x, -self.cam_y, 0, 0, 0, self.mapa_largura, self.mapa_altura)

        if self.jogador.ataque1 or self.jogador.ataque2:
            self.jogador.desenhar_ataque(self.cam_x, self.cam_y)
        else:
            self.jogador.desenhar(self.cam_x, self.cam_y)

        if hasattr(self, 'cliente') and self.cliente and self.dados_outro_jogador is not None:
            if self.dados_outro_jogador.get("ataque", {}).get("ataque1", False) or \
               self.dados_outro_jogador.get("ataque", {}).get("ataque2", False):
                self.desenhar_ataque_outro_jogador(self.dados_outro_jogador["ataque"])
            else:
                self.inimigo.desenhar(self.cam_x, self.cam_y)
            
            for i in range(3):
                x = 220 if self.player_id == 0 else 5
                if i < self.inimigo.vida:
                    pyxel.rect(x + i * 12, 5, 8, 8, pyxel.COLOR_RED)

        for inimigo in self.inimigos:
            inimigo.desenhar(self.cam_x, self.cam_y)

    def update_camera(self):
        self.cam_x = max(0, min(self.jogador.x - 128, self.mapa_largura - 256))
        self.cam_y = max(0, min(self.jogador.y - 96, self.mapa_altura - 192))

ChevalierGame()