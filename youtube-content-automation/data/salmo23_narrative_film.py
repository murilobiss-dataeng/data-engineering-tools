"""
Filme narrativo cinematográfico Salmo 23.

Análise, personagens, roteiro, storyboard, narração e prompts de cena.
Duração alvo: ~2:20–2:45.
"""

from typing import Any, Dict, List

PSALM_REF = "Salmo 23"
PSALM_TITLE = "O Senhor é meu Pastor"
PSALM_TEXT = """O Senhor é meu pastor; nada me faltará.
Ele me faz repousar em pastos verdejantes.
Leva-me às águas tranquilas.
Refrigera-me a alma.
Guia-me pelas veredas da justiça por amor do seu nome.
Ainda que eu ande pelo vale da sombra da morte, não temerei mal algum, porque tu estás comigo.
A tua vara e o teu cajado me consolam.
Preparas uma mesa perante mim na presença dos meus inimigos.
Unges a minha cabeça com óleo; o meu cálice transborda.
Certamente que a bondade e a misericórdia me seguirão todos os dias da minha vida.
E habitarei na casa do Senhor por longos dias."""

ANALYSIS: Dict[str, Any] = {
    "salmo": "Salmo 23",
    "mensagem_principal": (
        "Deus cuida como um pastor: sustenta, guia, protege no perigo "
        "e conduz a uma vida de plenitude e comunhão."
    ),
    "contexto": (
        "Poema atribuído a Davi. Metáfora pastoral do Antigo Oriente: "
        "o pastor garante pastagem, água, proteção e direção ao rebanho."
    ),
    "conflito": "Atravessar o vale da sombra da morte medo, escuridão, ameaça.",
    "emocao_arco": [
        "confiança serena",
        "descanso",
        "refrigério",
        "tensão/medo",
        "coragem pela presença de Deus",
        "consolo",
        "abundância/gratidão",
        "paz eterna",
    ],
    "simbolos": {
        "pastor": "cuidado íntimo de Deus",
        "pastos verdejantes": "provisão e descanso",
        "águas tranquilas": "paz e restauração",
        "veredas da justiça": "orientação moral e propósito",
        "vale da sombra": "sofrimento, risco, mortalidade",
        "vara e cajado": "disciplina protetora e guia",
        "mesa": "honra e provisão mesmo sob pressão",
        "óleo": "consagração, alegria, dignidade",
        "cálice que transborda": "abundância da graça",
        "bondade e misericórdia": "companheiros constantes",
        "casa do Senhor": "comunhão duradoura com Deus",
    },
    "transformacao": (
        "De dependência cotidiana do Pastor → confronto com o medo no vale → "
        "confiança renovada pela presença → celebração e esperança de habitar com Deus."
    ),
    "conclusao": "Proteção, paz e confiança: nada falta a quem o Senhor pastoreia.",
}

STYLE_LOCK = (
    "stylized 3D animated feature film still, cinematic animated storytelling, "
    "smooth rendered characters, painterly lighting, volumetric golden light, "
    "rich earth tones, emotional expressive animation, soft depth of field, "
    "NOT photorealistic, NOT live action, NOT photo, "
    "NO text, NO watermark, NO logo, NO modern objects"
)

CHARACTER_LOCK = (
    "SAME ANIMATED CHARACTER in every shot: David (King David / Davi), Levantine shepherd about 28 years old, "
    "stylized 3D animation look, olive skin, warm brown eyes, short dark curly hair, "
    "neat full dark beard, white linen tunic with brown leather sash, brown sandals, "
    "wooden shepherd staff, gentle but resilient face. "
    "Keep identical face, hair, beard, clothing and staff across all frames."
)

