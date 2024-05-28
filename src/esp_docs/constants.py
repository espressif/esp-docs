from collections import defaultdict


TARGET_NAMES = {'esp8266': 'ESP8266',
                'esp32': 'ESP32',
                'esp32s2': 'ESP32-S2',
                'esp32s3': 'ESP32-S3',
                'esp32c3': 'ESP32-C3',
                'esp32c2': 'ESP32-C2',
                'esp32h2': 'ESP32-H2',
                'esp32c5': 'ESP32-C5',
                'esp32c6': 'ESP32-C6',
                'esp32c61': 'ESP32-C61',
                'esp32p4': 'ESP32-P4'
                }

TARGETS = list(TARGET_NAMES.keys())

TOOLCHAIN_PREFIX = defaultdict(lambda: 'riscv32-esp-elf')
TOOLCHAIN_PREFIX['esp8266'] = 'xtensa-lx106-elf'
TOOLCHAIN_PREFIX['esp32'] = 'xtensa-esp32-elf'
TOOLCHAIN_PREFIX['esp32s2'] = 'xtensa-esp32s2-elf'
TOOLCHAIN_PREFIX['esp32s3'] = 'xtensa-esp32s3-elf'
