class Consts:
    # Jogador 1
    ANDANDO = [0, 1, 2, 3, 4, 5, 6, 7]
    ATAQUE_FRAME1 = (16, 48)
    ATAQUE_FRAME2 = (48, 48)
    ATAQUE_FRAME3 = (80, 64)
    ATAQUE_FRAME4 = (128, 64)
    ATAQUE_FRAME5 = (168, 64)

    ATAQUE2_FRAME1 = (16, 96)
    ATAQUE2_FRAME2 = (48, 96)
    ATAQUE2_FRAME3 = (80, 96)
    ATAQUE2_FRAME4 = (112, 96)
    ATAQUE2_FRAME5 = (144, 96)

    DANO_FRAMES = [(0, 32), (16, 32), (32, 32), (48, 32)]
    MORTE_FRAMES = [(0, 128), (16, 128), (32, 128), (48, 128)]

    # Hitboxes Jogador 1
    ATAQUE1_HITBOXES = [
        (20, 10, 12, 10),   # Frame 1
        (22, 10, 10, 12),   # Frame 2
        (24, 12, 11, 10),   # Frame 3
        (25, 12, 10, 10),   # Frame 4
        (25, 12, 10, 10),   # Frame 5
    ]

    ATAQUE2_HITBOXES = [
        (18, 5, 14, 10),    # Frame 1
        (18, 6, 14, 10),    # Frame 2
        (18, 7, 14, 10),    # Frame 3
        (18, 6, 14, 10),    # Frame 4
        (18, 6, 14, 10),    # Frame 5
    ]

    # Jogador 2
    PARADO_P2 = [(16,0)]
    ANDANDO_P2 = [(0,144), (16,144),(32,144),(48,144),(64,144),(80,144),(96,144),(112,144)]
    ATAQUE_FRAME1_P2 = (16, 184)
    ATAQUE_FRAME2_P2 = (48, 176)
    ATAQUE_FRAME3_P2 = (80, 192)
    ATAQUE_FRAME4_P2 = (128, 192)
    ATAQUE_FRAME5_P2 = (168, 192)

    ATAQUE2_FRAME1_P2 = (16, 224)
    ATAQUE2_FRAME2_P2 = (48, 224)
    ATAQUE2_FRAME3_P2 = (80, 224)
    ATAQUE2_FRAME4_P2 = (112, 224)
    ATAQUE2_FRAME5_P2 = (144, 224)

    DANO_FRAMES_P2 = [(0, 160), (16, 160), (32, 160), (48, 160)]
    MORTE_FRAMES_P2 = [(0, 208), (16, 208), (32, 208), (48, 208)]

    # Hitboxes Jogador 2 (diferentes do P1)
    ATAQUE1_HITBOXES_P2 = [
        (18, 12, 14, 8),    # Frame 1 - mais largo e mais baixo
        (20, 10, 12, 10),   # Frame 2
        (22, 8, 10, 12),    # Frame 3 - mais alto
        (24, 10, 8, 10),    # Frame 4
        (24, 10, 8, 10),    # Frame 5
    ]

    ATAQUE2_HITBOXES_P2 = [
        (16, 8, 16, 8),     # Frame 1 - mais largo
        (16, 10, 16, 6),    # Frame 2
        (16, 12, 16, 4),    # Frame 3
        (16, 10, 16, 6),    # Frame 4
        (16, 10, 16, 6),    # Frame 5
    ]

    # Inimigos
    Inimigo_Idle = [(0,0), (32,0), (64,0), (96,0), (128,0), (160,0)]
    INIMIGO_ANDANDO = [
        (0, 16), (24, 16), (48, 16), (72, 16),
        (96, 16), (120, 16), (144, 16)
    ]
    INIMIGO_DANO_FRAMES = [(0, 32), (24, 32), (48, 32), (72, 32)]
    INIMIGO_MORTE_FRAMES = [(0, 48), (24, 48), (56, 48), (88, 48)]
    INIMIGO_ATAQUE1 = [(0,64), (24,64), (48,64), (72,64), (112,64), (144,64)]

def tiles_em_linha(xs, y):
    return [(x, y) for x in xs]

TILES_SOLIDOS = (
    tiles_em_linha([18, 19], 27) +
    tiles_em_linha([18, 19], 28) +
    tiles_em_linha([0, 1, 2, 3, 4, 5, 9, 10], 5) +
    tiles_em_linha([0, 1, 2, 3, 4, 5, 8, 9, 10, 11], 6) +
    tiles_em_linha([0, 1, 4, 5, 8, 9, 10, 11], 7) +
    tiles_em_linha([0, 1, 4, 5, 8, 9, 10, 11], 8) +
    tiles_em_linha([0, 1, 2, 3, 4, 5, 8, 9, 10, 11], 9) +
    tiles_em_linha([0, 1, 2, 3, 4, 5, 8, 9, 10, 11], 10) +
    tiles_em_linha([12, 13, 14, 17], 21) +
    tiles_em_linha([12, 13, 17], 22) +
    tiles_em_linha([18, 19], 23) +
    tiles_em_linha([18, 19], 24) 
)


TILES_MORTAIS = (
    tiles_em_linha([24, 25, 26, 27, 28, 29], 13) +
    tiles_em_linha([24, 25, 26, 27, 28, 29], 14) +
    tiles_em_linha([24, 25, 26, 27, 28, 29], 15) +
    tiles_em_linha([24, 25, 26, 27, 28, 29], 16) + 
    tiles_em_linha([24, 25, 26, 27, 28, 29], 17) +
    tiles_em_linha([24, 25, 26, 27, 28, 29], 18)
)

TILES_PORTAO = (
    tiles_em_linha([23, 26], 1) +
    tiles_em_linha([23, 26], 2) +
    tiles_em_linha([23, 26], 3) +
    tiles_em_linha([23, 26], 4) 
)

