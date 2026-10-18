def to_coins(copper):
    """Convert copper pieces to a 'X GP, Y SP, Z CP' string."""
    gp, rest = divmod(copper, 100)   # 1 GP = 100 CP
    sp, cp = divmod(rest, 10)        # 1 SP = 10 CP
    return f"{gp} GP, {sp} SP, {cp} CP"


def calculate(bags):
    """Return (per_pc, per_employee, fund), all in copper pieces."""
    profit = bags * (30 - 5)         # 3 SP sale price, 0.5 SP material, in CP

    boss_pool = profit // 3
    employee_pool = profit // 3
    fund = profit - boss_pool - employee_pool

    per_pc = boss_pool // 5
    per_employee = employee_pool // 8

    fund += boss_pool - per_pc * 5
    fund += employee_pool - per_employee * 8

    return per_pc, per_employee, fund