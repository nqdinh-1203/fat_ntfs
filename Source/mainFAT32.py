from tkinter.constants import BOTH


def little_endian_to_integer(data, offset, size):
    power = 0
    sum = 0
    for i in range(size):
        x = data[i+offset]
        for j in range(8):
            if x & 1:
                sum = sum + int(pow(2, power))
            x = x >> 1
            power = power + 1
    return sum

class BootSector:
    """docstring for BootSector"""
    def __init__(self, disk):
        with open(f'\\\\.\\{disk}:', "rb") as fr:
            data = fr.read(512)

        self.bytesPerSec = little_endian_to_integer(data, 11, 2)        #So byte cho 1 sector
        self.secPerClus = little_endian_to_integer(data, 13, 1)         #So sector cho 1 cluster
        self.reservedSector = little_endian_to_integer(data, 14, 2)     #So sector de danh (reserved sector)
        self.numFATs = little_endian_to_integer(data, 16, 1)            #So bang FAT
        self.entryOfRoot = little_endian_to_integer(data, 17, 2)        #So entry bang RDET
        self.startSector = little_endian_to_integer(data, 28, 4)        #Vi tri bat dau cua Boot Sector
        self.totalSector = little_endian_to_integer(data, 32, 4)        #So sector trong volume
        self.fatSizeInSec = little_endian_to_integer(data, 36, 4)       #So sector trong 1 bang FAT
        self.rootClus = little_endian_to_integer(data, 44, 4)           #Chi so cluster dau tien cua RDET
        self.store_info = [self.bytesPerSec, self.secPerClus, self.reservedSector, self.numFATs, 
                            self.entryOfRoot, self.totalSector, self.fatSizeInSec,self.rootClus]

    def get_info(self):
        return self.store_info

class FAT32:
    entries_list = []

    def __init__(self, disk):
        bootSector = BootSector(disk)
        startByte = bootSector.reservedSector * bootSector.bytesPerSec 
        fatSizeInBytes = bootSector.fatSizeInSec * bootSector.bytesPerSec
        numberOfFATEntries = int(fatSizeInBytes / 4)
        
        with open(f'\\\\.\\{disk}:', "rb") as fr:
            fr.seek(startByte, 0)
            data = fr.read(fatSizeInBytes)
        
        count = 0
        for i in range(0, numberOfFATEntries):
            if little_endian_to_integer(data, 4 * i, 4) == 0:
                count +=1 
                if count >= 200:  
                    break
            self.entries_list.append(little_endian_to_integer(data, 4 * i, 4))

    def print(self):
        
        for i in range(len(self.entries_list)):
            if(self.entries_list[i] == 0):
                continue
            print(f'FAT Entry[{i}] = {self.entries_list[i]}')

def offset_data(data, offset):
    value = little_endian_to_integer(data, offset, 1)
    return hex(value)

def first_sector_of_cluster(clus, bootSector):
    # Tinh sector dau tien cua vung Data
    firstDataSector = bootSector.reservedSector + bootSector.numFATs * bootSector.fatSizeInSec 
    # Tinh sector dau tien cua cluster (clus)
    # Vì so hieu cluster bat dau tu gia tri 2 nên 2 entry đau cua bang FAT không duoc su dung
    return ((clus - 2) * bootSector.secPerClus) + firstDataSector

def get_sector_index(fat32, startCluster,disk):
    bootSector = BootSector(disk)
    sectorIdList = []
    start = bootSector.startSector
    sector = first_sector_of_cluster(startCluster,bootSector)
    for i in range(8):
        sectorIdList.append(sector+i+start)
                
    if fat32.entries_list[startCluster] !=0xFFFFFFF and startCluster >= 2:
        sector = first_sector_of_cluster(fat32.entries_list[startCluster],bootSector)
        for i in range(8):
            sectorIdList.append(sector+i+start)
    return sectorIdList

def read_content(fat32,clusterNum, disk):
    bootSector = BootSector(disk)
    content_sector = first_sector_of_cluster(clusterNum, bootSector)
    clusterSizeInBytes = bootSector.secPerClus * bootSector.bytesPerSec
    
    with open(f'\\\\.\\{disk}:', "rb") as fr:
        fr.seek(content_sector * bootSector.bytesPerSec, 0)
        data = fr.read(clusterSizeInBytes)

    content = ''
    j = 0
    while chr(data[j]) != '\x00':
        content += chr(data[j])
        j += 1
        if j == 4095:
            break
    if fat32.entries_list[clusterNum] !=0xFFFFFFF and clusterNum >= 2:
        content += read_content(fat32.entries_list[clusterNum], disk)
    return content

direct = '(Directory)'
file = '(File)'

class Directory:
    def __init__(self, disk):
        self.name = ''
        self.attribute = 0
        self.startCluster = 0
        self.fileSize = 0
        self.sector = []
        self.disk = disk

