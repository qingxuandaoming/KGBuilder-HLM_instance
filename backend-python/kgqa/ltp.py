# -*- coding: utf-8 -*-
"""
Natural Language Processing module for Question Answering.
Uses HanLP for tokenization, POS tagging, and NER.
"""

import re
try:
    import hanlp
except Exception:
    hanlp = None
from neo_db.config import similar_words as REL_MAP

# Load HanLP model
# Using the small multi-task learning model which balances accuracy and performance.
# It supports tokenization, POS tagging (CTB & PKU), NER, etc.
HanLP = None
if hanlp is not None:
    try:
        HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
    except Exception:
        HanLP = None

def _normalize_rel(w):
    return REL_MAP.get(w, w)

def get_target_array(words):
    parts = [p for p in re.split(r"的+", words) if p]

    entity = None
    if parts:
        first = parts[0]
        if HanLP is not None:
            doc = HanLP(first)
            tokens = doc.get('tok/fine', [])
            tags = doc.get('pos/pku', [])
            if tokens and isinstance(tokens[0], list):
                tokens = tokens[0]
                tags = tags[0]
            for w, t in zip(tokens, tags):
                if t == 'nr':
                    entity = w
                    break
        if entity is None:
            m = re.findall(r"[\u4e00-\u9fff]+", first)
            entity = m[0] if m else first

    rels = []
    if len(parts) == 1:
        seg = re.sub(r"(是谁|是|谁|哪位|何人|\?|？)+", "", words)
        if HanLP is not None:
            doc = HanLP(seg)
            tokens = doc.get('tok/fine', [])
            tags = doc.get('pos/pku', [])
            if tokens and isinstance(tokens[0], list):
                tokens = tokens[0]
                tags = tags[0]
            cand = None
            for w, t in zip(tokens, tags):
                if REL_MAP.get(w):
                    cand = w
                    break
                if t == 'n' and not cand:
                    cand = w
            if cand:
                rels.append(_normalize_rel(cand))
        else:
            m = re.findall(r"[\u4e00-\u9fff]+", seg)
            if m:
                rels.append(_normalize_rel(m[-1]))
    for seg in parts[1:]:
        seg = re.sub(r"(是谁|是|谁|哪位|何人|\?|？)+", "", seg).strip()
        if re.search(r"[和与及、]", seg):
            items = [s for s in re.split(r"[和与及、]", seg) if s]
            norm_items = [_normalize_rel(i) for i in items]
            rels.append("|".join(norm_items))
            continue
        if HanLP is not None:
            doc = HanLP(seg)
            tokens = doc.get('tok/fine', [])
            tags = doc.get('pos/pku', [])
            if tokens and isinstance(tokens[0], list):
                tokens = tokens[0]
                tags = tags[0]
            candidate = None
            for w, t in zip(tokens, tags):
                if REL_MAP.get(w):
                    candidate = w
                    break
                if t == 'n' and not candidate:
                    candidate = w
            rels.append(_normalize_rel(candidate or seg))
        else:
            rels.append(_normalize_rel(seg))

    if entity is None:
        return []
    return [entity] + rels
