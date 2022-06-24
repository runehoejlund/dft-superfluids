import numpy as np

a=np.array([0,2,4,1])
print(a[0:len(a)])
A=np.array([[1,2],[3,4]])
Af=A.flatten()
Amax=np.max(A)
print(Amax)
print(np.where(A==Amax))
print(np.where(A==Amax)[1][0])