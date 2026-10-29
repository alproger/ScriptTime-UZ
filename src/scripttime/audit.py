"""Reproducible risk and error report, NOT a publishable benchmark."""
from __future__ import annotations
import json
from collections import defaultdict, Counter
from .__main__ import DATASETS, ROOT
from .evaluate import candidate_difficulty, evaluate, load_data, summary
from .analysis import paired_question_bootstrap

def report(case="challenge"):
    if case not in DATASETS:
        raise ValueError(f"Unknown case: {case}")
    a,b=DATASETS[case]
    docs,queries=load_data(ROOT/a,ROOT/b)
    records=evaluate(docs,queries)
    difficulty=candidate_difficulty(docs,queries)
    n_groups=len({q["question_id"] for q in queries})
    groups=defaultdict(list)
    for r in records:
        groups[(r["method"],r["evidence_mode"],r["script"])].append(r)
    strata={}
    for (method,mode,script),rs in sorted(groups.items()):
        strata[f"{method}/{mode}/{script}"]={
          "n_variants":len(rs),
          "correct_top1":sum(x["hit1"] for x in rs),
          "errors":sum(not x["hit1"] for x in rs),
          "unanswerable":sum(x["needs_abstention"] for x in rs),
          "false_answers":sum(x["false_answer"] for x in rs),
          "invalid_top1":sum(x["invalid_top1"] for x in rs),
        }
    try:
        bootstrap=paired_question_bootstrap(
            records,baseline="bm25",candidate="bm25_norm_time",
            metric="hit1",resamples=2000,seed=2026)
    except ValueError as exc:
        bootstrap={"error":str(exc)}
    return {
       "STATUS":"DEVELOPER_AUTHORED_DIAGNOSTIC_NOT_SCIENTIFIC_GOLD",
       "case":case,
       "n_source_linked_researcher_paraphrases":len(docs),
       "n_base_question_groups":n_groups,
       "n_correlated_script_variants":len(queries),
       "n_unanswerable_groups":len({q["question_id"] for q in queries
                                    if q.get("needs_abstention")=="1"}),
       "candidate_pool_size":len(docs),
       "eligible_candidate_summary":{
           "min":min(r["eligible_documents"] for r in difficulty),
           "max":max(r["eligible_documents"] for r in difficulty),
           "mean":round(sum(r["eligible_documents"] for r in difficulty)/len(difficulty),3),
           "single_candidate_variants":sum(r["is_single_candidate"] for r in difficulty),
           "zero_candidate_variants":sum(r["no_eligible_documents"] for r in difficulty)
       },
       "diagnostic_metrics":summary(records),
       "stratified_errors":strata,
       "paired_group_bootstrap_exploratory_only":bootstrap,
       "known_limitations":[
          "Human blind review and held-out sources absent.",
          "The 72 script variants come from 24 developer-authored base questions.",
          "Some passage validity intervals begin with an audited snapshot, not the original legal effective date.",
          "New-Latin variants are algorithmic and were not evaluated by a trained linguist.",
          "No calibrated confidence or reliable semantic abstention exists.",
          "Questions can contain target law names, lexical clues and dates.",
          "Do NOT use diagnostic percentages or bootstrap intervals as evidence of external performance."
       ]
    }

def main():
    print(json.dumps(report(),ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
