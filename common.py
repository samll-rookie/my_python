import gzip
import zipfile
import re
import pandas as pd

class Seq:
    """ deal with DNA method str"""

    def __init__(self, seq, dict_codon={}):
        self.seq = seq
        self.dict_codon = dict_codon

    def reverse(self):
        """
        input type : str
        get reverse seq str
        """
        return self.seq[::-1]

    def complement(self):
        """
        input type : str
        get complement seq str
        """
        d = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}
        return "".join([d[i] if i in d.keys() else "*" for i in self.seq.upper()])

    def revcom(self):
        """
        input type : str
        get reverse and complement seq
        """
        return self.complement()[::-1]

    def atgc(self):
        """
        input type: str
        stat seq letters count
        """
        A = self.seq.upper().count("A")
        T = self.seq.upper().count("T")
        G = self.seq.upper().count("G")
        C = self.seq.upper().count("C")
        length = len(self.seq)
        return A, T, G, C, length

    def repeat(self):
        """
        input type: str
        return 4 column: match seq, motif, match seq start, match seq end;  0-base;  [A-Z]{1,}  match motif;
        """
        a = re.finditer(r'(([A-Z]{1,})\2{1,})', self.seq)
        s = [[i.groups()[0], i.groups()[1], i.start(), i.end()] for i in a]
        return s

    def translaton(self):
        """
        input type: dict , str
        convert single or multiple str1 to str2 according to dict; no key in dict to *
        """
        seq = self.seq.upper().replace("T", "U")
        d = self.dict_codon
        result = "".join( [d[seq[i:i+3]] if seq[i:i+3] in d.keys() else "*" for i in range(0, len(seq), 3)] )
        return result


class Read_file:
    """ read general file """

    def __init__(self, file="", fq1="", fq2=""):
        self.file = file
        self.fq1 = fq1
        self.fq2 = fq2

    def gunzip(self):
        """ deal with gz and zip file """
        if self.file.endswith(".gz"):
            f = gzip.open(self.file,'rt')
        elif self.file.endswith(".zip"):
            f = zipfile.ZipFile(self.file)
        else:
            f = open(self.file,'r')
        return f

    def read_fasta(self):
        """
        read single  fasta file,return list generator
        """
        fa_id = ""
        fa_seq = ""
        for line in self.gunzip():
            if line.startswith('>'):
                if fa_id != "": yield [fa_id, fa_seq]
                fa_id = ""
                fa_seq = ""
                fa_id = line.split()[0][1:]
            else:
                fa_seq += line.upper().strip()
        yield [fa_id, fa_seq]


    def read_fastq(self):
        """
        read single fastq file,return list generator
        """
        f = self.gunzip()
        while True:
            l1 = f.readline().strip()
            if not l1: break
            l2 = f.readline().strip()
            l3 = f.readline().strip()
            l4 = f.readline().strip()
            yield [l1, l2, l3, l4]

    def read_pairs(self):
        """
        read fq1 and fq2 two file
        """
        f1 = self.read_fastq()
        f2 = self.read_fastq()
        while True:
            try:
                read1 = next(f1)
                read2 = next(f2)
                read1.extend(read2)
                yield read1
            except StopIteration:
                break

class Stat():

    def __init__(self):
        pass

    def entropy(self, fasta):
        '''
        input type: file； input multiple align fasta ;
        result: # Acount, Tcount, Gcount, Ccount, 最大频数的碱基，最大频数，总碱基数目，最大频数/总碱基数目, 最大频数/位点总的序列长度
        s= Stat().entropy("12.output.fa")
        s.to_csv("./12.output.fa.csv", sep="\t", index=0)
        '''
        f = Seq().read_fasta(fasta)
        a1 = [list(i[1]) for i in f]
        final = []
        for m in zip(*a1):
            name = ["A", "T", "G", "C"]
            Count = [m.count("A"), m.count("T"), m.count("G"), m.count("C")]
            s1 = list(zip(name, Count))
            site_letter, site_count = sorted(s1, key=lambda x: x[1], reverse=True)[0]
            # Acount, Tcount, Gcount, Ccount, 最大频数的碱基，最大频数，总碱基数目，最大频数/总碱基数目, 最大频数/位点总的序列长度
            result = Count[:] + [site_letter, site_count, sum(Count), round(site_count/sum(Count), 2), round(site_count/len(m),2)]
            final.append(result)
        s = pd.DataFrame(final, columns=['A', 'T', 'G', 'C', "max_letter", "max_count", "total_count", "ratio", "length"])
        return s

    def bed_shift(self, gene_bed):
        '''
        相邻行下一行的开始位置与上一行结束位置的区间长度统计
        input type: bed file(at leaet 3 col) etc: id start end(col1 can multiplex diff id)
        out:
                0     1   2   diff
            0  g1   3   7  NAN
            1  g1  12  37    5
            0  g2   2  14  NAN
            1  g2  17  27    3
        '''
        chr = {}
        bed = {}
        with open(gene_bed) as f:
            for line in f:
                elements = line.strip().split()
                k = elements[0]
                if (k in chr) and (k in bed):
                    chr[k].extend(elements[1:3])
                    bed[k].append(elements)
                else:
                    chr[k] = elements[1:3]
                    bed[k] = []
                    bed[k].append(elements)
        out = []
        for m in chr.keys():
            # print(m, chr[m], bed[m])
            c = [int(chr[m][i + 1]) - int(chr[m][i]) for i in range(1, len(chr[m]) - 1, 2)]
            c.insert(0, "NAN")
            result = pd.DataFrame(bed[m])
            result['diff'] = c
            out.append(result)
        return(pd.concat(out))
