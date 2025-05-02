# utils/logger.py
# version: 1.0.0
# changelog:
# - v1.0.0: DualLogger 클래스 생성 (로그 이중 출력)

import sys

class DualLogger:
    def __init__(self, path):
        self.terminal = sys.stdout
        self.log = open(path, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()
