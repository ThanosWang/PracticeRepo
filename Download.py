from github import Github
import os
import requests
import sys
import shutil
import json

if sys.version_info.major ==3:
    raw_input = input

g = Github('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')

repo = g.get_repo("ThanosWang/PracticeRepo")

Allmetadata = repo.get_contents('Metadata')

api_path = os.getcwd()

Flag = 0

def preparation():
    # Create a temporary folder for metadata
    if sys.version_info.major ==3:
        try:
            os.mkdir('MetadatafilesTemporaryFolder')
        except FileExistsError:
            os.chdir('MetadatafilesTemporaryFolder')
            return

    if sys.version_info.major ==2:
        try:
            os.mkdir('MetadatafilesTemporaryFolder')
        except Exception:
            os.chdir('MetadatafilesTemporaryFolder')
            return
    
    os.chdir('MetadatafilesTemporaryFolder')

    for i in Allmetadata:
        name = i.name
        url = 'https://raw.githubusercontent.com/ThanosWang/PracticeRepo/main/Metadata/'
        url += name
        metadata = requests.get(url)
        open(name,'wb').write(metadata.content)
    global Flag
    Flag = 1

   

print('You can search for model with Paper_id, Model Doi, pdg code or name (of certain particles).')

while True:
    search_type = raw_input('Please choose your keyword type:')

    if search_type == 'Paper_id':
        paper_id = raw_input('Please enter your needed paper_id:')
        if Flag == 0:
            preparation()
        for file in os.listdir('.'):
            with open(file) as metadata:
                metadatafile = json.load(metadata)
            if paper_id == metadatafile['Paper_id']:
                print('The metadata file %s has the paper_id you are looking for.' %(file))
    
    if search_type == 'Model Doi':
        Model_Doi = raw_input('Please enter your needed Model doi:')
        if Flag == 0:
            preparation()
        for file in os.listdir('.'):
            with open(file) as metadata:
                metadatafile = json.load(metadata)
            if Model_Doi == metadatafile['Model Doi']:
                print('The metadata file %s has Model Doi %s you are looking for.' %(file,metadatafile['Model Doi']))
    
    if search_type == 'pdg code':
        pdg_code = raw_input('Please enter your needed pdg code:').split(',')
        pdg_code_list = [int(i) for i in pdg_code]
        if Flag == 0:
            preparation()
        for file in os.listdir('.'):
            with open(file) as metadata:
                metadatafile = json.load(metadata)
            All_particles_pdg_code = [metadatafile['All Particles'][i] for i in metadatafile['All Particles']]
            pdg_dict = {}
            pdg_code_compare_result = all(i in All_particles_pdg_code for i in pdg_code_list)
            if pdg_code_compare_result:
                for i in metadatafile['All Particles']:
                    if metadatafile['All Particles'][i] in pdg_code_list:
                        pdg_dict[i] = metadatafile['All Particles'][i]
                print('The metadata file %s has particles %s you are looking for.' %(file,str(pdg_dict)))
    
    if search_type == 'name':
        particle_name_list = raw_input('Please enter your needed pdg code:').split(',')
        if Flag == 0:
            preparation()
        pdg_code_corresponding_list = []
        for file in os.listdir('.'):
            with open(file) as metadata:
                metadatafile = json.load(metadata)
            All_particles_name_list = [i for i in metadatafile['All Particles']]
            particle_compare_result = all(i in All_particles_name_list for i in particle_name_list)
            if particle_compare_result:
                pdg_code_corresponding_list = [metadatafile['All Particles'][i] for i in particle_name_list]
                break
        if pdg_code_corresponding_list != []:
            for file in os.listdir('.'):
                with open(file) as metadata:
                    metadatafile = json.load(metadata)
                All_particles_pdg_code = [metadatafile['All Particles'][i] for i in metadatafile['All Particles']]
                pdg_dict_from_particles = {}
                pdg_code_compare_result_from_particles = all(i in All_particles_pdg_code for i in pdg_code_corresponding_list)
                if pdg_code_compare_result_from_particles:
                    for i in metadatafile['All Particles']:
                        if metadatafile['All Particles'][i] in pdg_code_corresponding_list:
                            pdg_dict_from_particles[i] = metadatafile['All Particles'][i]
                    print('The metadata file %s has particles %s you are looking for.' %(file,str(pdg_dict_from_particles)))
            
    if raw_input('Do you still want to search for models? Please type in Yes or No.') == 'No':
        break
        
download_command = raw_input('You can choose the metadata you want to download, or type No to exsit:')

if download_command == 'No':
    os.chdir(api_path)
    shutil.rmtree('MetadatafilesTemporaryFolder')
    sys.exit()
else:
    download_list = download_command.split(',')
    download_doi_dic = {}
    for file in download_list:
        with open(file) as metadata:
            metadatafile = json.load(metadata)
        download_doi_dic[file] = metadatafile['Model Doi']
        
print(download_doi_dic)
os.chdir(api_path)
shutil.rmtree('MetadatafilesTemporaryFolder')

os.mkdir('UFOModelDownloadFileFolder')
os.chdir('UFOModelDownloadFileFolder')

