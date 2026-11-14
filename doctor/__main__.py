import argparse
from . import analyze as a

p = argparse.ArgumentParser(prog="doctor")
p.add_argument("csv")
p.add_argument("--table", default="my_source.my_table")
p.add_argument("--target-mb", type=int, default=128)
args = p.parse_args()
r = a.analyze(a.load(args.csv), args.target_mb)
print(f"files={r.total_files} small={r.small_files} ({r.small_ratio:.0%}) "
      f"median={r.median_mb:.1f}MB severity={r.severity}")
print(a.suggest(args.table, r))
