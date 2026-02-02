"""
Passagens da Bíblia para o canal Passagem do Dia.

Inclui versículos e trechos de diversos livros:
- Evangelhos (Mateus, Marcos, Lucas, João)
- Provérbios
- Isaías
- Romanos, Filipenses, etc.
"""

# Formato: (referência, texto_completo, tema/mood)
PASSAGENS_BIBLIA = [
    # =========================================================================
    # EVANGELHOS
    # =========================================================================
    (
        "João 3:16",
        """Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito,
para que todo aquele que nele crê não pereça, mas tenha a vida eterna.""",
        "love"
    ),
    (
        "João 14:6",
        """Respondeu Jesus: Eu sou o caminho, e a verdade e a vida.
Ninguém vem ao Pai, senão por mim.""",
        "truth"
    ),
    (
        "Mateus 11:28-30",
        """Vinde a mim, todos os que estais cansados e oprimidos, e eu vos aliviarei.
Tomai sobre vós o meu jugo, e aprendei de mim, que sou manso e humilde de coração.
E encontrareis descanso para as vossas almas.
Porque o meu jugo é suave e o meu fardo é leve.""",
        "peace"
    ),
    (
        "Mateus 5:14-16",
        """Vós sois a luz do mundo.
Não se pode esconder uma cidade edificada sobre um monte.
Nem se acende a candeia e se coloca debaixo do alqueire, mas no velador.
E alumia a todos os que estão na casa.
Assim resplandeça a vossa luz diante dos homens.""",
        "light"
    ),
    (
        "Lucas 6:31",
        """E como vós quereis que os homens vos façam, assim fazei-lhes vós também.""",
        "wisdom"
    ),
    (
        "João 8:12",
        """Falou-lhes, pois, Jesus outra vez, dizendo: Eu sou a luz do mundo.
Quem me segue não andará em trevas, mas terá a luz da vida.""",
        "light"
    ),
    (
        "Mateus 6:33",
        """Mas buscai primeiro o reino de Deus, e a sua justiça.
E todas estas coisas vos serão acrescentadas.""",
        "trust"
    ),
    (
        "Filipenses 4:13",
        """Posso todas as coisas naquele que me fortalece.""",
        "strength"
    ),
    (
        "Filipenses 4:6-7",
        """Não andeis ansiosos de coisa alguma.
Em tudo, porém, sejam conhecidas diante de Deus as vossas petições.
E a paz de Deus, que excede todo o entendimento, guardará os vossos corações.""",
        "peace"
    ),
    (
        "Romanos 8:28",
        """E sabemos que todas as coisas cooperam para o bem daqueles que amam a Deus.""",
        "trust"
    ),
    (
        "Romanos 8:38-39",
        """Porque estou certo de que nem a morte, nem a vida, nem os anjos, nem os principados.
Nem o presente, nem o porvir, nem as potestades.
Nem a altura, nem a profundidade, nem alguma outra criatura.
Nos poderá separar do amor de Deus, que está em Cristo Jesus nosso Senhor.""",
        "love"
    ),
    # =========================================================================
    # PROVÉRBIOS
    # =========================================================================
    (
        "Provérbios 3:5-6",
        """Confia no Senhor de todo o teu coração.
E não te estribes no teu próprio entendimento.
Reconhece-o em todos os teus caminhos, e ele endireitará as tuas veredas.""",
        "trust"
    ),
    (
        "Provérbios 16:3",
        """Entrega ao Senhor as tuas obras, e os teus desígnios serão estabelecidos.""",
        "trust"
    ),
    (
        "Provérbios 22:6",
        """Instrui o menino no caminho em que deve andar.
E até quando envelhecer não se desviará dele.""",
        "wisdom"
    ),
    (
        "Provérbios 15:1",
        """A resposta branda desvia o furor, mas a palavra dura suscita a ira.""",
        "wisdom"
    ),
    (
        "Provérbios 18:10",
        """O nome do Senhor é uma torre forte; o justo corre para ela e está em segurança.""",
        "protection"
    ),
    # =========================================================================
    # ISAÍAS
    # =========================================================================
    (
        "Isaías 40:31",
        """Mas os que esperam no Senhor renovarão as suas forças.
Subirão com asas como águias; correrão e não se cansarão.""",
        "hope"
    ),
    (
        "Isaías 41:10",
        """Não temas, porque eu sou contigo.
Não te assombres, porque eu sou o teu Deus.
Eu te fortaleço, e te ajudo, e te sustento com a destra da minha justiça.""",
        "protection"
    ),
    (
        "Isaías 43:2",
        """Quando passares pelas águas, eu serei contigo.
Quando pelos rios, eles não te submergirão.
Quando passares pelo fogo, não te queimarás.""",
        "protection"
    ),
    (
        "Isaías 53:5",
        """Mas ele foi ferido por causa das nossas transgressões.
E moído por causa das nossas iniquidades.
O castigo que nos traz a paz estava sobre ele.""",
        "hope"
    ),
    # =========================================================================
    # OUTRAS EPÍSTOLAS E LIVROS
    # =========================================================================
    (
        "Josué 1:9",
        """Não te mandei eu? Esforça-te e tem bom ânimo.
Não te atemorizes, nem te espantes; porque o Senhor teu Deus está contigo.""",
        "strength"
    ),
    (
        "Jeremias 29:11",
        """Porque eu bem sei os pensamentos que tenho a vosso respeito, diz o Senhor.
Pensamentos de paz e não de mal, para vos dar o fim que esperais.""",
        "hope"
    ),
    (
        "2 Coríntios 5:7",
        """Porque andamos por fé, e não por vista.""",
        "trust"
    ),
    (
        "Hebreus 11:1",
        """Ora, a fé é o firme fundamento das coisas que se esperam.
E a prova das coisas que se não veem.""",
        "faith"
    ),
    (
        "1 Coríntios 13:4-7",
        """O amor é paciente, é benigno.
O amor não arde em ciúmes, não se ufana, não se ensoberbece.
Não se conduz inconvenientemente, não busca os seus interesses.
Não se irrita, não se ressente do mal.
Não se alegra com a injustiça, mas regozija-se com a verdade.
Tudo sofre, tudo crê, tudo espera, tudo suporta.""",
        "love"
    ),
    (
        "Gálatas 5:22-23",
        """Mas o fruto do Espírito é: amor, alegria, paz, longanimidade.
Benignidade, bondade, fidelidade, mansidão, domínio próprio.""",
        "peace"
    ),
    (
        "Efésios 2:8-9",
        """Porque pela graça sois salvos, por meio da fé.
E isto não vem de vós; é dom de Deus.
Não vem das obras, para que ninguém se glorie.""",
        "grace"
    ),
]

