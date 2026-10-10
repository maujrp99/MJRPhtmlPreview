#!/usr/bin/env python3
# cópia carimbada do MJRP Harness · versão 2026-10-09 · fonte 3f3b7ea · não edite aqui — edite no harness e rode `new_project.py --refresh-kernel`
"""session_journal.py -- the AI Platform hooks of S-61: no decision is lost to a context compaction.

Born 2026-10-04: a compaction found the human's latest answers only in the AI Platform's own summary, not in the
repository, and the ## Now of MEMORY.md still described a step already done. Four modes, one per hook:

  precompact   PreCompact: appends to .mjrp/diary/<session>.md what the human said in the session -- their
               messages and the answers to the agent's questions (AskUserQuestion) -- and the skills invoked.
               The diary accumulates across compactions; each item is written once.
  reinject     SessionStart (source compact): prints the ## Now of MEMORY.md, the newest log entries and the tail
               of the diary, so the agent resumes from the repository and not only from the summary.
  gate         Stop: blocks the end of the turn (exit 2) while an answer of the human is newer than the newest
               log entry -- a decision taken and not registered.
  skill        PostToolUse (Skill): appends one line to data/raw/skill-usage.csv (date, time, skill, session) -- the log
               counts editions of a skill, this counts use.

The hooks run only where the AI Platform loads this project's settings (a local session in the project folder). A
cloud session that reaches the project through a bridge does not load them; there the guard is the git hook
commit-msg (log_entry_check.py) and the onboarding rule of registering each decision before moving on.
Hook input is the JSON the AI Platform sends on stdin. Python 3 stdlib only (ADR-0015: core).
"""
import csv
import json
import re
import sys
import zlib
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:
    from zoneinfo import ZoneInfo
    LOCAL = ZoneInfo("America/Sao_Paulo")
except Exception:  # Brasília has no daylight saving time since 2019
    LOCAL = timezone(timedelta(hours=-3))

REMINDER = re.compile(r"<system-reminder>.*?</system-reminder>", re.DOTALL)
ENTRY = re.compile(r"^## \[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\]", re.MULTILINE)
DIARY_ITEM = re.compile(r"<!-- id:([^ ]+) -->")
SENT_AT = re.compile(r"Message sent at \w+ (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) local time")


def local_time(iso):
    if iso.startswith("local:"):  # already in Brasília time (the human's own "sent at")
        return iso[6:]
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(LOCAL).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return "????-??-?? ??:??"


def clean(text):
    return REMINDER.sub("", text or "").strip()


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def read_transcript(path):
    """Yields (id, iso_time, kind, text): kind is 'human', 'answer' or 'skill'."""
    asks = {}
    try:
        lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return
    for line in lines:
        try:
            o = json.loads(line)
        except ValueError:
            continue
        ts, uid, typ = o.get("timestamp", ""), o.get("uuid", ""), o.get("type")
        if typ == "attachment" and (o.get("attachment") or {}).get("type") == "queued_command":
            raw = text_of(o["attachment"].get("prompt"))
            t = clean(raw)
            sent = SENT_AT.search(raw)
            if t and sent:  # a message the platform re-delivers keeps its own "sent at": one item, its real time
                uid, ts = "msg-" + sent.group(1).replace(" ", "T") + "-" + format(zlib.crc32(t.encode("utf-8")), "08x"), "local:" + sent.group(1)
            if t:
                yield uid, ts, "human", t
            continue
        msg = o.get("message") or {}
        content = msg.get("content")
        if typ == "assistant" and isinstance(content, list):
            for b in content:
                if b.get("type") == "tool_use" and b.get("name") == "AskUserQuestion":
                    asks[b.get("id")] = [q.get("question", "") for q in (b.get("input") or {}).get("questions", [])]
                if b.get("type") == "tool_use" and b.get("name") == "Skill":
                    yield b.get("id"), ts, "skill", str((b.get("input") or {}).get("skill", "?"))
        if typ == "user" and not o.get("isMeta"):
            if isinstance(content, list):
                for b in content:
                    if b.get("type") == "tool_result" and b.get("tool_use_id") in asks:
                        yield b.get("tool_use_id"), ts, "answer", clean(text_of(b.get("content")))
            t = clean(text_of(content))
            if t and not t.startswith("This session is being continued from a previous conversation"):
                yield uid, ts, "human", t


