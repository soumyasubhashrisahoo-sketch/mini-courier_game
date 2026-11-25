"""Command-line entry point.

    py main.py plan --parcels 14 --capacity 30 --seed 7
    py main.py benchmark
    py main.py play
"""

import argparse

from mini_courier import format_report, plan_trip
from mini_courier.benchmark import format_benchmark, run_benchmark
from mini_courier.server import serve_game


def main() -> None:
    parser = argparse.ArgumentParser(description="Mini-Courier Planner")
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan", help="plan one delivery trip")
    plan.add_argument("--parcels", type=int, default=14)
    plan.add_argument("--capacity", type=int, default=30, help="van capacity in kg")
    plan.add_argument("--seed", type=int, default=7)

    bench = sub.add_parser("benchmark", help="time each algorithm on growing inputs")
    bench.add_argument("--sizes", type=int, nargs="+", default=[100, 200, 400, 800])

    play = sub.add_parser("play", help="open the Courier Dash game in your browser")
    play.add_argument("--port", type=int, default=8000)
    play.add_argument("--no-browser", action="store_true", help="do not open a browser tab")

    args = parser.parse_args()
    if args.command == "play":
        serve_game(args.port, not args.no_browser)
    elif args.command == "plan":
        print(format_report(plan_trip(args.parcels, args.capacity, args.seed)))
    else:
        print(format_benchmark(run_benchmark(args.sizes), args.sizes))


if __name__ == "__main__":
    main()
