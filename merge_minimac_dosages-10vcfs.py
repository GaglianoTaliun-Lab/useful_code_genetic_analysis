import argparse
import pysam
import numpy as np
import gzip

argparser = argparse.ArgumentParser(description = 'Merges minimac4 imputation results and recomputes Rsq imputation quality score.')
argparser.add_argument('-i1', '--in-vcf1', metavar = 'file', dest = 'in_VCF1', required = True, help = 'First imputed VCF file.')
argparser.add_argument('-i2', '--in-vcf2', metavar = 'file', dest = 'in_VCF2', required = True, help = 'Second imputed VCF file.')
argparser.add_argument('-i3', '--in-vcf3', metavar = 'file', dest = 'in_VCF3', required = True, help = 'Third imputed VCF file.')
argparser.add_argument('-i4', '--in-vcf4', metavar = 'file', dest = 'in_VCF4', required = True, help = 'Fourth imputed VCF file.')
argparser.add_argument('-i5', '--in-vcf5', metavar = 'file', dest = 'in_VCF5', required = True, help = 'Fifth imputed VCF file.')
argparser.add_argument('-i6', '--in-vcf6', metavar = 'file', dest = 'in_VCF6', required = True, help = 'Sixth imputed VCF file.')
argparser.add_argument('-i7', '--in-vcf7', metavar = 'file', dest = 'in_VCF7', required = True, help = 'Seventh imputed VCF file.')
argparser.add_argument('-i8', '--in-vcf8', metavar = 'file', dest = 'in_VCF8', required = True, help = 'Eighth imputed VCF file.')
argparser.add_argument('-i9', '--in-vcf9', metavar = 'file', dest = 'in_VCF9', required = True, help = 'Ninth imputed VCF file.')
argparser.add_argument('-i10', '--in-vcf10', metavar = 'file', dest = 'in_VCF10', required = True, help = 'Tenth imputed VCF file.')
argparser.add_argument('-c', '--chromosomes', metavar = 'name', dest = 'chrom', required = True, type = str, help = 'Chromosome name.')
argparser.add_argument('-b', '--begin', metavar = 'position', dest = 'begin', required = True, type = int, help = 'Begin position.')
argparser.add_argument('-e', '--end', metavar = 'position', dest = 'end', required = True, type = int , help = 'End position.')
argparser.add_argument('-m', '--min-rsq', metavar = 'float', dest = 'min_rsq', required = True, type = float, help = 'Minimal combined R2 to write to final VCF.')
argparser.add_argument('-o', '--out', metavar = 'file', dest = 'out_VCF', required = True, help = 'Output merged VCF file.')


