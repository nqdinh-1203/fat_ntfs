li = []


def hex_2_signed_int(hex_str, bits):
    value = int(hex_str, 16)
    if value & (1 << (bits - 1)):
        value -= 1 << bits
    return value


class VBR(object):
    """docstring for VBR"""

    def __init__(self, disk):
        with open(f'\\\\.\\{disk}:', "rb") as fr:
            data = fr.read(512)  # đọc ra VBR chính là 512 byte đầu tiên của ổ đĩa logic

        # Đọc các thuộc tính trên BPB
        self.bytesPerSec = int.from_bytes(data[11:13], 'little')
        self.secPerClus = int.from_bytes(data[13:14], 'little')
        self.NumSecOrTrack = int.from_bytes(data[24:26], 'little')
        self.NumSide = int.from_bytes(data[26:28], 'little')
        self.startSecDisk = int.from_bytes(data[28:32], 'little')
        self.totalSector = int.from_bytes(data[40:48], 'little')
        self.startClusterMFT = int.from_bytes(data[48:56], 'little')
        self.startClusterMFTMirror = int.from_bytes(data[56:64], 'little')
        self.sizeOfMFTEntry = pow(2, abs(hex_2_signed_int(data[64:65].hex(), 8)))  # Đơn vị Byte
        self.volSerialNum = data[72:80].hex()
        self.store_info = [self.bytesPerSec,self.secPerClus,self.NumSecOrTrack,self.NumSide,self.startSecDisk,
            self.totalSector,self.startClusterMFT,self.startClusterMFTMirror,self.sizeOfMFTEntry,self.volSerialNum]
        
    def get_info(self):
        return self.store_info


# $STANDARD_INFOMATION
class StandardInformation:
    def __init__(self, data):
        # Header của attribute: 0 -> 15
        self.header = data[0:16]
        # Size của cả attr: 4 -> 7
        self.size = int.from_bytes(data[4:8], 'little')
        # Size của attr content: 16 -> 19
        self.size_content = int.from_bytes(data[16:20], 'little')
        # offset bắt đầu của nội dung: 20 -> 21
        self.attr_offset = int.from_bytes(data[20:22], 'little')

        # Nội dung của attribute
        attribute_data = data[self.attr_offset:self.size + 1]
        # Thời gian tạo tập tin: byte 0 -> 7
        self.created_date = attribute_data[0:8]  # Cần chuyển byte -> date

        # Giá trị cờ báo: 32 -> 35
        self.flag = attribute_data[32:36]

    def print(self, tab=''):
        print(f'{tab}[-] Standard Information:')
        print(f'{tab}Size: {self.size}')
        print(f'{tab}Size Of Content: {self.size_content}')
        print(f'{tab}Attribute Offset Content: {self.attr_offset}')
        print(f'{tab}Flag: {self.flag}')


# $FILE_NAME
class FileName:
    def __init__(self, data):
        # Header của attribute: 0 -> 15
        self.header = data[0:16]
        # Size của cả attr: 4 -> 7
        self.size = int.from_bytes(data[4:8], 'little')
        # Size của attr content: 16 -> 19
        self.size_content = int.from_bytes(data[16:20], 'little')
        # offset bắt đầu của nội dung: 20 -> 21
        self.attr_offset = int.from_bytes(data[20:22], 'little')

        # Nội dung của attribute
        attribute_data = data[self.attr_offset:self.size + 1]
        # Địa chỉ entry thu mục cha: byte 0 -> 7
        self.file_reference = attribute_data[0:8]
        # Thời gian tạo tập tin: 8 -> 15
        self.created_date = attribute_data[8:16]

        # Chiều dài tên tập tin: 64
        # print(int.from_bytes(attribute_data[64], 'little'))
        self.name_length = attribute_data[64]
        # Tên tập tin: 66 + name_length

        self.name = attribute_data[66:66 + self.name_length * 2].decode('utf-16', 'replace').replace('\x00', '')

        # Định dạng tên tập tin: 65
        self.namespace = attribute_data[65]

    def print(self, tab=''):
        print(f'{tab}[-] File Name:')
        print(f'{tab}Size: {self.size}')
        print(f'{tab}Size Of Content: {self.size_content}')
        print(f'{tab}Attribute Offset Content: {self.attr_offset}')
        print(f'{tab}File Reference: {self.file_reference}')
        print(f'{tab}File name: {self.name}')
        print(f'{tab}File name length: {self.name_length}')
        print(f'{tab}Namespace: {self.namespace}')


# $Data
class Data:
    def __init__(self, data):
        # Header của attribute: 0 -> 15
        self.header = data[0:16]
        # Size của cả attr: 4 -> 7
        self.size = int.from_bytes(data[4:8], 'little')
        # Size của attr content: 16 -> 19
        self.size_content = int.from_bytes(data[16:20], 'little')
        # offset bắt đầu của nội dung: 20 -> 21
        self.attr_offset = int.from_bytes(data[20:22], 'little')

        self.content = data[self.attr_offset:self.attr_offset + self.size_content].decode('utf-8', 'replace').replace('\x00', '')

    def print(self, tab=''):
        print(f'{tab}[-] Data:')
        print(f'{tab}Size: {self.size}')
        print(f'{tab}Size Of Content: {self.size_content}')
        print(f'{tab}Attribute Offset Content: {self.attr_offset}')
        print(f'{tab}Content: {self.content}')


