__program__ = 'Charge Mover Velocity Correction'
__author__ = 'Pablo Scrosati'
__version__ = '1.0'
__date__ = 'March 31, 2021'
__usage__ = 'python atomMatcher.py new_file old_file output_file'

__description__ = \
'''
new_file is the GRO file containing the charge-moved atoms.
old_file is the GRO file to extract velocities from (MUST CONTAIN VELOCITIES).
out_file is the GRO file to write the corrected configuration to.

This program scans through input coordinate files (in GRO format) to match atoms based on residue ID
and atom name. The logic relies that the relative positions of atoms only change by a maximum of
one atom position (as is the case if assuming only one proton will move per comparison). Following
matching, velocities from the old_file will be assigned to the atoms in new_file, compiled in a
final output file, out_file.
'''

import sys

def fileRead(file):
    with open(file) as f:
        lines = [line.rstrip() for line in f]
    return lines

def commandRead(argv=None):
    if argv == None:
        argv = sys.argv[1:]

    try:
        new_file = argv[0]
        old_file = argv[1]
        outfile = argv[2]
    except:
        print('Incorrect usage!\nUsage: ' + __usage__)
        sys.exit(1)

    new_list = fileRead(new_file)
    old_list = fileRead(old_file)
    return new_list, old_list, outfile

def matcher(original, new_file, outlist = [], flag=None, prot_index=None):
    header = [new_file[0], new_file[1]]
    lastline = new_file[-1]
    del original[0], original[0], new_file[0], new_file[0], original[-1], new_file[-1]
    for i in range(len(original)):
        if original[i][5:15].strip() == new_file[i][5:15].strip():
            outlist.append(new_file[i].rstrip() + ' ' + original[i][45:])

        elif i + 1 <= len(original) and original[i][5:15].strip() == new_file[i + 1][5:15].strip():
            if prot_index == None:
                prot_index = i
                outlist.append(new_file[i] + ' ')
            else:
                outlist.append(new_file[i].rstrip() + ' ' + original[i - 1][45:])

        elif i + 1 <= len(original) and original[i + 1][5:15].strip() == new_file[i][5:15].strip():
            if prot_index == None:
                prot_index = i
                flag = 1
            outlist.append(new_file[i].rstrip() + ' ' + original[i + 1][45:])

        else:
            if flag == 1:
                outlist.append(new_file[i] + ' ' + original[prot_index][45:])
            else:
                outlist[prot_index] = outlist[prot_index] + original[i][45:]
                outlist.append(new_file[i].rstrip() + ' ' + original[i - 1][45:])
    outlist.append(lastline)
    outlist.insert(0, header[1])
    outlist.insert(0, header[0])
    return outlist

def writer(list, outfile):
    with open(outfile, 'w') as f:
        for item in list:
            f.write('%s\n' % item)

if __name__ == '__main__':
    print(__program__ + ' v' + __version__ + '\n' + 'Author: ' + __author__ + '\n')
    files = commandRead()
    list = matcher(files[1], files[0])
    writer(list, files[2])
    print('Process completed successfully!')