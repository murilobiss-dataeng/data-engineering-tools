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

    # =========================================================================
    # NOVAS PASSAGENS – EVANGELHOS
    # =========================================================================
    (
        "Mateus 6:9-13",
        """Pai nosso, que estás nos céus, santificado seja o teu nome.
Venha o teu reino; faça-se a tua vontade assim na terra como no céu.
O pão nosso de cada dia dá-nos hoje.
E perdoa-nos as nossas dívidas, assim como nós perdoamos aos nossos devedores.
E não nos deixes cair em tentação; mas livra-nos do mal.""",
        "peace"
    ),
    (
        "João 1:12",
        """Mas a todos quantos o receberam deu-lhes o poder de serem feitos filhos de Deus.""",
        "grace"
    ),
    (
        "João 10:10",
        """Eu vim para que tenham vida e a tenham em abundância.""",
        "hope"
    ),
    (
        "João 15:12",
        """O meu mandamento é este: que vos ameis uns aos outros, assim como eu vos amei.""",
        "love"
    ),
    (
        "Mateus 28:19-20",
        """Ide portanto e fazei discípulos de todas as nações.
Ensinando-os a guardar todas as coisas que vos ordenei.
E eis que eu estou convosco todos os dias, até à consumação dos séculos.""",
        "trust"
    ),
    (
        "Lucas 1:37",
        """Porque para Deus nada é impossível.""",
        "faith"
    ),
    (
        "Marcos 9:23",
        """Tudo é possível ao que crê.""",
        "faith"
    ),
    (
        "Mateus 17:20",
        """Se tiverdes fé como um grão de mostarda, nada vos será impossível.""",
        "faith"
    ),
    (
        "João 6:35",
        """Disse-lhes Jesus: Eu sou o pão da vida; aquele que vem a mim não terá fome.""",
        "hope"
    ),
    (
        "João 11:25-26",
        """Disse-lhe Jesus: Eu sou a ressurreição e a vida.
Quem crê em mim, ainda que morra, viverá.""",
        "hope"
    ),

    # =========================================================================
    # NOVAS PASSAGENS – PROVÉRBIOS E SABEDORIA
    # =========================================================================
    (
        "Provérbios 4:23",
        """Sobre tudo o que guardar, guarda o teu coração, porque dele procedem as fontes da vida.""",
        "wisdom"
    ),
    (
        "Provérbios 12:25",
        """A ansiedade no coração do homem o abate, mas a boa palavra o alegra.""",
        "peace"
    ),
    (
        "Provérbios 16:9",
        """O coração do homem planeja o seu caminho, mas o Senhor lhe dirige os passos.""",
        "trust"
    ),
    (
        "Provérbios 19:21",
        """Muitos são os planos no coração do homem, mas o propósito do Senhor permanecerá.""",
        "trust"
    ),
    (
        "Provérbios 27:17",
        """O ferro com o ferro se afia, e o homem afia o rosto do seu amigo.""",
        "wisdom"
    ),
    (
        "Eclesiastes 3:1",
        """Tudo tem o seu tempo determinado; há tempo para todo propósito debaixo do céu.""",
        "wisdom"
    ),
    (
        "Eclesiastes 4:9-10",
        """Melhor é serem dois do que um.
Porque se um cair, o outro levanta o seu companheiro.""",
        "unity"
    ),

    # =========================================================================
    # NOVAS PASSAGENS – ISAÍAS E PROFETAS
    # =========================================================================
    (
        "Isaías 26:3",
        """Tu guardarás em paz aquele cuja mente está firme em ti; porque em ti confia.""",
        "peace"
    ),
    (
        "Isaías 55:8-9",
        """Porque os meus pensamentos não são os vossos pensamentos.
Assim como os céus são mais altos do que a terra, assim são os meus caminhos mais altos do que os vossos caminhos.""",
        "wisdom"
    ),
    (
        "Isaías 55:6",
        """Buscai ao Senhor enquanto se pode achar; invocai-o enquanto está perto.""",
        "hope"
    ),
    (
        "Jeremias 17:7",
        """Bem-aventurado o homem que confia no Senhor, e cuja esperança é o Senhor.""",
        "trust"
    ),
    (
        "Miqueias 6:8",
        """Ele te declarou, ó homem, o que é bom: que pratiques a justiça, e ames a benignidade, e andes humildemente com o teu Deus.""",
        "wisdom"
    ),
    (
        "Sofonias 3:17",
        """O Senhor teu Deus está no meio de ti, poderoso para salvar; ele se deleitará em ti com alegria.""",
        "peace"
    ),
    (
        "Naum 1:7",
        """O Senhor é bom, uma fortaleza no dia da angústia; e conhece os que nele confiam.""",
        "protection"
    ),

    # =========================================================================
    # NOVAS PASSAGENS – EPÍSTOLAS
    # =========================================================================
    (
        "Colossenses 3:2",
        """Pensai nas coisas que são de cima, e não nas que são da terra.""",
        "wisdom"
    ),
    (
        "Colossenses 3:23",
        """E tudo quanto fizerdes, fazei-o de todo o coração, como ao Senhor e não aos homens.""",
        "strength"
    ),
    (
        "1 Tessalonicenses 5:16-18",
        """Regozijai-vos sempre. Orai sem cessar. Em tudo dai graças.""",
        "gratitude"
    ),
    (
        "2 Timóteo 1:7",
        """Porque Deus não nos deu o espírito de temor, mas de poder, de amor e de moderação.""",
        "strength"
    ),
    (
        "Tiago 1:5",
        """Se algum de vós tem falta de sabedoria, peça-a a Deus, que a todos dá liberalmente.""",
        "wisdom"
    ),
    (
        "Tiago 1:12",
        """Bem-aventurado o homem que suporta a tentação; porque quando for provado receberá a coroa da vida.""",
        "hope"
    ),
    (
        "1 Pedro 5:7",
        """Lançando sobre ele toda a vossa ansiedade, porque ele tem cuidado de vós.""",
        "peace"
    ),
    (
        "1 João 4:8",
        """Aquele que não ama não conhece a Deus; porque Deus é amor.""",
        "love"
    ),
    (
        "1 João 4:18",
        """No amor não há temor; antes o perfeito amor lança fora o temor.""",
        "love"
    ),
    (
        "Apocalipse 3:20",
        """Eis que estou à porta e bato; se alguém ouvir a minha voz e abrir a porta, entrarei.""",
        "hope"
    ),

    # =========================================================================
    # LEITURAS – TRECHOS UM POUCO MAIS LONGOS (INÉDITOS)
    # =========================================================================
    (
        "Leitura – Romanos 12:9-12",
        """O amor seja não fingido. Aborrecei o mal e apegai-vos ao bem.
Amai-vos cordialmente uns aos outros com amor fraternal.
Não vos deixeis vencer do mal, mas vencei o mal com o bem.
Sede constantes na tribulação, perseverai na oração.""",
        "love"
    ),
    (
        "Leitura – Salmo 19:14 (oração)",
        """Sejam agradáveis as palavras da minha boca e a meditação do meu coração perante a tua face, ó Senhor, Rocha minha e Redentor meu.""",
        "wisdom"
    ),
    (
        "Leitura – Filipenses 4:8",
        """Finalmente, irmãos, tudo o que é verdadeiro, tudo o que é honesto, tudo o que é justo, tudo o que é puro, tudo o que é amável, tudo o que é de boa fama, nisso pensai.""",
        "wisdom"
    ),
    (
        "Leitura – Isaías 40:28-31",
        """Não sabes tu? Não ouviste que o eterno Deus, o Senhor, criador dos fins da terra, não se cansa?
Dá força ao cansado e multiplica as forças ao que não tem nenhum.
Os jovens se cansarão e se fatigarão, e os moços certamente cairão.
Mas os que esperam no Senhor renovarão as suas forças; subirão com asas como águias.""",
        "hope"
    ),
    (
        "Leitura – Deuteronômio 31:6",
        """Esforçai-vos e tende bom ânimo; não temais nem vos espanteis.
Porque o Senhor vosso Deus é convosco; não vos deixará nem vos desamparará.""",
        "strength"
    ),
    (
        "Leitura – Lamentações 3:22-23",
        """As misericórdias do Senhor são a causa de não sermos consumidos.
Novas são cada manhã; grande é a tua fidelidade.""",
        "hope"
    ),
    (
        "Leitura – Mateus 5:3-5",
        """Bem-aventurados os pobres de espírito, porque deles é o reino dos céus.
Bem-aventurados os que choram, porque eles serão consolados.
Bem-aventurados os mansos, porque eles herdarão a terra.""",
        "peace"
    ),
    (
        "Leitura – João 14:27",
        """Deixo-vos a paz, a minha paz vos dou; não vo-la dou como o mundo a dá.
Não se turbe o vosso coração, nem se atemorize.""",
        "peace"
    ),
    (
        "Leitura – Efésios 4:32",
        """Antes sede uns para com os outros benignos, misericordiosos, perdoando-vos uns aos outros.
Como também Deus vos perdoou em Cristo.""",
        "forgiveness"
    ),
    (
        "Leitura – 1 Coríntios 16:13-14",
        """Vigiai, estai firmes na fé, portai-vos varonilmente, sede fortes.
Todas as vossas coisas sejam feitas com amor.""",
        "strength"
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
    "gratitude": "heavenly",
    "forgiveness": "heavenly",
    "unity": "serene",
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