store_all_directory = []        
def read_directory(clusterNum, entryStartingPoint, fat,disk,tab=''):
    temp=Directory(disk)
    fat32 = FAT32(disk)
    bootSector = BootSector(disk)
    #Luu ten doc duoc trong entry phu
    stackTemp = []; stackLongName = []
    
    first_sector = first_sector_of_cluster(clusterNum, bootSector)
    clusterSizeInBytes = bootSector.secPerClus * bootSector.bytesPerSec

    # Cac entry cua Root Directory deu la 32 bytes
    totalEntries = int((bootSector.secPerClus * bootSector.bytesPerSec) / 32)


    with open(f'\\\\.\\{temp.disk}:', "rb") as fr:
        fr.seek(first_sector * bootSector.bytesPerSec, 0)
        data = fr.read(clusterSizeInBytes)

    for i in range(entryStartingPoint, totalEntries):
        # End of Entry
        if offset_data(data, 32 * i) == 0x0:
            break
        # Unused Entry caused By Deletion
        if offset_data(data, 32 * i) == 0xE5:
            continue

        attr = little_endian_to_integer(data, (32*i)+ 11, 1)
        x = None

        # Doc ten o Entry phu
        if attr == 0xF:
            # Moi lan doc 2 byte de co 1 ky tu
             # 1 --> 10
            for j in range(1, 10, 2):
                x = little_endian_to_integer(data, j + 32 * i, 2)
                if x == 0xffff:
                    break
                stackTemp.append(x)

            # 14 --> 25
            for j in range(14, 25, 2):
                x = little_endian_to_integer(data, j + 32 * i, 2)
                if x == 0xffff:
                    break
                stackTemp.append(x)

            # 28 --> 31
            for j in range(28, 31, 2):
                x = little_endian_to_integer(data, j + 32 * i, 2)
                if x == 0xffff:
                    break
                stackTemp.append(x)
            
            #Ten o entry phu duoc luu theo thu tu nguoc 
            while len(stackTemp) != 0:
                stackLongName.append(stackTemp.pop())
            continue
            
        if attr not in [0x10,0x20,0xF]:
            stackLongName=[]  # -> De loai bo cac entry phu cua cac file khong phai la tap tin hoac thu muc

        # Entry chinh cua tap tin/ thu muc
        if attr == 0x10 or attr == 0x20:
    
            temp.name=''   # -> De reset ten cua file
            for j in range(0,11):
                temp.name += chr(data[32 * i + j])
                
            if len(stackLongName) != 0:
                temp.name = ''
                for j in range(len(stackLongName)-1, 0, -1):
                    temp.name += chr(stackLongName.pop(j))
            stackLongName = []   # ->De xoa ten cua entry phu cua file nay de khong gan len file sau 
                                # -> Khong anh huong ten cua cac file khong co entry phu            
            temp.name = temp.name.strip()

            temp.fileSize = little_endian_to_integer(data,(32 * i)+ 28, 4)
            temp.startCluster = (little_endian_to_integer(data, (32 * i)+ 20, 2) * pow(2,16)) + little_endian_to_integer(data,(32 * i)+ 26, 2)
            temp.attribute = attr
            
            temp.sector = []
            temp.sector = get_sector_index(fat32,temp.startCluster,disk)
            
            store = []
            
            if attr == 0x20 :
                if temp.name.count('.') == 0 :
                    spl = temp.name.split(' ')
                    if len(spl) >=3: 
                        for i in range(len(spl)-1,0,-1):
                            if spl[i] == '' and spl[i-1] == '':
                                del spl[i]
                        spl[-2] = '.'
                        temp.name = ' '.join(spl).replace(' . ','.')
                    else:
                        temp.name = temp.name.replace(' ','.')
                
                store.append(f'{tab}File Name = {temp.name}\n') 
                store.append(f'{tab}File Size = {temp.fileSize}\n')
                store.append(f'{tab}Sector index: {temp.sector}\n')
                store.append(f'{tab}File Attribute = {temp.attribute} {direct if temp.attribute == 0x10 else file}\n')
                if temp.name[-3:] in ['txt','TXT']:
                    content = read_content(fat32,temp.startCluster,temp.disk)
                    if len(content) > 0:
                        content = content.replace('\n','\n'+tab)
                        store.append(f'{tab}Content of file txt: \n{tab}{content}\n')
                else:
                    content = 'Please use suitable program to read this file'
                    store.append(f'{tab}{content}\n')


            else:
                store.insert(0,f'{tab}File Name = {temp.name}\n')
                store.insert(1,f'{tab}File Size = {temp.fileSize}\n')
                store.insert(2,f'{tab}Sector index: {temp.sector}\n')
                store.insert(3,f'{tab}File Attribute = {temp.attribute} {direct if temp.attribute == 0x10 else file}\n')
                
                
            store_all_directory.append(store)

            if attr == 0x10: #Doc cay thu muc trong thu muc
                tab2 = tab
                tab2 += '\t'
                read_directory(temp.startCluster, 2, fat,temp.disk,tab2)
            
def get_store_all_directory(clusterNum, entryStartingPoint, fat,disk,tab):
    fat32 = FAT32(disk)
    directory = Directory(disk)
    directory = read_directory(2, 0, fat32, disk,'')

    return store_all_directory

#fat32 = FAT32('H')
# print('---------------')
#print(get_store_all_directory(2, 0, fat32, 'H', ''))
# directory = Directory('F')
# directory = read_directory(2, 0, fat32, '', 'F')