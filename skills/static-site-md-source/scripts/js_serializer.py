#!/usr/bin/env python3
"""Reusable JS-literal serializer for the MD->static-site pipeline.

WHY: json.dumps / yaml emitters produce INVALID JavaScript for a file like
  const X = { ... };
json.dumps gives '{"a": 1}' (fine as a value) but you still must wrap it in
`const X =` and it uses double quotes everywhere (ok) — the real traps are:
  - YAML flow/block emit produces `key: value` with NO `const`/commas -> invalid JS
  - trailing commas (fine in modern engines but risky)
  - unescaped quotes / backslashes / newlines inside strings
So: always use THIS function to emit the object literal.

Usage:
  from js_serializer import py_to_js
  out = "const DATA = " + py_to_js(my_dict) + ";"
"""
import re


def jstr(s: str) -> str:
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    s = s.replace("\r", "").replace("\n", "\\n").replace("\t", "\\t")
    return '"' + s + '"'


def is_plain_scalar(v) -> bool:
    return isinstance(v, (str, int, float, bool)) or v is None


def py_to_js(v, indent=0):
    """Serialize a Python value to a valid JS literal (multiline when needed)."""
    pad = "  " * indent
    pad1 = "  " * (indent + 1)
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "null"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        return jstr(v)
    if isinstance(v, list):
        if not v:
            return "[]"
        items = [py_to_js(x, indent + 1) for x in v]
        single = "[ " + ", ".join(items) + " ]"
        if all(is_plain_scalar(x) for x in v) and len(single) <= 90:
            return single
        body = ",\n".join(pad1 + it for it in items)
        return "[\n" + body + "\n" + pad + "]"
    if isinstance(v, dict):
        if not v:
            return "{}"
        entries = []
        for k, val in v.items():
            key = k if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", str(k)) else jstr(str(k))
            entries.append((key, val))
        simple = all(is_plain_scalar(val) for _, val in entries)
        if simple:
            single = "{ " + ", ".join(f"{k}: {py_to_js(val)}" for k, val in entries) + " }"
            if len(single) <= 90:
                return single
        lines = [f"{pad1}{k}: {py_to_js(val, indent + 1)}" for k, val in entries]
        return "{\n" + ",\n".join(lines) + "\n" + pad + "}"
    raise TypeError(f"Tipo não suportado: {type(v)}")
