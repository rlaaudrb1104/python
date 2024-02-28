import struct
import datetime
import pefile

def index(data_list):
  data_list.append(["member","data","description"])
  data_list.append(["―"*20,"―"*20,"―"*60])

def print_info (data_list):
  for data in data_list:
    num = len(data)
    if num == 3:
      print(data[0].ljust(20), str(data[1]).ljust(20), data[2].ljust(20))
    elif num == 5:
      print(data[0].ljust(20), str(data[1]).ljust(20), data[2].ljust(20), data[3].ljust(20), data[4].ljust(20))
    else:
      pass

def DOS_HEADER_INFO(pe):
  dos_header_list = []
  index(dos_header_list)
  dos_header_list.append(["e_magic", struct.pack('<H', pe.DOS_HEADER.e_magic).decode('utf8'), "DOS Signature"])
  dos_header_list.append(["e_lfanew",hex(pe.DOS_HEADER.e_lfanew), "NT header offset"])

  print_info(dos_header_list)

def NT_HEADERS_INFO(pe):
  nt_header_list = []
  index(nt_header_list)
  nt_header_list.append(["Signature", struct.pack('<I', pe.NT_HEADERS.Signature).decode('utf8').rstrip('\x00'), " NF Signature"])
  
  print_info(nt_header_list)


def FILE_HEADER_INFO (pe) :
    file_header_list = []
    index(file_header_list)
    
    timeStr = '1970-01-01 00:00:00'
    Thistime = datetime.datetime.strptime(timeStr, '%Y-%m-%d %H:%M:%S') 
    LastBuildtime = Thistime + datetime.timedelta(seconds=pe.FILE_HEADER.TimeDateStamp)

    file_header_list.append(["Machine", hex(pe.FILE_HEADER.Machine), "파일의 실행 대상 플랫폼 I386(0x014c), IA64(0x200), AMD64(0x8664)"])
    file_header_list.append(["NumberOfSections", pe.FILE_HEADER.NumberOfSections, "파일에 존재하는 section의 개수"])
    file_header_list.append(["SizeOfOptionalHeader", hex(pe.FILE_HEADER.SizeOfOptionalHeader), "OptionalHeader의 크기"])
    file_header_list.append(["Characteristics", hex(pe.FILE_HEADER.Characteristics), "이 파일의 속성을 나타내는 값 exe(0x0002), dll(0x2000)"])
    file_header_list.append(["TimeDateStamp", str(LastBuildtime), "해당 파일의 빌드 시간"])

    print_info (file_header_list)
    

def OPTIONAL_HEADER_INFO(pe):

  optional_header_list = []
  index(optional_header_list)
  optional_header_list.append(["Magic", hex(pe.OPTIONAL_HEADER.Magic), "Optional header를 구분하는 Signature 32bit(0x10b), 64bit(0x20b)"])
  optional_header_list.append(["AddressOfEntryPoint", hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint), "파일이 메모리에 매핑된 후 코드 시작 주소"])
  optional_header_list.append(["ImageBase",  hex(pe.OPTIONAL_HEADER.ImageBase), "PE파일이 매핑되는 시작주소 exe(0x400000), dll(0x1000000)"])
  optional_header_list.append(["SizeOfCode", hex(pe.OPTIONAL_HEADER.SizeOfCode), "IMAGE_SCN_CNT_CODE 속성을 갖는 섹션들의 총 사이즈 크기"])
  optional_header_list.append(["SectionAlignment", pe.OPTIONAL_HEADER.SectionAlignment, "메모리 상에서의 최소 섹션 단위"])
  optional_header_list.append(["FileAlignment", pe.OPTIONAL_HEADER.FileAlignment, "파일 상에서의 최소 섹션 단위"])
    
  print_info (optional_header_list)

def SECTION_HEAERS_INFO (pe) :
  
  section_header_list = []
  section_header_list.append(["Name", "Virual Address", "SizeOfRawData", "PointerToRawData", "Characteristics"])
  section_header_list.append(["―"*20,"―"*20,"―"*20,"―"*20,"―"*20])
  for section in pe.sections :
    section_header_list.append([section.Name.decode('utf8').rstrip('\x00'),hex(section.VirtualAddress),hex(section.SizeOfRawData),hex(section.PointerToRawData),hex(section.Characteristics)])

  print_info(section_header_list)
  print("―"*20,"―"*20)
  print("Name".ljust(20), "Section 이름")
  print("―"*20,"―"*20)
  print("VirtualAddress".ljust(20), "섹션의 RAV(ImageBase + VA)를 위한 VA 값")
  print("SizeOfRawData".ljust(20), "파일 상에서 섹션이 차지하는 크기")
  print("PointerToRawData".ljust(20), "파일 상에서 섹션이 시작하는 위치")
  print("Characteristics".ljust(20), "섹션의 특징")
  print("-> (0x20000000 = excutable, 0x40000000 = readable, 0x80000000 = writeable, 0x00000020 = contains code, 0x00000040 = contains initialized data)")
  print("")


path = input("파일 경로 입력 \n")
pe = pefile.PE(path)

print("1. [IMAGE_DOS_HEADER]")
print("2. [IMAGE_NT_HEADERS]")
print("3. └[IMAGE_FILE_HEADER]")
print("4. └[IMAGE_OPTIONAL_HEADER]")
print("5. [IMAGE_SECTION_HEADERS]")
for section in pe.sections:
    print("   └IMAGE_SECTION_HEADER " + section.Name.decode().rstrip('\x00'))

print("   [SECTIONS]")
for section in pe.sections:
    section_name = section.Name.decode().rstrip('\x00')
    print("   └SECTION " + section_name)
print("6. 종료")
num = input("분석 대상 선택:")

if num == '1' : 
  DOS_HEADER_INFO(pe)
elif num == '2' :
  NT_HEADERS_INFO(pe)
elif num == '3' :
  FILE_HEADER_INFO(pe)
elif num == '4' :
  OPTIONAL_HEADER_INFO(pe)
elif num == '5' :
  SECTION_HEAERS_INFO(pe)
elif num == '6' :
  exit
else:
  print("잘못된 입력입니다.")