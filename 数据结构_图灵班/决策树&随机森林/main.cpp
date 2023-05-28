#include "DecideForest.h"
#include <cmath>
#include <cstdlib>
using namespace std;
int main() {
    srand(unsigned(time(NULL)));
    DecideForest testForest(300, "data_small.txt");
    testForest.DoDecision("question.txt");
    
    return 0;
}
