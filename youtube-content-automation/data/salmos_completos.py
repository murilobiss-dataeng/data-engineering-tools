"""
Base de Salmos para o canal Salmo do Dia.

O livro de Salmos na Bíblia é composto por 150 salmos (cânticos/poemas),
localizados no Antigo Testamento, organizados em cinco partes/coleções.
Este módulo contém o texto integral dos salmos mais utilizados;
os demais podem ser referenciados por número (1-150).
"""

# Total de salmos no livro bíblico (Antigo Testamento)
TOTAL_SALMOS = 150

# Formato: (nome, texto_completo, tema/mood)
SALMOS_COMPLETOS = [
    # =========================================================================
    # SALMOS DE PAZ E CONFIANÇA
    # =========================================================================
    (
        "Salmo 23",
        """O Senhor é meu pastor; nada me faltará.
Ele me faz repousar em pastos verdejantes.
Leva-me às águas tranquilas.
Refrigera-me a alma.
Guia-me pelas veredas da justiça por amor do seu nome.
Ainda que eu ande pelo vale da sombra da morte, não temerei mal algum, porque tu estás comigo.
A tua vara e o teu cajado me consolam.
Preparas uma mesa perante mim na presença dos meus inimigos.
Unges a minha cabeça com óleo; o meu cálice transborda.
Certamente que a bondade e a misericórdia me seguirão todos os dias da minha vida.
E habitarei na casa do Senhor por longos dias.""",
        "peace"
    ),
    (
        "Salmo 121",
        """Levantarei os meus olhos para os montes, de onde vem o meu socorro.
O meu socorro vem do Senhor, que fez o céu e a terra.
Não deixará vacilar o teu pé; aquele que te guarda não dormitará.
Eis que não dormitará nem dormirá aquele que guarda a Israel.
O Senhor é quem te guarda; o Senhor é a tua sombra à tua mão direita.
O sol não te molestará de dia nem a lua de noite.
O Senhor te guardará de todo o mal; guardará a tua alma.
O Senhor guardará a tua entrada e a tua saída, desde agora e para sempre.""",
        "protection"
    ),
    (
        "Salmo 131",
        """Senhor, o meu coração não se elevou nem os meus olhos se levantaram.
Não me exercito em grandes matérias, nem em coisas muito elevadas para mim.
Certamente que me tenho portado e sossegado, como uma criança desmamada de sua mãe.
A minha alma está como uma criança desmamada.
Espere Israel no Senhor, desde agora e para sempre.""",
        "peace"
    ),

    # =========================================================================
    # SALMOS DE PROTEÇÃO E REFÚGIO
    # =========================================================================
    (
        "Salmo 91",
        """Aquele que habita no esconderijo do Altíssimo, à sombra do Onipotente descansará.
Direi do Senhor: Ele é o meu refúgio e a minha fortaleza, o meu Deus, em quem confio.
Porque ele te livrará do laço do passarinheiro, e da peste perniciosa.
Cobrir-te-á com as suas penas, e debaixo das suas asas te confiarás.
A sua verdade será o teu escudo e broquel.
Não temerás espanto noturno, nem seta que voe de dia.
Nem peste que ande na escuridão, nem mortandade que assole ao meio-dia.
Mil cairão ao teu lado, e dez mil à tua direita; mas não chegará a ti.
Somente com os teus olhos contemplarás, e verás a recompensa dos ímpios.
Porque tu, ó Senhor, és o meu refúgio. No Altíssimo fizeste a tua habitação.
Nenhum mal te sucederá, nem praga alguma chegará à tua tenda.
Porque aos seus anjos dará ordem a teu respeito, para te guardarem em todos os teus caminhos.
Eles te sustentarão nas suas mãos, para que não tropeces com o teu pé em pedra.
Pisarás o leão e a cobra; calcarás aos pés o filho do leão e a serpente.
Porquanto tão encarecidamente me amou, eu o livrarei.
Pô-lo-ei em retiro alto, porque conheceu o meu nome.
Ele me invocará, e eu lhe responderei; estarei com ele na angústia.
Livrá-lo-ei e o glorificarei. Com longura de dias o fartarei, e lhe mostrarei a minha salvação.""",
        "protection"
    ),
    (
        "Salmo 46",
        """Deus é o nosso refúgio e fortaleza, socorro bem presente na angústia.
Pelo que não temeremos, ainda que a terra se mude.
E ainda que os montes se transportem para o meio dos mares.
Ainda que as águas rujam e se perturbem, ainda que os montes se abalem pela sua braveza.
Há um rio cujas correntes alegram a cidade de Deus, o santuário das moradas do Altíssimo.
Deus está no meio dela; não será abalada. Deus a ajudará ao romper da manhã.
Os gentios se embraveceram; os reinos se moveram.
Ele fez ouvir a sua voz; a terra se derreteu.
O Senhor dos Exércitos está conosco; o Deus de Jacó é o nosso refúgio.
Vinde, contemplai as obras do Senhor.
Aquietai-vos e sabei que eu sou Deus.
Serei exaltado entre os gentios; serei exaltado sobre a terra.
O Senhor dos Exércitos está conosco; o Deus de Jacó é o nosso refúgio.""",
        "protection"
    ),
    (
        "Salmo 27",
        """O Senhor é a minha luz e a minha salvação; a quem temerei?
O Senhor é a fortaleza da minha vida; de quem me recearei?
Quando os malvados avançaram contra mim para comerem as minhas carnes, tropeçaram e caíram.
Ainda que um exército se acampe contra mim, o meu coração não temerá.
Ainda que a guerra se levante contra mim, nisso confiarei.
Uma coisa pedi ao Senhor, e a buscarei: que possa morar na casa do Senhor todos os dias da minha vida.
Para contemplar a formosura do Senhor e meditar no seu templo.
Porque no dia da adversidade me esconderá no seu pavilhão.
No segredo do seu tabernáculo me esconderá; sobre uma rocha me porá em alto.
E agora será exaltada a minha cabeça acima dos meus inimigos.
Oferecerei no seu tabernáculo sacrifícios de júbilo; cantarei e salmodiarei ao Senhor.
Ouve, ó Senhor, a minha voz com que clamo; tem também piedade de mim, e responde-me.
Quando tu disseste: Buscai o meu rosto; o meu coração te disse a ti: O teu rosto, Senhor, buscarei.
Não escondas de mim a tua face.
Espera no Senhor, anima-te, e ele fortalecerá o teu coração; espera, pois, no Senhor.""",
        "hope"
    ),

    # =========================================================================
    # SALMOS DE LOUVOR E GRATIDÃO
    # =========================================================================
    (
        "Salmo 34",
        """Bendirei ao Senhor em todo o tempo; o seu louvor estará continuamente na minha boca.
A minha alma se gloriará no Senhor; os mansos ouvirão e se alegrarão.
Engrandecei ao Senhor comigo, e juntos exaltemos o seu nome.
Busquei ao Senhor, e ele me respondeu; livrou-me de todos os meus temores.
Os que olham para ele serão iluminados; e os seus rostos não serão confundidos.
Este pobre clamou, e o Senhor o ouviu; salvou-o de todas as suas angústias.
O anjo do Senhor acampa-se ao redor dos que o temem, e os livra.
Provai e vede que o Senhor é bom; bem-aventurado o homem que nele confia.
Temei ao Senhor, vós os seus santos, pois nada falta aos que o temem.
Os leõezinhos necessitam e sofrem fome, mas àqueles que buscam ao Senhor bem nenhum faltará.
Vinde, meninos, ouvi-me; eu vos ensinarei o temor do Senhor.
Guarda a tua língua do mal, e os teus lábios de falarem o engano.
Aparta-te do mal e faze o bem; procura a paz e segue-a.
Os olhos do Senhor estão sobre os justos, e os seus ouvidos atentos ao seu clamor.
O Senhor está perto dos que têm o coração quebrantado, e salva os contritos de espírito.
Muitas são as aflições do justo, mas o Senhor o livra de todas.""",
        "praise"
    ),
    (
        "Salmo 103",
        """Bendize, ó minha alma, ao Senhor, e tudo o que há em mim bendiga o seu santo nome.
Bendize, ó minha alma, ao Senhor, e não te esqueças de nenhum dos seus benefícios.
Ele é quem perdoa todas as tuas iniquidades, quem sara todas as tuas enfermidades.
Quem redime a tua vida da perdição, quem te coroa de benignidade e de misericórdia.
Quem farta a tua boca de coisas boas, de modo que a tua mocidade se renova como a da águia.
O Senhor faz justiça e juízo a todos os oprimidos.
Fez conhecidos os seus caminhos a Moisés, e os seus feitos aos filhos de Israel.
Misericordioso e piedoso é o Senhor; longânimo e grande em benignidade.
Não repreenderá perpetuamente, nem conservará para sempre a sua ira.
Não nos tratou segundo os nossos pecados, nem nos retribuiu segundo as nossas iniquidades.
Pois assim como o céu está elevado acima da terra, assim é grande a sua misericórdia para com os que o temem.
Assim como está longe o oriente do ocidente, assim afasta de nós as nossas transgressões.
Como um pai se compadece de seus filhos, assim o Senhor se compadece daqueles que o temem.
Pois ele conhece a nossa estrutura; lembra-se de que somos pó.
Bendizei ao Senhor, todas as suas obras, em todos os lugares do seu domínio.
Bendize, ó minha alma, ao Senhor.""",
        "gratitude"
    ),
    (
        "Salmo 100",
        """Celebrai com júbilo ao Senhor, todas as terras.
Servi ao Senhor com alegria; apresentai-vos a ele com cântico.
Sabei que o Senhor é Deus; foi ele que nos fez, e não nós a nós mesmos.
Somos povo seu e ovelhas do seu pasto.
Entrai pelas portas dele com gratidão, e em seus átrios com louvor.
Rendei-lhe graças e bendizei o seu nome.
Porque o Senhor é bom, e a sua misericórdia dura para sempre.
E a sua fidelidade de geração em geração.""",
        "praise"
    ),
    (
        "Salmo 150",
        """Louvai ao Senhor!
Louvai a Deus no seu santuário; louvai-o no firmamento do seu poder.
Louvai-o pelos seus atos poderosos; louvai-o conforme a excelência da sua grandeza.
Louvai-o com o som de trombeta; louvai-o com o saltério e a harpa.
Louvai-o com o tamborim e a flauta; louvai-o com instrumentos de cordas e com órgãos.
Louvai-o com címbalos sonoros; louvai-o com címbalos retumbantes.
Tudo quanto tem fôlego louve ao Senhor.
Louvai ao Senhor!""",
        "praise"
    ),

    # =========================================================================
    # SALMOS DE ESPERANÇA E CONFORTO
    # =========================================================================
    (
        "Salmo 42",
        """Como o cervo brama pelas correntes das águas, assim suspira a minha alma por ti, ó Deus!
A minha alma tem sede de Deus, do Deus vivo.
Quando entrarei e me apresentarei ante a face de Deus?
As minhas lágrimas servem-me de mantimento de dia e de noite.
Enquanto me dizem constantemente: Onde está o teu Deus?
Quando me lembro disto, dentro de mim derramo a minha alma.
Por que estás abatida, ó minha alma, e por que te perturbas em mim?
Espera em Deus, pois ainda o louvarei, pela salvação da sua presença.
De dia o Senhor mandará a sua misericórdia, e de noite a sua canção estará comigo.
Por que estás abatida, ó minha alma? Por que te perturbas em mim?
Espera em Deus, pois ainda o louvarei. Ele é a salvação da minha face e o meu Deus.""",
        "hope"
    ),
    (
        "Salmo 62",
        """Só em Deus, ó minha alma, espera silenciosamente; dele vem a minha salvação.
Só ele é a minha rocha e a minha salvação; é a minha defesa alta; não serei muito abalado.
Confiai nele, ó povo, em todos os tempos; derramai perante ele o vosso coração.
Deus é o nosso refúgio.
Uma vez falou Deus, duas vezes o ouvi: que o poder pertence a Deus.
A ti também, Senhor, pertence a misericórdia; pois retribuirás a cada um segundo a sua obra.""",
        "trust"
    ),
    (
        "Salmo 37",
        """Não te indignes por causa dos malfeitores, nem tenhas inveja dos que praticam a iniquidade.
Porque cedo serão ceifados como a erva, e murcharão como a verdura.
Confia no Senhor e faze o bem; habitarás na terra, e verdadeiramente serás alimentado.
Deleita-te também no Senhor, e te concederá os desejos do teu coração.
Entrega o teu caminho ao Senhor; confia nele, e ele tudo fará.
E ele fará sobressair a tua justiça como a luz, e o teu juízo como o meio-dia.
Descansa no Senhor e espera nele; não te indignes por causa daquele que prospera em seu caminho.
Deixa a ira e abandona o furor; não te indignes de forma alguma para fazer o mal.
Porque os malfeitores serão desarraigados; mas aqueles que esperam no Senhor herdarão a terra.
Os passos de um homem bom são confirmados pelo Senhor, e ele se deleita no seu caminho.
Ainda que caia, não ficará prostrado, pois o Senhor o sustém com a sua mão.
Fui moço, e agora sou velho; mas nunca vi desamparado o justo, nem a sua descendência a mendigar o pão.
Aparta-te do mal e faze o bem, e terás morada para sempre.
Espera no Senhor, e guarda o seu caminho, e te exaltará para herdares a terra.""",
        "trust"
    ),

    # =========================================================================
    # SALMOS DE ARREPENDIMENTO E PERDÃO
    # =========================================================================
    (
        "Salmo 51",
        """Tem misericórdia de mim, ó Deus, segundo a tua benignidade.
Segundo a multidão das tuas misericórdias, apaga as minhas transgressões.
Lava-me completamente da minha iniquidade, e purifica-me do meu pecado.
Porque eu conheço as minhas transgressões, e o meu pecado está sempre diante de mim.
Contra ti, contra ti somente pequei, e fiz o que é mal à tua vista.
Eis que em iniquidade fui formado, e em pecado me concebeu minha mãe.
Eis que amas a verdade no íntimo, e no oculto me fazes conhecer a sabedoria.
Purifica-me com hissopo, e ficarei puro; lava-me, e ficarei mais branco do que a neve.
Faze-me ouvir júbilo e alegria, para que gozem os ossos que esmagaste.
Esconde a tua face dos meus pecados, e apaga todas as minhas iniquidades.
Cria em mim, ó Deus, um coração puro, e renova em mim um espírito reto.
Não me lances fora da tua presença, e não retires de mim o teu Espírito Santo.
Torna a dar-me a alegria da tua salvação, e sustém-me com um espírito voluntário.
Então ensinarei aos transgressores os teus caminhos, e os pecadores a ti se converterão.
Os sacrifícios para Deus são o espírito quebrantado.
A um coração quebrantado e contrito não desprezarás, ó Deus.""",
        "repentance"
    ),
    (
        "Salmo 32",
        """Bem-aventurado aquele cuja transgressão é perdoada, e cujo pecado é coberto.
Bem-aventurado o homem a quem o Senhor não imputa maldade, e em cujo espírito não há engano.
Quando eu guardei silêncio, envelheceram os meus ossos pelo meu bramido em todo o dia.
Porque de dia e de noite a tua mão pesava sobre mim.
O meu humor tornou-se em secura de estio.
Confessei-te o meu pecado, e a minha maldade não encobri.
Dizia eu: Confessarei ao Senhor as minhas transgressões; e tu perdoaste a maldade do meu pecado.
Por isso todo aquele que é santo orará a ti, a tempo de te poder achar.
Tu és o meu refúgio; tu me preservas da angústia; tu me cinges de alegres cantos de livramento.
Instruir-te-ei e ensinar-te-ei o caminho que deves seguir; guiar-te-ei com os meus olhos.
Alegrai-vos no Senhor, e regozijai-vos, vós os justos.
E cantai alegremente, todos vós que sois retos de coração.""",
        "forgiveness"
    ),
    (
        "Salmo 130",
        """Das profundezas a ti clamo, ó Senhor.
Senhor, escuta a minha voz; sejam os teus ouvidos atentos à voz das minhas súplicas.
Se tu, Senhor, observares as iniquidades, Senhor, quem subsistirá?
Mas contigo está o perdão, para que sejas temido.
Aguardo ao Senhor; a minha alma o aguarda, e espero na sua palavra.
A minha alma anseia pelo Senhor, mais do que os guardas pela manhã.
Espere Israel no Senhor, porque no Senhor há misericórdia, e nele há abundante redenção.
E ele remirá a Israel de todas as suas iniquidades.""",
        "repentance"
    ),

    # =========================================================================
    # SALMOS DE SABEDORIA
    # =========================================================================
    (
        "Salmo 1",
        """Bem-aventurado o homem que não anda segundo o conselho dos ímpios.
Nem se detém no caminho dos pecadores, nem se assenta na roda dos escarnecedores.
Antes tem o seu prazer na lei do Senhor, e na sua lei medita de dia e de noite.
Pois será como a árvore plantada junto a ribeiros de águas, a qual dá o seu fruto no seu tempo.
As suas folhas não cairão, e tudo quanto fizer prosperará.
Não são assim os ímpios; mas são como a moinha que o vento espalha.
Por isso os ímpios não subsistirão no juízo, nem os pecadores na congregação dos justos.
Porque o Senhor conhece o caminho dos justos; porém o caminho dos ímpios perecerá.""",
        "wisdom"
    ),
    (
        "Salmo 19",
        """Os céus declaram a glória de Deus e o firmamento anuncia a obra das suas mãos.
Um dia faz declaração a outro dia, e uma noite mostra sabedoria a outra noite.
Não há linguagem nem fala onde não se ouça a sua voz.
A sua linha se estende por toda a terra, e as suas palavras até ao fim do mundo.
A lei do Senhor é perfeita, e refrigera a alma.
O testemunho do Senhor é fiel, e dá sabedoria aos simples.
Os preceitos do Senhor são retos e alegram o coração.
O mandamento do Senhor é puro, e ilumina os olhos.
O temor do Senhor é limpo, e permanece eternamente.
Os juízos do Senhor são verdadeiros e justos juntamente.
Mais desejáveis são do que o ouro, sim, do que muito ouro fino.
E mais doces do que o mel e o licor dos favos.
Também por eles é admoestado o teu servo; e em os guardar há grande recompensa.
Sejam agradáveis as palavras da minha boca e a meditação do meu coração perante a tua face, ó Senhor, Rocha minha e Redentor meu.""",
        "wisdom"
    ),
    (
        "Salmo 139",
        """Senhor, tu me sondaste, e me conheces.
Tu sabes o meu assentar e o meu levantar; de longe entendes o meu pensamento.
Cercas o meu andar e o meu deitar; e conheces todos os meus caminhos.
Não havendo ainda palavra alguma na minha língua, eis que logo, ó Senhor, tudo conheces.
Tu me cercaste por detrás e por diante, e puseste sobre mim a tua mão.
Tal ciência é para mim maravilhosa demais; tão alta que não a posso atingir.
Para onde me irei do teu espírito, ou para onde fugirei da tua face?
Se subir ao céu, lá tu estás; se fizer no inferno a minha cama, eis que tu ali estás também.
Se tomar as asas da alva, se habitar nas extremidades do mar, até ali a tua mão me guiará.
E a tua destra me susterá.
Eu te louvarei, porque de um modo assombroso, e tão maravilhoso fui feito.
Maravilhosas são as tuas obras, e a minha alma o sabe muito bem.
Sonda-me, ó Deus, e conhece o meu coração; prova-me, e conhece os meus pensamentos.
E vê se há em mim algum caminho mau, e guia-me pelo caminho eterno.""",
        "wisdom"
    ),

    # =========================================================================
    # SALMOS DE CLAMOR E SÚPLICA
    # =========================================================================
    (
        "Salmo 6",
        """Senhor, não me repreendas na tua ira, nem me castigues no teu furor.
Tem misericórdia de mim, Senhor, porque sou fraco.
Sara-me, Senhor, porque os meus ossos estão perturbados.
Até a minha alma está muito perturbada; e tu, Senhor, até quando?
Volta-te, Senhor, livra a minha alma; salva-me por amor da tua misericórdia.
Porque na morte não há lembrança de ti; no sepulcro quem te louvará?
Já estou cansado do meu gemido; toda a noite faço nadar a minha cama.
Regando o meu leito com as minhas lágrimas.
Apartai-vos de mim todos os que praticais a iniquidade.
Porque o Senhor ouviu a voz do meu pranto.
O Senhor ouviu a minha súplica; o Senhor aceitará a minha oração.""",
        "cry"
    ),
    (
        "Salmo 13",
        """Até quando te esquecerás de mim, Senhor? Para sempre?
Até quando esconderás de mim o teu rosto?
Até quando consultarei com a minha alma, tendo tristeza no meu coração cada dia?
Até quando se exaltará o meu inimigo sobre mim?
Atende-me, ouve-me, ó Senhor meu Deus.
Ilumina os meus olhos para que eu não adormeça na morte.
Para que o meu inimigo não diga: Prevaleci contra ele.
E os meus adversários não se alegrem, vindo eu a vacilar.
Mas eu confio na tua misericórdia; na tua salvação se alegrará o meu coração.
Cantarei ao Senhor, porquanto me tem feito muito bem.""",
        "cry"
    ),
    (
        "Salmo 86",
        """Inclina, Senhor, os teus ouvidos, e ouve-me, porque estou necessitado e sou pobre.
Guarda a minha alma, pois sou santo; ó Deus meu, salva o teu servo, que em ti confia.
Tem misericórdia de mim, ó Senhor, pois a ti clamo todo o dia.
Alegra a alma do teu servo, pois a ti, Senhor, levanto a minha alma.
Pois tu, Senhor, és bom, e pronto a perdoar, e abundante em benignidade para todos os que te invocam.
Dá ouvidos, Senhor, à minha oração e atende à voz das minhas súplicas.
No dia da minha angústia clamo a ti, porque tu me respondes.
Entre os deuses não há semelhante a ti, Senhor, nem há obras como as tuas.
Todas as nações que fizeste virão e se prostrarão perante a tua face, Senhor, e glorificarão o teu nome.
Porque tu és grande e fazes maravilhas; só tu és Deus.
Ensina-me, Senhor, o teu caminho, e andarei na tua verdade.
Une o meu coração ao temor do teu nome.
Louvar-te-ei, Senhor Deus meu, com todo o meu coração, e glorificarei o teu nome para sempre.""",
        "cry"
    ),

    # =========================================================================
    # SALMOS DE FORÇA E VITÓRIA
    # =========================================================================
    (
        "Salmo 18",
        """Eu te amarei, ó Senhor, fortaleza minha.
O Senhor é a minha rocha, e o meu lugar forte, e o meu libertador.
O meu Deus, a minha fortaleza, em quem confio.
O meu escudo, e a força da minha salvação, o meu alto refúgio.
Invocarei o Senhor, digno de louvor, e ficarei livre dos meus inimigos.
Cordas de morte me cingiram, e torrentes de impiedade me assombraram.
Cordas do inferno me cercaram, laços de morte me surpreenderam.
Na minha angústia invoquei ao Senhor, e clamei ao meu Deus.
Desde o seu templo ouviu a minha voz, e o meu clamor chegou perante a sua face.
Ele estendeu a mão desde o alto, e me tomou; tirou-me das muitas águas.
Livrou-me do meu inimigo forte e dos que me odiavam.
O Senhor foi o meu amparo.
E me trouxe para um lugar espaçoso; livrou-me, porque tinha prazer em mim.
Viva o Senhor, e bendita seja a minha rocha.
E exaltado seja o Deus da minha salvação.""",
        "strength"
    ),
    (
        "Salmo 144",
        """Bendito seja o Senhor, minha rocha, que ensina as minhas mãos para a peleja e os meus dedos para a guerra.
Benignidade minha e fortaleza minha, alto refúgio meu e meu libertador.
Escudo meu, em quem eu confio, e o que sujeita o meu povo a mim.
Senhor, que é o homem, para que o conheças? E o filho do homem, para que o estimes?
O homem é semelhante à vaidade; os seus dias são como a sombra que passa.
Abaixa, ó Senhor, os teus céus, e desce; toca os montes, e fumegarão.
Envia os teus raios, e dissipa-os; arremessa as tuas setas, e desbarata-os.
Estende as tuas mãos desde o alto; livra-me, e arrebata-me das muitas águas.
Bem-aventurado o povo a quem assim sucede.
Bem-aventurado o povo cujo Deus é o Senhor.""",
        "strength"
    ),

    # =========================================================================
    # SALMOS DE NOITE E VIGÍLIA
    # =========================================================================
    (
        "Salmo 4",
        """Ouve-me quando eu clamo, ó Deus da minha justiça; na angústia me deste largueza.
Tem misericórdia de mim, e ouve a minha oração.
Filhos dos homens, até quando convertereis a minha glória em infâmia?
Até quando amareis a vaidade e buscareis a mentira?
Sabei que o Senhor separou para si aquele que é piedoso.
O Senhor ouvirá quando eu clamar a ele.
Perturbai-vos e não pequeis; falai com o vosso coração sobre a vossa cama, e calai-vos.
Oferecei sacrifícios de justiça, e confiai no Senhor.
Muitos dizem: Quem nos mostrará o bem?
Senhor, exalta sobre nós a luz do teu rosto.
Puseste alegria no meu coração, maior do que a deles quando o seu trigo e o seu vinho se multiplicam.
Em paz também me deitarei e dormirei, porque só tu, Senhor, me fazes habitar em segurança.""",
        "night"
    ),
    (
        "Salmo 63",
        """Ó Deus, tu és o meu Deus; de madrugada te buscarei.
A minha alma tem sede de ti; o meu corpo te deseja muito em uma terra seca e cansada, onde não há água.
Para ver a tua força e a tua glória, como te vi no santuário.
Porque a tua benignidade é melhor do que a vida; os meus lábios te louvarão.
Assim eu te bendirei enquanto viver; em teu nome levantarei as minhas mãos.
A minha alma se fartará, como de tutano e de gordura.
E a minha boca te louvará com alegres lábios, quando me lembrar de ti na minha cama.
E meditar em ti nas vigílias da noite.
Porque tu tens sido o meu auxílio; então, à sombra das tuas asas me regozijarei.
A minha alma está pegada a ti; a tua destra me sustém.""",
        "night"
    ),
    (
        "Salmo 134",
        """Olhai, bendizei ao Senhor todos vós, servos do Senhor.
Que assistis de noite na casa do Senhor.
Levantai as mãos para o santuário, e bendizei ao Senhor.
O Senhor, que fez o céu e a terra, te abençoe desde Sião.""",
        "night"
    ),

    # =========================================================================
    # SALMOS DE COMUNHÃO E UNIDADE
    # =========================================================================
    (
        "Salmo 133",
        """Oh! Quão bom e quão suave é que os irmãos vivam em união!
É como o óleo precioso sobre a cabeça, que desce sobre a barba, a barba de Arão.
Que desce à orla das suas vestes.
Como o orvalho de Hermom, que desce sobre os montes de Sião.
Porque ali o Senhor ordena a bênção e a vida para sempre.""",
        "unity"
    ),
    (
        "Salmo 122",
        """Alegrei-me quando me disseram: Vamos à casa do Senhor.
Os nossos pés estão dentro das tuas portas, ó Jerusalém.
Jerusalém está edificada como uma cidade bem compacta.
Aonde sobem as tribos, as tribos do Senhor, ao testemunho de Israel, para louvarem o nome do Senhor.
Porque ali estão os tronos do juízo, os tronos da casa de Davi.
Orai pela paz de Jerusalém; prosperarão aqueles que te amam.
Haja paz dentro de teus muros, e prosperidade dentro dos teus palácios.
Por causa dos meus irmãos e amigos, direi: Paz seja contigo.
Por causa da casa do Senhor nosso Deus, buscarei o teu bem.""",
        "unity"
    ),

    # =========================================================================
    # SALMOS DE NATUREZA E CRIAÇÃO
    # =========================================================================
    (
        "Salmo 8",
        """Ó Senhor, Senhor nosso, quão admirável é o teu nome em toda a terra.
Pois puseste a tua glória sobre os céus!
Da boca das crianças e dos que mamam tu suscitaste força.
Quando vejo os teus céus, obra dos teus dedos, a lua e as estrelas que preparaste.
Que é o homem mortal para que te lembres dele? E o filho do homem, para que o visites?
Contudo, pouco menor o fizeste do que os anjos, e de glória e de honra o coroaste.
Fazes com que ele tenha domínio sobre as obras das tuas mãos.
Tudo puseste debaixo de seus pés: Todas as ovelhas e bois, e até mesmo os animais do campo.
As aves dos céus, e os peixes do mar, e tudo o que passa pelas veredas dos mares.
Ó Senhor, Senhor nosso, quão admirável é o teu nome sobre toda a terra!""",
        "creation"
    ),
    (
        "Salmo 104",
        """Bendize, ó minha alma, ao Senhor!
Senhor, meu Deus, tu és magnificentíssimo; estás vestido de glória e de majestade.
Ele é o que se cobre de luz como de um vestido, que estende os céus como uma cortina.
Que põe nas águas as suas câmaras, e faz das nuvens o seu carro, e anda sobre as asas do vento.
Faz dos seus anjos ventos, dos seus ministros um fogo flamejante.
Lançou os fundamentos da terra; ela não vacilará em tempo algum.
Tu a cobriste com o abismo, como com um vestido; as águas estavam sobre os montes.
Ele faz crescer a erva para o gado, e a verdura para o serviço do homem.
Para que tire da terra o pão, e o vinho que alegra o coração do homem.
E o azeite que faz reluzir o seu rosto, e o pão que fortalece o coração do homem.
Ó Senhor, quão variadas são as tuas obras! Todas as coisas fizeste com sabedoria.
A terra está cheia das tuas riquezas.
Cantarei ao Senhor enquanto eu viver; cantarei louvores ao meu Deus enquanto eu existir.
Seja-lhe agradável a minha meditação; eu me alegrarei no Senhor.
Bendize, ó minha alma, ao Senhor. Louvai ao Senhor!""",
        "creation"
    ),
    (
        "Salmo 148",
        """Louvai ao Senhor!
Louvai ao Senhor desde os céus, louvai-o nas alturas.
Louvai-o, todos os seus anjos; louvai-o, todos os seus exércitos.
Louvai-o, sol e lua; louvai-o, todas as estrelas luzentes.
Louvai-o, céus dos céus, e as águas que estão sobre os céus.
Louvem o nome do Senhor, pois mandou, e logo foram criados.
E os confirmou para sempre; deu-lhes uma lei que não será quebrada.
Louvai ao Senhor desde a terra: vós, baleias, e todos os abismos.
Fogo e saraiva, neve e vapores, e vento tempestuoso que executa a sua palavra.
Montes e todos os outeiros, árvores frutíferas e todos os cedros.
As feras e todos os gados, répteis e aves voadoras.
Reis da terra e todos os povos, príncipes e todos os juízes da terra.
Jovens e donzelas, velhos e meninos, louvem o nome do Senhor.
Porque só o seu nome é exaltado; a sua glória está sobre a terra e o céu.
Louvai ao Senhor!""",
        "creation"
    ),

    # =========================================================================
    # NOVOS SALMOS – PAZ E CONFIANÇA
    # =========================================================================
    (
        "Salmo 3",
        """Senhor, como se têm multiplicado os meus adversários!
Muitos são os que se levantam contra mim.
Mas tu, ó Senhor, és o meu escudo; és a minha glória e o que exalta a minha cabeça.
Com a minha voz clamei ao Senhor, e ele me ouviu.
Eu me deitei e dormi; acordei, porque o Senhor me sustentou.
Não terei medo de dez milhares de pessoas que se puseram contra mim ao meu redor.
Levanta-te, Senhor; salva-me, Deus meu.""",
        "peace"
    ),
    (
        "Salmo 5",
        """Dá ouvidos às minhas palavras, ó Senhor; considera a minha meditação.
Atende à voz do meu clamor, Rei meu e Deus meu.
Pela manhã ouvirás a minha voz; pela manhã me apresentarei a ti.
Porque tu não és um Deus que tenha prazer na iniquidade.
Tu destruirás aqueles que falam a mentira.
Mas quanto a mim, entrarei em tua casa pela grandeza da tua misericórdia.
E em teu temor me prostrarei no teu santo templo.
Guia-me, Senhor, na tua justiça.""",
        "trust"
    ),
    (
        "Salmo 11",
        """No Senhor confio. Como dizeis à minha alma: Fuge para o vosso monte, como pássaro?
Porque eis que os ímpios armam o arco.
Os fundamentos se destroem; que pode fazer o justo?
O Senhor está no seu santo templo; o trono do Senhor está nos céus.
Os seus olhos contemplam; as suas pálpebras provam os filhos dos homens.
O Senhor prova o justo.""",
        "trust"
    ),
    (
        "Salmo 16",
        """Guarda-me, ó Deus, porque em ti confio.
Disse ao Senhor: Tu és o meu Senhor; não tenho outro bem além de ti.
O Senhor é a porção da minha herança e do meu cálice.
Manterás o meu quinhão.
As linhas caíram-me em lugares deleitosos; sim, a minha herança é formosa para mim.
Bendigo ao Senhor que me aconselhou; até de noite o meu coração me instrui.
Ao Senhor tenho sempre diante de mim; estando ele à minha direita, não serei abalado.
Portanto está alegre o meu coração e a minha glória se regozija.""",
        "peace"
    ),
    (
        "Salmo 20",
        """O Senhor te ouça no dia da angústia; o nome do Deus de Jacó te proteja.
Envie-te socorro desde o santuário, e te sustenha desde Sião.
Lembre-se de todas as tuas ofertas e aceite os teus holocaustos.
Conceda-te conforme o desejo do teu coração e cumpra todo o teu propósito.
Celebraremos a tua vitória e em nome do nosso Deus arvoraremos pendões.
Agora sei que o Senhor salva o seu ungido.""",
        "hope"
    ),
    (
        "Salmo 24",
        """Do Senhor é a terra e a sua plenitude; o mundo e os que nele habitam.
Porque ele a fundou sobre os mares e a estabeleceu sobre os rios.
Quem subirá ao monte do Senhor, ou quem estará no seu lugar santo?
Aquele que é limpo de mãos e puro de coração.
Este receberá a bênção do Senhor e a justiça do Deus da sua salvação.
Levantai, ó portas, as vossas cabeças; e levantai-vos, ó entradas eternas.
E entrará o Rei da glória. Quem é este Rei da glória? O Senhor forte e poderoso.""",
        "praise"
    ),
    (
        "Salmo 25",
        """A ti, ó Senhor, levanto a minha alma.
Deus meu, em ti confio; não seja eu envergonhado.
Faze-me conhecer os teus caminhos, ó Senhor; ensina-me as tuas veredas.
Guia-me na tua verdade e ensina-me.
Porque tu és o Deus da minha salvação; em ti espero todo o dia.
Lembra-te, Senhor, das tuas misericórdias e das tuas benignidades.
Porque são desde a eternidade.
Bom e reto é o Senhor; por isso ensinará o caminho aos pecadores.""",
        "trust"
    ),
    (
        "Salmo 28",
        """A ti clamo, ó Senhor, Rocha minha; não emudeças para comigo.
Ouve a voz das minhas súplicas quando a ti clamo.
O Senhor é a minha força e o meu escudo; nele confiou o meu coração.
O Senhor é a força do seu povo; é a fortaleza salvadora do seu ungido.
Salva o teu povo e abençoa a tua herança; e apascenta-os e exalta-os para sempre.""",
        "strength"
    ),
    (
        "Salmo 29",
        """Dai ao Senhor, ó filhos dos poderosos, dai ao Senhor glória e força.
Dai ao Senhor a glória devida ao seu nome; adorai o Senhor na beleza da santidade.
A voz do Senhor ouve-se sobre as águas; o Deus da glória troveja.
A voz do Senhor é poderosa; a voz do Senhor é cheia de majestade.
O Senhor dará força ao seu povo; o Senhor abençoará o seu povo com paz.""",
        "praise"
    ),
    (
        "Salmo 30",
        """Exaltar-te-ei, ó Senhor, porque me levantaste.
Cantarei ao Senhor, pois me fez bem.
O Senhor fez subir a minha alma da sepultura; guardaste-me a vida.
Converteste o meu pranto em regozijo.
Para que a minha glória te cante louvores e não se cale.
Senhor, meu Deus, eu te darei graças para sempre.""",
        "gratitude"
    ),
    (
        "Salmo 33",
        """Regozijai-vos no Senhor, vós justos, pois aos retos convém o louvor.
Louvai ao Senhor com harpa; cantai-lhe cânticos com saltério.
Porque a palavra do Senhor é reta, e todas as suas obras são fiéis.
Ele ama a justiça e o juízo; a terra está cheia da bondade do Senhor.
O Senhor desfaz o conselho das nações; quebranta os intentos dos povos.
Bem-aventurada é a nação cujo Deus é o Senhor.
A nossa alma espera no Senhor; ele é o nosso auxílio e o nosso escudo.""",
        "praise"
    ),
    (
        "Salmo 40",
        """Esperei com paciência no Senhor, e ele se inclinou para mim e ouviu o meu clamor.
Pôs um novo cântico na minha boca, um hino ao nosso Deus.
Muitos verão isso e temerão, e confiarão no Senhor.
Bem-aventurado o homem que põe no Senhor a sua confiança.
Muitas são, ó Senhor meu Deus, as maravilhas que tens feito.
Não há quem se compare a ti.""",
        "trust"
    ),
    (
        "Salmo 43",
        """Faze-me justiça, ó Deus, e pleiteia a minha causa contra uma nação ímpia.
Tu és o Deus da minha fortaleza; por que me rejeitaste?
Envia a tua luz e a tua verdade para me guiarem.
Então irei ao altar de Deus, ao Deus da minha alegria e regozijo.
E te louvarei com harpa, ó Deus, Deus meu.
Por que estás abatida, ó minha alma? Espera em Deus, pois ainda o louvarei.""",
        "hope"
    ),
    (
        "Salmo 54",
        """Salva-me, ó Deus, pelo teu nome, e faze-me justiça pelo teu poder.
Ouve a minha oração, ó Deus; inclina os teus ouvidos às palavras da minha boca.
Porque homens estranhos se levantaram contra mim.
Eis que Deus é o meu ajudador; o Senhor é com aqueles que sustêm a minha alma.
Voltará o mal sobre os meus inimigos.
Eu te sacrificarei voluntariamente; louvarei o teu nome, ó Senhor, porque é bom.""",
        "protection"
    ),
    (
        "Salmo 56",
        """Tem misericórdia de mim, ó Deus, pois o homem quer devorar-me.
Os meus inimigos me oprimem cada dia.
Quando temo, confio em ti.
Em Deus louvarei a sua palavra; em Deus pus a minha confiança.
Que me pode fazer o homem?
Entrega os meus prantos ao teu odre; não estão eles no teu livro?
Em Deus louvarei a sua palavra; no Senhor louvarei a sua palavra.""",
        "trust"
    ),
    (
        "Salmo 61",
        """Ouve, ó Deus, o meu clamor; atende à minha oração.
Desde a extremidade da terra clamo a ti, quando o meu coração desfalece.
Leva-me à rocha que é mais alta do que eu.
Porque tu és o meu refúgio, uma torre forte contra o inimigo.
Assim habitarei no teu tabernáculo para sempre; confiarei à sombra das tuas asas.
Porque tu, ó Deus, ouviste os meus votos; deste-me a herança dos que temem o teu nome.""",
        "protection"
    ),
    (
        "Salmo 70",
        """Apressa-te, ó Deus, em me livrar; Senhor, apressa-te em socorrer-me.
Fiquem envergonhados e confundidos os que buscam a minha alma.
Voltem atrás e envergonhem-se os que desejam o meu mal.
Mas regozijem-se e alegrem-se em ti todos os que te buscam.
E digam continuamente: Magnificado seja o Deus que tem prazer no meu bem-estar.
Eu sou pobre e necessitado; apressa-te, ó Deus; tu és o meu auxílio e o meu libertador.""",
        "cry"
    ),
    (
        "Salmo 84",
        """Quão amáveis são os teus tabernáculos, ó Senhor dos Exércitos!
A minha alma anela e deseja os átrios do Senhor.
O meu coração e a minha carne clamam pelo Deus vivo.
Bem-aventurados os que habitam em tua casa; louvar-te-ão continuamente.
Bem-aventurado o homem cuja força está em ti.
Vale de lágrimas fazem dele um lugar de fontes.
O Senhor Deus é sol e escudo; o Senhor dará graça e glória.""",
        "hope"
    ),
    (
        "Salmo 90",
        """Senhor, tu tens sido o nosso refúgio de geração em geração.
Antes que os montes nascessem, ou que tu formasses a terra e o mundo.
De eternidade a eternidade tu és Deus.
Tu reduzes o homem à destruição; e dizes: Voltai, filhos dos homens.
Porque mil anos são aos teus olhos como o dia de ontem que passou.
Ensina-nos a contar os nossos dias de tal maneira que alcancemos corações sábios.
Satisfaze-nos de manhã com a tua benignidade.""",
        "wisdom"
    ),
    (
        "Salmo 92",
        """Bom é louvar ao Senhor, e cantar louvores ao teu nome, ó Altíssimo.
Anunciar de manhã a tua benignidade e de noite a tua fidelidade.
Os justos florescerão como a palmeira; crescerão como o cedro no Líbano.
Plantados na casa do Senhor, florescerão nos átrios do nosso Deus.
Na velhice ainda darão frutos; serão viçosos e florescentes.
Para anunciar que o Senhor é reto; ele é a minha rocha e nele não há injustiça.""",
        "praise"
    ),
    (
        "Salmo 93",
        """O Senhor reina; está vestido de majestade.
O Senhor se revestiu e cingiu de poder; o mundo também está firmado.
O teu trono está firme desde a antiguidade; tu és desde a eternidade.
Os rios levantam, ó Senhor, os rios levantam o seu ruído.
O Senhor nas alturas é mais poderoso do que o ruído das grandes águas.
Os teus testemunhos são mui fiéis; a santidade convém à tua casa, ó Senhor, para sempre.""",
        "praise"
    ),
    (
        "Salmo 95",
        """Vinde, cantemos ao Senhor; jubilemos à rocha da nossa salvação.
Apresentemo-nos ante a sua face com louvor; jubilemos a ele com salmos.
Porque o Senhor é Deus grande, e Rei grande acima de todos os deuses.
Nele estão as profundezas da terra, e as alturas dos montes são dele.
O mar é dele, e ele o fez; e as suas mãos formaram a terra seca.
Vinde, adoremos e prostremo-nos; ajoelhemos diante do Senhor que nos criou.
Porque ele é o nosso Deus, e nós povo do seu pasto e ovelhas da sua mão.""",
        "praise"
    ),
    (
        "Salmo 96",
        """Cantai ao Senhor um cântico novo; cantai ao Senhor, toda a terra.
Cantai ao Senhor, bendizei o seu nome; anunciai a sua salvação de dia em dia.
Declarai entre as nações a sua glória, entre todos os povos as suas maravilhas.
Porque grande é o Senhor e mui digno de louvor.
Honra e majestade estão diante dele; força e formosura no seu santuário.
Dai ao Senhor, ó famílias dos povos, dai ao Senhor glória e força.
Tributai ao Senhor a glória devida ao seu nome; trazei ofertas e entrai nos seus átrios.""",
        "praise"
    ),
    (
        "Salmo 116",
        """Amo ao Senhor, porque ouviu a minha voz e as minhas súplicas.
Porque inclinou a seu ouvido a mim, invocá-lo-ei em todos os meus dias.
Laços de morte me cercaram; encontrei aperto e tristeza.
Então invoquei o nome do Senhor: Ó Senhor, livra a minha alma.
Gracioso é o Senhor e justo; o nosso Deus é misericordioso.
Retribuirei os meus votos ao Senhor, na presença de todo o seu povo.
Preciosa é aos olhos do Senhor a morte dos seus santos.
Ó Senhor, verdadeiramente sou teu servo; livraste a minha alma da morte.""",
        "gratitude"
    ),
    (
        "Salmo 117",
        """Louvai ao Senhor, todas as nações; louvai-o, todos os povos.
Porque a sua benignidade é grande para conosco, e a verdade do Senhor permanece para sempre.
Louvai ao Senhor!""",
        "praise"
    ),
    (
        "Salmo 118",
        """Louvai ao Senhor, porque ele é bom; porque a sua misericórdia dura para sempre.
Melhor é confiar no Senhor do que confiar no homem.
O Senhor é a minha força e o meu cântico; tornou-se a minha salvação.
A pedra que os edificadores rejeitaram tornou-se a cabeça da esquina.
Este é o dia que o Senhor fez; regozijemo-nos e alegremo-nos nele.
Tu és o meu Deus, e eu te louvarei; tu és o meu Deus, e eu te exaltarei.
Louvai ao Senhor, porque ele é bom; porque a sua misericórdia dura para sempre.""",
        "gratitude"
    ),
    (
        "Salmo 120",
        """Na minha angústia clamei ao Senhor, e ele me ouviu.
Senhor, livra a minha alma dos lábios mentirosos e da língua enganosa.
Que te será dado, ou que te será acrescentado, língua enganosa?
Guias de guerra, com brasas de zimbro.
Ai de mim, que habito em Meseque e que moro nas tendas de Quedar!
Há muito que a minha alma habita com aqueles que odeiam a paz.
Eu sou pela paz; mas quando falo, eles são pela guerra.""",
        "cry"
    ),
    (
        "Salmo 123",
        """A ti levanto os meus olhos, ó tu que habitas nos céus.
Eis que assim como os olhos dos servos atentam para a mão dos seus senhores.
Assim os nossos olhos atentam para o Senhor nosso Deus.
Tem misericórdia de nós, ó Senhor, tem misericórdia de nós.
A nossa alma está farta da zombaria daqueles que estão à sua vontade.""",
        "cry"
    ),
    (
        "Salmo 124",
        """Se não fora o Senhor, que esteve ao nosso lado, ora diga Israel.
Se não fora o Senhor, quando os homens se levantaram contra nós.
Então nos teriam engolido vivos, quando a sua ira se acendeu contra nós.
Então as águas teriam transbordado sobre a nossa alma.
Bendito seja o Senhor, que não nos deu por presa aos seus dentes.
A nossa alma escapou como um pássaro do laço dos passarinheiros.
O nosso socorro está no nome do Senhor, que fez o céu e a terra.""",
        "gratitude"
    ),
    (
        "Salmo 125",
        """Os que confiam no Senhor são como o monte de Sião, que não se abala.
Assim como estão os montes ao redor de Jerusalém, assim o Senhor está ao redor do seu povo.
Porque o cetro da impiedade não permanecerá sobre a sorte dos justos.
Faze bem, ó Senhor, aos bons e aos que são retos de coração.
Quanto àqueles que se desviam para os seus caminhos tortuosos, o Senhor os levará com os que praticam a iniquidade.
Paz sobre Israel.""",
        "trust"
    ),
    (
        "Salmo 126",
        """Quando o Senhor trouxe do cativeiro os que voltaram a Sião, éramos como os que sonham.
Então a nossa boca se encheu de riso e a nossa língua de cântico.
Então se dizia entre as nações: Grandes coisas fez o Senhor a estes.
Grandes coisas fez o Senhor por nós, e por isso estamos alegres.
Traze-nos outra vez, ó Senhor, como as correntes no sul.
Os que semeiam com lágrimas segarão com alegria.""",
        "hope"
    ),
    (
        "Salmo 127",
        """Se o Senhor não edificar a casa, em vão trabalham os que a edificam.
Se o Senhor não guardar a cidade, em vão vigia a sentinela.
Inútil vos será levantar de madrugada, repousar tarde, comer o pão de dores.
Porque assim dá ele aos seus amados o sono.
Eis que os filhos são herança do Senhor, e o fruto do ventre o seu galardão.
Bem-aventurado o homem que enche deles a sua aljava.""",
        "wisdom"
    ),
    (
        "Salmo 128",
        """Bem-aventurado aquele que teme ao Senhor e anda nos seus caminhos.
Pois comerás do trabalho das tuas mãos; feliz serás, e te irá bem.
A tua mulher será como a videira frutífera no interior da tua casa.
Os teus filhos como plantas de oliveira à roda da tua mesa.
Eis que assim será abençoado o homem que teme ao Senhor.
O Senhor te abençoe desde Sião, para que vejas a prosperidade de Jerusalém.""",
        "peace"
    ),
    (
        "Salmo 132",
        """Lembra-te, ó Senhor, de Davi e de todas as suas aflições.
Como jurou ao Senhor e fez voto ao Forte de Jacó.
Não entrarei na tenda da minha casa, nem subirei ao leito da minha cama.
Até que eu ache lugar para o Senhor, morada para o Forte de Jacó.
Eis que ouvimos falar dela em Efrata; achamo-la no campo do bosque.
Entraremos nos seus tabernáculos; nos prostraremos ante o escabelo dos seus pés.""",
        "praise"
    ),
    (
        "Salmo 138",
        """Louvar-te-ei de todo o meu coração; na presença dos deuses a ti cantarei.
Inclinar-me-ei para o teu santo templo e louvarei o teu nome.
Por causa da tua benignidade e da tua verdade.
No dia em que clamei, me respondeste; e alentaste com força a minha alma.
Todos os reis da terra te louvarão, ó Senhor, quando ouvirem as palavras da tua boca.
Ainda que o Senhor é excelso, atenta para o humilde.""",
        "gratitude"
    ),
    (
        "Salmo 145",
        """Exaltar-te-ei, ó Deus meu Rei, e bendirei o teu nome para todo o sempre.
Cada dia te bendirei e louvarei o teu nome para todo o sempre.
Grande é o Senhor e mui digno de louvor; a sua grandeza é inescrutável.
Uma geração louvará as tuas obras à outra geração.
O Senhor é benigno em todas as suas obras, e piedoso em todos os seus caminhos.
O Senhor está perto de todos os que o invocam.
Abre a tua mão e satisfazes o desejo de todo ser vivente.
O Senhor é justo em todos os seus caminhos e santo em todas as suas obras.
O Senhor está perto de todos os que o invocam, de todos os que o invocam em verdade.
Louvai ao Senhor.""",
        "praise"
    ),
    (
        "Salmo 146",
        """Louvai ao Senhor. Louva, ó minha alma, ao Senhor.
Louvarei ao Senhor enquanto viver; cantarei louvores ao meu Deus enquanto eu existir.
Não confieis nos príncipes, nem no filho do homem, em quem não há salvação.
Bem-aventurado aquele que tem o Deus de Jacó por seu auxílio.
O Senhor fez o céu e a terra, o mar e tudo o que neles há.
Ele mantém a verdade para sempre; faz justiça aos oprimidos.
O Senhor abre os olhos aos cegos; o Senhor levanta os abatidos.
O Senhor ama os justos; o Senhor guarda os estrangeiros.""",
        "praise"
    ),
    (
        "Salmo 147",
        """Louvai ao Senhor, porque é bom cantar louvores ao nosso Deus.
O Senhor edifica Jerusalém; ajunta os dispersos de Israel.
Sara os quebrantados de coração e liga as suas feridas.
Ele conta o número das estrelas; chama a todas pelos seus nomes.
Grande é o nosso Senhor e de grande poder; o seu entendimento é infinito.
O Senhor levanta os mansos e abate os ímpios até à terra.
Cantai ao Senhor com ação de graças; cantai louvores ao nosso Deus.""",
        "praise"
    ),
    (
        "Salmo 149",
        """Louvai ao Senhor! Cantai ao Senhor um cântico novo.
O seu louvor na congregação dos santos.
Alegre-se Israel naquele que o criou; regozijem-se os filhos de Sião no seu Rei.
Louvem o seu nome com danças; cantem-lhe louvor com tamboril e harpa.
Porque o Senhor se agrada do seu povo; adornará os mansos com a salvação.
Exultem os santos em glória; alegrem-se nos seus leitos.
Louvai ao Senhor!""",
        "praise"
    ),
]