def log_file():
    try:
        from log_entry_check import log_path
        return ROOT / log_path(ROOT, "")
    except Exception:
        return ROOT / "docs" / "log.md"


def newest_entry():
    try:
        times = ENTRY.findall(log_file().read_text(encoding="utf-8"))
        return max(times) if times else None
    except OSError:
        return None


def diary_path(session):
    return ROOT / ".mjrp" / "diary" / f"{session or 'unknown'}.md"


def precompact(hook):
    path = diary_path(hook.get("session_id"))
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_text(encoding="utf-8") if path.exists() else f"# Diário da sessão {hook.get('session_id')}\n\n"
    seen = set(DIARY_ITEM.findall(old))
    label = {"human": "MJRP disse", "answer": "MJRP respondeu", "skill": "skill invocada"}
    new = []
    for uid, ts, kind, text in read_transcript(hook.get("transcript_path", "")):
        if uid and uid not in seen:
            seen.add(uid)
            body = text if len(text) <= 4000 else text[:4000] + " […]"
            new.append(f"- **{local_time(ts)}** · {label[kind]}: {body} <!-- id:{uid} -->\n")
    if new:
        path.write_text(old + "".join(new), encoding="utf-8")
    print(f"[session_journal] diário: {len(new)} item(ns) novo(s) em {path.relative_to(ROOT)}")
    return 0


def reinject(hook):
    from doctor import now_section
    out = ["## Retomada depois da compactação (S-61) — o repositório, não só o resumo", ""]
    mem = ROOT / "MEMORY.md"
    if mem.exists():
        body = now_section(mem.read_text(encoding="utf-8")) or []
        out += ["### MEMORY.md — ## Now", *body, ""]
    try:
        log = log_file().read_text(encoding="utf-8")
        parts = re.split(r"(?m)^(?=## \[)", log)[1:4]
        out += [f"### {log_file().relative_to(ROOT)} — as 3 entradas mais recentes", *[p.strip()[:2500] for p in parts], ""]
    except OSError:
        pass
    d = diary_path(hook.get("session_id"))
    if d.exists():
        items = [l for l in d.read_text(encoding="utf-8").splitlines() if l.startswith("- **")]
        out += [f"### Diário da sessão — os últimos {min(30, len(items))} itens ({d.relative_to(ROOT)})",
                *[DIARY_ITEM.sub("", l).rstrip() for l in items[-30:]], ""]
    out.append("Confira se toda resposta do diário mais nova que a última entrada do log está registrada antes de seguir.")
    print("\n".join(out))
    return 0


def gate(hook):
    if hook.get("stop_hook_active"):
        return 0  # already blocked once in this stop; never loop
    newest = newest_entry()
    pending = [(local_time(ts), text) for _, ts, kind, text in read_transcript(hook.get("transcript_path", ""))
               if kind == "answer" and (newest is None or local_time(ts) > newest)]
    if not pending:
        return 0
    first = pending[0]
    print(f"[session_journal] {len(pending)} resposta(s) do humano sem registro no log (a última entrada é de "
          f"{newest or 'nenhuma'}). A primeira, de {first[0]}: {first[1][:300]} — registre cada decisão no "
          f"{log_file().relative_to(ROOT)} (hora de `TZ=America/Sao_Paulo date`) e atualize o ## Now antes de "
          f"encerrar o turno (S-61).", file=sys.stderr)
    return 2


def skill(hook):
    name = (hook.get("tool_input") or {}).get("skill") or (hook.get("tool_input") or {}).get("name")
    if not name:
        return 0
    f = ROOT / "data" / "raw" / "skill-usage.csv"
    f.parent.mkdir(parents=True, exist_ok=True)
    new = not f.exists()
    now = datetime.now(LOCAL)
    with f.open("a", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(["date", "time", "skill", "session"])
        w.writerow([now.strftime("%Y-%m-%d"), now.strftime("%H:%M"), name, hook.get("session_id", "")])
    return 0


MODES = {"precompact": precompact, "reinject": reinject, "gate": gate, "skill": skill}


def main(argv):
    if not argv or argv[0] not in MODES:
        print(f"uso: session_journal.py {{{'|'.join(MODES)}}}  (JSON do hook no stdin)", file=sys.stderr)
        return 1
    try:
        hook = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        hook = {}
    try:
        return MODES[argv[0]](hook)
    except Exception as e:  # a broken hook must never take the session down
        print(f"[session_journal] {argv[0]} falhou: {e}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
