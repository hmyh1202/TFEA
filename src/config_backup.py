import os
import main
import read_conditions

def parent_dir(directory):
    pathlist = directory.split('/')
    newdir = '/'.join(pathlist[0:len(pathlist)-1])
    
    return newdir


#User defined input. Specify here the parameters used to run TFEA including full paths to all the necessary input files
#======================================================================================================================#

#Which parts of TFEA would you like to run? These are switches to turn on/off different modules in TFEA

#This module combines bed files from BED and merges them using bedtools. If False, it will assume BEDS[0] contains the bed file of interest (must be a sorted bed file)
COMBINE = True

#This module performs bedtools multicov which requires bam files and a bed file. It will count reads for each bam file across all regions in the inputted bed file
COUNT = True

#This module performs DESeq and then ranks regions based on the p-value obtained from DESeq, if you set this to false, TFEA will look for the DESeq file within your specified output directory
DESEQ = True

#This module performs the bulk of the calculation of TFEA and will most likely take the longest. Unless you just want to generate files, this should usually be set to True
CALCULATE = True

#Determines whether ES calculations will be run in parallel.
POOL=True
##POOL = False

#Determines whether you want TFEA to automatically make an output directory (within your specified output). If set to false, make sure your output directory has folders called temp_files, e_and_o, and plots
MAKE_DIRS = True

#Define the FDR cutoff to be used for calling significant hits
# FDRCUTOFF = pow(10,-6)
FDRCUTOFF = 0.1
PVALCUTOFF = 0.1
DRAWPVALCUTOFF = False

CONDITION = False
##CONDITION = True

if CONDITION:
    CONDITIONS='/scratch/Shares/dowell/pubgro/conditions_short_20161103_tentative.txt_20161107-165140.csv'
    ##SPECIFICCELLTYPE = 'HCT116'
    ##SPECIFICCELLTYPE = 'MCF7'
    SPECIFICCELLTYPE = 'AC16'
    ##LABEL1='DMSO_1hr'
    ##LABEL1='vehicle'
    LABEL1='control_notvechicle'
    ##LABEL2='Nutlin_1hr'
    ##LABEL2='E2_10min'
    LABEL2='TNFa_30min'
    BAMDIR='/scratch/Shares/dowell/pubgro_sortedbams/'
    #BEDDIR='/scratch/Shares/dowell/md_score_paper/tfit_bed_files/human/recent/'
    BEDDIR = '/scratch/Shares/dowell/md_score_paper/tfit_bed_files/human/archive/081/'
    ##KEYWORD='Allen2014'
    ##KEYWORD='Hah2013'
    KEYWORD='Luo2014'
    ##OUTPUT='/scratch/Users/rusi2317/projects/rotation/output/TFEA/Allen2014/'
    ##OUTPUT='/scratch/Users/rusi2317/projects/rotation/output/TFEA/Hah2013/'
    OUTPUT='/scratch/Users/rusi2317/projects/rotation/output/TFEA/Luo2014/'
    BAM1,BAM2,BEDS = read_conditions.run(CONDITIONS,KEYWORD,SPECIFICCELLTYPE,LABEL1,LABEL2,BAMDIR,BEDDIR)
