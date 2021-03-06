import os
import zipfile
import tarfile
import shutil
import sys
import json
import importlib
import requests

if sys.version_info.major ==3:
    raw_input = input

# Find the folder with compressed model file and metadata.json
Path = raw_input('Please enter your whole folder contain both your compressed model file and metadata.json:')

# Get into the folder
os.chdir(Path)

# Path of the folder's content
folder_path = os.getcwd()

# List of all files in the folder
original_file = os.listdir(folder_path)

#  Check if the folder contains and only contains required files
assert len(original_file) == 2

assert 'metadata.json' in original_file

for i in original_file:
    if i.endswith('.json'):
        pass
    else:
        assert i.endswith('.zip') or i.endswith('.tgz') or i.endswith('.tar.gz')
        # Uncompress the model file to a temprory folder to get ready for validation test
        if i.endswith('.zip'):
            with zipfile.ZipFile(i, 'r') as zip:
                zip.extractall('ModelFolder')
        else:
            tarfile.open(i).extractall('ModelFolder')

# Check the completeness of the whole model as a python package
sys.path.append(folder_path)

if sys.version_info.major ==3:
    modelpath = folder_path + '/ModelFolder'
    sys.path.insert(0,modelpath)

try:
    importlib.import_module('ModelFolder')
except SyntaxError:
    raise Exception('Your model may be not compatible with Python2, please use Python3 version instead.')
except ModuleNotFoundError:
    raise Exception('You model contains no parameters.py, please check again')
except AttributeError:
    raise Exception('You may forget to define variables in your imported modules, please check again.')
except NameError:
    raise Exception('You may forget to import/define some modules/variables, please check again.')
except TypeError:
    raise Exception('One/Some of your variables missing required positional argument, please check again.')


# Show all files in the model
ModelFiles = os.listdir('ModelFolder')
print('Your model contains')
print(ModelFiles)

# Check the existence of model-independent files
NeccessaryFiles = ['__init__.py', 'object_library.py', 'function_library.py', 'write_param_card.py']
MissingFiles = [i for i in NeccessaryFiles if i not in ModelFiles]
if MissingFiles != []:
    print('Your model lacks these files below')
    print(MissingFiles)
    raise Exception('Sorry, your upload fails since your model is short of some necessary files.')

# Get into the model folder and ready for furthur test
os.chdir('ModelFolder')

model_path = os.getcwd()

sys.path.insert(0,model_path)

try:
    import object_library
except ImportError:
    os.chdir(folder_path)
    shutil.rmtree('ModelFolder')
    raise Exception('Your model may not have object_library.py. Please check again')



try:
    import parameters
except ImportError:
    os.chdir(folder_path)
    shutil.rmtree('ModelFolder')
    raise Exception('Your model may not have parameters.py. Please check again')
# Check if parameters.py contains parameters
params = []
number_of_params = 0
for i in [item for item in dir(parameters) if not item.startswith("__")]:    
    item = getattr(parameters,i)
    if type(item) == (object_library.Parameter):
        params.append(item.name)
        number_of_params += 1

if len(params) == 0:
    raise Exception('There should be parameters defined in you parameters.py.')

print('You model contains %i parameters.' %(number_of_params))

del sys.modules['parameters']



try:
    import particles
except ImportError:
    os.chdir(folder_path)
    shutil.rmtree('ModelFolder')
    raise Exception('Your model may not have particles.py. Please check again')    
# Check if particles.py contains particles
particle_dict = {}
new_particle_dict = {}
pdg_code_list = []
number_of_particles = 0
spin = [1, 2, 3, 5]
elementary_particles = [1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6, 11, 12, 13, 14, 15, 16, -11, -12, -13, -14, -15, -16, 9, 21, 22, 23, 24, -24, 25, 35, 36, 37, -37]
for i in [item for item in dir(particles) if not item.startswith("__")]:
    item = getattr(particles,i)
    if type(item) == (object_library.Particle):
        number_of_particles += 1
        particle_dict[item.name] = item.pdg_code
        pdg_code_list.append(item.pdg_code)
        if item.spin in spin and item.pdg_code not in elementary_particles:
            new_particle_dict[item.name] = item.pdg_code

if len(particle_dict) == 0:
    raise Exception('There should be particles defined in you particles.py.')

if len(set(pdg_code_list)) != len(pdg_code_list):
    raise Exception('Some of your particles have same pdg code, please check again!')

print('You model contains %i particles and corresponding pdg code below:' %(number_of_particles))
print(particle_dict)
print('You model contains new elementary particles below:')
print(new_particle_dict)

del sys.modules['particles']



try:
    import lorentz
except ImportError:
    os.chdir(folder_path)
    shutil.rmtree('ModelFolder')
    raise Exception('Your model may not have lorentz.py. Please check again')
