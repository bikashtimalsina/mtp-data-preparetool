import numpy as np
import outcar_process as ops 
data=ops.mtpoutcar("./OUTCAR")
sysinfo=data.get_sysinfo_energy()
nions=sysinfo['ions']
ionsname=sysinfo['ions_name']
ionspertype=sysinfo['ions_per_type']
typemtp=[]
index=[i for i in range(len(ionsname))]
for i in range(len(ionspertype)):
    for j in range(ionspertype[i]):
        typemtp.append(index[i])
stress=sysinfo['stress']
energy=sysinfo['energy']
lattice=data.get_lattice_vectors()
direct_lattice=lattice['direct']
position_energy=data.get_pos_forces(nions)
posenergy=position_energy['position-force']
with open("data.cfg","w") as file:
    for i in range(len(energy)):
        file.writelines("BEGIN_CFG")
        file.writelines("\n")
        file.writelines(" Size")
        file.writelines("\n")
        file.writelines("\t {}".format(nions))
        file.writelines("\n")
        file.writelines(" Supercell")
        file.writelines("\n")
        for j in range(3):
            file.writelines("\t\t {:.6f}\t {:.6f}\t {:.6f}".format(direct_lattice[i][j][0],direct_lattice[i][j][1],direct_lattice[i][j][2]))
            file.writelines("\n")
        file.writelines(" AtomData:  id type       cartes_x      cartes_y      cartes_z           fx          fy          fz")
        file.writelines("\n")
        for k in range(nions):
            nid='{0: <4}'.format(str(k+1))
            attype='{0: <4}'.format(str(typemtp[k]))
            file.writelines("\t\t\t {} \t {} \t {:.8f} \t {:.8f} \t {:.8f} \t {:.8f} \t {:.8f} \t {:.8f}".format(nid,attype,posenergy[i][k,0],posenergy[i][k,1],\
            posenergy[i][k,2],posenergy[i][k,3],posenergy[i][k,4],posenergy[i][k,5]))
            file.writelines("\n")
        file.writelines(" Energy")
        file.writelines("\n")
        file.writelines("\t {}".format(energy[i]))
        file.writelines("\n")
        file.writelines(" PlusStress:  xx          yy          zz          yz          xz          xy")
        file.writelines("\n")
        file.writelines("\t\t {:.8f} \t {:.8f} \t {:.8f} \t {:.8f} \t {:.8f} \t {:.8f}".format(stress[i][0],stress[i][1],stress[i][2],stress[i][3],stress[i][4],stress[i][5]))
        file.writelines("\n")
        file.writelines(" Feature   EFS_by   VASP")
        file.writelines("\n")
        file.writelines("END_CFG")
        file.writelines("\n")
        file.writelines("\n")
file.close()
