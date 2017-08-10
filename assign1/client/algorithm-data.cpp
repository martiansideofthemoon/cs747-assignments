#include "algorithm-data.h"


double klDivergence(double p, double q) {
    if (p == 0.0 || q == 0.0) {
        return 0.0;
    } else if (p == 1.0 || q == 1.0) {
        return 0.0;
    } else {
        double t1 = p * log(p / q);
        double t2 = (1 - p) * log((1 - p) / (1 - q));
        return (t1 + t2);
    }
}

BaseAlgorithm::BaseAlgorithm(int numArms) {
    for (int i = 0; i < numArms; i++) {
        successes.push_back(0.0);
        total.push_back(0);
        objective.push_back(0.0);
    }
    currentBestObjective = -1.0;
    currentBestArm = -1;
}


BaseAlgorithm::~BaseAlgorithm() {}


void BaseAlgorithm::printArmHistory() {
    for(unsigned int i = 0; i < total.size(); i++) {
        cout << "Arm " << i << ": " << successes[i] << "/" << total[i] << "; ";
    }
    cout << endl;
}


void BaseAlgorithm::printObjective() {
    for(unsigned int i = 0; i < total.size(); i++) {
        cout << "Arm " << i << ": " << objective[i] << "; ";
    }
    cout << endl;
}


EpsilonGreedy::EpsilonGreedy(int numArms): BaseAlgorithm(numArms) {}


EpsilonGreedy::~EpsilonGreedy() {}


void EpsilonGreedy::updateHistory(int prevArm, float reward) {
    total[prevArm]++;
    successes[prevArm] += reward;
    float newMean = (float)successes[prevArm] / total[prevArm];
    if (prevArm == currentBestArm) {
        currentBestObjective = newMean;
    } else if (newMean > currentBestObjective) {
        currentBestObjective = newMean;
        currentBestArm = prevArm;
    }
}


UCB::UCB(int numArms): BaseAlgorithm(numArms) {}


UCB::~UCB() {}


void UCB::updateHistory(int prevArm, float reward, int pulls) {
    total[prevArm]++;
    successes[prevArm] += reward;
    currentBestObjective = -1;
    for (unsigned int i = 0; i < total.size(); i++) {
        if (total[i] == 0) {
            objective[i] = -1.0;
        } else {
            objective[i] = (double)successes[i] / total[i] + sqrt(2 * log(pulls) / total[i]);
        }
        if (objective[i] > currentBestObjective) {
            currentBestObjective = objective[i];
            currentBestArm = i;
        }
    }
}


KL_UCB::KL_UCB(int numArms): BaseAlgorithm(numArms) {}


KL_UCB::~KL_UCB() {}


void KL_UCB::updateHistory(int prevArm, float reward, int pulls) {
    total[prevArm]++;
    successes[prevArm] += reward;
    // Not getting into unnecessary computation before all initial samples taken
    if (pulls < (int)total.size() - 1) return;

    currentBestObjective = -1;
    double rhs = 0.0;
    if (pulls > 1) {
        rhs = log(pulls) + CONSTANT * log(log(pulls));
    }
    for (unsigned int i = 0; i < total.size(); i++) {
        if (total[i] == 0) {
            objective[i] = -1.0;
        } else {
            double rhs_i = rhs / (double) total[i];
            double p_estimate = (double)successes[i] / total[i];
            // Implementing a binary search to find optimal q
            double left_q = p_estimate;
            double right_q = 1.0;
            double q_estimate = (left_q + right_q) / 2;
            double kld = klDivergence(p_estimate, q_estimate);
            while(kld > rhs_i || (rhs_i - kld) > THRESHOLD) {
                // Since KLD is strictly increasing with q in [p_estimate, 1]
                if (kld > rhs_i) {
                    // This will reduce the next q_estimate, and hence kld
                    right_q = q_estimate;
                } else {
                    // This will increase the next q_estimate, and hence kld
                    left_q = q_estimate;
                }
                q_estimate = (left_q + right_q) / 2;
                kld = klDivergence(p_estimate, q_estimate);
                if (1 - q_estimate < THRESHOLD) {
                    break;
                }
            }
            cout << "klDivergence " << kld << " RHS " << rhs_i << " Q-Estimate " << q_estimate << endl;
            objective[i] = q_estimate;
        }
        if (objective[i] > currentBestObjective) {
            currentBestObjective = objective[i];
            currentBestArm = i;
        }
    }
}


ThompsonSampling::ThompsonSampling(int numArms): BaseAlgorithm(numArms) {}


ThompsonSampling::~ThompsonSampling() {}


void ThompsonSampling::updateHistory(int prevArm, float reward, gsl_rng* randGenerator) {
    total[prevArm]++;
    successes[prevArm] += reward;
    currentBestObjective = -1;
    for (unsigned int i = 0; i < total.size(); i++) {
        objective[i] = gsl_ran_beta(randGenerator, successes[i] + 1, total[i] - successes[i] + 1);
        if (objective[i] > currentBestObjective) {
            currentBestObjective = objective[i];
            currentBestArm = i;
        }
    }
}