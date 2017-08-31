from config.arguments import parser
from algorithms import MDP, linear_program, howard_pi, random_pi, batch_pi


def main():
    args = parser.parse_args()
    mdp = MDP(args.mdp)
    if args.algorithm == 'lp':
        policy, value = linear_program(mdp, args)
    elif args.algorithm == 'hpi':
        policy, value = howard_pi(mdp, args)
    elif args.algorithm == 'rpi':
        policy, value = random_pi(mdp, args)
    else:
        policy, value = batch_pi(mdp, args)
    for i, j in zip(value, policy):
        print("%.10f\t%d" % (i, j))


if __name__ == '__main__':
    main()
