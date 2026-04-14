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
    # --- Faltantes acrescentados (sem duplicar números já listados acima); Salmo 119 omitido por tamanho ---
    (
        "Salmo 2",
        """Por que se amotinam as nações, e os povos maquinam em vão?
Os reis da terra se levantam, e os príncipes consultam juntos contra o Senhor e contra o seu ungido, dizendo:
Rompamos as suas ataduras, e sacudamos de nós as suas cordas.
Aquele que habita nos céus se rirá; o Senhor zombará deles.
Então lhes falará na sua ira, e os perturbará no seu furor, dizendo:
Eu, porém, ungi o meu Rei sobre o meu santo monte de Sião.
Publicarei o decreto: o Senhor me disse: Tu és meu Filho, hoje te gerei.
Pede-me, e eu te darei as nações por herança, e as extremidades da terra por tua possessão.
Com vara de ferro os regerás, e quebrando-os como a um vaso de oleiro.
Agora, pois, ó reis, sede prudentes; e vós, juízes da terra, emendai-vos.
Servi ao Senhor com temor, e regozijai-vos com tremor.
Beijai o Filho, para que se não ire, e pereçais no caminho, quando em breve se acender a sua ira.
Bem-aventurados todos os que nele confiam.""",
        "strength",
    ),
    (
        "Salmo 7",
        """Senhor, meu Deus, em ti confio; salva-me de todos os que me perseguem, e livra-me,
Para que ninguém arrebate, qual leão, a minha alma, despedaçando-a, sem haver quem a livre.
Senhor, meu Deus, se eu fiz isto, se há injustiça nas minhas mãos,
Se paguei com mal ao que paz tinha comigo (antes livrei ao que me oprimia sem causa),
Persiga o inimigo a minha alma, e alcance-a; calque a minha vida no chão, e reduza a minha glória ao pó.
Levanta-te, Senhor, na tua ira; exalta-te por causa do furor dos meus opressores; e desperta por mim o juízo que ordenaste.
E a congregação dos povos te cercará; por isso, tu, Senhor, reinarás sobre elas lá em cima.
O Senhor julga os povos; faze-me justiça, Senhor, conforme a minha retidão e conforme a minha integridade que há em mim.
Acabe-se a malícia dos ímpios, e estabeleça-se o justo; pois tu sondas os corações e os rins, ó Deus justo.
O meu escudo está em Deus, que salva os retos de coração.
Deus é juiz justo, e Deus que se ira todos os dias.
Se o homem não se converter, ele afiará a sua espada; já tem armado o seu arco e está aparelhado.
Também lhe preparou armas mortíferas; e fará as suas setas inflamadas.
Eis que o ímpio concebeu iniquidade, e está grávida de malícia, e dá à luz mentira.
Cavou um poço, e o fez fundo, e caiu na cova que fez.
A sua malícia tornará sobre a sua cabeça, e a sua violência descerá sobre o seu próprio crânio.
Eu louvarei ao Senhor segundo a sua justiça, e cantarei louvores ao nome do Senhor Altíssimo.""",
        "cry",
    ),
    (
        "Salmo 9",
        """Eu te louvarei, ó Senhor, de todo o meu coração; contarei todas as tuas maravilhas.
Em ti me alegrarei e saltarei de prazer; cantarei louvores ao teu nome, ó Altíssimo.
Quando os meus inimigos se tornarem atrás, cairão e perecerão diante da tua face.
Porque mantiveste o meu direito e a minha causa; assentaste-te no trono, julgando retamente.
Repreendeste os gentios, destruíste os ímpios; apagaste o nome deles para sempre e eternamente.
Ó inimigo! acabaram-se as assolações para sempre; e tu destruíste as cidades; e a sua memória pereceu com elas.
Mas o Senhor permanece para sempre; preparou o seu trono para o juízo.
E ele julgará o mundo com justiça; julgará os povos com retidão.
Assim o Senhor será refúgio para o oprimido, refúgio em tempos de angústia.
E em ti confiarão os que conhecem o teu nome; porquanto tu, Senhor, não desamparaste os que te buscam.
Cantai louvores ao Senhor, que habita em Sião; entre os povos anunciai os seus feitos.
Porque requer o sangue se lembra deles; não se esquece do clamor dos aflitos.
Tem misericórdia de mim, Senhor; vê a minha aflição, daqueles que me odeiam.
Tu que me levantas das portas da morte, para que eu conte todos os teus louvores nas portas da filha de Sião, e me alegre na tua salvação.
Os gentios afundaram-se na cova que fizeram; na rede que ocultaram ficou preso o seu pé.
O Senhor é conhecido pelo juízo que fez; o ímpio foi enlaçado na obra de suas mãos.
Os ímpios serão lançados no inferno, e todas as nações que se esquecem de Deus.
Porque o necessitado não será esquecido para sempre, nem a esperança dos pobres perecerá perpetuamente.
Levanta-te, Senhor; não prevaleça o homem; sejam julgados os gentios diante de tua face.
Põe-lhes medo, Senhor; para que saibam os gentios que não são mais do que homens.""",
        "praise",
    ),
    (
        "Salmo 10",
        """Por que te estás ao longe, Senhor? Por que te escondes nos tempos de angústia?
O ímpio, segundo a sua soberba, persegue o pobre; alcançem-no as maquinações que intentou.
Porque o ímpio gloria-se do desejo da sua alma, e o que ganha injustamente bendiz e maldiz ao Senhor.
Quanto à iniquidade do ímpio, segundo a altivez do seu nariz, diz: Não será castigado; não há Deus.
Os seus caminhos são sempre prósperos; os teus juízos estão longe dele, de todo o seu desejo; presumem contra os seus inimigos.
Disse nos seu coração: Não serei abalado, porque nunca me verei na adversidade.
A sua boca está cheia de maldição, e de enganos, e de fraude; debaixo da sua língua há malícia e iniquidade.
Põe-se de emboscada nas aldeias; nos lugares ocultos mata o inocente; os seus olhos estão ocultamente postos sobre o pobre.
Arma de emboscada, como o leão no seu covil; arma de emboscada para roubar os pobres; rouba os pobres, quando o atrai na sua rede.
Encurva-se, agacha-se, para que os pobres caiam em suas fortes garras.
Disse nos seu coração: Deus esqueceu-se; cobriu o seu rosto; nunca verá isto.
Levanta-te, ó Senhor Deus, levanta a tua mão; não te esqueças dos necessitados.
Por que blasfema de Deus o ímpio, dizendo no seu coração: Tu não inquirirás?
Tu o viste, porque atentas para o trabalho e enfado, para o tomares na tua mão; a ti o pobre se consagra; tu és o amparo do órfão.
Quebra tu o braço do ímpio e malvado; esquadrinha a sua maldade, até que a não possas achar.
O Senhor é Rei para sempre e sempre; da sua terra perecerão os gentios.
Senhor, tu tens ouvido o desejo dos humildes; tu confirmarás o seu coração, inclinarás o teu ouvido,
Para fazeres justiça ao órfão e ao oprimido, a fim de que o homem, que é da terra, não mais inspire terror.""",
        "cry",
    ),
    (
        "Salmo 12",
        """Salva-nos, Senhor, porque faltam os homens bons; porque entre os filhos dos homens não há lealdade.
Cada um fala com falsidade ao seu próximo; falam com lábios lisonjeiros e coração fingido.
Corte o Senhor todos os lábios lisonjeiros e a língua que fala soberbamente.
Aqueles que dizem: Com a nossa língua prevaleceremos; os nossos lábios a nós pertencem; quem sobre nós é senhor?
Por causa da opressão dos pobres, e do gemido dos necessitados, levantar-me-ei agora, diz o Senhor; porei em salvo aquele para quem eles assopram.
As palavras do Senhor são palavras puras, como prata refinada num forno de barro, purificada sete vezes.
Tu os guardarás, Senhor; desta geração os livrarás para sempre.
Os ímpios andam por toda parte, quando os vils dos filhos dos homens são exaltados.""",
        "trust",
    ),
    (
        "Salmo 14",
        """Disse o néscio no seu coração: Não há Deus. Corromperam-se, e abominavelmente obram iniquidade; não há quem faça o bem.
O Senhor olhou desde os céus para os filhos dos homens, para ver se havia algum que entendesse, e buscasse a Deus.
Desviaram-se todos, e juntamente se fizeram imundos; não há quem faça o bem, não há nem um sequer.
Acaso não têm conhecimento todos os que obram iniquidade, que comem o meu povo como se comessem pão, e não invocam ao Senhor?
Ali se acharam em grande temor, porque Deus está na geração dos justos.
Quiséreis frustrar o conselho dos pobres, mas o Senhor é o seu refúgio.
Oh, se de Sião viesse a salvação de Israel! Quando o Senhor fizer voltar os cativos do seu povo, então se regozijará Jacó, e Israel se alegrará.""",
        "wisdom",
    ),
    (
        "Salmo 15",
        """Senhor, quem habitará no teu tabernáculo? Quem morará no teu santo monte?
Aquele que anda sinceramente, e obra justiça, e fala a verdade no seu coração.
Aquele que não difama com a sua língua, nem faz mal ao seu próximo, nem acolhe opróbrio contra o seu próximo.
Aquele a cujos olhos o réprobo é desprezado; mas honra os que temem ao Senhor; aquele que, embora jure com dano seu, não muda.
Aquele que não dá o seu dinheiro à usura, nem recebe peitas contra o inocente. Quem assim faz nunca será abalado.""",
        "wisdom",
    ),
    (
        "Salmo 17",
        """Ouve, ó Senhor, a justiça; atende ao meu clamor; dá ouvidos à minha oração, que não é feita com lábios enganosos.
Saia diante de ti o meu juízo, e vejam os teus olhos a retidão.
Provaste o meu coração; visitaste-me de noite; examinaste-me, e nada achaste; propus que a minha boca não transgredisse.
Quanto às obras dos homens, pela palavra dos teus lábios me guardei dos caminhos do cruel.
Deste os meus passos nos teus caminhos, para que os meus pés não vacilem.
Eu te chamei, ó Deus, por me ouvires; inclina para mim os teus ouvidos, e escuta as minhas palavras.
Faze maravilhosas as tuas beneficências, tu que salvas com a tua destra os que se refugiam de ti dos seus inimigos.
Guarda-me como à menina do olho; esconde-me, à sombra das tuas asas,
Dos ímpios que me oprimem, dos meus inimigos mortais, que me cercam.
Na sua gordura encerraram o seu coração; com a boca falam soberbamente.
Cercaram-nos agora os nossos passos; fixaram em nós os seus olhos para nos lançarem por terra.
Parecem leões, que desejam fazer presa; e como leõezinhos, que se escondem em lugares ocultos.
Levanta-te, Senhor, detém-o, derriba-o; livra a minha alma dos ímpios, pela tua espada;
Dos homens, pela tua mão, Senhor, dos homens do mundo, cujo trato é só nesta vida, de cujo ventre és tu o teu tesouro; dos quais sacias a seus filhos, e ainda deixam o resto aos seus filhos.
Quanto a mim, em justiça verei a tua face; satisfazer-me-ei, quando acordar, com a tua semelhança.""",
        "cry",
    ),
    (
        "Salmo 21",
        """O rei se alegra na tua força, Senhor; e na tua salvação quão grandemente se regozija!
Concedeste-lhe o desejo do seu coração, e não lhe negaste a petição dos seus lábios.
Porque o prevês com bênçãos de bondade; puseste-lhe na cabeça uma coroa de ouro fino.
Vida te pediu, e lha deste, comprimento de dias para todo o sempre.
Grande é a sua glória pela tua salvação; honra e majestade puseste sobre ele.
Porque o puseste por bênçãos perpetuamente; tu o alegras na alegria com a tua face.
Porque o rei confia no Senhor, e pela misericórdia do Altíssimo nunca será abalado.
A tua mão alcançará todos os teus inimigos; a tua destra alcançará os que te odeiam.
Tu os farás como um forno ardente no tempo da tua ira; o Senhor os devorará na sua ira, e o fogo os consumirá.
E tu destruirás o seu fruto da terra, e a sua descendência dentre os filhos dos homens.
Porque intentaram o mal contra ti; maquinaram um ardil, mas nada prevalecerão.
Porque tu os porás em fuga; nas tuas cordas prepararás flechas contra o rosto deles.
Exalta-te, Senhor, na tua força; assim cantaremos e louvaremos o teu poder.""",
        "strength",
    ),
    (
        "Salmo 22",
        """Deus meu, Deus meu, por que me desamparaste? Por que se acham longe da minha salvação as palavras do meu bramido?
Deus meu, clamo de dia, e tu não ouves; de noite também, e não tenho sossego.
Porém tu és santo, entronizado entre os louvores de Israel.
Nossos pais confiaram em ti; confiaram, e tu os livraste.
A ti clamaram, e escaparam; em ti confiaram, e não foram confundidos.
Mas eu sou verme, e não homem; opróbrio dos homens, e desprezado do povo.
Todos os que me veem zombam de mim; arreganham os lábios e meneiam a cabeça, dizendo:
Confiou no Senhor, que o livre; que o livre, pois nele tem prazer.
Porém tu és o que me tiraste do ventre; fizeste-me confiar quando estava aos seios de minha mãe.
Sobre ti fui lançado desde a madre; tu és o meu Deus desde o ventre de minha mãe.
Não te alongues de mim, porque a angústia está perto, e não há quem ajude.
Muitos touros me cercam, fortes touros de Basã me rodeiam.
Abriram contra mim as suas bocas, como um leão que range e ruge.
Como águas sou derramado, e todos os meus ossos se desconjuntaram; o meu coração é como cera, derreteu-se no meio das minhas entranhas.
Como um caco se secou a minha força, e a minha língua se pegou ao meu paladar; e me puseste no pó da morte.
Porque me cercaram cães; o ajuntamento de malignos me fechou; traspassaram-me as mãos e os pés.
Contarei todos os meus ossos; eles me veem, e olham para mim.
Repartem entre si as minhas vestes, e sobre a minha tunica deitam sortes.
Tu, porém, ó Senhor, não te alongues de mim; ó minha força, apressa-te em socorrer-me.
Livra da espada a minha alma; do poder do cão a minha vida.
Salva-me da boca do leão; sim, ouve-me desde os chifres dos unicórnios.
Anunciarei o teu nome aos meus irmãos; louvar-te-ei no meio da congregação.
Louvai ao Senhor, vós que o temeis; glorificai-o, vós todos os da descendência de Jacó, e temei-o vós todos os da descendência de Israel.
Porque não desprezou nem aborreceu a aflição do aflito, nem escondeu dele o seu rosto; antes, quando clamou a ele, o ouviu.
De ti será o meu louvor na grande congregação; pagarei os meus votos perante os que o temem.
Os mansos comerão e fartar-se-ão; louvarão ao Senhor os que o buscam; o vosso coração viverá para sempre.
Lembrar-se-ão, e converter-se-ão ao Senhor os fins da terra; e todas as famílias das nações adorarão diante de ti.
Porque o reino é do Senhor, e ele domina sobre as nações.
Todos os que na terra se acharem fartos comerão e adorarão; e os que descem ao pó se prostrarão diante dele, e ninguém poderá conservar a sua alma com vida.
Uma descendência o servirá, e será contada ao Senhor para uma geração.
Virão e anunciarão a sua justiça a um povo que há de nascer, porque ele o fez.""",
        "hope",
    ),
    (
        "Salmo 26",
        """Julga-me, Senhor, pois tenho andado na minha sinceridade, e confiado no Senhor sem vacilar.
Examina-me, Senhor, e prova-me; esquadrinha os meus rins e o meu coração.
Porque a tua benignidade está diante dos meus olhos, e ando na tua verdade.
Não me assento com homens vãos, nem converso com os dissimulados.
Aborreço a congregação de malignos, e não me assento com os ímpios.
Lavo as minhas mãos na inocência; assim andarei ao redor do teu altar, ó Senhor,
Para publicar com voz de louvor, e contar todas as tuas maravilhas.
Senhor, eu amo a habitação da tua casa e o lugar onde permanece a tua glória.
Não apanhes a minha alma com a dos pecadores, nem a minha vida com a dos homens sanguinários,
Em cujas mãos há maldade, e cuja destra está cheia de subornos.
Eu, porém, ando na minha sinceridade; livra-me, e tem misericórdia de mim.
O meu pé está na retidão; nas congregações louvarei ao Senhor.""",
        "trust",
    ),
    (
        "Salmo 31",
        """Em ti, ó Senhor, confio; nunca seja eu confundido; livra-me na tua justiça.
Inclina para mim os teus ouvidos, livra-me depressa, e sê a minha firme rocha, uma casa fortíssima que me salve.
Porque tu és a minha rocha e a minha fortaleza; por amor do teu nome guia-me e encaminha-me.
Tira-me da rede que para mim ocultaram, pois tu és a minha força.
Nas tuas mãos entrego o meu espírito; tu me remiste, ó Senhor Deus da verdade.
Aborreço os que atentam para vãos ídolos; eu confio no Senhor.
Eu me alegrarei e me regozijarei na tua misericórdia, pois consideraste a minha aflição; conheceste a minha alma nas angústias.
E não me encerraste nas mãos do inimigo; puseste os meus pés em lugar largo.
Tem misericórdia de mim, ó Senhor, que estou angustiado; consumidos estão de tristeza os meus olhos, a minha alma e o meu ventre.
Porque a minha vida está gasta de tristeza, e os meus anos de suspiros; a minha força descai por causa da minha iniquidade, e os meus ossos se consomem.
Por causa de todos os meus inimigos fui o opróbrio dos meus vizinhos, e muito dos meus conhecidos; fugiram de mim os que me veem pela rua.
Estou esquecido deles como um morto; sou como um vaso quebrado.
Porque ouço a murmuração de muitos, temor há ao redor de mim, consultando juntos contra mim, intentam tirar-me a vida.
Mas eu confio em ti, ó Senhor; digo: Tu és o meu Deus.
Os meus tempos estão nas tuas mãos; livra-me das mãos dos meus inimigos e dos que me perseguem.
Faze resplandecer o teu rosto sobre o teu servo; salva-me pela tua misericórdia.
Não me deixes confundido, ó Senhor, pois te invoquei; deixa confundidos os ímpios, emudeçam na sepultura.
Emudeçam os lábios mentirosos, que falam coisas más contra os justos, com soberba e desprezo.
Quão grande é a tua bondade, que guardaste para os que te temem, e que fizeste para os que em ti confiam, diante dos filhos dos homens!
Tu os escondes, no secreto da tua face, da contenda dos homens; tu os ocultas no teu pavilhão da contenda das línguas.
Bendito seja o Senhor, porque fez maravilhosamente a sua misericórdia para comigo numa cidade cercada.
Eu dizia na minha precipitação: Cortado estou diante dos teus olhos; não obstante ouviste a voz das minhas súplicas, quando clamei a ti.
Amai ao Senhor, vós todos os seus santos; o Senhor guarda os fiéis, e retribui abundantemente ao soberbo.
Esforçai-vos, e ele fortalecerá o vosso coração, vós todos os que esperais no Senhor.""",
        "trust",
    ),
    (
        "Salmo 35",
        """Contende, Senhor, com os que contendem comigo; luta contra os que lutam contra mim.
Pega do escudo e da broquel, e levanta-te em minha ajuda.
Tira da lança e do machado o teu adversário; e dize à minha alma: Eu sou a tua salvação.
Sejam confundidos e abatidos os que buscam a minha vida; voltem atrás e confundam-se os que maquinam males contra mim.
Sejam como o moinho diante do vento; e o anjo do Senhor os persiga.
Seja o seu caminho escuro e escorregadio; e o anjo do Senhor os persiga.
Porque sem causa me armaram a sua rede numa cova; sem causa cavaram para a minha alma.
Venha sobre ele destruição não sabida; e a rede que ele ocultou o apanhe; caia nessa mesma destruição.
Então a minha alma se alegrará no Senhor; ela se regozijará na sua salvação.
Todos os meus ossos dirão: Senhor, quem é como tu, que livras o pobre daquele que é mais forte do que ele, sim, o pobre e o necessitado daquele que o rouba?
Maliciosas testemunhas se levantam; de coisas que não sei me perguntam.
Tornam-me mal por bem, para abatimento da minha alma.
Mas, quanto a mim, quando estavam enfermos, vestia saco; humilhava a minha alma com jejum; e a minha oração voltava para o meu seio.
Como se fosse meu amigo ou meu irmão, assim me portava; como quem chora por sua mãe, assim me humilhava de luto.
Mas eles se alegraram na minha adversidade, e se congregaram; congregaram-se contra mim, e eu não o sabia; dilaceravam-me, e não cessavam.
Com hipócritas zombadores em festins, rangeram contra mim os seus dentes.
Senhor, até quando verás isto? Livra a minha alma das suas assolações, e a minha predilecta dos leõezinhos.
Louvar-te-ei na grande congregação; entre muitíssimo povo te louvarei.
Não se alegrem de mim os que são meus inimigos sem causa, nem pisquem os olhos os que me odeiam sem razão.
Porque não falam paz; antes maquinam enganos contra os quietos da terra.
E abrem contra mim a sua boca; dizem: Ah! Ah! os nossos olhos o viram.
Tu o viste, ó Senhor; não te cales; Senhor, não te alongues de mim.
Desperta-te, e acorda para o meu julgamento, para a minha causa, meu Deus e meu Senhor.
Julga-me segundo a tua justiça, Senhor meu Deus, e não se alegrem de mim.
Não digam em seus corações: Ah! alma nossa! Nem digam: Nós o havemos devorado!
Envergonhem-se e confundam-se juntos os que se alegram com o meu mal; cubram-se de vergonha e confusão os que se engrandecem contra mim.
Cantem e alegrem-se os que desejam a minha justiça; e digam continuamente: O Senhor seja engrandecido, o qual deseja a paz do seu servo.
E a minha língua falará da tua justiça e do teu louvor todo o dia.""",
        "cry",
    ),
    (
        "Salmo 36",
        """A transgressão do ímpio diz ao meu íntimo: Não há temor de Deus diante dos seus olhos.
Porque lisonjeia a si mesmo aos seus olhos, até que a sua iniquidade se descubra ser detestável.
As palavras da sua boca são malícia e engano; deixou de ser sábio e de fazer o bem.
Maquina a malícia na sua cama; põe-se no caminho que não é bom; não aborrece o mal.
Senhor, a tua benignidade chega até aos céus, e a tua fidelidade até às nuvens.
A tua justiça é como as grandes montanhas; os teus juízos são um grande abismo; tu, Senhor, conservas a homens e a animais.
Quão preciosa é, ó Deus, a tua benignidade! por isso os filhos dos homens se acolhem à sombra das tuas asas.
Eles se fartarão da gordura da tua casa, e os farás beber da corrente das tuas delícias.
Porque em ti está o manancial da vida; na tua luz veremos a luz.
Estende a tua benignidade sobre os que te conhecem, e a tua justiça sobre os retos de coração.
Não venha sobre mim o pé da soberba, e não me mova a mão dos ímpios.
Ali caem os que obram iniquidade; são derribados e não se podem levantar.""",
        "trust",
    ),
    (
        "Salmo 38",
        """Senhor, não me repreendas na tua ira, nem me castigues no teu furor.
Porque as tuas flechas se cravaram em mim, e a tua mão sobre mim pesadamente desceu.
Não há coisa sã na minha carne, por causa da tua indignação; nem há paz nos meus ossos, por causa do meu pecado.
Porque as minhas iniquidades subiram sobre a minha cabeça; como carga pesada são demais para mim.
As minhas chagas cheiram mal e supuram, por causa da minha loucura.
Estou abatido e muito humilhado; ando de luto todo o dia.
Porque as minhas ilhargas estão cheias de ardor, e não há coisa sã na minha carne.
Estou esmorecido e abatido sobremodo; rugo pela agitação do meu coração.
Senhor, diante de ti está todo o meu desejo, e o meu suspiro não te é oculto.
O meu coração palpita, as minhas forças me faltam; quanto à luz dos meus olhos, ela me deixou.
Os meus amigos e os meus companheiros se afastam da minha praga; e os meus parentes se põem longe.
Também os que buscam a minha vida me armam ciladas, e os que procuram o meu mal dizem coisas que me podem danar, e imaginam enganos todo o dia.
Mas eu, como surdo, não ouvia, e, como mudo, não abria a boca.
Assim fui como quem não ouve, e em cuja boca não há reprovações.
Porque em ti, Senhor, espero; tu me ouvirás, Senhor meu Deus.
Porque dizia eu: Ouve-me, para que não se alegrem de mim; quando resvalam os meus pés, eles se engrandecem contra mim.
Porque eu estou prestes a cair, e a minha dor está sempre diante de mim.
Porque confessarei a minha iniquidade; estar-me-ei ansioso por causa do meu pecado.
Mas os meus inimigos são vivazes e fortes, e os que sem razão me odeiam se multiplicam.
Os que retribuem mal por bem são meus adversários, porquanto sigo o que é bom.
Não me desampares, Senhor, meu Deus; não te alongues de mim.
Apressa-te em socorrer-me, Senhor, minha salvação.""",
        "repentance",
    ),
    (
        "Salmo 39",
        """Eu disse: Guardarei os meus caminhos, para não pecar com a minha língua; guardarei a minha boca com freio, enquanto os ímpios estiverem diante de mim.
Emudeci-me em silêncio; calava-me acerca do bem, e a minha dor redobrou.
Aqueceu-se-me o coração dentro de mim; enquanto eu meditava acendeu-se o fogo; então falei com a minha língua:
Faze-me saber, Senhor, o meu fim, e qual a medida dos meus dias, para que eu sinta quanto sou frágil.
Eis que fizeste os meus dias como a palmos diante de ti; a minha idade é como nada diante de ti; na verdade todo homem em seu melhor estado é totalmente vaidade.
Na verdade cada um anda em uma vaidade; na verdade em vão se inquieta; ajunta tesouros, e não sabe quem os levará.
E agora, Senhor, que espero eu? A minha esperança está em ti.
Livra-me de todas as minhas transgressões; não me faças o opróbrio dos loucos.
Emudeci-me, não abri a minha boca, porque tu o fizeste.
Tira de sobre mim a tua praga; estou consumido pela correção da tua mão.
Quando com repreensões castigas alguém por causa da iniquidade, fazes com que as suas formosuras se consumam como traça; assim é vaidade todo homem.
Ouve, Senhor, a minha oração, e inclina os teus ouvidos ao meu clamor; não te cales perante as minhas lágrimas, porque sou estrangeiro contigo e peregrino, como todos os meus pais.
Desvia de mim a tua praga, antes que eu me vá, e não exista mais.""",
        "cry",
    ),
    (
        "Salmo 41",
        """Bem-aventurado é aquele que acode ao necessitado; o Senhor o livrará no dia mau.
O Senhor o guardará, e o conservará vivo; será bem-aventurado na terra; tu não o entregarás à vontade dos seus inimigos.
O Senhor o fortalecerá sobre o leito da enfermidade; tu o restaurarás da sua doença.
Eu disse: Senhor, tem misericórdia de mim; sara a minha alma, porque pequei contra ti.
Os meus inimigos falam mal de mim, dizendo: Quando morrerá, e perecerá o seu nome?
E se algum deles vem visitar-me, diz coisas vãs; no seu coração amontoa maldade; quando sair, é isso que fala.
Todos os que me odeiam murmuram secretamente contra mim; contra mim maquinam o mal, dizendo:
Pestilência maligna se lhe pegou; e o que se deitou não tornará a levantar-se.
Até o meu próprio amigo íntimo, em quem eu confiava, que comia do meu pão, levantou contra mim o calcanhar.
Mas tu, Senhor, tem misericórdia de mim, e levanta-me, para que lhes retribua.
Com isto conhecerei que te agradas de mim, que o meu inimigo não triunfará de mim.
Quanto a mim, tu me susténs na minha sinceridade, e me puseste na tua presença para sempre.
Bendito seja o Senhor Deus de Israel, de eternidade a eternidade. Amém e Amém.""",
        "hope",
    ),
    (
        "Salmo 45",
        """O meu coração trasborda de boa palavra; dirijo os meus versos a um Rei; a minha língua é como a pena de um hábil escrivão.
És formoso, mais do que os filhos dos homens; a graça se derramou nos teus lábios; por isso Deus te abençoou para sempre.
Cinge a tua espada ao teu lado, ó valente, com a tua glória e a tua majestade.
E nesta tua majestade cavalga vitoriosamente pela causa da verdade, da mansidão e da justiça; e a tua destra te ensinará coisas terríveis.
As tuas setas são agudas nos corações dos inimigos do Rei; os povos caem debaixo de ti.
O teu trono, ó Deus, é para sempre; cetro de equidade é o cetro do teu reino.
Amaste a justiça, e odiaste a iniquidade; por isso Deus, o teu Deus, te ungiu com óleo de alegria, mais do que a teus companheiros.
A mirra, o aloés e a cássia perfumeiam todos os teus vestidos; desde os palácios de marfim te alegram.
Entre as tuas damas há filhas de reis; à tua direita está a rainha com ornato de ouro de Ofir.
Ouve, filha, e olha, e inclina os teus ouvidos; esquece-te do teu povo, e da casa de teu pai.
Então o rei desejará a tua formosura; encurva-te a ele, porque ele é teu senhor.
E a filha de Tiro virá com presente; os ricos do povo suplicarão o teu favor.
Toda gloriosa está a filha do rei no seu interior; de ouro é o seu vestido.
Com vestidos bordados será conduzida ao rei; as virgens, suas companheiras que a seguem, te serão trazidas.
Serão levadas com alegria e regozijo; entrarão no palácio do rei.
Em lugar de teus pais estarão teus filhos, de quem te farás príncipes sobre toda a terra.
Eu farei lembrar o teu nome de geração em geração; por isso os povos te louvarão eternamente e para sempre.""",
        "praise",
    ),
    (
        "Salmo 47",
        """Batei palmas, todos os povos; acudi a Deus com voz de triunfo.
Porque o Senhor Altíssimo é terrível, e é o grande Rei sobre toda a terra.
Ele subjugará os povos debaixo de nós, e as nações debaixo dos nossos pés.
Ele nos escolherá a nossa herança, a glória de Jacó, a quem amou.
Deus subiu com júbilo, o Senhor com o som de trombeta.
Cantai louvores a Deus, cantai louvores; cantai louvores ao nosso Rei, cantai louvores.
Porque Deus é o Rei de toda a terra; cantai louvores com entendimento.
Deus reina sobre as nações; Deus se assenta sobre o trono da sua santidade.
Os príncipes dos povos se ajuntam para serem o povo do Deus de Abraão; porque os escudos da terra são de Deus; ele é muito exaltado.""",
        "praise",
    ),
    (
        "Salmo 48",
        """Grande é o Senhor e mui digno de louvor na cidade do nosso Deus, no seu santo monte.
Alegre-se a formosura do seu excelso monte, o monte de Sião para os lados do norte, a cidade do grande Rei.
Nos seus palácios Deus se fez conhecido por alto refúgio.
Porque eis que os reis se ajuntaram; eles juntos passaram adiante.
Eles próprios, vendo-o, ficaram maravilhados; perturbaram-se e fugiram apressadamente.
Ali os agarrou a tremor; dor tomou o que de parturiente é.
Com o vento oriental quebras os navios de Társis.
Como temos ouvido, assim vimos na cidade do Senhor dos Exércitos, na cidade do nosso Deus; Deus a confirma para sempre.
Lembramo-nos, ó Deus, da tua benignidade, no meio do teu templo.
Segundo o teu nome, ó Deus, assim é o teu louvor até aos fins da terra; a tua destra está cheia de justiça.
Alegre-se o monte de Sião; alegrem-se as filhas de Judá por causa dos teus juízos.
Rodeai Sião, e cercai-a; contai as suas torres.
Ponde nos seus antemuros o vosso coração, e considerai os seus palácios, para que o conteis à geração seguinte.
Porque este Deus é o nosso Deus para sempre; ele será nosso guia até à morte.""",
        "praise",
    ),
    (
        "Salmo 49",
        """Ouvi isto, vós todos os povos; inclinai os ouvidos, todos os moradores do mundo,
Tanto humildes como grandes, tanto ricos como pobres.
A minha boca falará de sabedoria; e a meditação do meu coração será de entendimento.
Inclinarei os meus ouvidos a uma parábola; decifrarei o meu enigma na harpa.
Por que temerei eu nos dias maus, quando a iniquidade dos que me seguem me cercar?
Aqueles que confiam na sua fazenda, e se gloriam na multidão das suas riquezas,
Nenhum deles de modo algum pode remir a seu irmão, ou dar a Deus o resgate dele
(Pois a redenção da sua alma é caríssima, e cessará para sempre),
Para que viva para sempre e não veja corrupção.
Porque verá que os sábios morrem, assim como o néscio e o bruto perecem, e deixam a outros as suas riquezas.
O seu pensamento íntimo é que as suas casas durarão perpetuamente, e as suas habitações de geração em geração; chamam às suas terras pelos seus próprios nomes.
Todavia o homem que está em honra não permanece; antes é como os animais, que perecem.
Este caminho deles é a sua loucura; contudo a sua posteridade aprova as suas palavras.
Como ovelhas são postos na sepultura; a morte os apascentará; e os justos terão domínio sobre eles pela manhã.
Mas Deus remirá a minha alma do poder da sepultura, pois me receberá.""",
        "wisdom",
    ),
    (
        "Salmo 50",
        """O Deus poderoso, o Senhor, falou, e chamou a terra desde o nascimento do sol até ao seu ocaso.
Desde Sião, perfeição da formosura, resplandece Deus.
Virá o nosso Deus, e não se calará; adiante dele um fogo devorador, e ao redor dele haverá grande tormenta.
Chama os céus lá em cima, e a terra, para julgar o seu povo.
Congregai os meus santos, aqueles que fizeram comigo aliança por sacrifício.
E os céus anunciarão a sua justiça; pois Deus mesmo é o juiz.
Ouve, povo meu, e eu falarei; ó Israel, e eu testificarei contra ti: Eu sou Deus, o teu Deus.
Não te repreenderei pelos teus sacrifícios, ou holocaustos, de contínuo perante mim.
Pois meu é todo animal da selva, e as alimárias sobre milhares de montanhas.
Se eu tivesse fome, não to diria, pois meu é o mundo e a sua plenitude.
Oferece a Deus sacrifício de louvor, e paga ao Altíssimo os teus votos.
E invoca-me no dia da angústia; eu te livrarei, e tu me glorificarás.
Mas ao ímpio diz Deus: Que tens tu que recitar os meus estatutos e que tomar a minha aliança na tua boca,
Pois aborreces a correção e lanças as minhas palavras para detrás de ti?
Quem oferece louvor me glorificará; e ao que bem ordena o seu caminho eu mostrarei a salvação de Deus.""",
        "wisdom",
    ),
    (
        "Salmo 52",
        """Por que te glorias na malícia, ó homem poderoso? A bondade de Deus permanece continuamente.
A tua língua intenta o mal, como uma navalha afiada, traçando enganos.
Amas o mal mais do que o bem, e a mentira mais do que a verdade.
Amas todas as palavras devoradoras, ó língua fraudulenta.
Também Deus te destruirá para sempre; arrebatar-te-á, e desarraigar-te-á da tua habitação, e arrancar-te-á da terra dos viventes.
E os justos o verão, e temerão; e se rirão dele, dizendo:
Eis aqui o homem que não pôs em Deus a sua fortaleza; antes confiou na abundância das suas riquezas, e se fortaleceu na sua maldade.
Mas eu sou como a oliveira verde na casa de Deus; confio na misericórdia de Deus para sempre e eternamente.
Para sempre te louvarei, porque tu o fizeste; e esperarei no teu nome, porque é bom diante dos teus santos.""",
        "trust",
    ),
    (
        "Salmo 53",
        """Disse o néscio no seu coração: Não há Deus. Corromperam-se e cometeram abominável iniquidade; não há quem faça o bem.
Deus olhou desde os céus para os filhos dos homens, para ver se havia algum que entendesse e buscasse a Deus.
Desviaram-se todos, e juntamente se fizeram imundos; não há quem faça o bem, não há nem um sequer.
Acaso não têm conhecimento os que obram iniquidade, os que comem o meu povo como se comessem pão? Não invocam a Deus.
Ali se acharam em grande temor, onde temor não havia, porque Deus espalhou os ossos daquele que se acampou contra ti; tu os confundiste, porque Deus os rejeitou.
Oh, se de Sião viesse a salvação de Israel! Quando Deus fizer voltar os cativos do seu povo, então se regozijará Jacó, e Israel se alegrará.""",
        "wisdom",
    ),
    (
        "Salmo 57",
        """Tem misericórdia de mim, ó Deus, tem misericórdia de mim, pois em ti a minha alma confia; e à sombra das tuas asas me abrigo, até que passem as calamidades.
Clamarei ao Deus Altíssimo, ao Deus que por mim tudo executa.
Ele enviará desde os céus, e me salvará, enquanto o que procura devorar-me me afronta; Deus enviará a sua misericórdia e a sua verdade.
A minha alma está entre leões; e eu jazo entre os que estão abrasados, filhos dos homens, cujos dentes são lanças e flechas, e a sua língua espada afiada.
Sê exaltado, ó Deus, sobre os céus; seja a tua glória sobre toda a terra.
Armaram rede aos meus passos; a minha alma está abatida; cavaram uma cova diante de mim, mas eles mesmos caíram nela.
Preparado está o meu coração, ó Deus, preparado está o meu coração; cantarei e salmodiarei.
Desperta, glória minha; despertai, saltério e harpa; eu mesmo despertarei ao romper da alva.
Louvar-te-ei, Senhor, entre os povos; cantar-te-ei entre as nações.
Pois a tua misericórdia é grande até aos céus, e a tua verdade até às nuvens.
Sê exaltado, ó Deus, sobre os céus; e seja a tua glória sobre toda a terra.""",
        "hope",
    ),
    (
        "Salmo 58",
        """Acaso falais vós deveras justiça, ó congregação? Julgais retamente, ó filhos dos homens?
Antes no coração maquinais perversidades; na terra pesais a violência das vossas mãos.
Alienam-se os ímpios desde a madre; andam errados desde que nasceram, falando mentiras.
Têm veneno semelhante ao veneno da serpente; são como a cobra surda, que tapa os ouvidos,
Para não ouvir a voz dos encantadores, do encantador perito em encantamentos.
Quebra-lhes os dentes na boca, ó Deus; arranca, Senhor, os queixais aos leõezinhos.
Derretam-se como águas que se escoam; quando armarem as suas flechas, fiquem elas como embotadas.
Sejam como a lesma que se derrete e se desfaz, como o aborto de mulher, que nunca viu o sol.
Antes que as vossas panelas sintam o calor dos espinhos, tanto verdes como ardentes, ele os arrebatará como por um redemoinho.
O justo se alegrará quando vir a vingança; lavará os seus pés no sangue do ímpio.
Então dirá o homem: Deveras há uma recompensa para o justo; deveras há um Deus que julga na terra.""",
        "cry",
    ),
    (
        "Salmo 59",
        """Livra-me, meu Deus, dos meus inimigos; defende-me daqueles que se levantam contra mim.
Livra-me dos que praticam a iniquidade, e salva-me dos homens sanguinários.
Porque eis que armam ciladas à minha alma; os poderosos se ajuntam contra mim, sem transgressão minha ou pecado meu, ó Senhor.
Correm e se preparam, sem culpa minha; desperta para me ajudares, e olha.
Tu, pois, Senhor Deus dos Exércitos, Deus de Israel, desperta para visitares todos os gentios; não tenhas misericórdia de nenhum dos que praticam a iniquidade.
Voltam à tarde; dão ganidos como cães, e rodeiam a cidade.
Eis que eles se fazem fortes com a sua boca; espadas estão nos seus lábios; porque dizem: Quem ouve?
Mas tu, Senhor, te rirás deles; zombarás de todos os gentios.
Por causa da sua força, eu te aguardarei; pois Deus é a minha alta defesa.
Deus me enviará a sua misericórdia; Deus me fará ver o meu desejo sobre os meus inimigos.
Não os mates, para que o meu povo se não esqueça; espalha-os pelo teu poder.
Mas eu cantarei a tua força; pela manhã louvarei com alegria a tua misericórdia.
Porque tu tens sido o meu alto refúgio e proteção no dia da minha angústia.
A ti, ó minha força, cantarei louvores; porque Deus é a minha alta defesa e o Deus da minha misericórdia.""",
        "protection",
    ),
    (
        "Salmo 60",
        """Ó Deus, tu nos rejeitaste, tu nos espalhaste; tu te indignaste; volta-te para nós.
Abalaste a terra e a fendeste; sara as suas fendas, pois ela treme.
Fizeste ver ao teu povo duras coisas; fizeste-nos beber o vinho da perturbação.
Deste um estandarte aos que te temem, para o arvorarem no alto por causa da verdade.
Para que os teus amados se livrem, salva com a tua destra e ouve-nos.
Deus disse na sua santidade: Eu me regozijarei; repartirei a Siquém, e medirei o vale de Sucote.
Meu é Gileade, e meu é Manassés; Efraim é a força da minha cabeça; Judá é o meu legislador.
Moabe é a minha bacia de lavar; sobre Edom lançarei o meu sapato; sobre a Filístia jubilarei.
Quem me conduzirá à cidade forte? Quem me guiará até Edom?
Não serás tu, ó Deus, que nos rejeitaste? e não sairás, ó Deus, com os nossos exércitos?
Dá-nos auxílio contra o adversário, pois vão é o socorro do homem.
Em Deus faremos proezas; porque ele é que pisará os nossos inimigos.""",
        "strength",
    ),
    (
        "Salmo 44",
        """Ó Deus, nós ouvimos com os nossos ouvidos, e nossos pais nos têm contado os feitos que realizaste em seus dias, nos tempos da antiguidade.
Como expulsaste os gentios com a tua mão, e os plantaste; como afligiste os povos, e os aumentaste.
Porque não conquistaram a terra pela sua espada, nem o seu braço os salvou; mas a tua destra, e o teu braço, e a luz do teu rosto, porquanto te agradaste deles.
Tu és o meu Rei, ó Deus; ordena salvações para Jacó.
Por ti derrubaremos os nossos inimigos; pelo teu nome pisaremos os que se levantam contra nós.
Pois eu não confiarei no meu arco, nem a minha espada me salvará.
Mas tu nos salvaste dos nossos inimigos, e confundiste os que nos odiavam.
Em Deus nos gloriamos todo o dia, e louvaremos o teu nome para sempre.
Mas agora tu nos rejeitaste e nos confundiste, e não sais com os nossos exércitos.
Tu nos fazes retirar do inimigo, e os que nos odeiam nos tomam como saque.
Porque a tua causa somos entregues como ovelhas para o matadouro, e nos espalhaste entre os gentios.
Levanta-te em nosso auxílio, e resgata-nos por amor da tua benignidade.""",
        "cry",
    ),
    (
        "Salmo 55",
        """Dá ouvidos, ó Deus, à minha oração, e não te escondas da minha súplica.
Atende-me, e ouve-me; lamento na minha queixa, e faço ruído,
Por causa da voz do inimigo e por causa da opressão do ímpio; pois lançam sobre mim iniquidade, e com ira me odeiam.
O meu coração está dorido dentro de mim, e terrores de morte caíram sobre mim.
Temor e tremor vieram sobre mim, e o horror me cobriu.
E eu disse: Ah, se eu tivesse asas como a pomba! Voaria e estaria em descanso.
Eis que fugiria para longe, e ficaria no deserto.
Eu me apressaria a escapar da fúria do vento e da tempestade.
Destrói, Senhor, e divide as suas línguas; pois tenho visto violência e contenda na cidade.
Dia e noite a cercam sobre os seus muros; malícia e trabalho estão no meio dela.
Porque não era um inimigo que me afrontava; então eu o suportaria; nem era o que me odiava que se engrandecia contra mim; então dele me esconderia;
Mas eras tu, homem meu igual, meu guia e meu íntimo amigo.
Nós tínhamos doce comunhão, e andávamos em companhia na casa de Deus.
Eu, porém, invocarei a Deus, e o Senhor me salvará.
Lança o teu cuidado sobre o Senhor, e ele te sustentará; nunca permitirá que o justo seja abalado.""",
        "cry",
    ),
    (
        "Salmo 64",
        """Ouve, ó Deus, a minha voz na minha oração; preserva a minha vida do temor do inimigo.
Esconde-me do secreto conselho dos maus e do tumulto dos que praticam a iniquidade;
Os quais afiaram a sua língua como espada, e armaram para suas flechas palavras amargas,
Para de lugares ocultos atirarem sobre o íntegro; disparam sobre ele repentinamente, e não temem.
Firmam-se em mau intento; falam de armar laços secretamente; dizem: Quem os verá?
Eles apuram as iniquidades; investigam diligentemente; e o íntimo pensamento de cada um e o seu coração é profundo.
Mas Deus disparará sobre eles uma flecha, e de repente serão feridos.
Assim farão com que a sua própria língua se volte contra eles; todos os que os virem fugirã0.
E todos os homens temerão, e anunciarão a obra de Deus, e considerarão atentamente o que fez.
O justo se alegrará no Senhor, e confiará nele; e todos os retos de coração se gloriarão.""",
        "protection",
    ),
    (
        "Salmo 65",
        """A ti, ó Deus, espera o louvor em Sião, e a ti se pagará o voto.
Ó tu que ouves as orações! a ti virá toda a carne.
Iniquidades prevalecem contra mim; mas tu perdoas as nossas transgressões.
Bem-aventurado aquele a quem tu escolhes, e fazes chegar a ti, para que habite em teus átrios; nós seremos satisfeitos da bondade da tua casa e do teu santo templo.
Com coisas tremendas, em justiça nos responderás, ó Deus da nossa salvação, esperança de todos os confins da terra e dos que estão longe sobre o mar.
Tu, que pela tua força estabeleces os montes, cingido de poder;
Que aplacas o ruído dos mares, o ruído das suas ondas, e o tumulto das nações.
Corôas o ano com a tua bondade, e os teus caminhos destilam gordura.
Os pastos do deserto destilam, e os outeiros cingem-se de alegria.
Os campos cobrem-se de rebanhos, e os vales vestem-se de trigo; por isso eles se regozijam e cantam.""",
        "gratitude",
    ),
    (
        "Salmo 66",
        """Louvai a Deus com voz de júbilo, todas as terras.
Cantai a glória do seu nome; dai glória ao seu louvor.
Dizei a Deus: Quão terríveis são as tuas obras! pela grandeza do teu poder se submeterão a ti os teus inimigos.
Toda a terra te adorará, e te cantará salmos; cantará o teu nome.
Vinde, e vede as obras de Deus; é terrível nos seus feitos para com os filhos dos homens.
Converteu o mar em terra seca; passaram o rio a pé; ali nos alegramos nele.
Ele governa eternamente pelo seu poder; os seus olhos estão sobre as nações; os rebeldes não se exaltem.
Bendizei, povos, ao nosso Deus, e fazei ouvir a voz do seu louvor,
O qual sustém com vida a nossa alma, e não consente que os nossos pés vacilem.
Eu entrarei em tua casa com holocaustos; pagar-te-ei os meus votos.
Vinde, ouvi, todos os que temeis a Deus, e eu contarei o que ele fez à minha alma.
Bendito seja Deus, que não rejeitou a minha oração, nem desviou de mim a sua misericórdia.""",
        "praise",
    ),
    (
        "Salmo 67",
        """Deus tenha misericórdia de nós e nos abençoe; e faça resplandecer o seu rosto sobre nós.
Para que se conheça na terra o teu caminho, e em todas as nações a tua salvação.
Louvem-te os povos, ó Deus; louvem-te os povos todos.
Alegrem-se e regozijem-se as nações, pois julgarás os povos com equidade, e governarás as nações sobre a terra.
Louvem-te os povos, ó Deus; louvem-te os povos todos.
Então a terra dará o seu fruto; e Deus, o nosso Deus, nos abençoará.
Deus nos abençoará, e todas as extremidades da terra o temerão.""",
        "gratitude",
    ),
    (
        "Salmo 68",
        """Levante-se Deus, e sejam dissipados os seus inimigos; e fujam diante dele os que o odeiam.
Como se dissipa a fumaça, assim os dissiparás; como a cera se derrete diante do fogo, assim pereçam os ímpios diante de Deus.
Mas alegrem-se os justos; regozijem-se na presença de Deus, e folguem de alegria.
Cantai a Deus, cantai louvores ao seu nome; exaltai aquele que cavalga sobre os céus; seu nome é Senhor; e exultai diante dele.
Pai de órfãos e juiz de viúvas é Deus, no seu lugar santo.
Deus faz que o solitário viva em família; liberta aqueles que estão presos em grilhões; mas os rebeldes habitam em terra seca.
Bendito seja o Senhor, que dia a dia nos carrega de benefícios; o Deus da nossa salvação.
O nosso Deus é o Deus da salvação; e a Deus, o Senhor, pertencem as saídas para escapar da morte.
Cantai a Deus, ó reinos da terra; cantai louvores ao Senhor.
Para que saibais que a tua força é poderosa; dá a tua força ao teu povo; bendito seja Deus!""",
        "strength",
    ),
    (
        "Salmo 69",
        """Salva-me, ó Deus, pois as águas entraram até à minha alma.
Atolo-me em profundo lamaçal, onde se não pode estar em pé; entrei na profundeza das águas, onde a corrente me leva.
Estou cansado de clamar; a minha garganta se secou; os meus olhos desfalecem, esperando o meu Deus.
Os que sem causa me odeiam são mais do que os cabelos da minha cabeça; poderosos são os que procuram destruir-me, sendo meus inimigos sem causa.
Tornei a pagar o que não furtei.
Ó Deus, tu bem conheces a minha insensatez; e os meus pecados não te são encobertos.
Não sejam envergonhados por minha causa aqueles que esperam em ti, ó Senhor Deus dos Exércitos; não sejam confundidos por minha causa aqueles que te buscam, ó Deus de Israel.
Porque por amor de ti tenho suportado afronta; a confusão cobriu o meu rosto.
Pois o zelo da tua casa me devorou, e as afrontas dos que te afrontam caíram sobre mim.
Mas, quanto a mim, a minha oração é a ti, Senhor, num tempo aceitável; ó Deus, ouve-me segundo a grandeza da tua misericórdia.
Livra-me do lamaçal, e não me deixes atolar; seja eu livre dos que me odeiam, e das profundezas das águas.
Louvarei o nome de Deus com cântico, e engrandecê-lo-ei com louvor.""",
        "cry",
    ),
    (
        "Salmo 71",
        """Em ti, Senhor, confio; nunca seja eu confundido.
Livra-me na tua justiça, e faze que eu escape; inclina os teus ouvidos para mim, e salva-me.
Sê tu a minha habitação forte, à qual possa recorrer de contínuo; tu és a minha rocha e a minha fortaleza.
Ó Deus meu, livra-me da mão do ímpio, e da mão do homem injusto e cruel.
Pois tu és a minha esperança, Senhor Deus; tu és a minha confiança desde a minha mocidade.
Não me rejeites no tempo da velhice; quando se for acabando a minha força, não me desampares.
Eu, porém, esperarei de contínuo, e te louvarei cada vez mais.
Ó Deus, não te alongues de mim; ó meu Deus, apressa-te em ajudar-me.
A minha boca relatará a tua justiça e a tua salvação todo o dia.""",
        "trust",
    ),
    (
        "Salmo 72",
        """Ó Deus, dá ao rei os teus juízos e a tua justiça ao filho do rei.
Ele julgará o teu povo com justiça, e aos teus pobres com juízo.
Florescerá o justo em seus dias, e abundância de paz, até que não haja lua.
Dominará de mar a mar e desde o rio até às extremidades da terra.
Os reis de Társis e das ilhas trarão presentes; os reis de Sabá e de Seba oferecerão dons.
Sim, todos os reis se prostrarão perante ele; todas as nações o servirão.
Porque ele livrará ao necessitado quando clamar, como também ao aflito e ao que não tem quem o ajude.
Redimirá a sua alma do engano e da violência; e precioso será o seu sangue aos seus olhos.
Bendito seja o Senhor Deus, o Deus de Israel, que só ele faz maravilhas.
E bendito seja para sempre o seu nome glorioso; e encha-se toda a terra da sua glória. Amém e Amém.""",
        "praise",
    ),
    (
        "Salmo 73",
        """Verdadeiramente bom é Deus para com Israel, para com os limpos de coração.
Quanto a mim, porém, quase que os meus pés resvalaram; pouco faltou para que se desviassem os meus passos.
Pois eu tinha inveja dos soberbos, ao ver a prosperidade dos ímpios.
Até que entrei no santuário de Deus; então entendi eu o fim deles.
Certamente tu os puseste em lugares escorregadios; tu os lanças em ruína.
Mas para mim bom é aproximar-me de Deus; pus a minha confiança no Senhor Deus, para anunciar todas as tuas obras.""",
        "wisdom",
    ),
    (
        "Salmo 74",
        """Ó Deus, por que nos rejeitaste para sempre? Por que se acende a tua ira contra as ovelhas do teu pasto?
Lembra-te da tua congregação, que adquiriste desde a antiguidade.
Levanta os teus passos para as perpétuas assolações; tudo quanto o inimigo tem feito mal no santuário.
Não entregues às feras a alma da tua rolinha; não te esqueças para sempre da vida dos teus aflitos.
Atenta para a aliança; porque os lugares tenebrosos da terra estão cheios de moradas de crueldade.
Levanta-te, ó Deus, pleiteia a tua causa; lembra-te das afrontas que o louco te faz cada dia.
Não te esqueças do clamor dos teus adversários; o tumulto daqueles que se levantam contra ti aumenta continuamente.""",
        "cry",
    ),
    (
        "Salmo 75",
        """A ti, ó Deus, glorificamos, a ti glorificamos, e invocamos o teu nome; as tuas maravilhas o declaram.
Quando eu ocupar o lugar determinado, julgarei retamente.
Porque Deus é o juiz: a um abate, e a outro exalta.
Mas eu anunciarei isto para sempre; cantarei louvores ao Deus de Jacó.
E todas as forças dos ímpios serão quebrantadas, mas as forças dos justos serão exaltadas.""",
        "praise",
    ),
    (
        "Salmo 76",
        """Em Judá é Deus conhecido; o seu nome é grande em Israel.
E em Salém está o seu tabernáculo, e a sua morada em Sião.
Tu és mais ilustre e glorioso do que os montes de presa.
Visto que tu és tremendo, quem poderá estar em pé à tua vista, quando te irares?
Tu fizeste ouvir o juízo desde os céus; a terra tremeu e se aquietou,
Quando Deus se levantou para julgar, para livrar a todos os mansos da terra.
Fazei votos, e pagai-os ao Senhor vosso Deus; tragam presentes ao Tremendo.
Ele ceifará o espírito dos príncipes; é tremendo para com os reis da terra.""",
        "strength",
    ),
    (
        "Salmo 77",
        """Clamei a Deus com a minha voz; a Deus levantei a minha voz, e ele inclinou para mim os ouvidos.
No dia da minha angústia busquei ao Senhor; a minha alma recusava ser consolada.
Lembrava-me de Deus, e me perturbava; queixava-me, e o meu espírito desfalecia.
Disse: Isto é enfermidade minha; mas eu me lembrarei dos anos da destra do Altíssimo.
Recordarei as obras do Senhor; certamente me lembrarei das tuas maravilhas da antiguidade.
O teu caminho, ó Deus, está no santuário; quem é tão grande deus como o nosso Deus?
Tu és o Deus que faz maravilhas; fizeste conhecida a tua força entre os povos.
Com o teu braço remiste o teu povo.
Guiaste o teu povo como a um rebanho pela mão de Moisés e de Arão.""",
        "hope",
    ),
    (
        "Salmo 78",
        """Escutai a minha lei, povo meu; inclinai os ouvidos às palavras da minha boca.
Abrirei a minha boca numa parábola; proporei enigmas da antiguidade.
O que ouvimos e aprendemos, e o que nossos pais nos contaram,
Não o encobriremos aos seus filhos, contando à geração futura os louvores do Senhor e a sua força, e as maravilhas que fez.
Todavia, eles se esqueceram das suas obras, e das maravilhas que lhes fizera ver.
Mas ele, misericordioso, perdoou a iniquidade, e não os destruiu.
E conduziu o seu povo como ovelhas, e os guiou pelo deserto como a um rebanho.
E os levou à fronteira da sua santidade, ao monte que a sua destra adquiriu.""",
        "wisdom",
    ),
    (
        "Salmo 79",
        """Ó Deus, as nações entraram na tua herança; profanaram o teu santo templo; reduziram Jerusalém a montões.
Deram os cadáveres dos teus servos por comida às aves dos céus, e a carne dos teus santos às alimárias da terra.
Derramaram o sangue deles como água em redor de Jerusalém, e não houve quem os sepultasse.
Até quando, Senhor? Indignar-te-ás para sempre?
Ajuda-nos, ó Deus da nossa salvação, por amor da glória do teu nome; e livra-nos, e perdoa os nossos pecados por amor do teu nome.
Então nós, teu povo e ovelhas do teu pasto, te louvaremos eternamente; de geração em geração cantaremos o teu louvor.""",
        "cry",
    ),
    (
        "Salmo 80",
        """Ó Pastor de Israel, dá ouvidos; tu, que guias a José como a um rebanho, que estás entre os querubins, resplandece.
Desperta o teu poder, e vem salvar-nos.
Ó Deus, faze-nos voltar, e faze resplandecer o teu rosto, e seremos salvos.
Até quando te indignarás contra a oração do teu povo?
Tu os sustentaste com pão de lágrimas, e lhes deste a beber lágrimas em abundância.
Restaura-nos, ó Deus dos Exércitos; faze resplandecer o teu rosto, e seremos salvos.""",
        "hope",
    ),
    (
        "Salmo 81",
        """Cantai a Deus, nossa fortaleza; jubilai ao Deus de Jacó.
Tomai o saltério, e trazei o adufe, a harpa suave e o saltério.
Tocai a trombeta na lua nova, no tempo determinado da nossa solenidade.
Porque isto é um estatuto para Israel, e uma ordenança do Deus de Jacó.
Eu sou o Senhor teu Deus, que te tirei da terra do Egito; abre bem a tua boca, e eu a encherei.
Mas o meu povo não quis ouvir a minha voz; e Israel não me quis.
Oh, se o meu povo me ouvira! se Israel andasse nos meus caminhos!
Eu o sustentaria com o trigo mais fino, e o saciaria com o mel da rocha.""",
        "praise",
    ),
    (
        "Salmo 82",
        """Deus está na congregação dos poderosos; julga no meio dos deuses.
Até quando julgareis injustamente, e aceitareis a aparência dos ímpios?
Defendei o pobre e o órfão; fazei justiça ao aflito e necessitado.
Livrai o pobre e o necessitado; tirai-os das mãos dos ímpios.
Eu disse: Vós sois deuses, e todos vós filhos do Altíssimo.
Todavia morrereis como homens, e caireis como qualquer dos príncipes.
Levanta-te, ó Deus, julga a terra; pois tu possuis todas as nações.""",
        "wisdom",
    ),
    (
        "Salmo 83",
        """Ó Deus, não estejas em silêncio; não te cales nem te aquietes, ó Deus.
Porque eis que os teus inimigos fazem tumulto, e os que te odeiam levantaram a cabeça.
Consultam astutamente contra o teu povo, e conspiram contra os teus protegidos.
Dize-lhes: Fazei-os como a roda; como a palha diante do vento.
Enche os seus rostos de vergonha, para que busquem o teu nome, Senhor.
Para que saibam que tu, cujo nome é Senhor, és o Altíssimo sobre toda a terra.""",
        "cry",
    ),
    (
        "Salmo 85",
        """Abençoaste, Senhor, a tua terra; fizeste voltar os cativos de Jacó.
Perdoaste a iniquidade do teu povo; cobriste todos os seus pecados.
Faze-nos voltar, ó Deus da nossa salvação, e faze cessar a tua ira de sobre nós.
Mostra-nos, Senhor, a tua misericórdia, e concede-nos a tua salvação.
Certamente que a sua salvação está perto daqueles que o temem, para que a glória habite em nossa terra.
A misericórdia e a verdade se encontraram; a justiça e a paz se beijaram.
A verdade brotará da terra, e a justiça olhará desde os céus.
Também o Senhor dará o bem, e a nossa terra dará o seu fruto.
A justiça irá adiante dele, e nos porá no caminho dos seus passos.""",
        "hope",
    ),
    (
        "Salmo 87",
        """O seu fundamento está nos montes santos.
O Senhor ama as portas de Sião mais do que todas as habitações de Jacó.
Coisas gloriosas se dizem de ti, ó cidade de Deus.
E de Sião se dirá: Este e aquele nasceram nela; e o mesmo Altíssimo a estabelecerá.
E cantores e tocadores de instrumentos estarão ali; todas as minhas fontes estão em ti.""",
        "praise",
    ),
    (
        "Salmo 88",
        """Ó Senhor Deus da minha salvação, diante de ti tenho clamado de dia e de noite.
Chegue a minha oração à tua presença; inclina os teus ouvidos ao meu clamor.
Porque a minha alma está cheia de angústias, e a minha vida se aproxima da sepultura.
Puseste-me no mais profundo do abismo, em trevas e nas profundezas.
Sobre mim pesa a tua ira; tu me afligiste com todas as tuas ondas.
Mas eu, Senhor, a ti tenho clamado; de madrugada te antecipará a minha oração.
Ó Senhor, por que rejeitas a minha alma? por que escondes de mim o teu rosto?
Estou aflito e prestes a morrer desde a mocidade; tenho sofrido os teus terrores e estou perturbado.""",
        "cry",
    ),
    (
        "Salmo 89",
        """As benignidades do Senhor cantarei perpetuamente; com a minha boca manifestarei a tua fidelidade de geração em geração.
Porque disse eu: a tua benignidade será edificada para sempre; nos próprios céus estabelecerás a tua fidelidade.
Tu disseste: Fiz um concerto com o meu escolhido; jurei ao meu servo Davi:
Para sempre estabelecerei a tua descendência, e firmarei o teu trono de geração em geração.
Bem-aventurado o povo que conhece o som festivo; andará, ó Senhor, na luz da tua face.
Porque tu és a glória da sua força; e pelo teu favor será exaltado o nosso poder.
O Senhor é a nossa defesa; e o Santo de Israel é o nosso Rei.
Bendito seja o Senhor para sempre. Amém e Amém.""",
        "praise",
    ),
    (
        "Salmo 94",
        """Ó Senhor Deus, a quem a vingança pertence; ó Deus, a quem a vingança pertence, resplandece.
Exalta-te, tu, que és juiz da terra; dá a paga aos soberbos.
Até quando os ímpios, Senhor, até quando os ímpios saltarão de prazer?
Até quando proferirão, e falarão coisas duras, e se gloriarão todos os que praticam a iniquidade?
Esmagam o teu povo, Senhor, e afligem a tua herança.
Matam a viúva e o estrangeiro, e ao órfão tiram a vida.
Dizem: O Senhor não o verá; nem para isto atentará o Deus de Jacó.
Atendei, ó brutais dentre o povo; e vós, loucos, quando sereis sábios?
O que fez o ouvido não ouvirá? ou o que formou o olho não verá?
O Senhor conhece os pensamentos do homem, que são vaidade.
Bem-aventurado é o homem a quem tu repreendes, ó Senhor, e a quem ensinas a tua lei,
Para lhe dares descanso dos dias maus, até que se abra a cova para o ímpio.
Mas o Senhor não rejeitará o seu povo, nem desamparará a sua herança.
O meu pé dizia: Resvala; a tua misericórdia, Senhor, me susteve.
O Senhor é a minha fortaleza e o meu Deus a rocha do meu refúgio.""",
        "wisdom",
    ),
    (
        "Salmo 97",
        """O Senhor reina; regozije-se a terra; alegrem-se as muitas ilhas.
Nuvens e escuridão estão ao redor dele; justiça e juízo são a base do seu trono.
Um fogo vai adiante dele, e abrasa os seus inimigos em redor.
Os céus anunciam a sua justiça, e todos os povos veem a sua glória.
Porque tu, Senhor, és o Altíssimo sobre toda a terra; muito mais exaltado és do que todos os deuses.
Vós que amais ao Senhor, aborrecei o mal; ele preserva as almas dos seus santos; ele os livra das mãos dos ímpios.
A luz semeia-se para o justo, e a alegria para os retos de coração.
Alegrai-vos, justos, no Senhor, e dai graças à memória da sua santidade.""",
        "praise",
    ),
    (
        "Salmo 98",
        """Cantai ao Senhor um cântico novo, porque ele fez maravilhas; a sua destra e o seu braço santo lhe alcançaram a salvação.
O Senhor fez notória a sua salvação; manifestou a sua justiça perante os olhos dos gentios.
Lembrou-se da sua benignidade e da sua fidelidade para com a casa de Israel; todas as extremidades da terra viram a salvação do nosso Deus.
Celebrai com júbilo ao Senhor, todas as terras; rompei e cantai, e salmodiai.
Salmodiai ao Senhor com harpa; com harpa e voz de canto.
Com trombetas e som de buzinas, exultai perante a face do Senhor, do Rei.
Ruja o mar e a sua plenitude; o mundo e os que nele habitam.
Os rios batam palmas; regozijem-se também as montanhas,
Perante a face do Senhor, porque vem a julgar a terra; com justiça julgará o mundo, e o povo com equidade.""",
        "praise",
    ),
    (
        "Salmo 99",
        """O Senhor reina; tremam os povos. Ele está assentado entre os querubins; comova-se a terra.
O Senhor é grande em Sião, e é excelso sobre todos os povos.
Louvem o teu nome grande e tremendo, pois é santo.
Exalta o Senhor nosso Deus, e prostrai-vos ante o escabelo de seus pés, porque ele é santo.
Exaltai ao Senhor nosso Deus, e prostrai-vos ante o seu santo monte, porque o Senhor nosso Deus é santo.""",
        "praise",
    ),
    (
        "Salmo 101",
        """Cantarei a misericórdia e o juízo; a ti, Senhor, cantarei.
Portar-me-ei com inteligência no caminho reto. Quando virás a mim?
Andarei em minha casa com um coração perfeito.
Não porei coisa má diante dos meus olhos; aborreço as obras daqueles que se desviam; nada disso se pegará a mim.
O coração perverso se apartará de mim; não conhecerei o mal.
Ao que difama o seu próximo às ocultas, eu o destruirei; aquele que tem olhar altivo e coração soberbo não suportarei.
Os meus olhos estarão sobre os fiéis da terra, para que se assentem comigo; o que anda num caminho reto, esse me servirá.
Nenhum enganador habitará dentro da minha casa; o que fala mentiras não estará firme perante os meus olhos.
Pela manhã destruirei todos os ímpios da terra, para cortar da cidade do Senhor todos os que praticam a iniquidade.""",
        "wisdom",
    ),
    (
        "Salmo 102",
        """Senhor, ouve a minha oração, e chegue a ti o meu clamor.
Não escondas de mim o teu rosto no dia da minha angústia; inclina para mim os teus ouvidos; no dia em que eu clamar, ouve-me depressa.
Porque os meus dias se consomem como fumaça, e os meus ossos ardem como um braseiro.
O meu coração está ferido e seco como a erva; até me esqueço de comer o meu pão.
Eu, porém, Senhor, permanecerei para sempre, e a tua memória de geração em geração.
Tu te levantarás e terás piedade de Sião, porque o tempo de te compadeceres dela, o tempo determinado, já chegou.
Porque os teus servos se agradam das suas pedras e se compadecem do seu pó.
As nações temerão o nome do Senhor, e todos os reis da terra a tua glória.
Ele atendeu a oração do desamparado, e não desprezou a sua oração.
Mas tu és o mesmo, e os teus anos nunca terão fim.""",
        "cry",
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
