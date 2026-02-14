#!/usr/bin/env python3
"""
YouTube Content Automation - Múltiplos canais

Uso (salmo_dia):
  python main.py salmo_dia                           # Apenas monta o vídeo (não publica)
  python main.py salmo_dia --upload                  # Gera e publica no YouTube
  python main.py salmo_dia --upload youtube twitter  # Publica no YouTube e no Twitter
  python main.py salmo_dia --upload youtube,twitter 16.02.26 09   # Destinos + agendar 16/02 9h
  python main.py salmo_dia --list                    # Lista conteúdo
  python main.py salmo_dia --index 0                 # Usa item no índice 0
  python main.py salmo_dia --upload youtube 16.02.26 09 --dry-run   # Dry-run com destinos

Agenda (vários canais/datas):
  python main.py agenda.txt                   # Um post por linha: canal  data  hora
  python main.py agenda.yaml                  # YAML com posts (channel, date, time)
  Canal por variável:  CANAL=salmo_dia python main.py --upload 16.02.2026 09
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
    labels = {"youtube": "YouTube", "twitter": "Twitter/X", "kwai": "Kwai", "instagram": "Instagram", "tiktok": "TikTok", "facebook": "Facebook", "linkedin": "LinkedIn", "pinterest": "Pinterest"}
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


def _normalize_date(s):
    """DD.MM.AAAA ou DD-MM-AA → DD/MM/AAAA."""
    if not s or not s.strip():
        return None
    s = s.strip().replace("-", "/").replace(".", "/")
    parts = s.split("/")
    if len(parts) != 3:
        return None
    d, m, y = parts[0], parts[1], parts[2]
    if len(y) == 2:
        y = "20" + y
    return f"{int(d):02d}/{int(m):02d}/{y}"


def _normalize_time(s):
    """09 ou 09:00 → 09:00."""
    if not s or not str(s).strip():
        return "09:00"
    s = str(s).strip()
    if ":" in s:
        return s
    return f"{int(s):02d}:00" if s.isdigit() else "09:00"


def _looks_like_date(token):
    """True se token parece data (ex.: 16.02.26, 16.02.2026, 16/02/26)."""
    if not token or not isinstance(token, str):
        return False
    t = token.strip().replace("-", ".").replace("/", ".")
    parts = t.split(".")
    if len(parts) != 3:
        return False
    return all(p.isdigit() and len(p) <= 4 for p in parts)


def _parse_upload_extra(extra):
    """
    Separa argumentos posicionais após --upload em: destinos, data, hora.
    Ex.: ['youtube', 'twitter', '16.02.26', '09'] -> (['youtube', 'twitter'], '16/02/2026', '09:00')
    Ex.: ['16.02.26', '09'] -> ([], '16/02/2026', '09:00')
    Ex.: ['youtube'] -> (['youtube'], None, None)
    """
    if not extra:
        return [], None, None
    i = 0
    while i < len(extra) and not _looks_like_date(extra[i]):
        i += 1
    dest_tokens = [t.strip() for t in extra[:i] if t and str(t).strip()]
    date_str = _normalize_date(extra[i]) if i < len(extra) else None
    time_str = _normalize_time(extra[i + 1]) if i + 1 < len(extra) else "09:00"
    return dest_tokens, date_str, time_str


def _schedule_at_from_date_time(date_str, time_str):
    """Converte data (DD/MM/AAAA) e hora (HH:MM) em ISO para publishAt."""
    from datetime import datetime
    if not date_str:
        return None
    try:
        parts = date_str.strip().split("/")
        if len(parts) != 3:
            return None
        day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
        t = (time_str or "09:00").strip().replace(":", " ")
        sp = t.split()
        hour = int(sp[0]) if sp else 9
        minute = int(sp[1]) if len(sp) > 1 else 0
        local = datetime(year, month, day, hour, minute)
        if hasattr(datetime.now(), "astimezone") and datetime.now().astimezone().tzinfo:
            local = local.replace(tzinfo=datetime.now().astimezone().tzinfo)
        return local.isoformat()
    except (ValueError, IndexError):
        return None


def _cron_line(channel, date_str, time_str):
    """Gera linha de crontab para rodar o main nessa data/hora (minuto hora dia mês dia_semana)."""
    from datetime import date
    try:
        day, month, year = map(int, date_str.strip().split("/"))
        t = (time_str or "09:00").strip().replace(":", " ").split()
        hour = int(t[0]) if t else 9
        minute = int(t[1]) if len(t) > 1 else 0
        d = date(year, month, day)
        wday = (d.weekday() + 1) % 7  # 0-6 dom-sáb para cron
        root = os.path.dirname(os.path.abspath(__file__))
        cmd = f"cd {root} && {sys.executable} main.py {channel} --upload {date_str.replace('/', '.')} {hour}"
        return f"{minute} {hour} {day} {month} {wday} {cmd}"
    except Exception:
        return ""


def _load_agenda_txt(path):
    """Carrega agenda de arquivo .txt: uma linha por post (canal  data  hora)."""
    posts = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 3:
                posts.append({"channel": parts[0], "date": parts[1], "time": parts[2]})
    return posts


def _load_agenda_yaml(path):
    """Carrega agenda de arquivo .yaml: lista em posts com channel, date, time."""
    try:
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        raw = data.get("posts", data) if isinstance(data, dict) else (data if isinstance(data, list) else [])
        posts = []
        for p in raw or []:
            if isinstance(p, dict):
                ch = p.get("channel") or p.get("canal")
                dt = p.get("date") or p.get("data")
                tm = p.get("time") or p.get("hora", "09")
                if ch and dt:
                    posts.append({"channel": ch, "date": str(dt), "time": str(tm)})
        return posts
    except Exception:
        return []


def run_salmo_dia(args):
    """Canal Salmo do Dia: salmos e passagens da Bíblia em um só canal."""
    from channels.salmo_dia.channel_processor import SalmoDiaProcessor

    # Garantir que upload vá para o canal salmo_dia (não dica_carreira_dia nem outro)
    os.environ["CONTENT_CHANNEL_ID"] = "salmo_dia"

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

    do_upload = getattr(args, "upload", False) or args.publish
    schedule_at = getattr(args, "schedule_at", None)
    dry_run = getattr(args, "dry_run", False)

    if do_upload and dry_run:
        dest_part = (getattr(args, "publish_to") or "").replace(",", " ").strip()
        extra_part = f" {dest_part}" if dest_part else ""
        if schedule_at and "T" in schedule_at:
            ymd = schedule_at.split("T")[0]
            parts = ymd.split("-")
            date_br = f"{parts[2]}/{parts[1]}/{parts[0]}" if len(parts) == 3 else ymd
            time_str = schedule_at.split("T")[1][:5]
            h = time_str.split(":")[0].lstrip("0") or "0"
            print(f"  [dry-run] Comando que seria executado:")
            print(f"    python main.py {args.channel} --upload{extra_part} {date_br.replace('/', '.')} {h}")
            cron = _cron_line(args.channel, date_br, time_str)
            if cron:
                print(f"  Crontab: {cron}")
        else:
            print(f"  [dry-run] python main.py {args.channel} --upload{extra_part}")
        print()
        return

    # Saída sempre em outputs (nunca na root); path absoluto para o canal salmo_dia
    root = os.path.dirname(os.path.abspath(__file__))
    output_dir = args.output if os.path.isabs(args.output) else os.path.join(root, args.output)
    processor = SalmoDiaProcessor(output_dir=output_dir)
    print("\n" + "="*60)
    print("  SALMO DO DIA – Salmos e passagens da Bíblia")
    print("="*60 + "\n")

    publish_dest = parse_publish_to(getattr(args, "publish_to", None)) if do_upload else None

    if do_upload:
        result = processor.process_and_publish(
            salmo_index=args.index,
            publish_destinations=publish_dest or ["youtube"],
            schedule_at=schedule_at,
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
    if do_upload:
        pub = result.get("publish") or {}
        if pub.get("youtube", {}).get("cancelled"):
            print("\n  ⛔ Upload cancelado (conteúdo já publicado).")
        else:
            print_publish_results(pub)
        if schedule_at:
            print(f"\n  📅 Agendado para: {schedule_at}")
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
Exemplos de comando:
  python main.py salmo_dia
      → Só monta o vídeo (não publica)

  python main.py salmo_dia --upload
      → Gera o vídeo e publica no YouTube

  python main.py salmo_dia --upload youtube twitter
      → Publica no YouTube e no Twitter

  python main.py salmo_dia --upload youtube,twitter 16.02.2026 09
      → Publica no YouTube e Twitter e programa para 16/02/2026 às 9h

  python main.py salmo_dia --upload youtube 16.02.2026 09 --dry-run
      → Dry-run: mostra comando e crontab (não executa)

  python main.py salmo_dia --list
      → Lista todo o conteúdo (salmos e passagens)

  python main.py salmo_dia --index 0 --upload youtube
      → Usa o item no índice 0 e publica no YouTube

  python main.py agenda.txt
  python main.py config/agenda-exemplo.yaml
      → Processa agenda (vários canais/datas, um post por linha ou YAML)

  CANAL=salmo_dia python main.py --upload 16.02.2026 09
      → Canal vindo da variável de ambiente
        """
    )
    parser.add_argument("channel", nargs="?", default=default, help=f"Canal (ex: salmo_dia, padrão: {default})")
    parser.add_argument("--upload", "-u", action="store_true", help="Publica (opcional: DESTINOS depois, ex. youtube twitter; depois DATA HORA para agendar)")
    parser.add_argument("--list", "-l", action="store_true", help="Lista conteúdo do canal")
    parser.add_argument("--index", "-i", type=int, default=None, help="Índice do item (use --list)")
    parser.add_argument("--publish", "-p", action="store_true", help="Equivalente a --upload")
    parser.add_argument("--publish-to", type=str, default=None, metavar="DESTINOS", help="youtube,twitter,... ou all")
    parser.add_argument("--output", "-o", type=str, default="outputs", help="Diretório de saída")
    parser.add_argument("--info", type=int, default=None, help="Mostra informações de um item")
    parser.add_argument("--dry-run", action="store_true", help="Com --upload: só mostra comando e crontab, não executa")

    args, extra = parser.parse_known_args()

    # Canal pode vir do ambiente (ex.: CANAL=salmo_dia python main.py --upload 16.02.2026 09)
    if not args.channel or args.channel == default:
        args.channel = os.environ.get("CANAL") or os.environ.get("CHANNEL") or args.channel or default

    # Primeiro argumento pode ser arquivo de agenda (agenda.txt ou agenda.yaml)
    if args.channel and os.path.isfile(args.channel):
        agenda_path = args.channel
        if agenda_path.endswith(".yaml") or agenda_path.endswith(".yml"):
            posts = _load_agenda_yaml(agenda_path)
        else:
            posts = _load_agenda_txt(agenda_path)
        if not posts:
            print("Nenhum post na agenda.")
            sys.exit(0)
        root = os.path.dirname(os.path.abspath(__file__))
        for i, p in enumerate(posts):
            ch = p.get("channel", "")
            dt = _normalize_date(p.get("date", "").replace("-", "/").replace(".", "/"))
            tm = _normalize_time(p.get("time", "09"))
            if ch not in channels:
                print(f"  [{i+1}] Canal inválido: {ch}, pulando.")
                continue
            if not dt:
                print(f"  [{i+1}] Data inválida: {p.get('date')}, pulando.")
                continue
            print(f"\n  [{i+1}/{len(posts)}] {ch} em {dt} às {tm}")
            args.channel = ch
            args.upload = True
            args.publish = True
            args.schedule_at = _schedule_at_from_date_time(dt, tm)
            args.dry_run = False
            if ch == "salmo_dia":
                run_salmo_dia(args)
            else:
                run_generic_channel(args)
        return

    # Canal deve ser um dos disponíveis (pode ter vindo como posicional ou default)
    if args.channel not in channels:
        parser.error(f"Canal inválido: '{args.channel}'. Canais: {', '.join(channels)}")

    # Com --upload: posicionais = [DESTINOS] DATA HORA (ex.: youtube twitter 16.02.26 09)
    args.schedule_at = None
    if args.upload or args.publish:
        dest_tokens, date_str, time_str = _parse_upload_extra(extra)
        if dest_tokens:
            # Destinos posicionais: youtube, twitter ou youtube,twitter
            args.publish_to = ",".join(dest_tokens).replace(" ", "")
        if date_str:
            args.schedule_at = _schedule_at_from_date_time(date_str, time_str)
            if args.schedule_at:
                print(f"  📅 Agendando postagem para {date_str} às {time_str}\n")

    if args.channel == "salmo_dia":
        run_salmo_dia(args)
    else:
        if args.list or args.info is not None:
            print(f"  Canal '{args.channel}': --list e --info disponíveis apenas para salmo_dia.")
        run_generic_channel(args)


if __name__ == "__main__":
    main()
