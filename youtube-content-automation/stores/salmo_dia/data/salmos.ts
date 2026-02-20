export interface Salmo {
  id: string;
  slug: string;
  titulo: string;
  numero: number;
  texto: string;
  tema: string;
  dataPublicacao: string;
}

export const salmos: Salmo[] = [
  {
    id: "1",
    slug: "salmo-23",
    titulo: "O Senhor é meu pastor",
    numero: 23,
    tema: "Confiança",
    dataPublicacao: "2025-01-15",
    texto: `O Senhor é meu pastor; nada me faltará.
Ele me faz repousar em pastos verdejantes.
Leva-me às águas tranquilas.
Refrigera-me a alma.
Guia-me pelas veredas da justiça por amor do seu nome.
Ainda que eu ande pelo vale da sombra da morte, não temerei mal algum, porque tu estás comigo.
A tua vara e o teu cajado me consolam.
Preparas uma mesa perante mim na presença dos meus inimigos.
Unges a minha cabeça com óleo; o meu cálice transborda.
Certamente que a bondade e a misericórdia me seguirão todos os dias da minha vida.
E habitarei na casa do Senhor por longos dias.`,
  },
  {
    id: "2",
    slug: "salmo-91",
    titulo: "Aquele que habita no esconderijo",
    numero: 91,
    tema: "Proteção",
    dataPublicacao: "2025-01-16",
    texto: `Aquele que habita no esconderijo do Altíssimo, à sombra do Onipotente descansará.
Direi do Senhor: Ele é o meu refúgio e a minha fortaleza, o meu Deus, em quem confio.
Porque ele te livrará do laço do passarinheiro, e da peste perniciosa.
Cobrir-te-á com as suas penas, e debaixo das suas asas te confiarás.
A sua verdade será o teu escudo e broquel.
Não temerás espanto noturno, nem seta que voe de dia.
Mil cairão ao teu lado, e dez mil à tua direita; mas não chegará a ti.
Somente com os teus olhos contemplarás, e verás a recompensa dos ímpios.
Porque tu, ó Senhor, és o meu refúgio. No Altíssimo fizeste a tua habitação.`,
  },
  {
    id: "3",
    slug: "salmo-121",
    titulo: "Levantarei os meus olhos para os montes",
    numero: 121,
    tema: "Socorro",
    dataPublicacao: "2025-01-17",
    texto: `Levantarei os meus olhos para os montes, de onde vem o meu socorro.
O meu socorro vem do Senhor, que fez o céu e a terra.
Não deixará vacilar o teu pé; aquele que te guarda não dormitará.
Eis que não dormitará nem dormirá aquele que guarda a Israel.
O Senhor é quem te guarda; o Senhor é a tua sombra à tua mão direita.
O sol não te molestará de dia nem a lua de noite.
O Senhor te guardará de todo o mal; guardará a tua alma.
O Senhor guardará a tua entrada e a tua saída, desde agora e para sempre.`,
  },
  {
    id: "4",
    slug: "salmo-27",
    titulo: "O Senhor é a minha luz",
    numero: 27,
    tema: "Esperança",
    dataPublicacao: "2025-01-18",
    texto: `O Senhor é a minha luz e a minha salvação; a quem temerei?
O Senhor é a fortaleza da minha vida; de quem me recearei?
Quando os malvados avançaram contra mim para comerem as minhas carnes, tropeçaram e caíram.
Ainda que um exército se acampe contra mim, o meu coração não temerá.
Ainda que a guerra se levante contra mim, nisso confiarei.
Uma coisa pedi ao Senhor, e a buscarei: que possa morar na casa do Senhor todos os dias da minha vida.
Para contemplar a formosura do Senhor e meditar no seu templo.
Espera no Senhor, anima-te, e ele fortalecerá o teu coração; espera, pois, no Senhor.`,
  },
  {
    id: "5",
    slug: "salmo-46",
    titulo: "Deus é o nosso refúgio",
    numero: 46,
    tema: "Refúgio",
    dataPublicacao: "2025-01-19",
    texto: `Deus é o nosso refúgio e fortaleza, socorro bem presente na angústia.
Pelo que não temeremos, ainda que a terra se mude.
E ainda que os montes se transportem para o meio dos mares.
Ainda que as águas rujam e se perturbem, ainda que os montes se abalem pela sua braveza.
Há um rio cujas correntes alegram a cidade de Deus, o santuário das moradas do Altíssimo.
Deus está no meio dela; não será abalada. Deus a ajudará ao romper da manhã.
Aquietai-vos e sabei que eu sou Deus.
O Senhor dos Exércitos está conosco; o Deus de Jacó é o nosso refúgio.`,
  },
];

export function getSalmoBySlug(slug: string): Salmo | undefined {
  return salmos.find((s) => s.slug === slug);
}

export function getSalmosRecentes(limit = 5): Salmo[] {
  return [...salmos]
    .sort((a, b) => b.dataPublicacao.localeCompare(a.dataPublicacao))
    .slice(0, limit);
}

/** Salmo do dia (mock: primeiro da lista como "hoje") */
export function getSalmoDoDia(): Salmo {
  return salmos[0];
}
