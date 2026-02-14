"""
Base de dicas de carreira para o canal Dica de Carreira do Dia.
Formato: (tema, texto_da_dica, mood).
"""

DICAS_CARREIRA = [
    (
        "LinkedIn",
        "Atualize seu perfil semanalmente. Perfis ativos têm 5x mais chances de aparecer em buscas e serem vistos por recrutadores. Inclua palavras-chave da sua área e um resumo que mostre resultados.",
        "growth",
    ),
    (
        "Networking",
        "Um café por semana com alguém da área pode mudar sua trajetória. Não peça emprego na primeira conversa. Ofereça valor, compartilhe ideias e construa relacionamentos genuínos.",
        "connection",
    ),
    (
        "Feedback",
        "Peça feedback regularmente. Crescimento vem do que você não vê. Escolha pessoas que você admira e pergunte: o que eu poderia fazer diferente? E agradeça com mente aberta.",
        "growth",
    ),
    (
        "Aprendizado",
        "Quinze minutos por dia em um curso ou leitura já faz diferença em um ano. Consistência bate intensidade. Escolha um tema e mantenha o ritmo.",
        "discipline",
    ),
    (
        "Entrevista",
        "Pesquise a empresa e prepare perguntas. Mostre interesse genuíno pela cultura e pelos desafios. Entrevista é via de mão dupla: você também está escolhendo.",
        "preparation",
    ),
    (
        "Currículo",
        "Um currículo de uma página para menos de dez anos de experiência. Use verbos de ação e números: quantos projetos, quantas pessoas, qual impacto.",
        "clarity",
    ),
    (
        "Salário",
        "Pesquise faixas salariais antes de negociar. Sites como Glassdoor e comunidades da área ajudam. Você não precisa ser o primeiro a dizer um número.",
        "preparation",
    ),
    (
        "Produtividade",
        "Planeje o dia na noite anterior. Três prioridades claras evitam sobrecarga e aumentam foco. Produtividade não é fazer mais, é fazer o que importa primeiro.",
        "discipline",
    ),
    (
        "Foco",
        "Trabalhe em blocos de 50 minutos sem distração. Notificações desligadas são um superpoder moderno. Concentração profunda gera resultados visíveis.",
        "discipline",
    ),
    (
        "Promoção",
        "Se quer ser promovido, comece a agir como o cargo acima. Resolva problemas antes que peçam. Liderança é percebida antes de ser oficial.",
        "growth",
    ),
    (
        "Reputação",
        "Sua reputação é construída em microações: pontualidade, clareza, responsabilidade. Pessoas confiam em quem entrega o combinado.",
        "clarity",
    ),
    (
        "Liderança",
        "Liderar não é controlar, é remover obstáculos. Bons líderes perguntam mais do que ordenam e escutam mais do que falam.",
        "connection",
    ),
    (
        "Erro",
        "Erros viram ativos quando geram aprendizado. Assuma rápido, corrija rápido e documente o que mudou. Maturidade profissional se mostra na recuperação.",
        "growth",
    ),
    (
        "Comunicação",
        "Seja claro e direto. Mensagens longas escondem decisões. Comunicação eficiente economiza tempo e constrói autoridade.",
        "clarity",
    ),
    (
        "Autoridade",
        "Ensine o que você sabe. Compartilhar conhecimento aumenta sua visibilidade e reforça domínio técnico.",
        "growth",
    ),
    (
        "Tempo",
        "Proteja seu tempo como protege dinheiro. Dizer não para tarefas irrelevantes é dizer sim para crescimento real.",
        "discipline",
    ),
    (
        "Confiança",
        "Confiança profissional vem da preparação silenciosa. Estude antes, pratique antes, revise antes. Segurança é construída nos bastidores.",
        "preparation",
    ),
    (
        "Ansiedade",
        "Nervosismo antes de reuniões é normal. Respire, organize três pontos-chave e fale devagar. Clareza reduz ansiedade.",
        "clarity",
    ),
    (
        "Crescimento",
        "Busque ambientes que te desafiem. Conforto prolongado estagna carreira. Desconforto controlado acelera evolução.",
        "growth",
    ),
    (
        "Marca pessoal",
        "Tudo que você publica comunica quem você é. Trate sua presença digital como extensão da sua carreira.",
        "growth",
    ),
    (
        "Aprender rápido",
        "Explique o que aprendeu para outra pessoa. Ensinar consolida conhecimento e revela lacunas.",
        "discipline",
    ),
    (
        "Decisão",
        "Decisões atrasadas custam mais que decisões imperfeitas. Ajuste no caminho, mas avance.",
        "preparation",
    ),
    (
        "Mentoria",
        "Um mentor acelera anos em meses. Procure quem já chegou onde você quer estar.",
        "connection",
    ),
    (
        "Energia",
        "Gerencie energia, não só tempo. Sono, alimentação e pausas impactam desempenho profissional.",
        "discipline",
    ),
    (
        "Prioridade",
        "Se tudo é urgente, nada é importante. Hierarquia de tarefas define sucesso diário.",
        "clarity",
    ),
    (
        "Visibilidade",
        "Trabalho invisível raramente é reconhecido. Documente resultados e comunique conquistas com dados.",
        "growth",
    ),
    (
        "Aprendizado contínuo",
        "Carreira não tem linha de chegada. Atualização constante é requisito, não diferencial.",
        "growth",
    ),
    (
        "Coragem",
        "Converse sobre oportunidades antes de se sentir 100% pronto. Crescimento exige exposição controlada.",
        "transition",
    ),
    (
        "Rotina",
        "Rotinas simples vencem talentos inconsistentes. Pequenos hábitos constroem grandes trajetórias.",
        "discipline",
    ),
    (
        "Clareza de meta",
        "Quem não define direção aceita qualquer destino. Escreva metas específicas e revisite semanalmente.",
        "clarity",
    ),
    (
        "Relacionamento",
        "Trate colegas com respeito constante. Mercado é menor do que parece e reputações circulam rápido.",
        "connection",
    ),
    (
        "Execução",
        "Ideias valem pouco sem execução. Comece imperfeito, mas comece.",
        "growth",
    ),
    (
        "Mudança de área",
        "Transfira habilidades em vez de listar só cargos. Comunicação, gestão de projetos e análise de dados valem em qualquer setor. Conte histórias que provem isso.",
        "transition",
    ),
]

MOOD_TO_PALETTE = {
    "growth": "professional_green",
    "connection": "warm_blue",
    "discipline": "focused_gray",
    "preparation": "confident_navy",
    "clarity": "clean_white",
    "transition": "balanced_teal",
}
