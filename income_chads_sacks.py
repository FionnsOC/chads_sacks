import math

def to_coins(silver):
    """Convert an amount in silver pieces to a 'X GP, Y SP, Z CP' string."""
    total_cp = math.floor(silver * 10)        # 1 SP = 10 CP
    gp, rest = divmod(total_cp, 100)     # 1 GP = 100 CP
    sp, cp = divmod(rest, 10)
    return f"{gp} GP, {sp} SP, {cp} CP"

bags = int(input("How many bags sold? "))

# We assume that each bag sells for 3 SP (30 CP) on average
# and costs 0.5 SP (5 CP) to make.
profit = bags * (30 - 5)             # in copper

boss_pool = profit // 3              # 1/3 to the bosses / stakeholders
employee_pool = profit // 3          # 1/3 to the employees
fund = profit - boss_pool - employee_pool   # 1/3 to the fund (+ any CP left from the split by 3)

# Payouts are rounded down to whole copper pieces
per_pc = boss_pool // 5
per_employee = employee_pool // 8

# Whatever could not be paid out evenly goes to the fund
fund += boss_pool - per_pc * 5
fund += employee_pool - per_employee * 8

print(f"Each member of the party has earned {to_coins(per_pc)}")
print(f"Each employee has earned {to_coins(per_employee)}")
print(f"The health/education fund receives {to_coins(fund)}")