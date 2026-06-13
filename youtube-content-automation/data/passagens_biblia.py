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
    # NOVAS PASSAGENS – VERSÍCULOS ADICIONAIS
    # =========================================================================
    (
        "Mateus 7:7",
        """Pedi, e dar-se-vos-á; buscai, e achareis; batei, e abrir-se-vos-á.""",
        "faith"
    ),
    (
        "Mateus 6:34",
        """Portanto, não vos inquieteis com o dia de amanhã, porque o dia de amanhã cuidará de si mesmo.
Basta a cada dia o seu mal.""",
        "peace"
    ),
    (
        "Mateus 28:20",
        """E eis que estou convosco todos os dias, até à consumação dos séculos.""",
        "trust"
    ),
    (
        "João 16:33",
        """No mundo tereis aflições, mas tende bom ânimo; eu venci o mundo.""",
        "strength"
    ),
    (
        "Lucas 12:32",
        """Não temais, ó pequeno rebanho, porque aprouve ao Pai dar-vos o reino.""",
        "peace"
    ),
    (
        "Romanos 5:8",
        """Mas Deus prova o seu amor para conosco, em que Cristo morreu por nós, sendo nós ainda pecadores.""",
        "love"
    ),
    (
        "Romanos 12:2",
        """E não vos conformeis com este mundo, mas transformai-vos pela renovação do vosso entendimento.""",
        "wisdom"
    ),
    (
        "Romanos 15:13",
        """O Deus de esperança vos encha de todo o gozo e paz na vossa fé.""",
        "hope"
    ),
    (
        "1 Coríntios 10:13",
        """Fiel é Deus, que não vos deixará tentar acima do que podeis; antes com a tentação dará também o escape.""",
        "strength"
    ),
    (
        "2 Coríntios 12:9",
        """A minha graça te basta, porque o meu poder se aperfeiçoa na fraqueza.""",
        "grace"
    ),
    (
        "Gálatas 6:9",
        """E não nos cansemos de fazer o bem, porque a seu tempo ceifaremos, se não desfalecermos.""",
        "hope"
    ),
    (
        "Efésios 3:20",
        """Ora, àquele que é poderoso para fazer tudo muito mais abundantemente além daquilo que pedimos ou pensamos.""",
        "faith"
    ),
    (
        "Efésios 6:10",
        """No demais, irmãos meus, fortalecei-vos no Senhor e na força do seu poder.""",
        "strength"
    ),
    (
        "Filipenses 1:6",
        """Tendo por certo isto mesmo, que aquele que em vós começou a boa obra a aperfeiçoará até ao dia de Jesus Cristo.""",
        "trust"
    ),
    (
        "Filipenses 2:13",
        """Porque Deus é o que opera em vós tanto o querer como o efetuar, segundo a sua boa vontade.""",
        "faith"
    ),
    (
        "Hebreus 4:16",
        """Cheguemos, pois, com confiança ao trono da graça, para alcançarmos misericórdia e acharmos graça.""",
        "grace"
    ),
    (
        "Hebreus 13:8",
        """Jesus Cristo é o mesmo ontem, e hoje, e eternamente.""",
        "truth"
    ),
    (
        "Salmo 46:10",
        """Aquietai-vos, e sabei que eu sou Deus; serei exaltado entre as nações.""",
        "peace"
    ),
    (
        "Salmo 55:22",
        """Lança o teu cuidado sobre o Senhor, e ele te susterá; nunca permitirá que o justo seja abalado.""",
        "trust"
    ),
    (
        "Deuteronômio 6:5",
        """Amarás, pois, o Senhor teu Deus de todo o teu coração, e de toda a tua alma, e de todas as tuas forças.""",
        "love"
    ),
    (
        "2 Crônicas 7:14",
        """Se o meu povo, que se chama pelo meu nome, se humilhar, e orar, e buscar a minha face, eu os ouvirei do céu e os perdoarei.""",
        "repentance"
    ),
    (
        "Habacuque 3:17-18",
        """Ainda que a figueira não floresça, nem haja fruto na vide; todavia eu me alegrarei no Senhor.""",
        "hope"
    ),
    (
        "Neemias 8:10",
        """Porque a alegria do Senhor é a vossa força.""",
        "strength"
    ),
    (
        "Salmo 34:8",
        """Provai e vede que o Senhor é bom; bem-aventurado o homem que nele confia.""",
        "trust"
    ),
    (
        "Salmo 37:5",
        """Entrega o teu caminho ao Senhor; confia nele, e ele o fará.""",
        "trust"
    ),

    # =========================================================================
    # MAIS PASSAGENS – VERSÍCULOS POPULARES
    # =========================================================================
    (
        "Salmo 23:1",
        """O Senhor é meu pastor; nada me faltará.""",
        "peace"
    ),
    (
        "Salmo 91:1",
        """Aquele que habita no esconderijo do Altíssimo, à sombra do Onipotente descansará.""",
        "protection"
    ),
    (
        "Salmo 16:11",
        """Tu me farás ver os caminhos da vida; na tua presença há plenitude de alegria.""",
        "hope"
    ),
    (
        "Salmo 27:14",
        """Espera no Senhor, anima-te, e ele fortalecerá o teu coração; espera, pois, no Senhor.""",
        "hope"
    ),
    (
        "Salmo 30:5",
        """O choro pode durar uma noite, mas a alegria vem pela manhã.""",
        "hope"
    ),
    (
        "Salmo 32:5",
        """Confessei-te o meu pecado, e a minha iniquidade não encobri; e tu perdoaste a iniquidade do meu pecado.""",
        "forgiveness"
    ),
    (
        "Salmo 51:10",
        """Cria em mim, ó Deus, um coração puro, e renova em mim um espírito reto.""",
        "repentance"
    ),
    (
        "Salmo 73:26",
        """A minha carne e o meu coração desfalecem; mas Deus é a fortaleza do meu coração e a minha porção para sempre.""",
        "trust"
    ),
    (
        "Salmo 84:11",
        """Porque o Senhor Deus é sol e escudo; o Senhor dará graça e glória; nenhum bem lhes negará aos que andam retamente.""",
        "protection"
    ),
    (
        "Salmo 90:12",
        """Ensina-nos a contar os nossos dias, de tal maneira que alcancemos corações sábios.""",
        "wisdom"
    ),
    (
        "Salmo 100:4",
        """Entrai pelas suas portas com louvor, e em seus átrios com hinos; louvai-o e bendizei o seu nome.""",
        "gratitude"
    ),
    (
        "Salmo 103:12",
        """Quanto está longe o oriente do ocidente, assim afasta de nós as nossas transgressões.""",
        "forgiveness"
    ),
    (
        "Salmo 118:24",
        """Este é o dia que fez o Senhor; regozijemo-nos e alegremo-nos nele.""",
        "gratitude"
    ),
    (
        "Salmo 119:105",
        """Lâmpada para os meus pés é a tua palavra, e luz para o meu caminho.""",
        "wisdom"
    ),
    (
        "Salmo 121:1-2",
        """Levantarei os meus olhos para os montes; de onde vem o meu socorro?
O meu socorro vem do Senhor, que fez o céu e a terra.""",
        "protection"
    ),
    (
        "Salmo 145:9",
        """O Senhor é bom para todos, e as suas misericórdias são sobre todas as suas obras.""",
        "love"
    ),
    (
        "Salmo 150:6",
        """Tudo quanto tem fôlego louve ao Senhor. Louvai ao Senhor.""",
        "praise"
    ),
    (
        "Gênesis 28:15",
        """Eis que estou contigo, e te guardarei por onde quer que fores, e te farei tornar a esta terra.""",
        "protection"
    ),
    (
        "Êxodo 14:14",
        """O Senhor pelejará por vós, e vós vos calareis.""",
        "strength"
    ),
    (
        "Números 6:24-26",
        """O Senhor te abençoe e te guarde; o Senhor faça resplandecer o seu rosto sobre ti e tenha misericórdia de ti.
O Senhor sobre ti levante o seu rosto e te dê a paz.""",
        "peace"
    ),
    (
        "Deuteronômio 31:8",
        """O Senhor é quem vai adiante de ti; ele será contigo, não te deixará nem te desamparará.""",
        "trust"
    ),
    (
        "Josué 24:15",
        """Eu e a minha casa serviremos ao Senhor.""",
        "faith"
    ),
    (
        "1 Samuel 16:7",
        """Porque o Senhor não vê como vê o homem, pois o homem vê o que está diante dos olhos, porém o Senhor olha para o coração.""",
        "wisdom"
    ),
    (
        "Mateus 5:4",
        """Bem-aventurados os que choram, porque eles serão consolados.""",
        "hope"
    ),
    (
        "Mateus 5:9",
        """Bem-aventurados os pacificadores, porque eles serão chamados filhos de Deus.""",
        "peace"
    ),
    (
        "Mateus 19:26",
        """Para Deus tudo é possível.""",
        "faith"
    ),
    (
        "Mateus 22:37",
        """Amarás o Senhor teu Deus de todo o teu coração, e de toda a tua alma, e de todo o teu entendimento.""",
        "love"
    ),
    (
        "Marcos 10:27",
        """Para Deus tudo é possível.""",
        "faith"
    ),
    (
        "Marcos 11:24",
        """Tudo o que pedirdes, orando, crede que o recebereis, e assim o tereis.""",
        "faith"
    ),
    (
        "Lucas 1:45",
        """Bem-aventurada aquela que creu, porque se cumprirá tudo o que da parte do Senhor lhe foi dito.""",
        "faith"
    ),
    (
        "Lucas 11:28",
        """Antes bem-aventurados os que ouvem a palavra de Deus e a guardam.""",
        "wisdom"
    ),
    (
        "Lucas 18:27",
        """As coisas que são impossíveis aos homens são possíveis a Deus.""",
        "faith"
    ),
    (
        "João 4:24",
        """Deus é Espírito, e importa que os que o adoram o adorem em espírito e em verdade.""",
        "truth"
    ),
    (
        "João 7:37-38",
        """Se alguém tem sede, venha a mim e beba.
Quem crê em mim, como diz a Escritura, rios de água viva correrão do seu interior.""",
        "hope"
    ),
    (
        "João 13:34",
        """Um novo mandamento vos dou: que vos ameis uns aos outros; como eu vos amei.""",
        "love"
    ),
    (
        "João 15:13",
        """Ninguém tem maior amor do que este: de dar alguém a vida pelos seus amigos.""",
        "love"
    ),
    (
        "João 17:3",
        """E a vida eterna é esta: que te conheçam a ti, o único Deus verdadeiro, e a Jesus Cristo, a quem enviaste.""",
        "truth"
    ),
    (
        "Atos 16:31",
        """Crê no Senhor Jesus Cristo e serás salvo, tu e a tua casa.""",
        "faith"
    ),
    (
        "Romanos 3:23",
        """Porque todos pecaram e destituídos estão da glória de Deus.""",
        "repentance"
    ),
    (
        "Romanos 6:23",
        """Porque o salário do pecado é a morte, mas o dom gratuito de Deus é a vida eterna, por Jesus Cristo nosso Senhor.""",
        "grace"
    ),
    (
        "Romanos 10:9",
        """Se com a tua boca confessares ao Senhor Jesus, e em teu coração creres que Deus o ressuscitou dos mortos, serás salvo.""",
        "faith"
    ),
    (
        "Romanos 10:17",
        """De sorte que a fé é pelo ouvir, e o ouvir pela palavra de Deus.""",
        "faith"
    ),
    (
        "Romanos 14:8",
        """Porque quer vivamos quer morramos, somos do Senhor.""",
        "trust"
    ),
    (
        "1 Coríntios 15:57",
        """Graças a Deus, que nos dá a vitória por nosso Senhor Jesus Cristo.""",
        "strength"
    ),
    (
        "2 Coríntios 9:8",
        """E Deus é poderoso para fazer abundar em vós toda a graça.""",
        "grace"
    ),
    (
        "Gálatas 2:20",
        """Já não sou eu quem vive, mas Cristo vive em mim; e a vida que agora vivo na carne, vivo-a na fé do Filho de Deus.""",
        "faith"
    ),
    (
        "Efésios 2:10",
        """Porque somos feitura sua, criados em Cristo Jesus para as boas obras.""",
        "hope"
    ),
    (
        "Efésios 4:2",
        """Com toda a humildade e mansidão, com longanimidade, suportando-vos uns aos outros em amor.""",
        "love"
    ),
    (
        "Filipenses 2:3",
        """Nada façais por contenda ou por vanglória, mas por humildade; cada um considere os outros superiores a si mesmo.""",
        "unity"
    ),
    (
        "Filipenses 3:14",
        """Prossigo para o alvo, ao prêmio da soberana vocação de Deus em Cristo Jesus.""",
        "strength"
    ),
    (
        "Filipenses 4:19",
        """O meu Deus, segundo as suas riquezas, suprirá todas as vossas necessidades.""",
        "trust"
    ),
    (
        "Colossenses 1:17",
        """E ele é antes de todas as coisas, e nele tudo subsiste.""",
        "truth"
    ),
    (
        "Colossenses 3:15",
        """E a paz de Deus, para a qual também fostes chamados em um corpo, domine em vossos corações.""",
        "peace"
    ),
    (
        "1 Tessalonicenses 5:24",
        """Fiel é aquele que vos chama, o qual também o fará.""",
        "trust"
    ),
    (
        "2 Tessalonicenses 3:3",
        """Mas o Senhor é fiel, que vos confirmará e guardará do maligno.""",
        "protection"
    ),
    (
        "1 Timóteo 4:12",
        """Ninguém despreze a tua mocidade; mas sê o exemplo dos fiéis, na palavra, no trato, no amor, no espírito, na fé, na pureza.""",
        "wisdom"
    ),
    (
        "2 Timóteo 2:13",
        """Se formos infiéis, ele permanece fiel; não pode negar-se a si mesmo.""",
        "trust"
    ),
    (
        "Hebreus 10:23",
        """Retenhamos firmes a confissão da nossa esperança, porque fiel é o que prometeu.""",
        "hope"
    ),
    (
        "Hebreus 13:5",
        """Porque ele disse: De maneira alguma te deixarei, nunca jamais te abandonarei.""",
        "trust"
    ),
    (
        "Tiago 4:6",
        """Deus resiste aos soberbos, mas dá graça aos humildes.""",
        "grace"
    ),
    (
        "1 Pedro 2:9",
        """Mas vós sois a geração eleita, o sacerdócio real, a nação santa, o povo adquirido.""",
        "hope"
    ),
    (
        "1 João 1:9",
        """Se confessarmos os nossos pecados, ele é fiel e justo para nos perdoar os pecados e nos purificar de toda a injustiça.""",
        "forgiveness"
    ),
    (
        "Apocalipse 21:4",
        """E Deus limpará de seus olhos toda a lágrima; e não haverá mais morte, nem pranto, nem clamor, nem dor.""",
        "hope"
    ),
    (
        "Provérbios 1:7",
        """O temor do Senhor é o princípio do conhecimento.""",
        "wisdom"
    ),
    (
        "Provérbios 9:10",
        """O temor do Senhor é o princípio da sabedoria, e o conhecimento do Santo é o entendimento.""",
        "wisdom"
    ),
    (
        "Provérbios 10:12",
        """O ódio excita contendas, mas o amor cobre todas as transgressões.""",
        "love"
    ),
    (
        "Provérbios 14:12",
        """Há caminho que ao homem parece direito, mas o fim dele são os caminhos da morte.""",
        "wisdom"
    ),
    (
        "Provérbios 17:17",
        """Em todo o tempo ama o amigo, e na angústia nasce o irmão.""",
        "love"
    ),
    (
        "Provérbios 24:16",
        """Porque sete vezes cai o justo, e se levanta; mas os ímpios caem no mal.""",
        "strength"
    ),
    (
        "Provérbios 28:26",
        """O que confia no seu próprio coração é insensato; mas o que anda sabiamente será livre.""",
        "wisdom"
    ),
    (
        "Isaías 9:6",
        """Porque um menino nos nasceu, um filho se nos deu; e o governo estará sobre os seus ombros; e o seu nome será: Maravilhoso, Conselheiro, Deus Forte, Pai da Eternidade, Príncipe da Paz.""",
        "hope"
    ),
    (
        "Isaías 12:2",
        """Eis que Deus é a minha salvação; eu confiarei e não temerei, porque o Senhor Jeová é a minha força e o meu cântico.""",
        "strength"
    ),
    (
        "Isaías 30:21",
        """E os teus ouvidos ouvirão a palavra que está por detrás de ti, dizendo: Este é o caminho, andai nele.""",
        "wisdom"
    ),
    (
        "Isaías 54:10",
        """Porque os montes se desviarão e os outeiros tremerão, mas a minha benignidade não se desviará de ti.""",
        "love"
    ),
    (
        "Jeremias 33:3",
        """Clama a mim, e responder-te-ei, e anunciar-te-ei coisas grandes e firmes que não sabes.""",
        "faith"
    ),
    (
        "Lamentações 3:25",
        """Bom é o Senhor para os que esperam nele, para a alma que o busca.""",
        "hope"
    ),
    (
        "Daniel 2:20",
        """Bendito seja o nome de Deus para todo o sempre, porque dele é a sabedoria e a força.""",
        "wisdom"
    ),
    (
        "Zacarias 4:6",
        """Não por força nem por violência, mas pelo meu Espírito, diz o Senhor dos Exércitos.""",
        "strength"
    ),
    (
        "Malaquias 3:10",
        """Trazei todos os dízimos à casa do tesouro, e provai-me nisto, diz o Senhor dos Exércitos, se eu não vos abrir as janelas do céu.""",
        "trust"
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
    (
        "Leitura – Isaías 43:1-3",
        """Mas agora, assim diz o Senhor que te criou, ó Jacó, e que te formou, ó Israel:
Não temas, porque eu te remi; chamei-te pelo teu nome, tu és meu.
Quando passares pelas águas, estarei contigo; e quando pelos rios, eles não te submergirão.
Porque eu sou o Senhor teu Deus, o Santo de Israel, o teu Salvador.""",
        "protection"
    ),
    (
        "Leitura – Romanos 8:31-35",
        """Que diremos, pois, a estas coisas? Se Deus é por nós, quem será contra nós?
Aquele que nem mesmo a seu próprio Filho poupou, antes o entregou por todos nós.
Quem nos separará do amor de Cristo? A tribulação, ou a angústia, ou a perseguição?
Em todas estas coisas somos mais do que vencedores, por aquele que nos amou.""",
        "strength"
    ),
    (
        "Leitura – Salmo 27:1-3",
        """O Senhor é a minha luz e a minha salvação; a quem temerei?
O Senhor é a força da minha vida; de quem me recearei?
Ainda que um exército me cercasse, o meu coração não temeria.
Se eu confiar no Senhor, não temerei.""",
        "protection"
    ),
    (
        "Leitura – Salmo 139:13-16",
        """Pois possuíste o meu interior; entreteceste-me no ventre de minha mãe.
Eu te louvarei, porque de um modo assombroso e maravilhoso fui feito.
Os teus olhos viram o meu corpo ainda informe; todos os meus dias estavam escritos no teu livro.""",
        "wisdom"
    ),
    (
        "Leitura – 2 Coríntios 4:16-18",
        """Por isso não desfalecemos; mas, ainda que o nosso homem exterior se corrompa, o interior se renova de dia em dia.
Porque a nossa leve e momentânea tribulação produz para nós um peso eterno de glória.
Enquanto não olhamos para as coisas que se veem, mas para as que se não veem.""",
        "hope"
    ),
    (
        "Leitura – Gálatas 6:9-10",
        """E não nos cansemos de fazer o bem, porque a seu tempo ceifaremos, se não desfalecermos.
Então, enquanto temos tempo, façamos o bem a todos, mas principalmente aos da família da fé.""",
        "hope"
    ),
    (
        "Leitura – Hebreus 12:1-2",
        """Pondo de parte todo o embaraço e o pecado que tão de perto nos rodeia, corramos com paciência a carreira que nos está proposta.
Olhando para Jesus, autor e consumador da fé, que pelo gozo que lhe estava proposto, suportou a cruz.""",
        "faith"
    ),
    (
        "Leitura – Tiago 4:7-8",
        """Sujeitai-vos, pois, a Deus, resisti ao diabo, e ele fugirá de vós.
Chegai-vos a Deus, e ele se chegará a vós. Limpai as mãos, pecadores; e vós de duplo ânimo, purificai os corações.""",
        "wisdom"
    ),
    (
        "Leitura – Provérbios 3:11-12",
        """Filho meu, não rejeites a correção do Senhor, nem te enojes da sua repreensão.
Porque o Senhor repreende a quem ama, assim como o pai ao filho a quem quer bem.""",
        "wisdom"
    ),
    (
        "Leitura – Mateus 6:25-27",
        """Por isso vos digo: Não andeis ansiosos pela vossa vida, quanto ao que haveis de comer ou de beber.
Olhai para as aves do céu: não semeiam, nem ceifam, nem ajuntam em celeiros; e vosso Pai celestial as alimenta.
E qual de vós, por mais que se esforce, pode acrescentar um côvado à sua estatura?""",
        "peace"
    ),
    (
        "Leitura – Salmo 23:1-4",
        """O Senhor é meu pastor; nada me faltará.
Ele me faz repousar em pastos verdejantes; leva-me às águas tranquilas.
Refrigera-me a alma; guia-me pelas veredas da justiça por amor do seu nome.
Ainda que eu ande pelo vale da sombra da morte, não temerei mal algum, porque tu estás comigo.""",
        "peace"
    ),
    (
        "Leitura – Salmo 91:1-4",
        """Aquele que habita no esconderijo do Altíssimo, à sombra do Onipotente descansará.
Direi do Senhor: Ele é o meu refúgio e a minha fortaleza, o meu Deus, em quem confio.
Porque ele te livrará do laço do passarinheiro, e da peste perniciosa.
Cobrir-te-á com as suas penas, e debaixo das suas asas te confiarás.""",
        "protection"
    ),
    (
        "Leitura – Salmo 103:1-5",
        """Bendize, ó minha alma, ao Senhor, e tudo o que há em mim bendiga o seu santo nome.
Bendize, ó minha alma, ao Senhor, e não te esqueças de nenhum de seus benefícios.
É ele quem perdoa todas as tuas iniquidades, e sara todas as tuas enfermidades.
É ele quem redime a tua vida da cova, e te coroa de benignidade e de misericórdia.""",
        "gratitude"
    ),
    (
        "Leitura – Salmo 46:1-3",
        """Deus é o nosso refúgio e fortaleza, socorro bem presente na angústia.
Portanto não temeremos, ainda que a terra se mude, e ainda que os montes se transportem para o meio dos mares.
Ainda que as águas rujam e se perturbem, ainda que os montes se abalem pela sua braveza.""",
        "protection"
    ),
    (
        "Leitura – Salmo 51:10-12",
        """Cria em mim, ó Deus, um coração puro, e renova em mim um espírito reto.
Não me lances fora da tua presença, e não retires de mim o teu Espírito Santo.
Restitui-me a alegria da tua salvação, e sustém-me com um espírito voluntário.""",
        "repentance"
    ),
    (
        "Leitura – Isaías 53:4-5",
        """Certamente ele tomou sobre si as nossas enfermidades, e as nossas dores levou sobre si.
Mas ele foi traspassado pelas nossas transgressões, e moído pelas nossas iniquidades.
O castigo que nos traz a paz estava sobre ele, e pelas suas pisaduras fomos sarados.""",
        "hope"
    ),
    (
        "Leitura – Isaías 12:2-3",
        """Eis que Deus é a minha salvação; eu confiarei e não temerei.
Cantai ao Senhor, porque fez coisas grandiosas; saibam-no todos os moradores da terra.
E com alegria tirareis águas das fontes da salvação.""",
        "strength"
    ),
    (
        "Leitura – Jeremias 29:11-13",
        """Porque eu bem sei os pensamentos que tenho a vosso respeito, diz o Senhor; pensamentos de paz, e não de mal.
Então me invocareis, e ireis, e orareis a mim, e eu vos ouvirei.
E buscar-me-eis e me achareis, quando me buscardes de todo o vosso coração.""",
        "hope"
    ),
    (
        "Leitura – Josué 1:8-9",
        """Não se aparte da tua boca o livro desta lei; antes medita nele dia e noite.
Não to mandei eu? Esforça-te e tem bom ânimo; não temas nem te espantes.
Porque o Senhor teu Deus é contigo por onde quer que andares.""",
        "strength"
    ),
    (
        "Leitura – Provérbios 3:5-8",
        """Confia no Senhor de todo o teu coração, e não te estribes no teu próprio entendimento.
Reconhece-o em todos os teus caminhos, e ele endireitará as tuas veredas.
Não sejas sábio a teus próprios olhos; teme ao Senhor e aparta-te do mal.
Será isto saúde para o teu âmago, e medula para os teus ossos.""",
        "wisdom"
    ),
    (
        "Leitura – Mateus 5:6-8",
        """Bem-aventurados os que têm fome e sede de justiça, porque eles serão fartos.
Bem-aventurados os misericordiosos, porque eles alcançarão misericórdia.
Bem-aventurados os limpos de coração, porque eles verão a Deus.""",
        "peace"
    ),
    (
        "Leitura – João 15:1-5",
        """Eu sou a videira verdadeira, e meu Pai é o lavrador.
Todo o ramo que em mim não dá fruto, ele o corta; e limpa todo aquele que dá fruto.
Permanecei em mim, e eu em vós. Como o ramo não pode dar fruto de si mesmo, se não permanecer na videira.
Eu sou a videira, vós sois os ramos; quem permanece em mim, e eu nele, esse dá muito fruto.""",
        "faith"
    ),
    (
        "Leitura – Romanos 12:1-2",
        """Rogo-vos, pois, irmãos, pelas misericórdias de Deus, que apresenteis os vossos corpos em sacrifício vivo, santo e agradável a Deus.
E não vos conformeis com este mundo, mas transformai-vos pela renovação do vosso entendimento.
Para que experimenteis qual seja a boa, agradável e perfeita vontade de Deus.""",
        "wisdom"
    ),
    (
        "Leitura – 1 Coríntios 13:4-7",
        """O amor é paciente, o amor é benigno; o amor não inveja; o amor não trata com leviandade, nem se ensoberbece.
Não se porta com indecência, não busca os seus interesses, não se irrita, não suspeita mal.
Não se regozija com a injustiça, mas regozija-se com a verdade.
Tudo sofre, tudo crê, tudo espera, tudo suporta.""",
        "love"
    ),
    (
        "Leitura – Efésios 6:10-11",
        """No demais, irmãos meus, fortalecei-vos no Senhor e na força do seu poder.
Revesti-vos de toda a armadura de Deus, para que possais estar firmes contra as astutas ciladas do diabo.""",
        "strength"
    ),
    (
        "Leitura – Colossenses 3:12-14",
        """Revesti-vos, pois, como eleitos de Deus, santos e amados, de entranhas de misericórdia, de benignidade, humildade, mansidão, longanimidade.
Suportando-vos uns aos outros, e perdoando-vos uns aos outros, se alguém tiver queixa contra outro.
Acima de tudo, porém, revesti-vos de amor, que é o vínculo da perfeição.""",
        "unity"
    ),
    (
        "Leitura – 1 Pedro 2:9-10",
        """Mas vós sois a geração eleita, o sacerdócio real, a nação santa, o povo adquirido.
Que em tempos passados não era povo, mas agora é povo de Deus; que não tinha alcançado misericórdia, mas agora tem alcançado misericórdia.""",
        "hope"
    ),
    (
        "Leitura – Apocalipse 21:3-4",
        """E ouvi uma grande voz do céu, que dizia: Eis o tabernáculo de Deus com os homens.
E Deus limpará de seus olhos toda a lágrima; e não haverá mais morte, nem pranto, nem clamor, nem dor.
Porque já as primeiras coisas são passadas.""",
        "hope"
    ),
    (
        "Leitura – Lucas 15:20-24",
        """E, levantando-se, foi para seu pai. Estando ele ainda longe, viu-o seu pai, e teve compaixão.
E, correndo, lançou-se-lhe ao pescoço, e o beijou.
Mas o pai disse aos seus servos: Trazei a melhor roupa, e vesti-o; e ponde um anel na sua mão, e alparcas nos pés.
Porque este meu filho estava morto, e reviveu; tinha-se perdido, e achou-se.""",
        "forgiveness"
    ),
    (
        "Leitura – Salmo 121:1-4",
        """Levantarei os meus olhos para os montes; de onde vem o meu socorro?
O meu socorro vem do Senhor, que fez o céu e a terra.
Não deixará vacilar o teu pé; aquele que te guarda não dormitará.
Eis que não dormitará nem dormirá aquele que guarda a Israel.""",
        "protection"
    ),
    (
        "Leitura – Salmo 34:18-19",
        """Perto está o Senhor dos que têm o coração quebrantado, e salva os contritos de espírito.
Muitas são as aflições do justo, mas o Senhor de todas o livra.""",
        "hope"
    ),
    (
        "Leitura – Salmo 37:3-5",
        """Confia no Senhor e faze o bem; habitarás na terra, e verdadeiramente serás alimentado.
Deleita-te também no Senhor, e te concederá os desejos do teu coração.
Entrega o teu caminho ao Senhor; confia nele, e ele o fará.""",
        "trust"
    ),
    (
        "Leitura – Mateus 7:24-25",
        """Todo aquele, pois, que escuta estas minhas palavras e as pratica, assemelhá-lo-ei ao homem prudente.
Que edificou a sua casa sobre a rocha; e desceu a chuva, e correram rios, e assopraram ventos.
E não caiu, porque estava edificada sobre a rocha.""",
        "wisdom"
    ),
    (
        "Leitura – Marcos 4:39-40",
        """E, despertando, repreendeu o vento, e disse ao mar: Cala-te, aquieta-te.
E o vento se aquietou, e houve grande bonança.
E disse-lhes: Por que sois tão tímidos? Como não tendes fé?""",
        "faith"
    ),
    (
        "Leitura – Atos 2:38",
        """Arrependei-vos, e cada um de vós seja batizado em nome de Jesus Cristo para remissão dos pecados.
E recebereis o dom do Espírito Santo.""",
        "repentance"
    ),
    (
        "Leitura – 2 Timóteo 1:7-8",
        """Porque Deus não nos deu o espírito de temor, mas de poder, de amor e de moderação.
Portanto não te envergonhes do testemunho de nosso Senhor, nem de mim, que sou prisioneiro seu.""",
        "strength"
    ),
    (
        "Leitura – Hebreus 13:5-6",
        """Porque ele disse: De maneira alguma te deixarei, nunca jamais te abandonarei.
De sorte que com confiança digamos: O Senhor é o meu ajudador, e não temerei o que me possa fazer o homem.""",
        "trust"
    ),
    (
        "Leitura – Tiago 1:2-4",
        """Meus irmãos, tende por motivo de grande gozo o passardes por várias provações.
Sabendo que a prova da vossa fé opera a paciência.
Tenha, porém, a paciência a sua obra perfeita, para que sejais perfeitos e completos, sem faltar em coisa alguma.""",
        "strength"
    ),
    (
        "Leitura – 1 João 3:1-2",
        """Vede quão grande amor nos tem concedido o Pai, que fôssemos chamados filhos de Deus.
Por isso o mundo não nos conhece, porque não o conhece a ele.
Amados, agora somos filhos de Deus, e ainda não é manifesto o que havemos de ser.
Mas sabemos que, quando ele se manifestar, seremos semelhantes a ele.""",
        "love"
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
    "repentance": "sacred",
    "praise": "dawn",
    "gratitude": "heavenly",
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