# Mapeamento de mood para paleta visual
MOOD_TO_PALETTE = {
    "peace": "heavenly",
    "protection": "sacred",
    "hope": "dawn",
    "praise": "dawn",
    "gratitude": "heavenly",
    "trust": "serene",
    "repentance": "sacred",
    "forgiveness": "heavenly",
    "wisdom": "serene",
    "cry": "sacred",
    "strength": "sacred",
    "night": "heavenly",
    "unity": "serene",
    "creation": "dawn",
}

def get_salmo_by_name(nome: str):
    """Busca um salmo pelo nome."""
    for salmo in SALMOS_COMPLETOS:
        if salmo[0].lower() == nome.lower():
            return salmo
    return None

def get_salmo_by_index(index: int):
    """Busca um salmo pelo índice na lista (0 a len-1)."""
    if 0 <= index < len(SALMOS_COMPLETOS):
        return SALMOS_COMPLETOS[index]
    return None


def get_salmo_by_number(numero: int):
    """
    Busca um salmo pelo número bíblico (1 a 150).
    Retorna (nome, texto, mood) se tivermos o texto; senão None.
    """
    if numero < 1 or numero > TOTAL_SALMOS:
        return None
    nome = f"Salmo {numero}"
    for salmo in SALMOS_COMPLETOS:
        if salmo[0].lower() == nome.lower():
            return salmo
    return None


def get_palette_for_salmo(salmo_nome: str, mood: str = None) -> str:
    """Retorna a paleta visual recomendada para o salmo."""
    if mood and mood in MOOD_TO_PALETTE:
        return MOOD_TO_PALETTE[mood]
    return "heavenly"

def list_all_salmos():
    """Lista todos os salmos disponíveis (com texto integral)."""
    print(f"\n{'='*60}")
    print("  SALMOS DISPONÍVEIS (com texto integral)")
    print(f"  Livro de Salmos: {TOTAL_SALMOS} salmos no total")
    print(f"{'='*60}\n")
    
    for i, (nome, texto, mood) in enumerate(SALMOS_COMPLETOS):
        versos = len([l for l in texto.strip().split('\n') if l.strip()])
        palette = MOOD_TO_PALETTE.get(mood, "heavenly")
        print(f"  [{i:2d}] {nome:<12} | {versos:2d} versos | {mood:<12} | {palette}")
    
    print(f"\n{'='*60}")
    print(f"  Com texto: {len(SALMOS_COMPLETOS)} | Total no livro: {TOTAL_SALMOS}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    list_all_salmos()
