__author__ = 'Jonathan Rubin'

import os
import time
import sys
import argparse
import configparser
import config_parser
from multiprocessing import Pool
import multiprocessing as mp

def run():
    #Home directory, gets the full path (no '/' at the end) to the folder containing this script
    homedir = os.path.dirname(os.path.realpath(__file__))

    parser = argparse.ArgumentParser(description='Transcription Factor Enrichment Analysis (TFEA) takes as input a configuration file (.ini) and outputs a folder containing TFEA results.',usage='TFEA --config CONFIG.ini [--sbatch email@address.com]')
    parser.add_argument('--config',help='REQUIRED. A configuration file containing .ini suffix (ex. config.ini). See example in the examples folder.')
    parser.add_argument('--sbatch',default=False,help='OPTIONAL. Submits an sbatch job. If specified, input an e-mail address.')
    if len(sys.argv)==1:
        # display help message when no args are passed.
        parser.print_help()
        sys.exit(1)
    sbatch = parser.parse_args().sbatch
    configfile = parser.parse_args().config
    config = configparser.ConfigParser(interpolation = configparser.ExtendedInterpolation())
    config.read(configfile)

    if sbatch == False:
        output,filedir,figuredir,e_and_o = make_out_directories(True,config)
    elif str(sbatch) == 'SUBMITTED':
        output,filedir,figuredir,e_and_o = make_out_directories(False,config)
    else:
        output,filedir,figuredir,e_and_o = make_out_directories(True,config)
        scriptdir = parent_dir(homedir) + '/scripts/'
        script = scriptdir + 'run_main.sbatch'
        email = str(sbatch)
        os.system("sbatch --error=" + e_and_o + "%x.err --output=" + e_and_o + "%x.out --mail-user="+email+" --export=src="+homedir+",config=" +configfile+ " " + script)
        sys.exit("TFEA has been submitted using an sbatch script, use qstat to check its progress.")



    #Run the config_parser script which will create variables for all folders and paths to use throughout TFEA
    config_parser.run(homedir+'/',config,output,filedir,figuredir)


    #Import scripts from this package
    import combine_bed
    import count_reads
    import rank_regions
    import DESeq
    import motif_distance
    import ES_calculator
    import create_html
    import config
    import meta_eRNA



    #This module takes the input list of BED files, concatenates them, and then merges them via bedtools.
    COMBINEtime = time.time()
    if config.COMBINE:
        BED = combine_bed.run()
    else:
        BED = config.BEDS[0]
    COMBINEtime = time.time()-COMBINEtime 

    #This module counts reads from all Bam files in BAM1 and BAM2 and creates count_file with this info.
    COUNTtime = time.time()
    if config.COUNT:
        print "Counting reads in regions..."
        count_reads.run(BED)
        print "done"
    COUNTtime = time.time()-COUNTtime

    #This module runs DESeq on specified 
    DESEQtime = time.time()
    if config.DESEQ:
        print "Running DESeq..."
        DESeq.run()
        rank_regions.deseqfile()
        print "done"
    DESEQtime = time.time()-DESEQtime

    #Scans ranked BED regions for motifs of interest and records them in distance file
    if config.CALCULATE:
        cpus = mp.cpu_count()
        if cpus > 64:
            cpus = 64

        p = Pool(cpus)
        args = [(x) for x in config.BAM1+config.BAM2]
        millions_mapped = p.map(meta_eRNA.samtools_flagstat,args)

        print "Finding motif hits in regions..."
        if config.SINGLEMOTIF == False:
            TFresults = list()
            CALCULATEtime = 0.0
            if config.POOL:
                a = time.time()
                args = [(x,millions_mapped) for x in os.listdir(config.MOTIF_HITS)]
                p = Pool(cpus)
                TFresults = p.map(ES_calculator.run,args)
                CALCULATEtime += time.time() - a
                create_html.createTFtext(TFresults)
            else:
                for MOTIF_FILE in os.listdir(config.MOTIF_HITS):
                    a = time.time()

                    #This module is where the bulk of the analysis is done. The functions below calculate ES,NES,p-value,FDR for each TF motif in
                    #the HOCOMOCO database.
                    results = ES_calculator.run((MOTIF_FILE,millions_mapped))
                    if results != "no hits":
                        TFresults.append(results)
                        CALCULATEtime += time.time()-a
                        print MOTIF_FILE + " calculation done in: " + str(CALCULATEtime) + "s"
                    else:
                        print "No motifs within specified window for: ", MOTIF_FILE
            TFresults = ES_calculator.FDR(TFresults)
            create_html.run(TFresults,COMBINEtime,COUNTtime,DESEQtime,CALCULATEtime)

        #Note if you set the SINGLEMOTIF variable to a specific TF, this program will be unable to determine an FDR for the given motif.
        else:
            results = ES_calculator.run((config.SINGLEMOTIF,millions_mapped))
            create_html.single_motif(results)
    print "done"


def make_out_directories(dirs,config):
    #Output directory
    output = config['DATA']['OUTPUT'].strip("'")
    if dirs:
        if not os.path.isdir(output + 'TFEA_output-0/'):
            output = output + 'TFEA_output-0/'
            os.makedirs(output)
        else:
            outputfolders = list()
            for folder in os.listdir(output):
                if 'TFEA_output' in folder:
                    outputfolders.append(int(folder.split('-')[1]))
            output = output + 'TFEA_output-' + str(max(outputfolders)+1) + '/'
            os.makedirs(output)
    else:
        outputfolders = list()
        for folder in os.listdir(output):
            if 'TFEA_output' in folder:
                outputfolders.append(int(folder.split('-')[1]))
        output = output + 'TFEA_output-' + str(max(outputfolders)) + '/'


    #Temporary files will go in this directory
    filedir = output + 'temp_files/'
    if dirs:
        if not os.path.isdir(filedir):
            os.makedirs(filedir)

    #Error and out files will go in this directory
    e_and_o = output + 'e_and_o/'
    if dirs:
        if not os.path.isdir(e_and_o):
            os.makedirs(e_and_o)


    #Directory where plots used in html file will be stored.
    figuredir = output + 'plots/'
    if dirs:
        if not os.path.isdir(figuredir):
            os.makedirs(figuredir)

    return output,filedir,figuredir,e_and_o

#Return parent directory
def parent_dir(directory):
    pathlist = directory.split('/')
    newdir = '/'.join(pathlist[0:len(pathlist)-1])
    
    return newdir