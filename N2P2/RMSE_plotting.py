import os
import matplotlib.pyplot as plt
path_baseline = f'/baseline_path' #Enter path to baseline model
path_modified = f'/modified_path' #Enter path to modified model
#output_path = "/rwthfs/rz/cluster/hpcwork/p0020330/SiddhantB_MiniThesis/00_nnp/parallelization_test/Energy_trend" 
#open(output_path, 'w')                          #to erase contents


#for item in os.listdir(path):
with open(path_baseline, "r") as f :          #open poscar file as read only
    energies_test_baseline = []
    energies_train_baseline = []
    count = 0                           #index of each file
    for line in f : 
        
        count += 1                      #first line for elements present
        #print("Test : ", line)
        #print("Count : ", count)
        if count >= 1247 and (count - 1247) % 4 == 0 :
            line = line.strip().split()
            if line[3] == 'finished:' :
                #print('break')
                break
            #lines = [line.strip() for line in f if line.strip() != '']
            #print("line : ", line)
            energies_test_baseline.append(float(line[4]))
            energies_train_baseline.append(float(line[3]))

'''learning_rate = path_modified.strip().split('/')[10]
print(learning_rate)
print(learning_rate[-1])'''


#for item in os.listdir(path):
with open(path_modified, "r") as f :          #open poscar file as read only
    energies_test_modified = []
    energies_train_modified = []
    count = 0                           #index of each file
    for line in f : 
        
        count += 1                      #first line for elements present
        #print("Test : ", line)
        #print("Count : ", count)
        if count >= 1247 and (count - 1247) % 4 == 0 :
            line = line.strip().split()
            if line[3] == 'finished:' :
                #print('break')
                break
            #lines = [line.strip() for line in f if line.strip() != '']
            #print("line : ", line)
            energies_test_modified.append(float(line[4]))
            energies_train_modified.append(float(line[3]))

train_rmse_diff = [i - j for i , j in zip(energies_train_modified , energies_train_baseline)]
test_rmse_diff  = [i - j for i , j in zip(energies_test_modified  , energies_test_baseline)]


# train performance
fig = plt.figure()
plt.plot(energies_train_baseline[1:])
plt.plot(energies_train_modified[1:])
plt.plot(train_rmse_diff[1:])
#plt.legend(['Baseline (1E-6)', f'LR = 1E-{learning_rate[-1]}', 'RMSE difference'], loc = 'upper right')
plt.legend(['Baseline dataset', 'Expanded dataset', 'RMSE difference'], loc = 'upper right')
plt.xlabel('Epochs')
plt.ylabel('RMSE energy in eV')
#plt.title(f'Comparision of training performance between baseline and LR = 1E-{learning_rate[-1]}')
plt.title(f'Training performance baseline vs expanded dataset')
#plt.savefig(f"RMSE difference training of LR = 1E-{learning_rate[-1]}")
plt.savefig(f"RMSE_difference_training_of_expanded_dataset")

# test performance
fig = plt.figure()
plt.plot(energies_test_baseline[1:])
plt.plot(energies_test_modified[1:])
plt.plot(test_rmse_diff[1:])
#plt.legend(['Baseline (1E-6)', f'LR = 1E-{learning_rate[-1]}', 'RMSE difference'], loc = 'upper right')
plt.legend(['Baseline dataset', 'Expanded dataset', 'RMSE difference'], loc = 'upper right')
plt.xlabel('Epochs')
plt.ylabel('RMSE energy in eV')
#plt.title(f'Comparision of testing performance between baseline and LR = 1E-{learning_rate[-1]}')
plt.title(f'Testing performance baseline vs expanded dataset')
#plt.savefig(f"RMSE difference testing LR = 1E-{learning_rate[-1]}")
plt.savefig(f"RMSE_difference_testing_of_expanded_dataset")
