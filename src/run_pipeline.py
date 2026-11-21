"""One command to regenerate the synthetic data, analysis outputs, and dashboard."""
from generate_data import generate
from analyze import analyze
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
import subprocess,sys

def main():
    generate()
    print(analyze())
    subprocess.run([sys.executable,str(ROOT/'src'/'build_dashboard.py')],check=True)
if __name__=='__main__': main()
