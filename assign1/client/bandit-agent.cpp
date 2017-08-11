#include <iostream>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <math.h>
#include <vector>
#include <random>
#include <string>

#include "gsl/gsl_rng.h"
#include "gsl/gsl_randist.h"

#include "algorithm-data.h"

#define MAXHOSTNAME 256

using namespace std;

void options(){

  cout << "Usage:\n";
  cout << "bandit-agent\n";
  cout << "\t[--numArms numArms]\n";
  cout << "\t[--randomSeed randomSeed]\n";
  cout << "\t[--horizon horizon]\n";
  cout << "\t[--hostname hostname]\n";
  cout << "\t[--port port]\n";
  cout << "\t[--algorithm algorithm]\n";
  cout << "\t[--epsilon epsilon]\n";

}


/*
  Read command line arguments, and set the ones that are passed (the others remain default.)
*/
bool setRunParameters(int argc, char *argv[], int &numArms, int &randomSeed, unsigned long int &horizon, string &hostname, int &port, string &algorithm, double &epsilon){

  int ctr = 1;
  while(ctr < argc){

    //cout << string(argv[ctr]) << "\n";

    if(string(argv[ctr]) == "--help"){
      return false; //This should print options and exit.
    }
    else if(string(argv[ctr]) == "--numArms"){
      if(ctr == (argc - 1)){
	return false;
      }
      numArms = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--randomSeed"){
      if(ctr == (argc - 1)){
	return false;
      }
      randomSeed = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--horizon"){
      if(ctr == (argc - 1)){
	return false;
      }
      horizon = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--hostname"){
      if(ctr == (argc - 1)){
	return false;
      }
      hostname = string(argv[ctr + 1]);
      ctr++;
    }
    else if(string(argv[ctr]) == "--port"){
      if(ctr == (argc - 1)){
	return false;
      }
      port = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--algorithm"){
      if(ctr == (argc - 1)){
  return false;
      }
      algorithm = string(argv[ctr + 1]);
      ctr++;
    }
     else if(string(argv[ctr]) == "--epsilon"){
      if(ctr == (argc - 1)){
  return false;
      }
      epsilon = atof(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else{
      return false;
    }

    ctr++;
  }

  return true;
}

/* ============================================================================= */
/* Write your algorithms here */
int sampleArm(string algorithm, double epsilon, int pulls, float reward,
              int numArms, int prevArm, BaseAlgorithm* baseData, gsl_rng* randGenerator) {
  if(algorithm.compare("rr") == 0) {
    return(pulls % numArms);
  }
  else if(algorithm.compare("epsilon-greedy") == 0) {
    EpsilonGreedy* data = static_cast<EpsilonGreedy*>(baseData);
    if (prevArm != -1) {
      data->updateHistory(prevArm, reward);
    }
    // data->BaseAlgorithm::printArmHistory();
    if(gsl_rng_uniform(randGenerator) < epsilon || data->currentBestObjective == -1) {
      // This happens with probability epsilon
      float randomArm = numArms * gsl_rng_uniform(randGenerator);
      return ((int) randomArm);
    } else {
      // This happens with probability 1-epsilon
      return data->currentBestArm;
    }
  }
  else if(algorithm.compare("UCB") == 0) {
    UCB* data = static_cast<UCB*>(baseData);
    if (prevArm != -1) {
      data->updateHistory(prevArm, reward, pulls);
    }
    if (pulls < numArms) {
      // For initial pulling of all arms
      return pulls;
    } else {
      // UCB objective implemented in updateHistory() function
      data->BaseAlgorithm::printArmHistory();
      data->BaseAlgorithm::printObjective();
      return data->currentBestArm;
    }
  }
  else if(algorithm.compare("KL-UCB") == 0) {
    KL_UCB* data = static_cast<KL_UCB*>(baseData);
    if (prevArm != -1) {
      data->updateHistory(prevArm, reward, pulls);
    }
    if (pulls < numArms) {
      // For initial pulling of all arms
      return pulls;
    } else {
      // KL-UCB objective implemented in updateHistory() function
      data->BaseAlgorithm::printArmHistory();
      data->BaseAlgorithm::printObjective();
      return data->currentBestArm;
    }
  }
  else if(algorithm.compare("Thompson-Sampling") == 0) {
    ThompsonSampling* data = static_cast<ThompsonSampling*>(baseData);
    if (prevArm != -1) {
      data->updateHistory(prevArm, reward, randGenerator);
      data->BaseAlgorithm::printArmHistory();
      return data->currentBestArm;
    } else {
      return 0;
    }
  }
  else{
    return -1;
  }
}

/* ============================================================================= */

BaseAlgorithm* setAlgorithmData(string algorithm, int numArms) {
  BaseAlgorithm* data;
  if (algorithm.compare("epsilon-greedy") == 0) {
    data = new EpsilonGreedy(numArms);
  } else if (algorithm.compare("UCB") == 0) {
    data = new UCB(numArms);
  } else if (algorithm.compare("KL-UCB") == 0) {
    data = new KL_UCB(numArms);
  } else if (algorithm.compare("Thompson-Sampling") == 0) {
    data = new ThompsonSampling(numArms);
  } else {
    data = new BaseAlgorithm(numArms);
  }
  return data;
}


int main(int argc, char *argv[]){
  // Run Parameter defaults.
  int numArms = 5;
  int randomSeed = time(0);
  unsigned long int horizon = 200;
  string hostname = "localhost";
  int port = 5000;
  string algorithm="random";
  double epsilon=0.0;

  //Set from command line, if any.
  if(!(setRunParameters(argc, argv, numArms, randomSeed, horizon, hostname, port, algorithm, epsilon))){
    //Error parsing command line.
    options();
    return 1;
  }

  struct sockaddr_in remoteSocketInfo;
  struct hostent *hPtr;
  int socketHandle;

  bzero(&remoteSocketInfo, sizeof(sockaddr_in));

  if((hPtr = gethostbyname((char*)(hostname.c_str()))) == NULL){
    cerr << "System DNS name resolution not configured properly." << "\n";
    cerr << "Error number: " << ECONNREFUSED << "\n";
    exit(EXIT_FAILURE);
  }

  if((socketHandle = socket(AF_INET, SOCK_STREAM, 0)) < 0){
    close(socketHandle);
    exit(EXIT_FAILURE);
  }

  memcpy((char *)&remoteSocketInfo.sin_addr, hPtr->h_addr, hPtr->h_length);
  remoteSocketInfo.sin_family = AF_INET;
  remoteSocketInfo.sin_port = htons((u_short)port);

  if(connect(socketHandle, (struct sockaddr *)&remoteSocketInfo, sizeof(sockaddr_in)) < 0){
    //code added
    cout<<"connection problem"<<".\n";
    close(socketHandle);
    exit(EXIT_FAILURE);
  }


  char sendBuf[256];
  char recvBuf[256];

  float reward = 0;
  unsigned long int pulls = 0;

  BaseAlgorithm* data = setAlgorithmData(algorithm, numArms);
  gsl_rng* randGenerator = gsl_rng_alloc(gsl_rng_mt19937);
  gsl_rng_set(randGenerator, randomSeed);

  int armToPull = sampleArm(algorithm, epsilon, pulls, reward, numArms, -1, data, randGenerator);

  sprintf(sendBuf, "%d", armToPull);

  cout << "Sending action " << armToPull << ".\n";
  while(send(socketHandle, sendBuf, strlen(sendBuf)+1, MSG_NOSIGNAL) >= 0){

    char temp;
    recv(socketHandle, recvBuf, 256, 0);
    sscanf(recvBuf, "%f %c %lu", &reward, &temp, &pulls);
    cout << "Received reward " << reward << ".\n";
    cout<<"Num of  pulls "<<pulls<<".\n";


    armToPull = sampleArm(algorithm, epsilon, pulls, reward, numArms, armToPull, data, randGenerator);

    sprintf(sendBuf, "%d", armToPull);
    cout << "Sending action " << armToPull << ".\n";
  }

  delete data;
  close(socketHandle);

  cout << "Terminating.\n";

  return 0;
}

