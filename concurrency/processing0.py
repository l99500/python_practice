from multiprocessing import Process, cpu_count
import time
import os


class MuchCPU(Process):
    def run(self):
        print(os.getpid())
        for i in range(200000000):
            pass


if __name__ == '__main__':
    process = [MuchCPU() for f in range(cpu_count())]
    t = time.time()
    for p in process:
        p.start()
    for p in process:
        p.join()
    print('work took {} seconds'.format((time.time() - t)))
