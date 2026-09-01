---
name: code-batch-constraints
description: Batch linopy constraint additions using linopy.merge. Use when adding constraints in a loop, optimizing model building, or refactoring add_constraints calls.
---

# Batch Linopy Constraints with linopy.merge

## Instructions

When you see a pattern of adding constraints one-by-one in a for-loop, refactor it to batch all constraints into a single `model.add_constraints` call using `linopy.merge`.

### Anti-pattern (slow, verbose)

```python
for region in regions:
    lhs = some_expression(region)
    model.add_constraints(lhs <= rhs_value, name=f"constraint_{region}")
```

### Correct pattern

```python
import linopy
import xarray as xr

# 1. Build LHS in a loop (when per-item logic like filtering is needed)
lhs_parts: list[linopy.LinearExpression] = []
valid_regions: list[str] = []
for region in regions:
    expr = some_expression(region)
    if expr is None:
        continue
    lhs_parts.append(expr)
    valid_regions.append(region)

if not lhs_parts:
    return

# 2. Merge LHS and assign meaningful coordinates
lhs = linopy.merge(lhs_parts, dim="region").assign_coords(region=valid_regions)

# 3. Compute RHS vectorized (pure data, no linopy needed)
rhs = xr.DataArray(rhs_values, coords={"region": valid_regions})

# 4. Single constraint call
model.add_constraints(lhs <= rhs, name="constraint")
```

### Key points

- Use `dim="<dim_name>"` with the a meaningful name.
- Use `.assign_coords()` after merge to label the dimension. D
- The RHS `xr.DataArray` (can also be a pandas object) must share the same dimension name and coordinates as the merged LHS.
- For scalar RHS values, use `xr.DataArray(values, coords={"dim": labels})` — no need for `xr.concat`.
- Separate LHS construction (often needs a loop for filtering/selecting) from RHS construction (often vectorizable with numpy/pandas).
- Both `model.add_constraints(lhs <= rhs, name=...)` and `model.add_constraints(lhs, "<=", rhs, name=...)` work.
- The constraint name no longer needs a per-item suffix — the coordinates on the merged expression handle uniqueness.

### When to apply

- Any loop that calls `model.add_constraints` per iteration
- Building up constraints from conditional or dynamic data sources
- Performance-sensitive model construction code
