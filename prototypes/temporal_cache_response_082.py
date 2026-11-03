"""Pure cache-response arithmetic for 082; no learned computation or I/O.

Inputs are already closed binary predictions/labels or exact feature bytes.
Constant answers across a source/question's six balanced permutations must
score 3/6. Feature-collision limits are exact deterministic-input upper bounds,
not a claim that a particular architecture can achieve the upper bound.
"""
from collections import Counter, defaultdict
from itertools import product


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def index_rows(rows, groups, value):
    allowed = set(groups)
    result = {}
    for row in rows:
        key = (row["group"], row["permutation"], row["question"])
        require(key[0] in allowed and key[1] in range(6) and key[2] in range(6),
                "UNEXPECTED_KEY")
        require(key not in result, "DUPLICATE_KEY")
        if value == "prediction":
            require(row.get("status") == "CLOSED", "NON_CLOSED_PREDICTION")
        require(row[value] in (0, 1), "NON_BINARY_VALUE")
        result[key] = int(row[value])
    require(set(result) == set(product(groups, range(6), range(6))), "INCOMPLETE_KEYS")
    return result


def balanced_truth(rows, groups):
    values = index_rows(rows, groups, "yes")
    for group, question in product(groups, range(6)):
        require(sum(values[group, p, question] for p in range(6)) == 3,
                "UNBALANCED_SOURCE_QUESTION")
    return values


def response_summary(real_rows, control1_rows, control2_rows, truth_rows, groups):
    """Describe cached decision changes; never evaluate a model or new input."""
    groups = tuple(groups)
    require(groups and len(set(groups)) == len(groups), "INVALID_GROUPS")
    truth = balanced_truth(truth_rows, groups)
    real = index_rows(real_rows, groups, "prediction")
    c1 = index_rows(control1_rows, groups, "prediction")
    c2 = index_rows(control2_rows, groups, "prediction")
    sensitive = invariant = correct_invariant = correct_sensitive = 0
    for group, question in product(groups, range(6)):
        answers = [real[group, p, question] for p in range(6)]
        correct = sum(real[group, p, question] == truth[group, p, question] for p in range(6))
        if len(set(answers)) == 1:
            invariant += 1
            require(correct == 3, "INVARIANT_VIEW_NOT_THREE_CORRECT")
            correct_invariant += correct
        else:
            sensitive += 1
            correct_sensitive += correct
    total = len(real)
    source_correct = sum(all(real[g, p, q] == truth[g, p, q]
                             for p, q in product(range(6), range(6))) for g in groups)
    return {
        "source_groups": len(groups), "items": total,
        "correct_items": correct_invariant + correct_sensitive,
        "source36_correct": source_correct,
        "source_question_views": 6 * len(groups),
        "permutation_sensitive_views": sensitive,
        "permutation_invariant_views": invariant,
        "correct_invariant_items": correct_invariant,
        "correct_sensitive_items": correct_sensitive,
        "real_control1_agree_items": sum(real[k] == c1[k] for k in real),
        "real_control2_agree_items": sum(real[k] == c2[k] for k in real),
        "control1_control2_agree_items": sum(c1[k] == c2[k] for k in real),
        "limitation": "cached binary response only; no assertion about logits or feature causality",
    }


def exact_feature_collision_limits(feature_bytes, truth_rows, groups):
    """Upper bounds from exact (ordered V bytes, q bytes) contradictions only.

    Include shape/dtype in each byte value. Identical Python bytes compare
    exactly even on a hash collision. Cross-source compatibility may tighten
    the source bound further; this function intentionally reports a bound.
    """
    groups = tuple(groups)
    truth = balanced_truth(truth_rows, groups)
    require(set(feature_bytes) == set(truth), "FEATURE_KEY_BINDING_MISMATCH")
    classes = defaultdict(Counter)
    local = defaultdict(lambda: defaultdict(set))
    for key, label in truth.items():
        features = feature_bytes[key]
        require(isinstance(features, tuple) and len(features) == 2
                and all(isinstance(x, bytes) for x in features), "FEATURES_NOT_EXACT_BYTES")
        classes[features][label] += 1
        local[key[0]][features].add(label)
    contradicting = sum(len(labels) == 2 for labels in classes.values())
    impossible = sum(any(len(labels) == 2 for labels in local[g].values()) for g in groups)
    return {
        "source_groups": len(groups), "items": len(truth),
        "unique_exact_inputs": len(classes),
        "conflicting_exact_input_classes": contradicting,
        "deterministic_item_correct_upper": sum(max(labels.values()) for labels in classes.values()),
        "within_source_impossible36_groups": impossible,
        "source36_correct_upper": len(groups) - impossible,
        "limitation": "exact-byte contradiction bound; not learnability or achieved model accuracy",
    }
