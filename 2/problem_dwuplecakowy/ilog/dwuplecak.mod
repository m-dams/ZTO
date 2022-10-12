/*********************************************
 * OPL 22.1.0.0 Model
 * Author: pieklik&dams
 * Creation Date: Mar 23, 2022 at 12:45:31
 *********************************************/
int items_count = ...;
int backpack_volume = ...;
range items = 1..items_count;
range features = 1..3;
range capabilities = 1..2;
int items_features [items][features] = ...;
dvar float solution [items][capabilities];
maximize sum(i in items) (solution[i][1] + solution[i][2]) * items_features[i][1];

subject to {
  forall(i in items) sum(c in capabilities) solution[i][c] <= 1;
  forall(i in items) sum(c in capabilities) solution[i][c] >= 0;
  forall(i in items) forall(c in capabilities) solution[i][c] <= 1;	
  forall(i in items) forall(c in capabilities) solution[i][c] >= 0;
  sum(i in items) solution[i][1] * items_features[i][2] <= backpack_volume;
  sum(i in items) solution[i][2] * items_features[i][3] <= backpack_volume;
}

execute {
  writeln(solution)
}