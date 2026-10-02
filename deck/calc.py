import math
k,ks,h,rw,re,rs = 100.0,20.0,50.0,0.354,745.0,3.0
mu,B,pbar,pwf = 1.0,1.2,3500.0,2500.0
dp = pbar-pwf
J0 = 0.00708*k*h/(mu*B*(math.log(re/rw)-0.75))
S  = (k/ks-1)*math.log(rs/rw)
Jd = 0.00708*k*h/(mu*B*(math.log(re/rw)-0.75+S))
q0, qd = J0*dp, Jd*dp
print(f"ln(re/rw)      = {math.log(re/rw):.2f}")
print(f"ln(re/rw)-0.75 = {math.log(re/rw)-0.75:.2f}  (slide 7 says ~6.9)")
print(f"S (Hawkins)    = {S:.2f}   -> slide 16 says 8.55, slide 2 uses 8.5")
print(f"J undamaged    = {J0:.2f} STB/d/psi -> slide 2 says 4.27")
print(f"J damaged      = {Jd:.2f} STB/d/psi -> slide 2 says 1.91")
print(f"q undamaged    = {q0:.0f} STB/d    -> 4,270")
print(f"q damaged      = {qd:.0f} STB/d    -> 1,910")
print(f"FE             = {Jd/J0:.3f}      -> 0.447")
print(f"drop           = {(Jd/J0-1)*100:.1f}%  -> -55%")
dps = 141.2*qd*B*mu*S/(k*h)
print(f"dp_skin        = {dps:.0f} psi    -> 553")
print(f"  check 141.2*qd*B*S/(k*h) = {141.2*qd*B*S/(k*h):.1f}")
# acidizing: S 8.55 -> 2
J2 = 0.00708*k*h/(mu*B*(math.log(re/rw)-0.75+2))
print(f"q at S=2       = {J2*dp:.0f} STB/d -> 3,310")
print(f"gain           = {J2*dp-qd:.0f} STB/d -> 1,405")
print(f"margin/day     = {(J2*dp-qd)*0.5*30:.0f} $/day -> 21,075 ; payback={300000/((J2*dp-qd)*0.5*30):.1f} d")
# slide 5: 30% of drawdown within 3 ft
print(f"\n30% check: SSR profile  p ~ ln(r_e/r)")
import numpy as np
def frac(r):  # fraction of total drawdown consumed between rw and r
    return (math.log(r/rw))/(math.log(re/rw)-0.75)
print(f"  fraction of drawdown from rw to 3 ft = {frac(3.0)*100:.1f}%  (slide 5 says 'about 30%')")