class MFTEntry:
    def __init__(self, entry_data):
        # Header của entry gồm 42 bytes đầu tiên
        self.header = entry_data[0:43]
        # Offset của attribute đầu tiên cũng là standard trong MFT entry là : 20 -> 21 trong header
        offset_standard_info = int.from_bytes(self.header[20:22], 'little')

        # Đọc attribute standard
        self.standard_info = StandardInformation(entry_data[offset_standard_info:])

        # Đọc attribute file_name
        offset_file_name = offset_standard_info + self.standard_info.size
        self.file_name = FileName(entry_data[offset_file_name:])

        # Đọc attribute Data
        offset_data = offset_file_name + self.file_name.size + 40
        self.data = Data(entry_data[offset_data:])

        # List cac tt/tm con
        self.sub_file = []

    # Lấy những entry con với entry cha là thư mục
    def get_sub(self, all_entry):
        for i in range(len(all_entry)):
            # Nếu tên entry con nằm trong data content của entry cha thì thêm vào list sub
            temp_entry = all_entry[i]
            if (temp_entry is not None) and (temp_entry.file_name.name in self.data.content) and (temp_entry.file_name.name != self.file_name.name):
                #temp_entry = all_entry[i]
                self.sub_file.append(temp_entry)
                all_entry[i] = None
                # Nếu entry con là thư mục thì tiếp tục xem con của entry con đó
                if temp_entry.standard_info.flag == b'\x00\x00\x00\x00':
                    temp_entry.get_sub(all_entry)

    def list(self, tab=''):
        file_list = [f'{tab}File Name = {self.file_name.name}\n']
        if self.standard_info.flag == b'\x00\x00\x00\x00':
            file_list.append(f'{tab}File Size = 0\n')
            file_list.append(f'{tab}File Attribute = Directory\n')
        else:
            file_list.append(f'{tab}File Size = {self.data.size_content}\n')
            file_list.append(f'{tab}File Attribute = File\n')
            #file_list.append(f'{tab}File Content = {self.data.content}\n')
            if (self.file_name.name[-3:] in ['txt','TXT']):
                file_list.append(f'{tab}File Content = {self.data.content}\n')
            else:
                file_list.append('Please use suitable program to read this file\n')
        li.append(file_list)

        if len(self.sub_file) > 0:
            for i in self.sub_file:
                tab2 = tab + '\t'
                i.list(tab2)


class MFT:
    def __init__(self, vbr, disk):
        self.MFT_entries_head = []
        self.MFT_entries_data = []

        # Vị trí Byte đầu tiên của MFT
        startByte = (vbr.startClusterMFT * vbr.secPerClus) * vbr.bytesPerSec

        with open(f'\\\\.\\{disk}:', "rb") as fr:
            # entry đang đọc
            index_entry = 0
            # Đọc các MFT entry head -> entry rỗng ở giữa entry head và các entry data
            while True:
                # Vị trí đọc MFT entry
                indexSeek = startByte + index_entry * vbr.sizeOfMFTEntry
                fr.seek(indexSeek)

                entryData = fr.read(vbr.sizeOfMFTEntry)

                # Nếu đọc 4 bytes đầu trong entry rỗng thì thoát while
                if entryData[0:4] == b'\x00\x00\x00\x00':
                    break
                else:
                    self.MFT_entries_head.append(entryData)

                index_entry += 1

            # Đọc các MFT entry rỗng -> entry data đầu tiên
            while True:
                indexSeek = startByte + index_entry * vbr.sizeOfMFTEntry
                fr.seek(indexSeek)

                entryData = fr.read(vbr.sizeOfMFTEntry)

                # Nếu đọc 4 bytes đầu trong entry khác rỗng thì thoát while
                if entryData[0:4] != b'\x00\x00\x00\x00':
                    break

                index_entry += 1

            # Đọc các MFT entry data đầu tiên -> entry rỗng sau entry này thì không còn gì ở sau nữa
            while True:
                indexSeek = startByte + index_entry * vbr.sizeOfMFTEntry
                fr.seek(indexSeek)

                entryData = fr.read(vbr.sizeOfMFTEntry)

                # Nếu đọc 4 bytes đầu trong entry rỗng thì thoát while
                if entryData[0:4] == b'\x00\x00\x00\x00':
                    break
                else:
                    entry_content = MFTEntry(entryData)
                    # Nếu là file rác thì không thêm vào
                    if (entry_content.data.size > entry_content.data.size_content) and (entry_content.data.size < 1024):
                        self.MFT_entries_data.append(entry_content)

                index_entry += 1

        # Lấy các tt/tm con của các Entry đồng thời remove tt/tm con đó ra khỏi list entry data
        for entry in self.MFT_entries_data:
            if entry is not None and entry.standard_info.flag == b'\x00\x00\x00\x00':
                entry.get_sub(self.MFT_entries_data)

    def get_list(self):
        for i in self.MFT_entries_data:
            if i is not None:
                i.list()


def get_store_all_directory(vbr, disk):
    vbr = VBR(disk)
    mft = MFT(vbr, disk)
    mft.get_list()

    return li
