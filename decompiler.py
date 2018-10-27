from pathlib import Path
import subprocess, os, time, urllib.request

def downloadFile(filename, url):
    try:
        print(f'Downloading {filename}...')
        f = urllib.request.urlopen(url)
        with open(filename, 'wb') as local_file:
            local_file.write(f.read())
    except urllib.request.HTTPError(e):
        print('HTTP Error')
    except urllib.request.URLError(e):
        print('URL Error')
def getMappings(version):
    r = input('Download new mappings? (y/n): ')
    if r == 'y':
        print('=== Downloading mappings ===')
        t=time.time()
        try:
            Path(f'mappings/{version}').mkdir()
        except FileExistsError:
            pass
        tsrg = f'https://raw.githubusercontent.com/skyrising/mc-data/master/snapshot/{version}/client/mapping.tsrg'
        downloadFile(f'mappings/{version}/mapping.tsrg', tsrg)
        t = time.time() - t
        print('Done in %.1fs' % t)

def remap(version):
    
    print('=== Remapping jar using SpecialSource ====')
    t=time.time()
    
    path = Path(f'~/AppData/Roaming/.minecraft/versions/{version}/{version}.jar').expanduser()
    mapp = Path(f'mappings/{version}/mapping.tsrg')
    specialsource = Path('./lib/SpecialSource.jar')

    if path.exists() and mapp.exists() and specialsource.exists():
        path = path.resolve()
        mapp = mapp.resolve()
        specialsource = specialsource.resolve()

        subprocess.run(['java','-jar',specialsource.__str__(),'--in-jar',path.__str__(),'--out-jar',f'./src/{version}-temp.jar','--srg-in',mapp.__str__()],shell=True)
        
        print(f'- New -> {version}-temp.jar')

        t = time.time() - t
        print('Done in %.1fs' % t)
    else:
        print(f'ERROR: Missing files')

def decompile(version):

    print('=== Decompiling using CFR ====')
    t=time.time()

    path = Path(f'./src/{version}-temp.jar')
    cfr = Path('./lib/cfr_0_132.jar')

    if path.exists() and cfr.exists():
        path = path.resolve()
        cfr = cfr.resolve()
        
        subprocess.run(['java','-jar',cfr.__str__(),path.__str__(),'--outputdir',f'./src/{version}','--caseinsensitivefs','true'],shell=True)
        
        print(f'- Removing -> {version}-temp.jar')
        os.remove(f'./src/{version}-temp.jar')

        t = time.time() - t
        print('Done in %.1fs' % t)
    else:
        print(f'ERROR: Missing files')

if __name__=="__main__":

    print('Current mappings:\nhttps://github.com/skyrising/mc-data/tree/master/latest/client')

    version = input('Version (eg 18w43b): ')

    if False: # Mappings
        getMappings(version)

    if False: # Remap
        remap(version)

    if True: #Decompile
        decompile(version)