/*********************************************
 * OPL 22.1.0.0 Model
 * Author: pieklik&dams
 * Creation Date: Mar 16, 2022 at 17:23:33
 *********************************************/
int executors_count = ...;
int tasks_count = ...;
range executors = 1..executors_count;
range tasks = 1..tasks_count;
int cost [executors][tasks] = ...;
dvar boolean solution [executors][tasks];
minimize sum(e in executors, t in tasks) solution[e][t] * cost[e][t];

subject to {
  forall(e in executors) sum(t in tasks) solution[e][t] == 1;
  forall(e in executors) sum(t in tasks) solution[t][e] == 1;
}

execute {
  writeln(solution)
  
  for (var e in executors)
  	for (var t in tasks)
  		if (solution[e][t] == 1)
  			writeln("executor: ", e, ", task: ", t)
}