#! /usr/bin/env python
import aipy as a, numpy as n, pylab as p,math as m
import sys, optparse

o = optparse.OptionParser()
a.scripting.add_standard_options(o, cal=True)
opts, args = o.parse_args(sys.argv[1:])


#th = n.arange(0, 2*n.pi, .01)
#fmts = (('k.','k-'), ('r.','r-.'))

x_0 = 600368.348500   #[m] UTM coordinates of ant 0 (GPS measured in GB)
y_0 = 4253657.024750
z_0 = 801.960
aa = a.cal.get_aa(opts.cal, .1, .1, 1)


antpos = [aa.get_baseline(0,i,src='z') for i in range(len(aa.ants))]
antpos = n.array(antpos) * a.const.len_ns / 100.

file = open(args[0],'r')
data = [s.split(',') for s in file.readlines()]

antpos_gps = n.array([map(float,[d[2],d[1],d[3]]) for d in data])

x,y,z = antpos[:,0]+x_0, antpos[:,1]+y_0, antpos[:,2]+z_0

cavg=15
dx,dy,dz = (0,0,0)
for i in range(200):
    dx_0 = n.random.normal(scale=2)
    dy_0 = n.random.normal(scale=2)
    dz_0 = n.random.normal(scale=2)
    antpos_t =  n.array(zip(x+dx+dx_0,y+dy+dy_0,z+dz+dz_0))
    diff= antpos_gps-antpos_t
    #rms = n.sqrt(n.variance(diff,axis=1))
    avg = n.average(diff,axis=0)
    ravg = n.sqrt(avg[0]**2+avg[1]**2+avg[2]**2)
    if ravg<cavg:
        dx +=dx_0;dy += dy_0; dz += dz_0
        cavg = ravg
#        print cavg
#print diff

for i,ant in enumerate(antpos_t):
    print "self_cal%d,%f,%f,%f,0" % (i,ant[1],ant[0],ant[2])
#p.figure()
#p.plot(antpos_gps[:,0],antpos_gps[:,1],'.')
#p.plot(antpos_t[:,0],antpos_t[:,1],'.')
#p.axis('equal')
##p.plot(x,y,'.')
#p.show()
#print dx,dy,dz

#p.figure()
#p.subplot(411)
#p.hist(diff[:,0])
#p.subplot(412)
#p.hist(diff[:,1])
#p.subplot(413)
#p.hist(diff[:,2])
#p.subplot(414)
#p.plot(diff[:,0],diff[:,1],'.')
#p.show()
#for i,l in enumerate(zip(x,y,z)):
#    print "self_cal%d,%f,%f,%f,%d"%(i,l[1],l[0],l[2],0)
#for l in antpos: print "[",l[0],",",l[1],",",l[2],"]"
#def fitfunc(vec):
#    r,cx, cy = vec
#    return ((n.sqrt((x-cx)**2 + (y-cy)**2) - r)**2).sum()
#if cnt==0: r,cx,cy = a.optimize.fmin(fitfunc, n.array([200., 0, 0]))
#print r, cx, cy
#circ_x, circ_y = r*n.cos(th), r*n.sin(th)
#if cnt==1: 
#   x_c =all_antpos[:,0,0] - cx
#   y_c =all_antpos[:,1,0] - cy
#   x_s =all_antpos[:,0,1] - cx
#   y_s =all_antpos[:,1,1] - cy
#
#   dr_a = n.zeros(len(x_c))
#   dt_a = n.zeros(len(x_c))
#   for i in range(len(x_c)):
#       dr_a[i]=m.sqrt(x_c[i]**2+y_c[i]**2) - r
#       dt_a[i]=(m.atan(y_c[i]/x_c[i]) - m.atan(y_s[i]/x_s[i]))*r
#   #p.plot(circ_x,circ_y,fmt2)
#fmt1,fmt2 = fmts[cnt % len(fmts)]
#p.plot(x,y, fmt1)
#for ant,(xa,ya,za) in enumerate(zip(x,y,z)):
#    hx,hy = 10*za*n.cos(th)+xa, 10*za*n.sin(th)+ya
#    if za > 0: fmt3 = '#eeeeee'
#    else: fmt3 = '#a0a0a0'
#    p.fill(hx,hy, fmt3,alpha=0.5)
#    
#p.grid()
#delta_coords = n.diff(all_antpos,axis=2)
##print x_c
#
#for d in delta_coords:
#    print d[0][0],',',d[1][0],',',d[2][0]
##p.ylim((-25,25))
##p.xlim(-150,150)
##p.ylim(-150,150)
#a = p.gca()
#a.set_aspect('equal')
##print p.axes()
#p.axes([0.4,0.4,0.2,0.2])
#p.plot(delta_coords[:,0],delta_coords[:,1],'.')
#p.xlim(-25,25)
#p.ylim(-25,25)
#p.figure()
#p.subplot(231)
#p.hist(delta_coords[:,0],20)
##(c,bins)=n.histogram(delta_coords[:,0],bins=10,new=True)
#print '<dx>','<dy>','<dz>','sigma(x,y,z)','<dr>', '<dtheta>'
#print n.mean(delta_coords,axis=0), n.std(delta_coords,axis=0),n.mean(dr_a),n.mean(dt_a),n.std(dr_a),n.std(dt_a)
#p.xlabel("delta x [m]")
#p.subplot(232)
#p.hist(delta_coords[:,1],20)
#p.xlabel("delta y [m]")
#p.subplot(233)
#p.hist(delta_coords[:,2],20)
#p.xlabel("delta z [m]")
#p.subplot(234)
#p.hist(dr_a,20)
#p.xlabel("delta r [m]")
#p.subplot(235)
#p.hist(dt_a,20)
#p.xlabel("delta l (r*theta) [m]")
##p.subplot(236)
##p.plot(r_a,t_a)
##print r_a,t_a
#p.show()