# Check if lorentz.py contains lorentz tensors
lorentz_tensor = []
number_of_lorentz_tensors = 0
for i in [item for item in dir(lorentz) if not item.startswith("__")]:    
    item = getattr(lorentz,i)
    if type(item) == (object_library.Lorentz):
        lorentz_tensor.append(item.name)
        number_of_lorentz_tensors += 1

if len(lorentz_tensor) == 0:
    raise Exception('There should be lorentz tensors defined in you lorentz.py.')

print('You model contains %i lorentz tensors.' %(number_of_lorentz_tensors))

del sys.modules['lorentz']



try:
    import coupling_orders
except ImportError:
    os.chdir(folder_path)
    shutil.rmtree('ModelFolder')
    raise Exception('Your model may not have coupling_orders.py. Please check again')
# Check if coupling_orders.py contains orders
coupling_order = []
number_of_coupling_orders = 0
for i in [item for item in dir(coupling_orders) if not item.startswith("__")]:
    item = getattr(coupling_orders,i)
    if type(item) == (object_library.CouplingOrder):
        coupling_order.append(item.name)
        number_of_coupling_orders += 1

if len(coupling_order) == 0:
    raise Exception('There should be coupling orders defined in you couplings.py.')

print('You model contains %i coupling orders.' %(number_of_coupling_orders))

del sys.modules['coupling_orders']



try:
    import couplings
except ImportError:
    os.chdir(folder_path)
    shutil.rmtree('ModelFolder')
    raise Exception('Your model may not have couplings.py. Please check again')
# Check if couplings.py contains couplings
coupling_tensor = []
number_of_coupling_tensors = 0
for i in [item for item in dir(couplings) if not item.startswith("__")]:
    item = getattr(couplings,i)
    if type(item) == (object_library.Coupling):
        coupling_tensor.append(item.name)
        number_of_coupling_tensors += 1

if len(coupling_tensor) == 0:
    raise Exception('There should be coupling tensors defined in you couplings.py.')

print('You model contains %i coupling tensors.' %(number_of_coupling_tensors))

del sys.modules['couplings']



try:
    import vertices
except ImportError:
    os.chdir(folder_path)
    shutil.rmtree('ModelFolder')
    raise Exception('Your model may not have verticesS.py. Please check again')
# Check if vertices.py contains vertices
vertex = []
number_of_vertices = 0
for i in [item for item in dir(vertices) if not item.startswith("__")]:
    item = getattr(vertices,i)
    if type(item) == (object_library.Vertex):
        vertex.append(item.name)
        number_of_vertices += 1

if len(vertex) == 0:
    raise Exception('There should be vertices defined in you vertices.py')

print('You model contains %i vertices.' %(number_of_vertices))

del sys.modules['vertices']



try:
    import propagators
    # Check if propagators.py contains propagators
    props = []
    number_of_propagators = 0
    for i in [item for item in dir(propagators) if not item.startswith("__")]:
        item = getattr(propagators,i)
        if type(item) == (object_library.Propagator):
            props.append(item.name)
            number_of_propagators += 1

    if len(props) == 0:
        raise Exception('There should be propagators defined in you propagators.py')

    print('You model contains %i propagators.' %(number_of_propagators))
    del sys.modules['propagators']  
except ImportError:
    pass



try:
    import decays
    # Check if decays.py contains decays
    decay = []
    number_of_decays = 0
    for i in [item for item in dir(decays) if not item.startswith("__")]:
        item = getattr(decays,i)
        if type(item) == (object_library.Decay):
            decay.append(item.name)
            number_of_decays += 1

    if len(decay) == 0:
        raise Exception('There should be decays defined in you decays.py')

    print('You model contains %i decays.' %(number_of_decays))
    del sys.modules['decays']
except ImportError:
    pass

# Finish the validation checking
sys.path.remove(model_path)
os.chdir(folder_path)
shutil.rmtree('ModelFolder')


# Check uploaded metadata.json
with open('metadata.json') as metadata:
    file = json.load(metadata)

assert file['Author']
assert file['Paper_id']
assert file['Keywords']

# Upload the model to Zenodo and get a Doi for the model


# Name the new model
modelname = raw_input('Please name your model:')
# Create new metadata
newcontent = {'Model name' : modelname,
              'Model Doi' : 1,
              'All Particles' : particle_dict,
              'New elementary particles' : new_particle_dict,
              'Number of parameters' : number_of_params,
              'Number of vertices' : number_of_vertices,
              'Number of coupling orders' : number_of_coupling_orders,
              'Number of coupling tensors' : number_of_coupling_tensors,
              'Number of lorentz tensors' : number_of_lorentz_tensors,
              'Model Python Version' : sys.version_info.major}

file.update(newcontent)

try:
    propagatornumber = {'Number of Propagators' : number_of_propagators}
    file.update(propagatornumber)
except NameError:
    pass

try:
    decaynumber = {'Number of Decays' : number_of_decays}
    file.update(decaynumber)
except NameError:
    pass


metadata_name = newcontent['Model name'] + '.json'
with open(metadata_name,'w') as metadata:
    json.dump(file,metadata,indent=2)
    

