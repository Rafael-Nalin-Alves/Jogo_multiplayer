import pyxel

class SpriteViewer:
    def __init__(self):
        pyxel.init(256, 256, title="Visualizador de Sprites IDLE Inimigo")
        pyxel.load("tileset.pyxres")
        
        # Configuração específica para o IDLE
        self.frames = [
            (0, 0, 32, 16),    # Frame 0
            (32, 0, 32, 16),   # Frame 1
            (64, 0, 32, 16),   # Frame 2
            (96, 0, 32, 16),   # Frame 3
            (128, 0, 32, 16),  # Frame 4
            (160, 0, 32, 16)   # Frame 5 (problema aqui)
        ]
        self.real_width = 22  # Largura real do sprite
        
        self.current_frame = 0
        self.flipped = True  # Começa mostrando flipado
        self.x_offset = 0
        
        pyxel.run(self.update, self.draw)

    def update(self):
        # Navegação entre frames
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        elif pyxel.btnp(pyxel.KEY_LEFT):
            self.current_frame = (self.current_frame - 1) % len(self.frames)
            
        # Controles adicionais
        if pyxel.btnp(pyxel.KEY_F):
            self.flipped = not self.flipped
        if pyxel.btnp(pyxel.KEY_A):
            self.x_offset -= 1
        if pyxel.btnp(pyxel.KEY_D):
            self.x_offset += 1
        if pyxel.btnp(pyxel.KEY_S):
            self.x_offset = 0

    def draw(self):
        pyxel.cls(0)
        
        u, v, w, h = self.frames[self.current_frame]
        
        # Informações na tela
        pyxel.text(5, 5, f"Frame: {self.current_frame} (← →)", 7)
        pyxel.text(5, 15, f"Tamanho: {w}x{h} (Real: {self.real_width})", 7)
        pyxel.text(5, 25, f"Flip: {'SIM' if self.flipped else 'NÃO'} (F)", 7)
        pyxel.text(5, 35, f"Offset X: {self.x_offset} (A/D, S=reset)", 7)
        
        # Posição de referência
        ref_x = 128 + self.x_offset
        ref_y = 128
        
        # Desenha o sprite
        if self.flipped:
            # Cálculo especial para o último frame flipado
            if self.current_frame == 5:  # Último frame
                adjusted_width = self.real_width
                draw_x = ref_x - (adjusted_width - 8)  # Ajuste fino para o último frame
                pyxel.blt(draw_x, ref_y, 1, u + w, v, -w, h, 11)
                
                # Debug - mostra área de desenho
                pyxel.rectb(draw_x-1, ref_y-1, w+2, h+2, 8)
                pyxel.text(draw_x, ref_y + h + 5, f"X:{draw_x}", 9)
            else:
                draw_x = ref_x - (self.real_width - 8)  # Ajuste padrão
                pyxel.blt(draw_x, ref_y, 1, u + w, v, -w, h, 11)
        else:
            pyxel.blt(ref_x, ref_y, 1, u, v, w, h, 11)
        
        # Ponto de ancoragem
        pyxel.rect(ref_x, ref_y, 1, 1, 8)
        
        # Desenha todos os frames em miniatura
        for i, (fu, fv, fw, fh) in enumerate(self.frames):
            x = 10 + i * (fw//2 + 5)
            y = 180
            if i == self.current_frame:
                pyxel.rectb(x-1, y-1, fw//2+2, fh//2+2, 10)
            pyxel.blt(x, y, 1, fu, fv, fw//2, fh//2, 11)
            pyxel.text(x, y + fh//2 + 5, str(i), 7)

# Inicia o visualizador
SpriteViewer()