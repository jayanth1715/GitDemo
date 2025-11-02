import argparse
import sys
from typing import Union, Optional


__version__ = "0.1.0"


Num = Union[int, float]


class Calculator:
	"""Simple calculator supporting basic arithmetic."""
	def add(self, a: Num, b: Num) -> Num:
		return a + b

	def sub(self, a: Num, b: Num) -> Num:
		return a - b

	def mul(self, a: Num, b: Num) -> Num:
		return a * b

	def div(self, a: Num, b: Num) -> Num:
		if b == 0:
			raise ZeroDivisionError("division by zero")
		return a / b


def parse_args(argv: Optional[list] = None) -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(description="Sample Python calculator demo")
	sub = parser.add_subparsers(dest="cmd", help="sub-commands")

	# calc subcommand
	calc = sub.add_parser("calc", help="perform a calculation")
	calc.add_argument("op", choices=["add", "sub", "mul", "div"], help="operation")
	calc.add_argument("a", type=float, help="first operand")
	calc.add_argument("b", type=float, help="second operand")

	# interactive REPL
	sub.add_parser("interactive", help="start interactive REPL")

	# run quick built-in tests
	parser.add_argument("--test", action="store_true", help="run basic self-tests and exit")

	return parser.parse_args(argv)


def sample_usage():
	"""Show programmatic use of the Calculator."""
	c = Calculator()
	print(f"Calculator demo v{__version__}")
	print("Sample usage:")
	print("  2 + 3 =", c.add(2, 3))
	print("  5 - 1 =", c.sub(5, 1))
	print("  4 * 2.5 =", c.mul(4, 2.5))
	try:
		print("  10 / 2 =", c.div(10, 2))
	except ZeroDivisionError as e:
		print("  error:", e)


def run_tests() -> int:
	"""Run a few assertions to validate behavior. Returns 0 on success, 1 on failure."""
	c = Calculator()
	try:
		assert c.add(1, 2) == 3
		assert c.sub(5, 3) == 2
		assert c.mul(3, 4) == 12
		assert abs(c.div(7, 2) - 3.5) < 1e-9
		# division by zero should raise
		try:
			c.div(1, 0)
			print("Expected ZeroDivisionError but none was raised.")
			return 1
		except ZeroDivisionError:
			pass
	except AssertionError as e:
		print("Test failed:", e)
		return 1

	print("All tests passed.")
	return 0


def repl():
	"""Simple REPL for doing calculations."""
	c = Calculator()
	print("Calculator REPL. Type 'quit' or 'exit' to stop.")
	while True:
		try:
			line = input("calc> ").strip()
		except (EOFError, KeyboardInterrupt):
			print()
			break
		if not line:
			continue
		if line.lower() in ("quit", "exit"):
			break
		parts = line.split()
		if len(parts) != 3:
			print("Usage: <op> <a> <b>   e.g. add 1 2")
			continue
		op, sa, sb = parts
		try:
			a = float(sa)
			b = float(sb)
		except ValueError:
			print("Operands must be Nums.")
			continue
		try:
			if op == "add":
				print(c.add(a, b))
			elif op == "sub":
				print(c.sub(a, b))
			elif op == "mul":
				print(c.mul(a, b))
			elif op == "div":
				print(c.div(a, b))
			else:
				print("Unknown op. Use add|sub|mul|div")
		except Exception as e:
			print("Error:", e)


def main(argv: Optional[list] = None) -> int:
	args = parse_args(argv)
	if args.test:
		return run_tests()

	if args.cmd == "calc":
		c = Calculator()
		op = args.op
		a = args.a
		b = args.b
		try:
			result = {
				"add": c.add,
				"sub": c.sub,
				"mul": c.mul,
				"div": c.div,
			}[op](a, b)
			print(result)
			return 0
		except Exception as e:
			print("Error:", e, file=sys.stderr)
			return 2

	if args.cmd == "interactive":
		repl()
		return 0

	# no subcommand: show sample usage
	sample_usage()
	return 0


if __name__ == "__main__":
	sys.exit(main())
