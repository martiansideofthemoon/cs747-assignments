import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--mdp", default="data/MDP2.txt", type=str, help="Path to MDP file")
parser.add_argument("--algorithm", default="lp", type=str, help="MDP Solver choice",
                    choices=["lp", "hpi", "rpi", "bspi"])
parser.add_argument("--batchsize", default=2, type=int, help="Batch size for bspi")
parser.add_argument("--randomseed", default=0, type=int, help="Seed to be used in rpi")
