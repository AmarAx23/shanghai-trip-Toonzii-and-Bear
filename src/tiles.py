# Computes the OSM tiles each day map needs (fit zoom on phone..desktop, -1 to +2) and returns per-day ranges.
import math
def lon2x(lon,z): return (lon+180)/360*2**z
def lat2y(lat,z): r=math.radians(lat); return (1-math.log(math.tan(r)+1/math.cos(r))/math.pi)/2*2**z
def fitzoom(b,w,h,pad=24,maxz=16):
    for z in range(maxz,0,-1):
        if (lon2x(b[3],z)-lon2x(b[1],z))*256<=w-2*pad and (lat2y(b[0],z)-lat2y(b[2],z))*256<=h-2*pad: return z
    return 1
def plan(route_pts):
    la=[p[0] for p in route_pts]; lo=[p[1] for p in route_pts]
    s,n,w,e=min(la),max(la),min(lo),max(lo); dla=(n-s)*.12; dlo=(e-w)*.12
    b=(s-dla,w-dlo,n+dla,e+dlo)
    zm,zd=fitzoom(b,330,220),fitzoom(b,600,220)
    zmin,zmax=min(zm,zd)-1,max(zm,zd)+2
    tiles=[]
    for z in range(zmin,zmax+1):
        m=1 if z<zmax else 0
        x0=int(lon2x(b[1],z))-m; x1=int(lon2x(b[3],z))+m; y0=int(lat2y(b[2],z))-m; y1=int(lat2y(b[0],z))+m
        tiles+=[f"{z}/{x}/{y}" for x in range(x0,x1+1) for y in range(y0,y1+1)]
    return dict(minZoom=zmin,maxZoom=zmax,bounds=[[b[0],b[1]],[b[2],b[3]]],tiles=tiles)