else:
    #Input a list of bed files with regions of interest to be analyzed. Ideally, these are meant to be Tfit output files corresponding to each bam file submitted. 
    #These files will be concatenated and merged (bedtools) to produce detected regions in all samples. If you only have one bed file with regions of interest
    #submit it as a single item in the BEDS list and set COMBINE to False.
    # BEDDIR = '/scratch/Shares/dowell/md_score_paper/tfit_bed_files/human/recent/'
    BEDDIR = '/scratch/Shares/dowell/md_score_paper/tfit_bed_files/human/archive/081/'
    ##BEDS = [BEDDIR+'SRR1105736-1_bidir_predictions.bed',BEDDIR+'SRR1105737-1_bidir_predictions.bed',BEDDIR+'SRR1105738-1_bidir_predictions.bed',BEDDIR+'SRR1105739-1_bidir_predictions.bed']
    BEDS = [BEDDIR+'SRR1105737-1_bidir_predictions.bed',BEDDIR+'SRR1105739-1_bidir_predictions.bed']
    ##BEDS = [BEDDIR+'SRR1015583-1_bidir_predictions.bed',BEDDIR+'SRR1015587-1_bidir_predictions.bed']
    ##BEDS = [BEDDIR+'SRR1015583-1_bidir_predictions.bed',BEDDIR+'SRR1015584-1_bidir_predictions.bed',BEDDIR+'SRR1015587-1_bidir_predictions.bed',BEDDIR+'SRR1015588-1_bidir_predictions.bed']
    ##BEDS = [BEDDIR+'SRR653421-1_bidir_predictions.bed',BEDDIR+'SRR653422-1_bidir_predictions.bed',BEDDIR+'SRR653425-1_bidir_predictions.bed',BEDDIR+'SRR653426-1_bidir_predictions.bed']
    #Input bam files as a list containing transcription data. Must specify at least two bam files. 
    #If multiple replicates, specify each as a full path in the appropriate list.
    BAMDIR ='/scratch/Shares/dowell/pubgro_sortedbams/'
    ##BAM1 = [BAMDIR+'SRR1105736.fastqbowtie2.sorted.bam',BAMDIR+'SRR1105737.fastqbowtie2.sorted.bam']
    ##BAM2 = [BAMDIR+'SRR1105738.fastqbowtie2.sorted.bam',BAMDIR+'SRR1105739.fastqbowtie2.sorted.bam']
    BAM1 = [BAMDIR+'SRR1105737.fastqbowtie2.sorted.bam']
    BAM2 = [BAMDIR+'SRR1105739.fastqbowtie2.sorted.bam']

    ##BAM1 = [BAMDIR+'SRR1015583.fastqbowtie2.sorted.bam']
    ##BAM2 = [BAMDIR+'SRR1015587.fastqbowtie2.sorted.bam']
    ##BAM1 = [BAMDIR+'SRR1015583.fastqbowtie2.sorted.bam',BAMDIR+'SRR1015584.fastqbowtie2.sorted.bam']
    ##BAM2 = [BAMDIR+'SRR1015587.fastqbowtie2.sorted.bam',BAMDIR+'SRR1015588.fastqbowtie2.sorted.bam']
    ##BAM1 = [BAMDIR+'SRR653421.fastqbowtie2.sorted.bam',BAMDIR+'SRR653422.fastqbowtie2.sorted.bam']
    ##BAM2 = [BAMDIR+'SRR653425.fastqbowtie2.sorted.bam',BAMDIR+'SRR653426.fastqbowtie2.sorted.bam']

    LABEL1 = 'DMSO_1hr'
    LABEL2 = 'Nutlin_1hr'

    ##LABEL1 = 'control_notvehicle'
    ##LABEL2 = 'TNFa_30min'

    #Specify conditions for bam files
    ##LABEL1 = 'vehicle'
    ##LABEL2 = 'E2_40min'

    OUTPUT = '/scratch/Users/rusi2317/projects/rotation/output/TFEA/Allen2014/'
    ##OUTPUT = '/scratch/Users/rusi2317/projects/rotation/output/TFEA/Luo2014/'
    ##OUTPUT = '/scratch/Users/rusi2317/projects/rotation/output/TFEA/Hah2013/'


    # #Input a list of bed files with regions of interest to be analyzed. Ideally, these are meant to be Tfit output files corresponding to each bam file submitted. 
    # #These files will be concatenated and merged (bedtools) to produce detected regions in all samples. If you only have one bed file with regions of interest
    # #submit it as a single item in the BEDS list and set COMBINE to False.
    # BEDDIR1 = '/scratch/Users/joru1876/Taatjes/170825_NB501447_0152_fastq_SERCAREP2_30REP1_RESEQUENCING/Demux/cat/trimmed/flipped/bowtie2/sortedbam/genomecoveragebed/fortdf/Tfit/'
    # BEDDIR2 = '/scratch/Users/joru1876/Taatjes/170207_K00262_0069_AHHMHVBBXX_SERCAREP1/cat/trimmed/flipped/bowtie2/sortedbam/genomecoveragebed/fortdf/Tfit_run2/'
    # BEDS = [BEDDIR1+'foot_print_testing-9_bidir_predictions.bed',BEDDIR1+'foot_print_testing-11_bidir_predictions.bed',BEDDIR2+'foot_print_testing-7_bidir_predictions.bed',BEDDIR2+'foot_print_testing-11_bidir_predictions.bed']

    # #Input bam files as a list containing transcription data. Must specify at least two bam files. 
    # #If multiple replicates, specify each as a full path in the appropriate list.
    # BAMDIR1 = '/scratch/Users/joru1876/Taatjes/170207_K00262_0069_AHHMHVBBXX_SERCAREP1/cat/trimmed/flipped/bowtie2/sortedbam/'
    # BAMDIR2 = '/scratch/Users/joru1876/Taatjes/170825_NB501447_0152_fastq_SERCAREP2_30REP1_RESEQUENCING/Demux/cat/trimmed/flipped/bowtie2/sortedbam/'
    # BAM1 = [BAMDIR1+'J12_trimmed.flip.fastq.bowtie2.sorted.bam',BAMDIR2+'J1DO1_AGTCAA_S1_L007and8_R1_001_trimmed.flip.fastq.bowtie2.sorted.bam']
    # BAM2 = [BAMDIR1+'J52_trimmed.flip.fastq.bowtie2.sorted.bam',BAMDIR2+'J5D451_GTCCGC_S3_L007and8_R1_001_trimmed.flip.fastq.bowtie2.sorted.bam']

    # #Specify conditions for bam files (no spaces allwed)
    # LABEL1 = '0_Serum'
    # LABEL2 = '45_Serum'

    # OUTPUT = '/scratch/Users/joru1876/TFEA_files/Rubin/'

