import json
import math
import random
import time
from datetime import datetime


class MachineSimulator:
    """Simule une machine avec 4 capteurs et des pannes aléatoires."""

    def __init__(self, machine_id="M1", fault_prob=0.02):
        self.machine_id = machine_id
        self.fault_prob = fault_prob
        self.t = 0
        self.fault = None
        self.fault_left = 0
        self.fault_total = 1

    def _maybe_start_fault(self):
        if self.fault is None and random.random() < self.fault_prob:
            self.fault = random.choice(["overheating", "vibration"])
            self.fault_total = random.randint(20, 40)
            self.fault_left = self.fault_total

    def read(self):
        self.t += 1
        self._maybe_start_fault()

        # Fonctionnement normal
        temperature = 60 + 2 * math.sin(self.t / 30) + random.gauss(0, 0.8)
        vibration = 2.0 + random.gauss(0, 0.15)
        current = 12 + random.gauss(0, 0.4)
        pressure = 6 + random.gauss(0, 0.1)
        label = 0

        # Panne en cours : dérive progressive
        if self.fault:
            progress = 1 - self.fault_left / self.fault_total
            label = 1
            if self.fault == "overheating":
                temperature += 25 * progress
                current += 3 * progress
            elif self.fault == "vibration":
                vibration += 3 * progress + random.gauss(0, 0.3)
                temperature += 5 * progress
            self.fault_left -= 1
            if self.fault_left <= 0:
                self.fault = None

        return {
            "machine_id": self.machine_id,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "temperature": round(temperature, 2),
            "vibration": round(vibration, 2),
            "current": round(current, 2),
            "pressure": round(pressure, 2),
            "fault": label,
        }


if __name__ == "__main__":
    machine = MachineSimulator("M1")
    while True:
        print(json.dumps(machine.read()))
        time.sleep(0.5)