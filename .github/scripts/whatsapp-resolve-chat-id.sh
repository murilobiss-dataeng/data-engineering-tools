#!/usr/bin/env bash
# Resolução de CHAT_ID para GitHub Actions (secrets CHAT_ID_ALL, CHAT_ID_* , CHAT_IDS).
# shellcheck disable=SC2034

# Canal: health | tech | ofertas | faith
# Ordem: CHAT_ID_ALL (linhas mb.CANAL: ou canal:) → CHAT_ID_HEALTH… → CHAT_IDS (health,tech,ofertas,faith).
resolve_chat_id_for_channel() {
  local ch="$1"
  local id=""
  if [ -n "${CHAT_ID_ALL:-}" ]; then
    id=$(printf '%s\n' "$CHAT_ID_ALL" | grep -iE "^[[:space:]]*(mb\.)?${ch}[[:space:]]*:" | head -1 | sed -E 's/^[^:]*:[[:space:]]*//' | tr -d '\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
  fi
  if [ -z "$id" ]; then
    case "$ch" in
      health) id="${CHAT_ID_HEALTH:-}" ;;
      tech) id="${CHAT_ID_TECH:-}" ;;
      ofertas) id="${CHAT_ID_OFERTAS:-}" ;;
      faith) id="${CHAT_ID_FAITH:-}" ;;
    esac
  fi
  if [ -z "$id" ] && [ -n "${CHAT_IDS:-}" ]; then
    local idx=1
    case "$ch" in
      health) idx=1 ;;
      tech) idx=2 ;;
      ofertas) idx=3 ;;
      faith) idx=4 ;;
    esac
    id=$(echo "$CHAT_IDS" | cut -d',' -f"$idx" | tr -d '\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
  fi
  printf '%s' "$id"
}

# Init / QR: qualquer ID válido para o bot listar canais (prioriza CHAT_ID → CHAT_ID_ALL → HEALTH → 1º CHAT_IDS).
resolve_chat_id_for_init() {
  local id=""
  if [ -n "${CHAT_ID:-}" ]; then
    printf '%s' "$CHAT_ID"
    return
  fi
  if [ -n "${CHAT_ID_ALL:-}" ]; then
    id=$(printf '%s\n' "$CHAT_ID_ALL" | grep -iE ':[[:space:]]*.+@' | head -1 | sed -E 's/^[^:]*:[[:space:]]*//' | tr -d '\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    if [ -n "$id" ]; then
      printf '%s' "$id"
      return
    fi
  fi
  if [ -n "${CHAT_ID_HEALTH:-}" ]; then
    printf '%s' "${CHAT_ID_HEALTH}"
    return
  fi
  if [ -n "${CHAT_IDS:-}" ]; then
    id=$(echo "$CHAT_IDS" | cut -d',' -f1 | tr -d '\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    printf '%s' "$id"
    return
  fi
  printf ''
}
