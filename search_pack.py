#!/usr/bin/env python3
import apt
import apt.debfile
import apt_pkg
import tempfile
import shutil
import json

tmpdir = tempfile.mkdtemp()
print(tmpdir)
apt_pkg.init()

package = apt_pkg.Cache()['gnome-shell']
rev = package.rev_depends_list
dependancy_dict = {}
for i in rev:
    print(i.parent_pkg.name, i.parent_ver.ver_str)
    if i.parent_pkg.name not in dependancy_dict.keys():
        dependancy_dict[i.parent_pkg.name] = []
    temp = f"{i.parent_pkg.name} {i.parent_ver.ver_str}"
    temp += " "
    temp += f"Depedency {i.target_pkg.name} {i.comp_type} {i.target_ver}"

    if dependancy_dict[i.parent_pkg.name] and apt_pkg.version_compare(dependancy_dict[i.parent_pkg.name][0][0], i.parent_ver.ver_str) < 0:
        print(f"package: {i.parent_pkg.name} comare {dependancy_dict[i.parent_pkg.name][0][0]} {i.parent_ver.ver_str}")
        dependancy_dict[i.parent_pkg.name] = []
    if dependancy_dict[i.parent_pkg.name] and apt_pkg.version_compare(dependancy_dict[i.parent_pkg.name][0][0], i.parent_ver.ver_str) > 0:
        continue
    dependancy_dict[i.parent_pkg.name].append([i.parent_ver.ver_str, temp])

for i in dependancy_dict.keys():
    tmp = apt.Cache()[i]
    #print(f"fun package {i} depend {dependancy_dict[i]}")
    file = tmp.versions[0].fetch_binary(tmpdir)
    deb = apt.debfile.DebPackage(file)
    #print(f"filenames: {deb.filelist}")
    
    if any('metadata.json' in s for s in deb.filelist):
        filenames = ['metadata.json' in s for s in deb.filelist]
        print("="*80)
        print(f"package {i} depend {dependancy_dict[i]}")
        for j in range(0, len(filenames)):
            if filenames[j]:
                file_str = deb.data_content((deb.filelist[j]))
                shell_version = json.loads(file_str)["shell-version"]
                print(f"file: {deb.filelist[j]} supported shell version: {shell_version}")
        print("="*80)
        

shutil.rmtree(tmpdir)
