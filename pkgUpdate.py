import re
import os
import xml.etree.ElementTree as et

et.register_namespace("","http://br-automation.co.at/AS/Package")

# Base path and working directory
base_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(base_path)
print(os.getcwd())
# Open file and transfer data to python memory
with open(os.path.join(base_path, '.gitmodules')) as f:
        data = f.read()

# Get path and url
paths = re.findall(r'path = (.*)\n', data)
urls = re.findall(r'url = (.*)\n', data)

# Extract url and path
extract = []
for i in range(len(paths)):
        path_url = {}
        path_url['path'] = paths[i]
        path_url['url'] = urls[i]
        extract.append(path_url)

# MAIN
for row in extract:
        print('-------------------------------------')
        submodule_path, submodule = os.path.split(row['path'])
        print('Folder:', submodule_path, '| Submodule: ', submodule)
        submodule_url = row['url']
        pkg_file = os.path.join(base_path, submodule_path, 'Package.pkg')

        tree = et.parse(pkg_file)

        root = tree.getroot()

        et.register_namespace("", root.get('xmlns'))

        packagePresent = False

        for element in root[0].findall('Object'):
                if submodule == element.text:
                        print(submodule, "- Already added to package")
                        packagePresent = True
                        break

        if packagePresent == False:
                print(submodule, '- Submodule added to package')

                new_tag = et.SubElement(root[0], 'Object')
                new_tag.text = submodule
                new_tag.attrib['Type'] = 'Package'
                new_tag.attrib['Description'] = row['url']
                tree.write(os.path.join(submodule_path, 'Package.pkg'))

print('-------------------------------------')



# # MAIN
# for row in extract:
#         print('-------------------------------------')
#         submodule_path, submodule = os.path.split(row['path'])
#         print('Folder:', submodule_path, '| Submodule: ', submodule)
#         submodule_url = row['url']
#         pkg_file = os.path.join(base_path, submodule_path, 'Package.pkg')

#         tree = et.parse(pkg_file)

#         root = tree.getroot()

#         for element in root:
#                 if submodule in element.text:
#                         print(submodule, "- Already added to package")
#                         break
#                 else:
#                         print(submodule, '- is not in the package')

#                         new_tag = et.SubElement(element, 'Object')
#                         new_tag.text = submodule
#                         new_tag.attrib['Type'] = 'Package'
#                         new_tag.attrib['Description'] = row['url']
#                         tree.write(os.path.join(submodule_path, 'Package.pkg'))

# print('-------------------------------------')