#Specify whether you want to run a single motif or a database. By default, TFEA runs on the latest version of HOCOMOCO obtained through MEME.
#Default:False. Change to a motif name if you want to run TFEA on a single motif (make sure your single motif is in the specified database).
##SINGLEMOTIF='HO_P53_HUMAN.H10MO.B.bed'
# SINGLEMOTIF='HO_PROX1_HUMAN.H10MO.D.bed'
# SINGLEMOTIF='HO_ZBED1_HUMAN.H10MO.D.bed'
# SINGLEMOTIF='HO_STA5A_MOUSE.H10MO.A.bed'
# SINGLEMOTIF='HO_IRF2_MOUSE.H10MO.C.bed'
# SINGLEMOTIF='HO_IRF4_MOUSE.H10MO.C.bed'

##Luo 2014motifs to be testedx
##SINGLEMOTIF='HO_RELB_HUMAN.H10MO.C.bed'
##SINGLEMOTIF='HO_REL_HUMAN.H10MO.C.bed'
##SINGLEMOTIF='HO_HMGA1_HUMAN.H10MO.D.bed'
##SINGLEMOTIF='HO_NFKB1_HUMAN.H10MO.B.bed'
##SINGLEMOTIF='HO_NFKB2_HUMAN.H10MO.D.bed'
##SINGLEMOTIF='HO_SP3_HUMAN.H10MO.B.bed'

SINGLEMOTIF=False

#This is a folder that contains PSSM hits across the genome. This folder is needed for running DE-Seq and must be downloaded separately
##MOTIF_HITS = '/scratch/Shares/dowell/older_md_score_paper_with_diff/supplements/ENCODE/HOCOMOCODatabaseFIMO/FIMO_OUT_HUMAN_v10_BEDS/'
# MOTIF_HITS = '/scratch/Shares/dowell/md_score_paper/PSSM_hits_genome_wide/pval6_mouse/'
MOTIF_HITS = '/scratch/Shares/dowell/md_score_paper/PSSM_hits_genome_wide/pval-6/'

#Specify path to motif logos
##HOMEDIR = main.homedir


HOMEDIR = os.path.dirname(os.path.realpath(__file__))
#HOMEDIR = main.homedir
#LOGOS = main.parent_dir(HOMEDIR) + '/mouse_logo/'
LOGOS = parent_dir(HOMEDIR) + '/human_logo/'


#============================================================================================================================================================
#Only change these settings if you know what you're doing.
H = 1500.0
h = 150.0