# Mapeamento de mood para paleta visual (compatível com salmos)
MOOD_TO_PALETTE = {
    "love": "heavenly",
    "truth": "sacred",
    "peace": "heavenly",
    "light": "dawn",
    "wisdom": "serene",
    "trust": "serene",
    "strength": "sacred",
    "protection": "sacred",
    "hope": "dawn",
    "faith": "heavenly",
    "grace": "heavenly",
}


def get_passagem_by_index(index: int):
    """Busca uma passagem pelo índice."""
    if 0 <= index < len(PASSAGENS_BIBLIA):
        return PASSAGENS_BIBLIA[index]
    return None


def get_passagem_by_referencia(referencia: str):
    """Busca uma passagem pela referência (ex: João 3:16)."""
    ref_lower = referencia.strip().lower()
    for p in PASSAGENS_BIBLIA:
        if p[0].lower() == ref_lower:
            return p
    return None


def get_palette_for_passagem(mood: str = None) -> str:
    """Retorna a paleta visual recomendada para a passagem."""
    if mood and mood in MOOD_TO_PALETTE:
        return MOOD_TO_PALETTE[mood]
    return "heavenly"


def list_all_passagens():
    """Lista todas as passagens disponíveis."""
    print(f"\n{'='*60}")
    print("  PASSAGENS DA BÍBLIA DISPONÍVEIS")
    print(f"{'='*60}\n")
    for i, (ref, texto, mood) in enumerate(PASSAGENS_BIBLIA):
        linhas = len([l for l in texto.strip().split("\n") if l.strip()])
        palette = MOOD_TO_PALETTE.get(mood, "heavenly")
        print(f"  [{i:2d}] {ref:<18} | {linhas} linhas | {mood:<10} | {palette}")
    print(f"\n{'='*60}")
    print(f"  Total: {len(PASSAGENS_BIBLIA)} passagens")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    list_all_passagens()
