"""Processor for Salmo do Dia channel."""

import os
from typing import Dict
from datetime import datetime

from core.video_generator import VideoGenerator
from core.template_engine import TemplateEngine
from core.text_to_speech_enhanced import EnhancedTextToSpeech
from core.image_processor import ImageProcessor


# Salmos completos para conteúdo diário (nome, texto integral)
SALMOS = [
    (
        "Salmo 23",
        """O Senhor é meu pastor; nada me faltará.
Ele me faz repousar em pastos verdejantes. Leva-me às águas tranqüilas.
Refrigera-me a alma. Guia-me pelas veredas da justiça por amor do seu nome.
Ainda que eu ande pelo vale da sombra da morte, não temerei mal algum, porque tu estás comigo; a tua vara e o teu cajado me consolam.
Preparas uma mesa perante mim na presença dos meus inimigos, unges a minha cabeça com óleo; o meu cálice transborda.
Certamente que a bondade e a misericórdia me seguirão todos os dias da minha vida; e habitarei na casa do Senhor por longos dias.""",
    ),
    (
        "Salmo 91",
        """Aquele que habita no esconderijo do Altíssimo, à sombra do Onipotente descansará.
Direi do Senhor: Ele é o meu refúgio e a minha fortaleza, o meu Deus, em quem confio.
Porque ele te livrará do laço do passarinheiro, e da peste perniciosa.
Cobrir-te-á com as suas penas, e debaixo das suas asas te confiarás; a sua verdade será o teu escudo e broquel.
Não temerás espanto noturno, nem seta que voe de dia.
Nem peste que ande na escuridão, nem mortandade que assole ao meio-dia.
Mil cairão ao teu lado, e dez mil à tua direita; mas não chegará a ti.
Somente com os teus olhos contemplarás, e verás a recompensa dos ímpios.
Porque tu, ó Senhor, és o meu refúgio. No Altíssimo fizeste a tua habitação.
Nenhum mal te sucederá, nem praga alguma chegará à tua tenda.
Porque aos seus anjos dará ordem a teu respeito, para te guardarem em todos os teus caminhos.
Eles te sustentarão nas suas mãos, para que não tropeces com o teu pé em pedra.
Pisarás o leão e a cobra; calcarás aos pés o filho do leão e a serpente.
Porquanto tão encarecidamente me amou, eu o livrarei; pô-lo-ei em retiro alto, porque conheceu o meu nome.
Ele me invocará, e eu lhe responderei; estarei com ele na angústia; livrá-lo-ei e o glorificarei.
Com longura de dias o fartarei, e lhe mostrarei a minha salvação.""",
    ),
    (
        "Salmo 27",
        """O Senhor é a minha luz e a minha salvação; a quem temerei? O Senhor é a fortaleza da minha vida; de quem me recearei?
Quando os malvados, meus adversários e meus inimigos, se chegaram contra mim para comerem as minhas carnes, tropeçaram e caíram.
Ainda que um exército se acampe contra mim, o meu coração não temerá; ainda que a guerra se levante contra mim, nisso confiarei.
Uma coisa pedi ao Senhor, e a buscarei: que possa morar na casa do Senhor todos os dias da minha vida, para contemplar a formosura do Senhor.
Porque no dia da adversidade me esconderá no seu pavilhão; no segredo do seu tabernáculo me esconderá.
E agora será exaltada a minha cabeça acima dos meus inimigos.
Portanto oferecerei no seu tabernáculo sacrifícios de júbilo; cantarei e salmodiarei ao Senhor.
Ouve, ó Senhor, a minha voz com que clamo; tem também piedade de mim, e responde-me.
Não escondas de mim o teu rosto. O Senhor é a minha luz e a minha salvação.""",
    ),
    (
        "Salmo 46",
        """Deus é o nosso refúgio e fortaleza, socorro bem presente na angústia.
Pelo que não temeremos, ainda que a terra se mude, e ainda que os montes se transportem para o meio dos mares.
Ainda que as águas rujam e se perturbem, ainda que os montes se abalem pela sua braveza.
Há um rio cujas correntes alegram a cidade de Deus, o santuário das moradas do Altíssimo.
Deus está no meio dela; não será abalada. Deus a ajudará ao romper da manhã.
Os gentios se embraveceram; os reinos se moveram; ele fez ouvir a sua voz; a terra se derreteu.
O Senhor dos Exércitos está conosco; o Deus de Jacó é o nosso refúgio.
Vinde, contemplai as obras do Senhor. Aquietai-vos e sabei que eu sou Deus.""",
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
    ),
]


def _shorten_for_shorts(texto: str, max_versos: int = 4) -> str:
    """Reduz o salmo para caber no short (primeiros versos)."""
    versos = [v.strip() for v in texto.strip().split("\n") if v.strip()]
    return "\n".join(versos[:max_versos]) if len(versos) > max_versos else texto


class SalmoDiaProcessor:
    """Process and generate content for Salmo do Dia channel."""

    def __init__(self, output_dir: str = "outputs"):
        self.video_generator = VideoGenerator(output_dir)
        self.template_engine = TemplateEngine()
        self.tts = EnhancedTextToSpeech(output_dir, voice="river")
        self.image_processor = ImageProcessor(output_dir)

    def process_salmo(self, generate_videos: bool = True) -> Dict:
        """Process a psalm and generate videos."""
        import random
        salmo_nome, salmo_inteiro = random.choice(SALMOS)
        short_script = f"{salmo_nome}\n\n{_shorten_for_shorts(salmo_inteiro)}"
        long_script = f"{salmo_nome}\n\n{salmo_inteiro}"
        title = f"{salmo_nome} | Salmo do Dia"
        description = f"📖 {salmo_nome}\n\n{salmo_inteiro}\n\n#palavra #reflexão #fé"
        tags = ["salmo", "bíblia", "reflexão", "palavra", "fé", salmo_nome.lower()]

        result = {"title": title, "description": description, "tags": tags}
        if generate_videos:
            print("  [1/6] Gerando áudio do short...", flush=True)
            short_audio = self.tts.generate_audio(short_script)
            print("  [2/6] Gerando áudio do vídeo longo...", flush=True)
            long_audio = self.tts.generate_audio(long_script)
            print("  [3/6] Criando background (cenário bíblico)...", flush=True)
            short_tpl = self.template_engine.get_shorts_template("salmo_dia")
            long_tpl = self.template_engine.get_long_form_template("salmo_dia")
            short_tpl = self.template_engine.apply_text_to_template(short_tpl, short_script, "center")
            long_tpl = self.template_engine.apply_text_to_template(long_tpl, long_script, "center")
            bg = self.image_processor.create_professional_background(
                (1920, 1080),
                keyword="biblical scene holy land Jerusalem ancient shepherd pasture sacred",
                palette="elegant",
                output_path=os.path.join(self.video_generator.output_dir, "salmo_bg.jpg")
            )
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            print("  [4/6] Renderizando short (pode levar 1-2 min)...", flush=True)
            short_path = self.video_generator.create_shorts_video(
                short_script, [bg], short_audio, short_tpl, f"salmo_short_{ts}.mp4"
            )
            print("  [5/6] Renderizando vídeo longo (pode levar 2-3 min)...", flush=True)
            long_path = self.video_generator.create_long_form_video(
                long_script, [bg], long_audio, long_tpl, f"salmo_long_{ts}.mp4"
            )
            result["short_video_path"] = short_path
            result["video_path"] = long_path
            print("  [6/6] Vídeos gerados.", flush=True)
        return result
