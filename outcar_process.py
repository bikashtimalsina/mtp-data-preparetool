import numpy as np
import re
class mtpoutcar:
    def __init__(self,filename):
        self.filename=filename
    def get_sysinfo_energy(self):
        energy_text=[]
        nions=[]
        ionspertype=[]
        ionname=[]
        stress=[]
        with open(self.filename,"r") as file:
            for line in file:
                enfind=re.findall("free  energy   TOTEN  =",line)
                numions=re.findall("NIONS",line)
                ionptype=re.findall("ions per type =",line)
                ionnamepattern='(?<=VRHFIN =)(.*)(?=:)'
                ion_name=re.findall(ionnamepattern,line)
                stress_find=re.findall("Total",line)
                if len(numions)>0:
                    ionpattern='(?<=NIONS)(.*)'
                    grab_nions=re.findall(ionpattern,line)
                    onlynumIpattern='(?<==)(.*)'
                    onlynumI=re.findall(onlynumIpattern,grab_nions[0])
                    nions.append(int(onlynumI[0].strip()))
                if len(ionptype)>0:
                    ionptpattern='(?<=ions per type =)(.*)'
                    grab_iptype=re.findall(ionptpattern,line)
                    iontypes=grab_iptype[0].strip()
                    ionspertype.append(np.int64(iontypes.split()))
                if len(ion_name)>0:
                    ionname.append(ion_name[0])
                if len(stress_find)>0:
                    stresspattern='(?<=Total)(.*)'
                    stressval=re.findall(stresspattern,line)
                    stresstensor=stressval[0].strip().split()
                    if len(stresstensor)==6:
                        stress.append(np.float64(stresstensor))
                if len(enfind)>0:
                    pattern='(?<=-)(.*)(?=[0-9])'
                    grab_energy=re.findall(pattern,line)
                    if len(grab_energy)>0:
                        energy_text.append(float("-"+grab_energy[0]))
        file.close()
        energy_sys={'ions':nions[0],'ions_name':ionname,'ions_per_type':ionspertype[0],'stress':stress,'energy':energy_text}
        return energy_sys
    def get_lattice_vectors(self):
        latindex=[]
        counter=1
        lattice_search="direct lattice vectors"        
        with open(self.filename,"r") as file:
            for line in file:
                all_lattice=re.findall(lattice_search,line)
                if len(all_lattice)>0:
                    latindex.append(counter)
                counter += 1
        file.close()
        all_direct=[]
        all_reciprocal=[]
        for i in range(len(latindex)):
            each_direc=[]
            each_reciproc=[]
            with open(self.filename,"r") as file:
                for index,line in enumerate(file):
                    if index+1>latindex[i] and index+1 <= latindex[i]+3:
                        each_direc.append(line.strip().split()[0])
                        each_direc.append(line.strip().split()[1])
                        each_direc.append(line.strip().split()[2])
                        each_reciproc.append(line.strip().split()[3])
                        each_reciproc.append(line.strip().split()[4])
                        each_reciproc.append(line.strip().split()[5])
                all_direct.append(np.reshape(np.float64(each_direc),(3,3)))
                all_reciprocal.append(np.reshape(np.float64(each_reciproc),(3,3)))
            file.close()
        latticeVectors={'direct':all_direct,'reciprocal':all_reciprocal}
        return latticeVectors
    def get_pos_forces(self,ionsNum):
        posforce_text='POSITION                                       TOTAL-FORCE \(eV\/Angst\)'
        posforce_index=[]
        counter=1
        with open(self.filename,"r") as file:
            for line in file:
                all_pos_force=re.findall(posforce_text,line)
                if len(all_pos_force)>0:
                    posforce_index.append(counter)
                counter += 1
        file.close()
        all_pforce=[]
        for i in range(len(posforce_index)):
            each_pforce=[]
            with open(self.filename,"r") as file:
                for index,line in enumerate(file):
                    if index+1>posforce_index[i]+1 and index+1 <= posforce_index[i]+1+ionsNum:
                        each_pforce.append(np.float64(line.strip().split()))
            all_pforce.append(np.matrix(each_pforce))
            file.close()
        posforcedict={"position-force":all_pforce} 
        return posforcedict
if __name__=="__main__":
    mtpoutcar