if __name__ == '__main__':
   args = argparser.parse_args()

   with pysam.VariantFile(args.in_VCF1, 'r') as vcf1, pysam.VariantFile(args.in_VCF2, 'r') as vcf2, gzip.open(args.out_VCF, "wt") as vcf_merged:
      if not 'R2' in vcf1.header.info:
         raise Exception(f'No meta-information entry about R2 INFO field found in {args.in_VCF1}!')
      if not 'R2' in vcf2.header.info:
         raise Exception(f'No meta-information entry about R2 INFO field found in {args.in_VCF2}!')
      if not 'R2' in vcf3.header.info:
         raise Exception(f'No meta-information entry about R2 INFO field found in {args.in_VCF3}!')
      if not 'R2' in vcf4.header.info:
         raise Exception(f'No meta-information entry about R2 INFO field found in {args.in_VCF4}!')
      if not 'R2' in vcf5.header.info:
         raise Exception(f'No meta-information entry about R2 INFO field found in {args.in_VCF5}!')
      if not 'R2' in vcf6.header.info:
         raise Exception(f'No meta-information entry about R2 INFO field found in {args.in_VCF6}!')
      if not 'R2' in vcf7.header.info:
         raise Exception(f'No meta-information entry about R2 INFO field found in {args.in_VCF7}!')
      if not 'R2' in vcf8.header.info:
         raise Exception(f'No meta-information entry about R2 INFO field found in {args.in_VCF8}!')
      if not 'R2' in vcf9.header.info:
         raise Exception(f'No meta-information entry about R2 INFO field found in {args.in_VCF9}!')
      if not 'R2' in vcf10.header.info:
         raise Exception(f'No meta-information entry about R2 INFO field found in {args.in_VCF10}!')
      if not 'TYPED_ONLY' in vcf1.header.info:
         raise Exception(f'No meta-information entry about TYPED_ONLY INFO field found in {args.in_VCF1}!')
      if not 'TYPED_ONLY' in vcf2.header.info:
         raise Exception(f'No meta-information entry about TYPED_ONLY INFO field found in {args.in_VCF2}!')
      if not 'TYPED_ONLY' in vcf3.header.info:
         raise Exception(f'No meta-information entry about TYPED_ONLY INFO field found in {args.in_VCF3}!')
      if not 'TYPED_ONLY' in vcf4.header.info:
         raise Exception(f'No meta-information entry about TYPED_ONLY INFO field found in {args.in_VCF4}!')
      if not 'TYPED_ONLY' in vcf5.header.info:
         raise Exception(f'No meta-information entry about TYPED_ONLY INFO field found in {args.in_VCF5}!')
      if not 'TYPED_ONLY' in vcf6.header.info:
         raise Exception(f'No meta-information entry about TYPED_ONLY INFO field found in {args.in_VCF6}!')
      if not 'TYPED_ONLY' in vcf7.header.info:
         raise Exception(f'No meta-information entry about TYPED_ONLY INFO field found in {args.in_VCF7}!')
      if not 'TYPED_ONLY' in vcf8.header.info:
         raise Exception(f'No meta-information entry about TYPED_ONLY INFO field found in {args.in_VCF8}!')
      if not 'TYPED_ONLY' in vcf9.header.info:
         raise Exception(f'No meta-information entry about TYPED_ONLY INFO field found in {args.in_VCF9}!')
      if not 'TYPED_ONLY' in vcf10.header.info:
         raise Exception(f'No meta-information entry about TYPED_ONLY INFO field found in {args.in_VCF10}!')

      samples1 = list(vcf1.header.samples)
      samples2 = list(vcf2.header.samples)
      samples3 = list(vcf3.header.samples)
      samples4 = list(vcf4.header.samples)
      samples5 = list(vcf5.header.samples)
      samples6 = list(vcf6.header.samples)
      samples7 = list(vcf7.header.samples)
      samples8 = list(vcf8.header.samples)
      samples9 = list(vcf9.header.samples)
      samples10 = list(vcf10.header.samples)
      samples_shared = set([s1 for s1 in samples1 if s1 in samples2])
      samples_combined = samples1 + [s2 for s2 in samples2 if s2 not in samples1]

      n = len(samples_combined)

      print(f'Samples in {args.in_VCF1}: {len(samples1)}')
      print(f'Samples in {args.in_VCF2}: {len(samples2)}')
      print(f'Samples in {args.in_VCF3}: {len(samples3)}')
      print(f'Samples in {args.in_VCF4}: {len(samples4)}')
      print(f'Samples in {args.in_VCF5}: {len(samples5)}')
      print(f'Samples in {args.in_VCF6}: {len(samples6)}')
      print(f'Samples in {args.in_VCF7}: {len(samples7)}')
      print(f'Samples in {args.in_VCF8}: {len(samples8)}')
      print(f'Samples in {args.in_VCF9}: {len(samples9)}')
      print(f'Samples in {args.in_VCF10}: {len(samples10)}')
      print(f'Samples shared: {len(samples_shared)}')
      print(f'Samples combined: {n}')

      hds_combined = np.zeros(n * 2, dtype = np.float64)

      vcf_merged.write('##fileformat=VCFv4.1\n')
      for c in vcf1.header.contigs:
         vcf_merged.write(f'##contig=<ID={c}>\n')
      vcf_merged.write('##INFO=<ID=VCF1_AF,Number=1,Type=Float,Description="Estimated Alternate Allele Frequency in VCF 1">\n')
      vcf_merged.write('##INFO=<ID=VCF1_R2,Number=1,Type=Float,Description="Estimated Imputation Accuracy (R-square) in VCF 1">\n')
      vcf_merged.write('##INFO=<ID=VCF2_AF,Number=1,Type=Float,Description="Estimated Alternate Allele Frequency in VCF 2">\n')
      vcf_merged.write('##INFO=<ID=VCF2_R2,Number=1,Type=Float,Description="Estimated Imputation Accuracy (R-square) in VCF 2">\n')
      vcf_merged.write('##INFO=<ID=VCF3_AF,Number=1,Type=Float,Description="Estimated Alternate Allele Frequency in VCF 3">\n')
      vcf_merged.write('##INFO=<ID=VCF3_R2,Number=1,Type=Float,Description="Estimated Imputation Accuracy (R-square) in VCF 3">\n')
      vcf_merged.write('##INFO=<ID=VCF4_AF,Number=1,Type=Float,Description="Estimated Alternate Allele Frequency in VCF 4">\n')
      vcf_merged.write('##INFO=<ID=VCF4_R2,Number=1,Type=Float,Description="Estimated Imputation Accuracy (R-square) in VCF 4">\n')
      vcf_merged.write('##INFO=<ID=VCF5_AF,Number=1,Type=Float,Description="Estimated Alternate Allele Frequency in VCF 5">\n')
      vcf_merged.write('##INFO=<ID=VCF5_R2,Number=1,Type=Float,Description="Estimated Imputation Accuracy (R-square) in VCF 5">\n')
      vcf_merged.write('##INFO=<ID=VCF6_AF,Number=1,Type=Float,Description="Estimated Alternate Allele Frequency in VCF 6">\n')
      vcf_merged.write('##INFO=<ID=VCF6_R2,Number=1,Type=Float,Description="Estimated Imputation Accuracy (R-square) in VCF 6">\n')
      vcf_merged.write('##INFO=<ID=VCF7_AF,Number=1,Type=Float,Description="Estimated Alternate Allele Frequency in VCF 7">\n')
      vcf_merged.write('##INFO=<ID=VCF7_R2,Number=1,Type=Float,Description="Estimated Imputation Accuracy (R-square) in VCF 7">\n')
      vcf_merged.write('##INFO=<ID=VCF8_AF,Number=1,Type=Float,Description="Estimated Alternate Allele Frequency in VCF 8">\n')
      vcf_merged.write('##INFO=<ID=VCF8_R2,Number=1,Type=Float,Description="Estimated Imputation Accuracy (R-square) in VCF 8">\n')
      vcf_merged.write('##INFO=<ID=VCF9_AF,Number=1,Type=Float,Description="Estimated Alternate Allele Frequency in VCF 9">\n')
      vcf_merged.write('##INFO=<ID=VCF9_R2,Number=1,Type=Float,Description="Estimated Imputation Accuracy (R-square) in VCF 9">\n')
      vcf_merged.write('##INFO=<ID=VCF10_AF,Number=1,Type=Float,Description="Estimated Alternate Allele Frequency in VCF 10">\n')
      vcf_merged.write('##INFO=<ID=VCF10_R2,Number=1,Type=Float,Description="Estimated Imputation Accuracy (R-square) in VCF 10">\n')
      vcf_merged.write('##INFO=<ID=AF,Number=1,Type=Float,Description="Combined Estimated Alternate Allele Frequency">\n')
      vcf_merged.write('##INFO=<ID=MAF,Number=1,Type=Float,Description="Combined Estimated Minor Allele Frequency">\n')
      vcf_merged.write('##INFO=<ID=R2,Number=1,Type=Float,Description="Combined Estimated Imputation Accuracy (R-square)">\n')
      vcf_merged.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
      vcf_merged.write('##FORMAT=<ID=DS,Number=1,Type=Float,Description="Estimated Alternate Allele Dosage : [P(0/1)+2*P(1/1)]">\n')
      vcf_merged.write(f'##vcf1={args.in_VCF1}\n')
      vcf_merged.write(f'##vcf2={args.in_VCF2}\n')
      vcf_merged.write(f'##vcf3={args.in_VCF3}\n')
      vcf_merged.write(f'##vcf4={args.in_VCF4}\n')
      vcf_merged.write(f'##vcf5={args.in_VCF5}\n')
      vcf_merged.write(f'##vcf6={args.in_VCF6}\n')
      vcf_merged.write(f'##vcf7={args.in_VCF7}\n')
      vcf_merged.write(f'##vcf8={args.in_VCF8}\n')
      vcf_merged.write(f'##vcf9={args.in_VCF9}\n')
      vcf_merged.write(f'##vcf10={args.in_VCF10}\n')
      vcf_merged.write('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t{}\n'.format('\t'.join(samples_combined)))

      for record1, record2 in zip(vcf1.fetch(contig = args.chrom, start = args.begin, stop = args.end), vcf2.fetch(contig = args.chrom, start = args.begin, stop = args.end)):
         assert record1.chrom == record2.chrom and record1.pos == record2.pos and record1.ref == record2.ref and record1.alts[0] == record2.alts[0], f'{record1.chrom}:{record1.pos}:{record1.ref}:{record1.alts[0]} vs {record2.chrom}:{record2.pos}:{record2.ref}:{record2.alts[0]}'         

         af1 = record1.info['AF']
         af2 = record2.info['AF']
         rsq1 = record1.info['R2']
         rsq2 = record2.info['R2']
         af3 = record3.info['AF']
         af4 = record4.info['AF']
         rsq3 = record3.info['R2']
         rsq4 = record4.info['R2']
         af5 = record5.info['AF']
         af6 = record6.info['AF']
         rsq5 = record5.info['R2']
         rsq6 = record6.info['R2']
         af7 = record7.info['AF']
         af8 = record8.info['AF']
         rsq7 = record7.info['R2']
         rsq8 = record8.info['R2']
         af9 = record9.info['AF']
         af10 = record10.info['AF']
         rsq9 = record9.info['R2']
         rsq10 = record10.info['R2']

         genotypes = []
         dosages = []
 
         for i, sample in enumerate(samples_combined):
            frmt1 = record1.samples.get(sample, None)
            frmt2 = record2.samples.get(sample, None)
 
            if frmt1 is None:
               phased = frmt2.phased
               gt = frmt2['GT']
               ds = frmt2['DS']
               hds = frmt2['HDS']
            elif frmt2 is None:
               phased = frmt1.phased
               gt = frmt1['GT']
               ds = frmt1['DS']
               hds = frmt1['HDS']
            else:
               if rsq1 >= rsq2:
                  phased = frmt1.phased
                  gt = frmt1['GT']
                  ds = frmt1['DS']
                  hds = frmt1['HDS']
               else:
                  phased = frmt2.phased
                  gt = frmt2['GT']
                  ds = frmt2['DS']
                  hds = frmt2['HDS']
             
            genotypes.append(f'{gt[0]}|{gt[1]}' if phased else f'{gt[0]}/{gt[1]}')
            dosages.append(ds)
            hds_combined[i * 2] = hds[0]
            hds_combined[i * 2 + 1] = hds[1]
         
         p = np.mean(hds_combined)
         if p > 0:
            rsq_combined = np.mean(np.square(hds_combined - p)) / (p * (1.0 - p))
         else:
            rsq_combined = 0.0

         if rsq_combined < args.min_rsq:
            continue

         vcf_merged.write('{chrom}\t{pos}\t{vid}\t{ref}\t{alts}\t{qual}\t{filters}\tVCF1_AF={af1:.5f};VCF2_AF={af2:.5f};VCF3_AF={af3:.5f};VCF4_AF={af4:.5f};VCF5_AF={af5:.5f};VCF6_AF={af6:.5f};VCF7_AF={af7:.5f};VCF8_AF={af8:.5f};VCF9_AF={af9:.5f};VCF10_AF={af10:.5f};VCF1_R2={rsq1:.5f};VCF2_R2={rsq2:.5f};VCF3_R2={rsq3:.5f};VCF4_R2={rsq4:.5f};VCF5_R2={rsq5:.5f};VCF6_R2={rsq6:.5f};VCF7_R2={rsq7:.5f};VCF8_R2={rsq8:.5f};VCF9_R2={rsq9:.5f};VCF10_R2={rsq10:.5f};AF={af_combined:.5f};MAF={maf_combined:.5f};R2={rsq_combined:.5f}\t{formats}\t{gt_ds}\n'.format(
               chrom = record1.chrom,
               pos = record1.pos,
               vid = record1.id,
               ref = record1.ref,
               alts = ','.join(record1.alts),
               qual = '.',
               filters = 'PASS',
               af1 = af1,
               af2 = af2,
               af3 = af3,
               af4 = af4,
               af5 = af5,
               af6 = af6,
               af7 = af7,
               af8 = af8,
               af9 = af9,
               af10 = af10,
               rsq1 = rsq1,
               rsq2 = rsq2,
               rsq3 = rsq3,
               rsq4 = rsq4,
               rsq5 = rsq5,
               rsq6 = rsq6,
               rsq7 = rsq7,
               rsq8 = rsq8,
               rsq9 = rsq9,
               rsq10 = rsq10,
               af_combined = p,
               maf_combined = p if p < 0.5 else 1.0 - p,
               rsq_combined = rsq_combined,
               formats = 'GT:DS',
               gt_ds = '\t'.join(f'{gt}:{ds:.3f}' for gt, ds in zip(genotypes, dosages)  )
               ))
