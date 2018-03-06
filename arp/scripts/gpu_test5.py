import pycuda.autoinit
from pycuda import compiler, gpuarray, driver
import numpy as np
import math, time
import aipy

gpu_template = """
__global__ void MatSqrFloat(float *A, float*C)
{
      const uint A_height = %(A_SHAPE0)s;
      const uint A_width  = %(A_SHAPE1)s;
      const uint row = blockIdx.x * blockDim.x + threadIdx.x;
      const uint col = blockIdx.y * blockDim.y + threadIdx.y;
      float Csum = 0;

      if (row >= A_height || col >= A_height) return;

      for (int i=0; i < A_width; i++) {
          Csum += A[row * A_width + i] * A[col * A_width +i];
      }
      C[row * A_height + col] = Csum;
}
"""

GPU = True
NANT = 64
START_JD = 2458000
END_JD = 2458001
INT_TIME = 21600
NSIDE = 512
#NSIDE = 128

times = np.arange(START_JD, END_JD, INT_TIME / aipy.const.s_per_day)

a_cpu = np.zeros(shape=(NANT,12*NSIDE**2), dtype=np.float32); a_cpu[:,:] = 1.
aa_cpu = np.empty(shape=(NANT,NANT), dtype=np.float32)

#block = (32, 32, 1) # make (32,16,1) for smaller GPUs
#block = (32, 16, 1) # make (32,16,1) for smaller GPUs
block = (8, 8, 1) # make (32,16,1) for smaller GPUs
#a_gpu = driver.mem_alloc(a_cpu.nbytes)
#aa_gpu = driver.mem_alloc(aa_cpu.nbytes)
a_gpu = gpuarray.empty(a_cpu.shape, a_cpu.dtype)
aa_gpu = gpuarray.empty((a_cpu.shape[0], a_cpu.shape[0]), a_cpu.dtype)
print aa_gpu.shape, aa_gpu.nbytes
gpu_code = gpu_template % {
        'A_SHAPE0': a_cpu.shape[0],
        'A_SHAPE1': a_cpu.shape[1],
        }
gpu_module = compiler.SourceModule(gpu_code)
matsqrcmplx = gpu_module.get_function("MatSqrFloat")
grid = (int(math.ceil(a_cpu.shape[0]/float(block[0]))),int(math.ceil(a_cpu.shape[0]/float(block[1]))))
print grid, block

import time
print '# Antennas:', NANT
print 'NSIDE:', NSIDE
print 'Starting', time.time()
for ti,jd in enumerate(times):
    print ti,'/',len(times)
    if GPU:
        t1 = time.time()
        #driver.memcpy_htod(a_gpu,a_cpu)
        a_gpu.set(a_cpu)
        t2 = time.time()
        matsqrcmplx(a_gpu, aa_gpu, grid=grid, block=block)
        t3 = time.time()
        #driver.memcpy_dtoh(aa_cpu, aa_gpu)
        aa_cpu = aa_gpu.get(aa_cpu)
        t4 = time.time()
        print t2-t1,t3-t2,t4-t3
    else:
        aa_cpu = np.dot(a_cpu, a_cpu.T.conj())

print 'Done', time.time()
