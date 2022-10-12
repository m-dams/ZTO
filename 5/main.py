from local_search import RS, SA, LinearCooling, GeometricCooling
from stop_conditions import IterationCondition, SinceLastImprovementCondition, CalcTimeCondition

if __name__ == "__main__":
    stop_condition = IterationCondition(10000)
    rs = RS(128, stop_condition)
    rs.generate_random_solution(100)
    rs.solve()
