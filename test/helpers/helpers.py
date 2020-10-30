import re

from thoipapy.predict import get_md5_checksum


class TestProtein:
    def __init__(self):
        self.tmd_seq = None
        self.full_seq = None
        self.protein_name = None
        self.acc = None
        self.md5 = None
        self.tmd_start = None
        self.tmd_end = None

    def with_ERBB3(self):
        self.tmd_seq = "MALTVIAGLVVIFMMLGGTFL"
        self.full_seq = "MVQNECRPCHENCTQGCKGPELQDCLGQTLVLIGKTHLTMALTVIAGLVVIFMMLGGTFLYWRGRRIQNKRAMRRYLERGESIEPLDPSEKANKVLA"
        self.protein_name = "P21860_ERBB3"
        self.acc = "P21860"
        self.md5 = get_md5_checksum(self.tmd_seq, self.full_seq)
        m = re.search(self.tmd_seq, self.full_seq)
        self.tmd_start = m.start()
        self.tmd_end = m.end()

    def with_ATP1B1(self):
        self.tmd_seq = "LLFYVIFYGCLAGIFIGTIQVMLLTI"
        self.full_seq = "MARGKAKEEGSWKKFIWNSEKKEFLGRTGGSWFKILLFYVIFYGCLAGIFIGTIQVMLLTISEFKPTYQDRVAPPGLTQIPQIQKTEISFRPNDPKSYEEYVRNIVRFLEKY"
        self.protein_name = "P05026_ATP1B1"
        self.acc = "P05026"
        self.md5 = get_md5_checksum(self.tmd_seq, self.full_seq)
        m = re.search(self.tmd_seq, self.full_seq)
        self.tmd_start = m.start()
        self.tmd_end = m.end()

    def with_BNIP3(self):
        self.tmd_seq = "VFLPSLLLSHLLAIGLGIYIG"
        self.full_seq = "RSSSKSSHCDSPPRSQTPQDTNRASETDTHSIGEKNSSQSEEDDIERRKEVESILKKNSDWIWDWSSRPENIPPKEFLFKHPKRTATLSMRNTSVMKKGGIFSAEFLKVFLPSLLLSHLLAIGLGIYIGRRLTTSTSTF"
        self.protein_name = "Q12983_BNIP3"
        self.acc = "Q12983"
        self.md5 = get_md5_checksum(self.tmd_seq, self.full_seq)
        m = re.search(self.tmd_seq, self.full_seq)
        self.tmd_start = m.start()
        self.tmd_end = m.end()

    def with_4ryiA2(self):
        self.tmd_seq = "PGMTIGMIWAVLFGLIALSVA"
        self.full_seq = "KKSSIIVFFLTYGLFYVSSVLFPIDRTWYDALEKPSWTPPGMTIGMIWAVLFGLIALSVAIIYNNYGFKPKTFWFLFLLNYIFNQAFSYFQFSQKNLFLATVDCLLVAITTLLLIMFSSNLSKVSAWLLIPYFLWSAFATYLSWTIYSIN"
        self.protein_name = "4ryiA2_TspO"
        self.acc = "4ryiA2"
        self.md5 = get_md5_checksum(self.tmd_seq, self.full_seq)
        m = re.search(self.tmd_seq, self.full_seq)
        self.tmd_start = m.start()
        self.tmd_end = m.end()
