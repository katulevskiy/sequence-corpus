import hashlib
import random
import subprocess
from case_factory import new_case


def rng_for(key):
    return random.Random(int.from_bytes(hashlib.sha256(("sequence-corpus:" + key).encode()).digest(), "big"))


def git(root, *args, **kwargs):
    return subprocess.run(["git", "-C", str(root), *args], check=True,
                          capture_output=True, text=True, **kwargs).stdout.strip()


def corpus_case(event_id):
    rng = rng_for(event_id + ':corpus')
    operation, values, argument, answer, scenario = new_case(rng, set())
    row = '\t'.join([operation, str(argument), ','.join(map(str, values)), ','.join(map(str, answer))]) + '\n'
    return row, f'test(corpus/{operation}): cover {scenario}'


