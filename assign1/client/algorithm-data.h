#include <vector>
#include <iostream>
#include <math.h>

#include "gsl/gsl_rng.h"
#include "gsl/gsl_randist.h"

#define THRESHOLD 10e-6
#define CONSTANT 3

using std::vector;
using std::cout;
using std::endl;

class BaseAlgorithm {
public:
    vector<float> successes;
    vector<int> total;
    vector<double> objective;
    float currentBestObjective;
    int currentBestArm;
    BaseAlgorithm(int numArms);
    ~BaseAlgorithm();
    void printArmHistory();
    void printObjective();
};

class EpsilonGreedy: public BaseAlgorithm {
public:
    EpsilonGreedy(int numArms);
    ~EpsilonGreedy();
    void updateHistory(int prevArm, float reward);
};

class UCB: public BaseAlgorithm {
public:
    UCB(int numArms);
    ~UCB();
    void updateHistory(int prevArm, float reward, int pulls);
};

class KL_UCB: public BaseAlgorithm {
public:
    KL_UCB(int numArms);
    ~KL_UCB();
    void updateHistory(int prevArm, float reward, int pulls);
};

class ThompsonSampling: public BaseAlgorithm {
public:
    ThompsonSampling(int numArms);
    ~ThompsonSampling();
    void updateHistory(int prevArm, float reward, gsl_rng* randGenerator);
};