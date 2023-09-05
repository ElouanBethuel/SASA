
import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d


DIAMETRE_H2O = 2.8 


# script to parse PDB files and add Radius and area of solvated sphere 

def parse_pdb_file(path_pdb_file, path_w_file):

	info = []

	with open(path_pdb_file , "r") as pdb_file , open(path_w_file, "w") as info_file:
		
		for line in pdb_file:
			if line.startswith("ATOM") == True:
				split_line = line.split()
				new_line = [split_line[1], split_line[2], split_line[3], split_line[6], split_line[7], split_line[8]]
				
				# add Van der Wadd radius
				
				if new_line[1].find("N") != -1:
					new_line.append("1.55")
					
				if new_line[1].find("O") != -1:
					new_line.append("1.52")
				
				if new_line[1].find("S") != -1:
					new_line.append("1.8")
				
				if new_line[1].find("C") != -1:
					new_line.append("1.7")
				
				info.append(new_line)
				info_file.write(f"{new_line}\n")

	return info
		

info = parse_pdb_file("7kh5.pdb", "extract_info.csv")


# function for generated 92 test point
# rappel calcul air sphère : 4 × π × R² = area 
# donc le rayon :  racine carré (area / 4*pie) 

def test_point(x,y,z, radius):

	#radius = np.sqrt(solvated_sphere_area / 4*np.pi)

	theta = np.random.uniform(0, np.pi, 92)
	phi = np.random.uniform(0, 2*np.pi, 92)
	test_x = x + (radius * np.sin(theta) * np.cos(phi))
	test_y = y + (radius * np.sin(theta) * np.sin(phi))
	test_z = z + (radius * np.cos(theta))

	return test_x, test_y, test_z
	
	


def test_point_graphic(x,y,z, radius):

	#radius = np.sqrt(solvated_sphere_area / 4*np.pi)
	
	theta = np.random.uniform(0, np.pi, 92)
	phi = np.random.uniform(0, 2*np.pi, 92)
	test_x = x + (radius * np.sin(theta) * np.cos(phi))
	test_y = y + (radius * np.sin(theta) * np.sin(phi))
	test_z = z + (radius * np.cos(theta))
	
	plt.figure()
	axes = plt.axes(projection="3d")
	
	# affiche coordonnées de l'atome
	axes.scatter(x, y, z, color='red')
	
	# On affiche notre nuage de points en 3D
	axes.scatter(test_x, test_y, test_z)
	
	plt.show()
	return test_x, test_y, test_z



def all_atomes_sondes(info_pdb):
	list_all_points = []
	for i in range(len(info_pdb)):
		x,y,z = test_point(float(info[i][3]), float(info[i][4]), float(info[i][5]), float(info[i][6]))
		point = [x,y,z]
		list_all_points.append(point)

	return list_all_points


list_all_atomes_sondes = all_atomes_sondes(info)
#print(list_all_atomes_sondes)




# retourne la liste des voisins d'un atome à partir de ses coordonnées 
# et d'un  seuil (treeshold : distance en Angstrom) 

def neigbords(num_atome, info, threeshold):

	info_pdb = info.copy()
	
	x = float(info_pdb[num_atome-1][3])
	y = float(info_pdb[num_atome-1][4])
	z = float(info_pdb[num_atome-1][5])
	
	del(info_pdb[num_atome-1])
	list_neigbords = []
	
	for i in range(len(info_pdb)):
			
			x_nb = float(info_pdb[i][3])
			y_nb = float(info_pdb[i][4])
			z_nb = float(info_pdb[i][5])
			
			d = np.sqrt((x - x_nb)**2 + (y - y_nb)**2 + (z - z_nb)**2)
			
			if d < threeshold : 
				list_neigbords.append(info_pdb[i])
				print(info_pdb[i])
	
	return list_neigbords 
	
	
list_nb = neigbords(1, info, 8)



def all_neigbords(info_pdb , threeshold):
	list_all_neigbords = []
	for i in range(len(info_pdb)):
		list_all_neigbords.append(neigbords(i+1, info, threeshold))

	return list_all_neigbords 
	




# CODE POUR PLOTER TT LES POINTS DE LA PROTEINE EN BLEUE
# ET LES VOISINS DE L'ATOME SELECTIONNE EN ROUGE 

list_x_pdb = []
list_y_pdb = []
list_z_pdb = []

for i in range(len(info)):
	list_x_pdb.append(float(info[i][3]))
	list_y_pdb.append(float(info[i][4]))
	list_z_pdb.append(float(info[i][5]))

array_x_pdb = np.asarray(list_x_pdb)
array_y_pdb = np.asarray(list_y_pdb)
array_z_pdb = np.asarray(list_z_pdb)

list_atomes_neigbords = neigbords(10, info, 5)

list_x_neigbords = []
list_y_neigbords = []
list_z_neigbords = []

for i in range(len(list_atomes_neigbords)):
	list_x_neigbords.append(float(list_atomes_neigbords[i][3]))
	list_y_neigbords.append(float(list_atomes_neigbords[i][4]))
	list_z_neigbords.append(float(list_atomes_neigbords[i][5]))
	
array_x_neigbords = np.asarray(list_x_neigbords)
array_y_neigbords = np.asarray(list_y_neigbords)
array_z_neigbords = np.asarray(list_z_neigbords)


plt.figure()
axes = plt.axes(projection="3d")
axes.scatter(array_x_pdb, array_y_pdb, array_z_pdb, color="blue")
axes.scatter(float(info[10][3]), float(info[10][4]), float(info[10][5]), s= 300, color="green")
axes.scatter(array_x_neigbords, array_y_neigbords, array_z_neigbords, s=200, color='red')
plt.show()






# fonction pour déterminer le pourcentage de sondes accessibles au solvant 
# pour chaque atome de la protéine 



def access_solvant(info, list_all_neigbords):

	list_prct_solv_atomes = []
	acc_prot = 0 

	for i in range(len(info)):
	
		a,b,c = test_point(float(info[i][3]), float(info[i][4]), float(info[i][5]), float(info[i][6]))
		
		neigbords = list_all_neigbords[i]
		nb_sondes = 0 
		
		for y in range(len(neigbords)):
			
			d,e,f = test_point(float(neigbords[y][3]), float(neigbords[y][4]), float(neigbords[y][5]), float(neigbords[y][6]))
			
			x_min = abs(np.subtract(a, d))
			x_min[x_min <= 1.4] = -1
			
			y_min = abs(np.subtract(b, e))
			y_min[y_min <= 1.4] = -1

			z_min = abs(np.subtract(c, f))
			z_min[z_min <= 1.4] = -1
			
			sum_coord = np.sum([x_min, y_min, z_min], axis=0)
			nb_sondes_acc = np.count_nonzero(sum_coord == -3)
			perct_acc = round((nb_sondes_acc * 100) / 92 , 2)
			
			list_prct_solv_atomes.append([info[i][1], info[i][2], perct_acc])
			
			acc_prot = acc_prot + perct_acc 
	
	
	#print(acc_prot/len(info))
	print(list_prct_solv_atomes)
	return list_prct_solv_atomes
			
		
#list_all_neigbords = all_neigbords(info , 2)
#access_solvant(info, list_all_neigbords)
	
	
	
	