CHARACTERS: List[Dict[str, Any]] = [
    {
        "nome": "Davi",
        "idade": 28,
        "aparencia": (
            "Pele oliva, olhos castanhos quentes, cabelo curto ondulado escuro, "
            "barba cheia bem cuidada, porte atlético de quem caminha colinas."
        ),
        "roupas": "Túnica de linho branco, faixa de couro marrom, sandálias, cajado de madeira.",
        "personalidade": "Quietude, fé prática, coragem silenciosa, ternura com o rebanho.",
        "emocao_arco": "Serenidade → apreensão → medo → confiança → gratidão → paz.",
        "papel": "Protagonista humano que vive a metáfora do Salmo 23.",
        "relacoes": "Pastor do rebanho; filho espiritual do Pastor divino (Deus).",
    },
    {
        "nome": "O Rebanho",
        "idade": "variado",
        "aparencia": "Ovelhas brancas e creme, algumas com marcas naturais.",
        "roupas": "—",
        "personalidade": "Dependente, confiante no pastor.",
        "emocao_arco": "Segurança → inquietação no vale → alívio na luz.",
        "papel": "Espelho da alma cuidada por Deus.",
        "relacoes": "Seguem Davi; simbolizam o povo sob cuidado divino.",
    },
    {
        "nome": "Presença do Senhor (simbólica)",
        "idade": "eterna",
        "aparencia": (
            "Não antropomorfizada de forma literal: luz dourada volumétrica, "
            "sombra protetora, vento suave, calor no cajado."
        ),
        "roupas": "—",
        "personalidade": "Fiel, protetora, íntima.",
        "emocao_arco": "Constante revelada com mais força no clímax.",
        "papel": "O Pastor verdadeiro do Salmo.",
        "relacoes": "Guarda e guia Davi.",
    },
]

# Narração completa em português brasileiro claro (sem misturar idiomas)
NARRATION_FULL = (
    "Nas colinas de Judá, ao romper da manhã, um pastor chamado Davi despertava com o rebanho. "
    "Ele não tinha riqueza, nem muro alto, mas tinha uma certeza: o Senhor era o seu Pastor. "
    "E por isso, nada lhe faltaria. "
    "Pelos pastos verdejantes, Davi guiava as ovelhas. Ali, o corpo descansava e o coração se aquietava. "
    "Ele as levava às águas tranquilas, um espelho de paz no meio da terra seca. "
    "E, ao beber daquela quietude, a alma se refrigerava. "
    "O caminho não era sempre fácil. Havia veredas estreitas, escolhas difíceis, "
    "mas o Pastor o guiava pelas veredas da justiça, por amor do Seu nome. "
    "Então veio o vale. Escuro. Silencioso. Onde a sombra da morte parecia caminhar ao lado. "
    "O medo apertou o peito de Davi. As ovelhas se inquietaram. "
    "Mas ele ergueu o olhar e sussurrou: Ainda que eu ande pelo vale, não temerei mal algum. "
    "Porque Tu estás comigo. "
    "Uma luz suave atravessou a escuridão. A vara e o cajado, presença e proteção, o consolavam. "
    "Ele avançou. Passo após passo. Até sair do vale para a luz. "
    "Diante dele, uma mesa. Provisão e honra, mesmo sob a pressão do medo. "
    "O óleo ungindo a cabeça. O cálice transbordando. "
    "E Davi compreendeu: a bondade e a misericórdia o seguiriam todos os dias da sua vida. "
    "Ao fim do caminho, a casa do Senhor se abria como um lar eterno. "
    "Paz. Proteção. Confiança. "
    "O Senhor é o meu Pastor, e nada me faltará."
)

