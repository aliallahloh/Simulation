from pathlib import Path
import yaml
import py_compile

# Run this file from:
#   rcstp_q1_experiment_package/benchmark_python
#
# Purpose:
#   Fix Path B3.2 dispatch/config placement without needing to download the ZIP.
#   Then run:
#       python rcstp_pathb32/FIX_B32_IN_PLACE.py
#       bash scripts/q1_pathb32/run_pathb32_smoke.sh

cfg_dir = Path('configs/q1_pathb32')
if not cfg_dir.exists():
    raise SystemExit('ERROR: configs/q1_pathb32 not found. Run from benchmark_python/.')

b32_variants = {
    'b32_exact_scenario_reference': {
        'include_sources': ['rcstp_v5_balanced', 'scenario_ensemble'],
        'dominance_filter': False,
        'score_mode': 'b32_exact_scenario_reference',
    },
    'b32_zero_risk_scenario_first_gate': {
        'include_sources': ['rcstp_v5_balanced', 'scenario_ensemble'],
        'dominance_filter': False,
        'score_mode': 'b32_zero_risk_scenario_first_gate',
    },
    'b32_strict_nonworse_proxy_override': {
        'include_sources': ['rcstp_v5_balanced', 'scenario_ensemble'],
        'dominance_filter': False,
        'score_mode': 'b32_strict_nonworse_proxy_override',
    },
    'b32_scenario_plus_plausible_veto': {
        'include_sources': ['rcstp_v5_balanced', 'scenario_ensemble'],
        'dominance_filter': False,
        'score_mode': 'b32_scenario_plus_plausible_veto',
    },
}

b31_keys = [
    'b31_stricter_scenario_first_safe_gate',
    'b31_scenario_default_high_margin',
    'b31_family_aware_safe_gate',
    'b31_no_override_on_risky_families',
]

for p in sorted(cfg_dir.glob('*.yaml')):
    raw = p.read_text()
    raw = '\n'.join([ln for ln in raw.splitlines() if ln.strip() != 'guardian_']) + '\n'
    data = yaml.safe_load(raw)

    exp = data.setdefault('experiment', {})
    exp['planners'] = [
        'astar_nominal',
        'scenario_ensemble',
        'rcstp_v4_2_full',
        'rcstp_v5_balanced',
        'rcstp_v5_b3_scenario_first_safe_gate',
        'rcstp_v5_b31_no_override_on_risky_families',
        'rcstp_v5_b32_exact_scenario_reference',
        'rcstp_v5_b32_zero_risk_scenario_first_gate',
        'rcstp_v5_b32_strict_nonworse_proxy_override',
        'rcstp_v5_b32_scenario_plus_plausible_veto',
    ]

    rcstp = data.setdefault('rcstp', {})
    variants = rcstp.setdefault('v5_ablation_variants', {})
    pathb = rcstp.setdefault('v5_pathb', {})

    for key in list(b31_keys) + list(b32_variants):
        if key in pathb:
            variants[key] = pathb.pop(key)

    for key, val in b32_variants.items():
        variants[key] = val

    rcstp['v5_pathb32'] = {
        'scenario_safe_max_plausible_collision': 0.35,
        'scenario_safe_max_blocked_rate': 0.40,
        'scenario_safe_min_nominal_clearance': 0.35,
        'scenario_max_nominal_collision': 0.0,
        'zero_risk_required_plausible_advantage': 0.18,
        'risky_family_required_plausible_advantage': 0.22,
        'nonworse_min_clearance_ratio_vs_scenario': 1.0,
        'nonworse_max_extra_robust_violation_vs_scenario': 0.0,
        'nonworse_max_extra_outside_robust_vs_scenario': 0.0,
        'nonworse_max_extra_cvar_cost_vs_scenario': 0.0,
        'scenario_veto_max_plausible_collision': 0.14,
    }

    p.write_text(yaml.safe_dump(data, sort_keys=False))
    print('fixed config:', p)

hs = Path('rcstp_experiments/algorithms/hybrid_selector.py')
text = hs.read_text()

if 'Path-B3.2 fail-fast audit variant' not in text:
    needle = "    robust = _robust_maps(bundle, cfg)\n\n    raw_candidates = []"
    branch = """    robust = _robust_maps(bundle, cfg)

    # Path-B3.2 fail-fast audit variant:
    # exact_scenario_reference must be the raw scenario-ensemble result.
    # It bypasses dominance, scalar ranking, B3/B3.1 gates, and RCSTP fallback.
    if score_mode == 'b32_exact_scenario_reference':
        ensemble = plan_scenario_ensemble(bundle, cfg, seed=seed)
        s = _score_path(
            ensemble.path,
            bundle,
            infeasible_penalty,
            robust['robust_clearance'],
            robust['robust_free'],
            cfg,
        )
        s['candidate_name'] = 'scenario_ensemble'
        s['source_rank'] = _source_rank('scenario_ensemble')
        s['selection_score_variant'] = s.get('selection_score', 0.0)
        s['ablation_variant'] = variant
        s['ablation_score_mode'] = score_mode
        s['ablation_dominance_filter'] = int(dominance_filter)
        s['dominance_survivor'] = 1
        s['selected_final'] = 1
        s['pathb32_gate_selected'] = 1
        s['pathb32_gate_reason'] = 'b32_exact_scenario_reference:direct_raw_scenario'
        candidate_debug = [dict(s)]
        candidate_debug += [
            {'candidate_name': 'ensemble::' + d['candidate_name'], **{k: v for k, v in d.items() if k != 'candidate_name'}}
            for d in (ensemble.candidate_debug or [])[:12]
        ]
        return HybridSelectorResult(
            path=list(ensemble.path) if ensemble.path is not None else None,
            selected_source='b32_exact_scenario_reference:scenario_ensemble',
            candidate_count=int(ensemble.candidate_count or 0),
            diverse_candidate_count=1,
            dominance_survivor_count=1,
            risk_route=float(s.get('plausible_collision_rate', float('nan'))),
            regret_route=0.0,
            switch_rate=1.0,
            candidate_debug=candidate_debug,
            graph_nodes=int(ensemble.graph_nodes or 0),
            graph_edges=int(ensemble.graph_edges or 0),
            centerline=None,
            tube_mask=None,
            robust_clearance=robust['robust_clearance'],
            robust_free=robust['robust_free'],
        )

    raw_candidates = []"""
    if needle not in text:
        raise SystemExit('ERROR: could not find robust/raw_candidates insertion point in hybrid_selector.py')
    text = text.replace(needle, branch, 1)

text = text.replace(
    "return mark(balanced, 'b32_exact_scenario_reference:no_scenario_available')",
    "raise RuntimeError('B3.2 exact-scenario-reference requested but no scenario_ensemble candidate exists.')"
)

hs.write_text(text)
py_compile.compile(str(hs), doraise=True)
print('patched:', hs)

for p in sorted(cfg_dir.glob('*.yaml')):
    data = yaml.safe_load(p.read_text())
    rcstp = data['rcstp']
    assert rcstp.get('alpha_geometry') == 0.04
    assert rcstp.get('alpha_scoring') == 0.3
    assert 'alpha: 0.35' not in p.read_text()
    assert all(ln.strip() != 'guardian_' for ln in p.read_text().splitlines())
    variants = rcstp.get('v5_ablation_variants', {})
    for key in b32_variants:
        assert key in variants, f'{key} missing from v5_ablation_variants in {p}'
        assert key not in rcstp.get('v5_pathb', {}), f'{key} incorrectly under v5_pathb in {p}'
    print('validated:', p)

print('B3.2 fixed-audit in-place patch complete.')
