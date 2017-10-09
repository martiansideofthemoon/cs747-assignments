# demonstrates how to call the server and the client
# modify according to your needs

mkdir results
i1_
for((n=0;n<50;n++))
do
    echo "----------------    SARSA \0 $n    ------------------"
    python3 ./server/server.py -port $((6000+$n)) -i 0 -rs $n -ne 1600 -q | tee "results/qlearning_0.1_rs$n.txt" &
    sleep 1
    python3 ./client/client.py -port $((6000+$n)) -rs $n -gamma 1 -algo qlearning -lambda 0
done
# for((n=0;n<50;n++))
# do
#     echo "----------------    SARSA \0 $n    ------------------"
#     python3 ./server/server.py -port $((6000+$n)) -i 1 -rs $n -ne 1600 -q | tee "results/i1_sarsa_accum_lambda0_rs$n.txt" &
#     sleep 1
#     python3 ./client/client.py -port $((6000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0
# done
# for((n=0;n<50;n++))
# do
#     echo "----------------    SARSA \0.1 $n    ------------------"
#     python3 ./server/server.py -port $((6000+$n)) -i 1 -rs $n -ne 1600 -q | tee "results/i1_sarsa_accum_lambda0.1_rs$n.txt" &
#     sleep 1
#     python3 ./client/client.py -port $((6000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.1
# done
# for((n=0;n<50;n++))
# do
#     echo "----------------    SARSA \0.2 $n    ------------------"
#     python3 ./server/server.py -port $((6000+$n)) -i 1 -rs $n -ne 1600 -q | tee "results/i1_sarsa_accum_lambda0.2_rs$n.txt" &
#     sleep 1
#     python3 ./client/client.py -port $((6000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.2
# done
# for((n=0;n<50;n++))
# do
#     echo "----------------    SARSA \0.3 $n    ------------------"
#     python3 ./server/server.py -port $((6000+$n)) -i 1 -rs $n -ne 1600 -q | tee "results/i1_sarsa_accum_lambda0.3_rs$n.txt" &
#     sleep 1
#     python3 ./client/client.py -port $((6000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.3
# done
# for((n=0;n<50;n++))
# do
#     echo "----------------    SARSA \0.4 $n    ------------------"
#     python3 ./server/server.py -port $((6000+$n)) -i 1 -rs $n -ne 1600 -q | tee "results/i1_sarsa_accum_lambda0.4_rs$n.txt" &
#     sleep 1
#     python3 ./client/client.py -port $((6000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.4
# done
# for((n=0;n<50;n++))
# do
#     echo "----------------    SARSA \0.5 $n    ------------------"
#     python3 ./server/server.py -port $((6000+$n)) -i 1 -rs $n -ne 1600 -q | tee "results/i1_sarsa_accum_lambda0.5_rs$n.txt" &
#     sleep 1
#     python3 ./client/client.py -port $((6000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.5
# done
# for((n=0;n<50;n++))
# do
#     echo "----------------    SARSA \0.6 $n    ------------------"
#     python3 ./server/server.py -port $((6000+$n)) -i 1 -rs $n -ne 1600 -q | tee "results/i1_sarsa_accum_lambda0.6_rs$n.txt" &
#     sleep 1
#     python3 ./client/client.py -port $((6000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.6
# done
# for((n=0;n<50;n++))
# do
#     echo "----------------    SARSA \0.7 $n    ------------------"
#     python3 ./server/server.py -port $((6000+$n)) -i 1 -rs $n -ne 1600 -q | tee "results/i1_sarsa_accum_lambda0.7_rs$n.txt" &
#     sleep 1
#     python3 ./client/client.py -port $((6000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.7
# done
# for((n=0;n<50;n++))
# do
#     echo "----------------    SARSA \0.8 $n    ------------------"
#     python3 ./server/server.py -port $((6000+$n)) -i 1 -rs $n -ne 1600 -q | tee "results/i1_sarsa_accum_lambda0.8_rs$n.txt" &
#     sleep 1
#     python3 ./client/client.py -port $((6000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.8
# done
# for((n=0;n<50;n++))
# do
#     echo "----------------    SARSA \0.9 $n    ------------------"
#     python3 ./server/server.py -port $((6000+$n)) -i 1 -rs $n -ne 1600 -q | tee "results/i1_sarsa_accum_lambda0.9_rs$n.txt" &
#     sleep 1
#     python3 ./client/client.py -port $((6000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.9
# done