# Storyboard: 20 cenas (~7–9s cada → ~2:20–2:40 com áudio)
SCENES: List[Dict[str, Any]] = [
    {
        "num": 1,
        "duration": 8.0,
        "act": "abertura",
        "cenario": "Colinas da Judeia ao amanhecer; névoa dourada.",
        "personagens": ["Davi"],
        "acao": "Título e despertar: Davi abre os olhos no alto da colina.",
        "emocao": "Expectativa serena",
        "dialogo": None,
        "narracao": (
            "Nas colinas de Judá, ao romper da manhã, um pastor chamado Davi despertava com o rebanho."
        ),
        "camera": "aerial wide → slow dolly in",
        "animacao": "neblina se move; luz do sol sobe",
        "iluminacao": "golden hour suave",
        "sfx": ["vento_leve", "passaros"],
        "musica": "pad_suave_inicio",
        "texto_tela": "Salmo 23 O Senhor é meu Pastor",
        "transicao": "crossfade",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "Wide aerial cinematic shot of Judean hills at dawn, golden mist in valleys, "
            "young shepherd David waking on a rocky overlook, staff beside him, flock nearby, "
            "hopeful sunrise, epic yet intimate."
        ),
    },
    {
        "num": 2,
        "duration": 8.0,
        "act": "abertura",
        "cenario": "Acampamento simples na encosta.",
        "personagens": ["Davi", "O Rebanho"],
        "acao": "Davi se ergue, segura o cajado, olha o rebanho.",
        "emocao": "Confiança quieta",
        "dialogo": None,
        "narracao": (
            "Ele não tinha riqueza, nem muro alto, mas tinha uma certeza: o Senhor era o seu Pastor."
        ),
        "camera": "medium tracking shot",
        "animacao": "tecido da túnica ao vento; ovelhas se mexem",
        "iluminacao": "luz lateral quente",
        "sfx": ["passos", "ovelhas"],
        "musica": "pad_suave_inicio",
        "texto_tela": None,
        "transicao": "crossfade",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "Medium shot of David standing among sheep on a hillside camp at sunrise, "
            "holding wooden staff, looking over the flock with quiet faith, warm side light."
        ),
    },
    {
        "num": 3,
        "duration": 7.5,
        "act": "abertura",
        "cenario": "Trilha estreita descendo a colina.",
        "personagens": ["Davi", "O Rebanho"],
        "acao": "Começa a caminhada; sorriso leve.",
        "emocao": "Paz / provisão",
        "dialogo": None,
        "narracao": "E por isso, nada lhe faltaria.",
        "camera": "slow zoom on face then pan to path",
        "animacao": "poeira fina nos pés",
        "iluminacao": "manhã clara",
        "sfx": ["passos", "vento_leve"],
        "musica": "pad_suave_inicio",
        "texto_tela": "Nada me faltará",
        "transicao": "crossfade",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "Close-up to medium of David walking a dusty path downhill with sheep following, "
            "slight peaceful smile, soft morning light, sense of provision and trust."
        ),
    },
    {
        "num": 4,
        "duration": 8.0,
        "act": "desenvolvimento",
        "cenario": "Pastagens verdes exuberantes.",
        "personagens": ["Davi", "O Rebanho"],
        "acao": "Rebanho pastando; Davi observa.",
        "emocao": "Descanso",
        "dialogo": None,
        "narracao": (
            "Pelos pastos verdejantes, Davi guiava as ovelhas. Ali, o corpo descansava e o coração se aquietava."
        ),
        "camera": "wide establishing + gentle pan",
        "animacao": "grama ao vento; ovelhas pastando",
        "iluminacao": "luz solar difusa, verdes vivos",
        "sfx": ["vento_grama", "ovelhas"],
        "musica": "pastoral_leve",
        "texto_tela": None,
        "transicao": "crossfade",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "Wide cinematic shot of lush green pastures, sheep grazing peacefully, "
            "David standing watch with staff, soft breeze in grass, restorative calm."
        ),
    },
    {
        "num": 5,
        "duration": 7.5,
        "act": "desenvolvimento",
        "cenario": "Clareira no pasto.",
        "personagens": ["Davi"],
        "acao": "Davi se deita na grama, olhos fechados um instante.",
        "emocao": "Repouso profundo",
        "dialogo": None,
        "narracao": "Ele as levava às águas tranquilas um espelho de paz no meio da terra seca.",
        "camera": "high angle soft dolly out",
        "animacao": "nuvens lentas; respiração",
        "iluminacao": "meio-dia suave filtrado",
        "sfx": ["vento_grama", "silencio"],
        "musica": "pastoral_leve",
        "texto_tela": None,
        "transicao": "crossfade",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "High angle of David resting in tall green grass, eyes closed, staff nearby, "
            "sheep in soft focus background, profound rest and safety."
        ),
    },
    {
        "num": 6,
        "duration": 8.0,
        "act": "desenvolvimento",
        "cenario": "Lago espelhado entre pedras.",
        "personagens": ["Davi", "O Rebanho"],
        "acao": "Chegam à água; ovelhas bebem; reflexão no lago.",
        "emocao": "Paz / refrigério",
        "dialogo": None,
        "narracao": "E, ao beber daquela quietude, a alma se refrigerava.",
        "camera": "slow push-in over water reflections",
        "animacao": "ondulações mínimas na água",
        "iluminacao": "reflexos prateados e dourados",
        "sfx": ["agua", "ovelhas"],
        "musica": "pastoral_leve",
        "texto_tela": "Águas tranquilas",
        "transicao": "crossfade",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "Cinematic lakeside scene, still mirror-like water reflecting sky, "
            "David kneeling to drink, sheep drinking nearby, serene restoration."
        ),
    },
    {
        "num": 7,
        "duration": 7.5,
        "act": "desenvolvimento",
        "cenario": "Vereda entre oliveiras.",
        "personagens": ["Davi"],
        "acao": "Caminha concentrado entre oliveiras; sol filtra folhas.",
        "emocao": "Determinação guiada",
        "dialogo": None,
        "narracao": (
            "O caminho não era sempre fácil. Havia veredas estreitas, escolhas difíceis,"
        ),
        "camera": "tracking side shot through trees",
        "animacao": "folhas e raios de luz (god rays)",
        "iluminacao": "luz volumétrica entre árvores",
        "sfx": ["passos", "folhas"],
        "musica": "tensao_sutil",
        "texto_tela": None,
        "transicao": "crossfade",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "Tracking shot of David walking a narrow path through ancient olive trees, "
            "volumetric god rays through leaves, thoughtful determination."
        ),
    },
    {
        "num": 8,
        "duration": 7.5,
        "act": "desenvolvimento",
        "cenario": "Trilha de pedras; horizonte ainda claro.",
        "personagens": ["Davi", "O Rebanho"],
        "acao": "Aponta o caminho; rebanho segue.",
        "emocao": "Obediência / direção",
        "dialogo": None,
        "narracao": (
            "mas o Pastor o guiava pelas veredas da justiça, por amor do Seu nome."
        ),
        "camera": "medium behind subject looking forward",
        "animacao": "poeira; ovelhas em fila",
        "iluminacao": "luz de tarde começando a esfriar",
        "sfx": ["passos", "ovelhas"],
        "musica": "tensao_sutil",
        "texto_tela": None,
        "transicao": "crossfade",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "Over-the-shoulder of David guiding sheep along a righteous stone path, "
            "afternoon light cooling, sense of guided purpose."
        ),
    },
    {
        "num": 9,
        "duration": 8.0,
        "act": "desenvolvimento",
        "cenario": "Entrada de um vale estreito e escuro.",
        "personagens": ["Davi", "O Rebanho"],
        "acao": "Nuvens pesadas; Davi hesita na entrada do vale.",
        "emocao": "Apreensão crescente",
        "dialogo": None,
        "narracao": (
            "Então veio o vale. Escuro. Silencioso. Onde a sombra da morte parecia caminhar ao lado."
        ),
        "camera": "low angle wide, then tilt up to storm clouds",
        "animacao": "nuvens rápidas; vento forte",
        "iluminacao": "contraste dramático, céu escuro",
        "sfx": ["vento_forte", "trovao_distante"],
        "musica": "conflito_crescendo",
        "texto_tela": None,
        "transicao": "crossfade_dark",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "Dramatic wide shot of David at the mouth of a dark narrow valley, "
            "storm clouds overhead, uneasy sheep, ominous atmosphere, fear approaching."
        ),
    },
    {
        "num": 10,
        "duration": 8.0,
        "act": "desenvolvimento",
        "cenario": "Interior do vale da sombra.",
        "personagens": ["Davi", "O Rebanho"],
        "acao": "Caminha tenso; olha para as paredes do vale.",
        "emocao": "Medo",
        "dialogo": None,
        "narracao": "O medo apertou o peito de Davi. As ovelhas se inquietaram.",
        "camera": "handheld-feeling tight tracking",
        "animacao": "poeira; sombras longas",
        "iluminacao": "azul-acinzentado frio, pouca luz",
        "sfx": ["respiracao", "eco", "ovelhas_inquietas"],
        "musica": "conflito_crescendo",
        "texto_tela": None,
        "transicao": "crossfade",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "Tight tracking shot inside a shadowed canyon valley, David tense with staff raised, "
            "frightened sheep close, cold blue-gray light, emotional fear."
        ),
    },
    {
        "num": 11,
        "duration": 8.0,
        "act": "climax",
        "cenario": "Centro do vale; Davi ajoelha.",
        "personagens": ["Davi"],
        "acao": "Fecha os olhos, cajado no peito, ora.",
        "emocao": "Medo → fé",
        "dialogo": "Ainda que eu ande pelo vale, não temerei mal algum.",
        "narracao": (
            "Mas ele ergueu o olhar e sussurrou: Ainda que eu ande pelo vale, não temerei mal algum."
        ),
        "camera": "extreme close-up face → pull back",
        "animacao": "lágrima contida; vento diminui",
        "iluminacao": "primeiro feixe de luz dourada",
        "sfx": ["respiracao", "silencio"],
        "musica": "climax_subindo",
        "texto_tela": "Não temerei mal algum",
        "transicao": "crossfade",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "Extreme close-up of David's emotional face in the dark valley, eyes lifting in prayer, "
            "first golden light beam touching his cheek, staff held to chest, faith overcoming fear."
        ),
    },
    {
        "num": 12,
        "duration": 8.0,
        "act": "climax",
        "cenario": "Vale iluminado por presença divina simbólica.",
        "personagens": ["Davi", "Presença do Senhor (simbólica)"],
        "acao": "Luz envolve Davi; expressão de alívio.",
        "emocao": "Consolo / presença",
        "dialogo": "Porque Tu estás comigo.",
        "narracao": "Porque Tu estás comigo.",
        "camera": "slow orbit around character in light",
        "animacao": "partículas de luz; vento suave",
        "iluminacao": "volumétrica dourada intensa",
        "sfx": ["vento_leve", "harmonia"],
        "musica": "climax_subindo",
        "texto_tela": "Tu estás comigo",
        "transicao": "crossfade",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "David standing in the valley bathed in powerful volumetric golden divine light, "
            "relieved emotional expression, particles of light, sacred presence without literal figure."
        ),
    },
    {
        "num": 13,
        "duration": 7.5,
        "act": "climax",
        "cenario": "Close das mãos no cajado.",
        "personagens": ["Davi"],
        "acao": "Mãos firmes no cajado iluminado.",
        "emocao": "Consolo",
        "dialogo": None,
        "narracao": (
            "Uma luz suave atravessou a escuridão. A vara e o cajado presença e proteção o consolavam."
        ),
        "camera": "macro/close-up insert",
        "animacao": "brilho no madeira; poeira dourada",
        "iluminacao": "luz quente no objeto",
        "sfx": ["harmonia"],
        "musica": "climax_pico",
        "texto_tela": None,
        "transicao": "crossfade",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "Close-up of David's weathered hands gripping the wooden shepherd staff, "
            "warm golden light wrapping the wood, dust motes, comfort and protection symbol."
        ),
    },
    {
        "num": 14,
        "duration": 8.5,
        "act": "climax",
        "cenario": "Saída do vale para planície iluminada.",
        "personagens": ["Davi", "O Rebanho"],
        "acao": "Davi emerge do vale; rebanho atrás; braço aberto à luz.",
        "emocao": "Libertação / vitória espiritual",
        "dialogo": None,
        "narracao": "Ele avançou. Passo após passo. Até sair do vale para a luz.",
        "camera": "hero wide shot + slow zoom out",
        "animacao": "vento forte positivo; luz explode",
        "iluminacao": "contraluz épica dourada",
        "sfx": ["vento_forte", "ovelhas"],
        "musica": "climax_pico",
        "texto_tela": None,
        "transicao": "crossfade_bright",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "Epic wide shot of David emerging from dark valley into blazing golden sunlight, "
            "sheep following, arms slightly open, emotional liberation, strongest moment of film."
        ),
    },
    {
        "num": 15,
        "duration": 8.0,
        "act": "conclusao",
        "cenario": "Clareira com mesa rústica preparada.",
        "personagens": ["Davi"],
        "acao": "Mesa com pão, frutas, azeite; Davi se aproxima emocionado.",
        "emocao": "Espanto / gratidão",
        "dialogo": None,
        "narracao": "Diante dele, uma mesa. Provisão e honra, mesmo sob a pressão do medo.",
        "camera": "dolly in to table then to Davi",
        "animacao": "chama de lampião suave; tecido",
        "iluminacao": "pôr do sol âmbar",
        "sfx": ["fogo_suave", "vento_leve"],
        "musica": "resolucao_emocional",
        "texto_tela": None,
        "transicao": "crossfade",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "Rustic banquet table prepared in a wilderness clearing at sunset, bread fruit oil, "
            "David approaching with awe and gratitude, amber light, honor and provision."
        ),
    },
    {
        "num": 16,
        "duration": 8.0,
        "act": "conclusao",
        "cenario": "Mesa; unção simbólica.",
        "personagens": ["Davi"],
        "acao": "Óleo na cabeça; cálice transborda vinho/água.",
        "emocao": "Abundância / dignidade",
        "dialogo": None,
        "narracao": "O óleo ungindo a cabeça. O cálice transbordando.",
        "camera": "close-up details montage feel (single frame rich)",
        "animacao": "gota de óleo; líquido derramando",
        "iluminacao": "brilhos quentes no metal/cerâmica",
        "sfx": ["liquido", "harmonia"],
        "musica": "resolucao_emocional",
        "texto_tela": "O meu cálice transborda",
        "transicao": "crossfade",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "Intimate cinematic detail: oil anointing David's head, overflowing cup on table, "
            "warm specular highlights, abundance and blessing, emotional gratitude."
        ),
    },
    {
        "num": 17,
        "duration": 7.5,
        "act": "conclusao",
        "cenario": "Caminho ao entardecer; luzes suaves seguindo.",
        "personagens": ["Davi", "Presença do Senhor (simbólica)"],
        "acao": "Davi caminha; duas luzes suaves (bondade e misericórdia) o acompanham.",
        "emocao": "Acompanhamento / esperança",
        "dialogo": None,
        "narracao": (
            "E Davi compreendeu: a bondade e a misericórdia o seguiriam todos os dias da sua vida."
        ),
        "camera": "rear tracking shot",
        "animacao": "duas orbes de luz suaves atrás",
        "iluminacao": "crepúsculo rosa-dourado",
        "sfx": ["passos", "vento_leve"],
        "musica": "resolucao_emocional",
        "texto_tela": None,
        "transicao": "crossfade",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "Rear tracking shot of David walking a dusk path, two soft glowing lights following him "
            "symbolizing goodness and mercy, pink-gold twilight, hopeful peace."
        ),
    },
    {
        "num": 18,
        "duration": 8.0,
        "act": "conclusao",
        "cenario": "Templo / casa do Senhor no horizonte ao pôr do sol.",
        "personagens": ["Davi"],
        "acao": "Davi contempla a casa do Senhor e avança em direção a ela.",
        "emocao": "Anseio sagrado / paz",
        "dialogo": None,
        "narracao": "Ao fim do caminho, a casa do Senhor se abria como um lar eterno.",
        "camera": "wide establishing + slow zoom",
        "animacao": "nuvens coloridas; pássaros",
        "iluminacao": "pôr do sol majestoso",
        "sfx": ["passaros", "vento_leve"],
        "musica": "final_paz",
        "texto_tela": None,
        "transicao": "crossfade",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "Wide majestic shot of ancient temple silhouette on a hill at sunset, "
            "David walking toward it with awe, eternal home feeling, peaceful sacred atmosphere."
        ),
    },
    {
        "num": 19,
        "duration": 7.5,
        "act": "conclusao",
        "cenario": "Close emocional de Davi.",
        "personagens": ["Davi"],
        "acao": "Sorriso sereno; olhos úmidos de gratidão.",
        "emocao": "Paz / gratidão / fé",
        "dialogo": None,
        "narracao": "Paz. Proteção. Confiança.",
        "camera": "portrait close-up slow zoom",
        "animacao": "brilho nos olhos; cabelo ao vento",
        "iluminacao": "luz residual do pôr do sol",
        "sfx": ["silencio", "vento_leve"],
        "musica": "final_paz",
        "texto_tela": None,
        "transicao": "crossfade",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "Portrait close-up of David with serene grateful smile, moist eyes, sunset rim light, "
            "deep peace and faith after the journey."
        ),
    },
    {
        "num": 20,
        "duration": 9.0,
        "act": "conclusao",
        "cenario": "Céu noturno com estrelas sobre as colinas; fade.",
        "personagens": ["Davi (silhueta distante)"],
        "acao": "Silhueta com rebanho sob estrelas; mensagem final.",
        "emocao": "Esperança eterna",
        "dialogo": None,
        "narracao": "O Senhor é o meu Pastor, e nada me faltará.",
        "camera": "extreme wide slow tilt to stars",
        "animacao": "estrelas; fade out",
        "iluminacao": "noite azul com toque dourado residual",
        "sfx": ["vento_leve", "passaros_noite"],
        "musica": "final_paz",
        "texto_tela": "O Senhor é o meu Pastor nada me faltará",
        "transicao": "fade_black",
        "prompt": (
            f"{STYLE_LOCK}. {CHARACTER_LOCK}. "
            "Extreme wide night shot of hills under stars, distant silhouette of shepherd and flock, "
            "peaceful eternal hope, cinematic ending frame, no readable text in image."
        ),
    },
]

AUDIO_STRATEGY = {
    "trilha": {
        "abertura": "pad orquestral suave, cordas baixas, esperança",
        "desenvolvimento": "tema pastoral com flauta/corda leve",
        "conflito": "drones escuros, percussão suave, tensão",
        "climax": "crescendo harmônico, brilho de cordas",
        "conclusao": "resolução maior, paz, fade longo",
    },
    "narracao": {
        "voz": "pt-BR-ThalitaMultilingualNeural",
        "tom": "cinematográfico, emocional, pausado",
    },
    "sfx": [
        "vento",
        "passos",
        "ovelhas",
        "água",
        "trovão distante",
        "respiração",
        "harmonia sutil",
    ],
}

SEED = 230023  # consistência visual entre gerações Leonardo
