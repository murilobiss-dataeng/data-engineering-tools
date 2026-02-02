#!/usr/bin/env python3
"""
YouTube Content Automation - Múltiplos canais

Canais (config em config/channels.yaml):
  - salmo_dia: Salmo do Dia – salmos e passagens da Bíblia em um só canal
  - curiosidade_dia, dica_carreira_dia, exercicio_dia, explicado_shorts,
    motivacao_dia, placar_dia, quanto_rende, receita_dia, series_explicadas

Uso:
  python main.py --channel salmo_dia              # Gera item aleatório (salmo ou passagem)
  python main.py --channel salmo_dia --list       # Lista todo o conteúdo
  python main.py --channel salmo_dia --index 0 --publish
"""

import argparse
import sys
import os
import importlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()


def parse_publish_to(value):
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    from core.publishers import parse_destinations
    return parse_destinations(value.strip())


def print_publish_results(publish_dict):
    if not publish_dict or not isinstance(publish_dict, dict):
        return
    labels = {"youtube": "YouTube", "twitter": "Twitter/X", "kwai": "Kwai", "instagram": "Instagram", "tiktok": "TikTok", "facebook": "Facebook", "linkedin": "LinkedIn"}
    for dest, r in publish_dict.items():
        name = labels.get(dest, dest)
        if isinstance(r, dict) and r.get("url"):
            print(f"\n  {name}: {r.get('url')}")
        elif isinstance(r, dict) and r.get("error"):
            print(f"\n  {name}: ⚠️ {r.get('error')}")


def load_channels_config():
    try:
        import yaml
        path = os.path.join(os.path.dirname(__file__), "config", "channels.yaml")
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
    except Exception:
        pass
    return {"channels": {"salmo_dia": {"id": "salmo_dia", "name": "Salmo do Dia", "enabled": True}}, "default_channel": "salmo_dia"}


def get_available_channels():
    cfg = load_channels_config()
    channels = cfg.get("channels", {})
    return [cid for cid, c in channels.items() if c.get("enabled", True)]


def run_salmo_dia(args):
    """Canal Salmo do Dia: salmos e passagens da Bíblia em um só canal."""
    from channels.salmo_dia.channel_processor import SalmoDiaProcessor

    if args.list:
        SalmoDiaProcessor.list_available_salmos()
        return

    if args.info is not None:
        info = SalmoDiaProcessor.get_salmo_info(args.info)
        if info:
            print(f"\n{'='*60}")
            print(f"  [{info.get('content_type', 'salmo')}] {info['nome']}")
            print(f"{'='*60}")
            print(f"  Mood: {info['mood']} | Paleta: {info['palette']}")
            print(f"  Versos: {info['num_versos']}")
            print(f"\n{info['texto']}")
            print(f"{'='*60}\n")
        else:
            print(f"❌ Índice {args.info} não encontrado")
        return

    processor = SalmoDiaProcessor(output_dir=args.output)
    print("\n" + "="*60)
    print("  SALMO DO DIA – Salmos e passagens da Bíblia")
    print("="*60 + "\n")

    publish_dest = parse_publish_to(getattr(args, "publish_to", None))
    if args.publish:
        result = processor.process_and_publish(
            salmo_index=args.index,
            publish_destinations=publish_dest
        )
    else:
        result = processor.process_salmo(
            generate_videos=True,
            salmo_index=args.index
        )

    print("\n" + "="*60)
    print("  RESULTADO")
    print("="*60)
    print(f"\n📖 {result.get('psalm_name')}")
    print(f"🎨 Paleta: {result.get('palette')}")
    print(f"\n📹 Vídeo: {result.get('short_video_path')}")
    print_publish_results(result.get("publish") or (result.get("twitter") and {"twitter": result["twitter"]}))
    print("\n" + "="*60 + "\n")


def run_generic_channel(args):
    """Carrega o processador do canal a partir de config e executa (sem --list/--info)."""
    cfg = load_channels_config()
    chan = cfg.get("channels", {}).get(args.channel)
    if not chan or not chan.get("processor"):
        print(f"❌ Canal '{args.channel}' sem processor em config/channels.yaml")
        sys.exit(1)
    spec = chan["processor"]
    try:
        mod_path, class_name = spec.rsplit(":", 1)
        mod = importlib.import_module(mod_path)
        ProcessorClass = getattr(mod, class_name)
        processor = ProcessorClass(output_dir=args.output)
        if hasattr(processor, "process_curiosidade"):
            result = processor.process_curiosidade(generate_videos=True)
        elif hasattr(processor, "process_dica"):
            result = processor.process_dica(generate_videos=True)
        elif hasattr(processor, "process_exercicio"):
            result = processor.process_exercicio(generate_videos=True)
        elif hasattr(processor, "process_topic"):
            result = processor.process_topic(generate_videos=True)
        elif hasattr(processor, "process_motivacao"):
            result = processor.process_motivacao(generate_videos=True)
        elif hasattr(processor, "process_match"):
            result = processor.process_match(generate_videos=True)
        elif hasattr(processor, "process_investment"):
            result = processor.process_investment(generate_videos=True)
        elif hasattr(processor, "process_receita"):
            result = processor.process_receita(generate_videos=True)
        elif hasattr(processor, "process_series"):
            result = processor.process_series(generate_videos=True)
        else:
            print(f"❌ Processador de '{args.channel}' não expõe método process_* conhecido.")
            sys.exit(1)
        print("\n  Resultado:", result.get("short_video_path") or result.get("video_path") or result)
    except Exception as e:
        print(f"❌ Erro ao executar canal '{args.channel}': {e}")
        sys.exit(1)


def main():
    channels = get_available_channels()
    default = load_channels_config().get("default_channel", "salmo_dia")

    parser = argparse.ArgumentParser(
        description="YouTube Content Automation - Múltiplos canais",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python main.py --channel salmo_dia
  python main.py --channel salmo_dia --list
  python main.py --channel salmo_dia --index 0 --publish --publish-to youtube,twitter
        """
    )
    parser.add_argument("--channel", "-c", choices=channels, default=default, help=f"Canal (padrão: {default})")
    parser.add_argument("--list", "-l", action="store_true", help="Lista conteúdo do canal")
    parser.add_argument("--index", "-i", type=int, default=None, help="Índice do item (use --list)")
    parser.add_argument("--publish", "-p", action="store_true", help="Publica nos destinos escolhidos")
    parser.add_argument("--publish-to", type=str, default=None, metavar="DESTINOS", help="youtube,twitter,kwai,instagram,tiktok,facebook,linkedin ou all")
    parser.add_argument("--output", "-o", type=str, default="outputs", help="Diretório de saída")
    parser.add_argument("--info", type=int, default=None, help="Mostra informações de um item")

    args = parser.parse_args()

    if args.channel == "salmo_dia":
        run_salmo_dia(args)
    else:
        if args.list or args.info is not None:
            print(f"  Canal '{args.channel}': --list e --info disponíveis apenas para salmo_dia.")
        run_generic_channel(args)


if __name__ == "__main__":
    main()
