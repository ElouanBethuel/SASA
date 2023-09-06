
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

	theta = np.random.uniform(0, np.pi, 92)
	phi = np.random.uniform(0, 2*np.pi, 92)
	test_x = x + (radius * np.sin(theta) * np.cos(phi))
	test_y = y + (radius * np.sin(theta) * np.sin(phi))
	test_z = z + (radius * np.cos(theta))
	
	point = np.array([test_x, test_y, test_z]).T

	return point
	
	


def test_point_graphic(x,y,z, radius):
	
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

	list_all_points = {}
	
	for atome in info_pdb:
	
		point = test_point(float(atome[3]), float(atome[4]), float(atome[5]), float(atome[6]))
		list_all_points[atome[0]]  = point

	return list_all_points




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

list_atomes_neigbords = neigbords(502, info, 5)

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


#plt.figure()
#axes = plt.axes(projection="3d")
#axes.scatter(array_x_pdb, array_y_pdb, array_z_pdb, color="blue")
#axes.scatter(float(info[502][3]), float(info[502][4]), float(info[502][5]), s= 300, color="green")
#axes.scatter(array_x_neigbords, array_y_neigbords, array_z_neigbords, s=200, color='red')
#plt.show()






# fonction pour déterminer le pourcentage de sondes accessibles au solvant 
# pour chaque atome de la protéine 



def access_solvant(info, list_all_neigbords, list_all_atomes_sondes):

	sum_acc_area = 0 

	for atome in info:
	
		sondes = list_all_atomes_sondes[atome[0]]
		
		neigbords = list_all_neigbords[i]
		nb_sondes = 0 
		
		for neigbord in neigbords:
			
			x_n = float(neigbord[3])
			y_n = float(neigbord[4])
			z_n = float(neigbord[5])
			
			point_n = np.array([x_n, y_n, z_n])
			
			#calcules les distances euclidiennes entre l'atome voisin et les sondes de l'atome 
			distances = np.linalg.norm(sondes - point_n, axis=1)
			

			points_inacessibles = distances < float(atome[6])
			indices_points_inacessibles = np.where(points_inacessibles)[0]
			sondes[indices_points_inacessibles] = -1
			
			
		nb_sondes_inacessibles = np.count_nonzero(sondes == -1)/3  # car 3 coordonnées x,y,z et -1 pour chaque 
		prct_acc_atome = 100 - ((nb_sondes_inacessibles / (np.size(sondes)/3)) * 100)
		
		area_acc_atome = (prct_acc_atome/100) * 4*np.pi*(float(atome[6])**2)
		
		sum_acc_area = sum_acc_area + area_acc_atome
		
		print(atome)
		print("\n")
		print(nb_sondes_inacessibles)
		print("\n")
		print(prct_acc_atome)
		print("\n")
		print(area_acc_atome)
		print("\n")
	
	print(sum_acc_area)
			

list_all_atomes_sondes = all_atomes_sondes(info)
list_all_neigbord = all_neigbords(info , 100)
access_solvant(info, list_all_neigbord, list_all_atomes_sondes)












