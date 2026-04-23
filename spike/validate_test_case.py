import json
from pathlib import Path

from sympy import Function, symbols, Derivative, Eq, sympify


# Build the SymPy parsing context.
# These are all the named objects that can appear in a test case's sympy field.
t = symbols("t")
mu_0, epsilon_0 = symbols("mu_0 epsilon_0", positive=True)

# Vector fields as time-dependent Functions (so Derivative(E, t) works):
E = Function("E")(t)
B = Function("B")(t)

# Vector operators on fields — as time-dependent Functions so they
# can appear inside Derivative() as well.
curl_E = Function("curl_E")(t)
curl_B = Function("curl_B")(t)
div_E = Function("div_E")(t)
div_B = Function("div_B")(t)
laplacian_E = Function("laplacian_E")(t)
curl_curl_E = Function("curl_curl_E")(t)
grad_div_E = Function("grad_div_E")(t)

# Expressions involving operators composed with derivatives.
# Step 1's RHS: curl applied to (-dB/dt), before we distribute the negative:
curl_of_neg_dB_dt = Function("curl_of_neg_dB_dt")(t)
# Step 2's RHS: curl applied to (dB/dt), after pulling out -1:
curl_of_dB_dt = Function("curl_of_dB_dt")(t)

# Gradient of zero — explicitly zero, so simplification works.
grad_of_zero = 0

# Assemble the local context dict that sympify() will use.
SYMPY_CONTEXT = {
    "t": t,
    "mu_0": mu_0,
    "epsilon_0": epsilon_0,
    "E": E,
    "B": B,
    "curl_E": curl_E,
    "curl_B": curl_B,
    "div_E": div_E,
    "div_B": div_B,
    "laplacian_E": laplacian_E,
    "curl_curl_E": curl_curl_E,
    "grad_div_E": grad_div_E,
    "curl_of_neg_dB_dt": curl_of_neg_dB_dt,
    "curl_of_dB_dt": curl_of_dB_dt,
    "grad_of_zero": grad_of_zero,
    "Derivative": Derivative,
    "Eq": Eq,
}

def validate_test_case(path: Path) -> bool:
    """Load a test case JSON and verify all sympy strings parse."""
    print(f"Validating: {path}")

    with open(path) as f:
        test_case = json.load(f)

    steps = test_case["expected_steps"]
    total = len(steps)
    failures = []

    for step in steps:
        step_num = step["step"]
        sympy_str = step["sympy"]
        try:
            parsed = sympify(sympy_str, locals=SYMPY_CONTEXT)
            print(f"  Step {step_num}: OK — parsed as {parsed}")
        except Exception as e:
            failures.append((step_num, sympy_str, str(e)))
            print(f"  Step {step_num}: FAILED — {e}")

    print()
    if failures:
        print(f"RESULT: {len(failures)} of {total} steps failed to parse.")
        return False
    else:
        print(f"RESULT: All {total} steps parsed successfully.")
        return True


if __name__ == "__main__":
    path = Path("spike/test_cases/em_wave_001.json")
    success = validate_test_case(path)
    exit(0 if success else 1)