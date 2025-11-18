import importlib.util

spec = importlib.util.spec_from_file_location("main", "./main.py")
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)
