#!/usr/bin/env python

"""
summarize_standard_events.py:

    count all standard events in a given FlatFile directory

"""

import os
import sys
from optparse import OptionParser, make_option

import psyco
#psyco.log()
#psyco.profile()
psyco.full()

# default directory
#defaultDir = '/r100/burge/shared/splice_graphs/mm6/FlatFiles/'
defaultDir = '/r100/burge/shared/splice_graphs/hg17/FlatFiles/'

# digest command line
opts = OptionParser(option_list=                                                                        \
                    [make_option('-d','--dir', dest='inDir', default=defaultDir,                        \
                                 help='input directory with standard event subdirectories [default: %s]' % defaultDir), \
                     make_option('-o','--out', dest='outFile',                                          \
                                 default='standard_events.hg17.summary.txt',                            \
                                 help='output file with summary of standard events [default: standard_events.hg17.summary.txt]'), \
                     ])
(options, args) = opts.parse_args()

if not os.path.isdir(options.inDir):
    print >> sys.stderr, "ERROR: input directory is not found.\n"
    opts.print_help(sys.stderr)
    sys.exit(0)

else:
    # get file list in directory
    subDirs          = [ d for d in os.listdir(options.inDir) if d.startswith('StandardEvents_')]
    subDirsTweaked   = [ d for d in os.listdir(options.inDir) if d.startswith('StandardEventsTweaked_')]
    subDirsFiltered  = [ d for d in os.listdir(options.inDir) if d.startswith('StandardEventsFiltered_')]
    subDirsCanonical = [ d for d in os.listdir(options.inDir) if d.startswith('StandardEventsCanonical_')]

    #output files with distances of neighboring sites
    try:
        outFile  = open(options.outFile, 'w')
    except:
        print >> sys.stderr, 'ERROR opening output files: %s' % sys.exc_info()[1]
    else:
        outFile.write("#standard events for SpliceGraph gene models, generated by summarize_standard_events.py\n")
        outFile.write("#indir: %s\n" % options.inDir)
        outFile.write("#counts are given for:\n")
        outFile.write("#  RAW DATA       : all transcript evidence\n")
        outFile.write("#  TWEAKED DATA   : alignments tweaked to optimize use of canonical splice sites (GT->AG or GC->AG)\n")
        outFile.write("#  FILTERED DATA  : at least two transcripts or canonical splice sites (GT->AG or GC->AG)\n")
        outFile.write("#  CANONICAL DATA : just canonical splice sites (GT->AG or GC->AG)\n")
        outFile.write("#output columns:\n")
        outFile.write("#  chr              : chromosome\n")
        outFile.write("#  event            : splicing pattern\n")
        outFile.write("#  nbEvents         : number of events observed in RAW DATA\n")
        outFile.write("#  nbEventsTweaked  : number of events observed in TWEAKED DATA\n")
        outFile.write("#  nbEventsFiltered : number of events observed in FILTERED DATA\n")
        outFile.write("#  nbEventsCanon    : number of events observed in CANONICAL DATA\n")
        outFile.write("#  nbGenes          : number of distinct gene models with that event observed in RAW DATA\n")
        outFile.write("#  nbGenesTweaked   : number of distinct gene models with that event observed in TWEAKED DATA\n")
        outFile.write("#  nbGenesFiltered  : number of distinct gene models with that event observed in FILTERED DATA\n")
        outFile.write("#  nbGenesCanon     : number of distinct gene models with that event observed in CANONICAL DATA\n")
        outFile.write("#chr\tevent\tnbEvents\tnbEventsTweaked\tnbEventsFiltered\tnbEventsCanon\tnbGenes\tnbGenesTweaked\tnbGenesFiltered\tnbGenesCanon\n")

        # raw data based
        geneCounts     = {} # format: geneCounts[chr][event][gnId] = nbEvents
        eventCounts    = {} # format: eventCounts[chr][event]      = nbEvents
        totGeneCounts  = {} # format: totGeneCounts[event][gnId]   = nbEvents  (over all chr)
        totEventCounts = {} # format: totEventCounts[event]        = nbEvents  (over all chr)
        # tweaked data based
        TgeneCounts     = {} # format: TgeneCounts[chr][event][gnId] = nbEvents
        TeventCounts    = {} # format: TeventCounts[chr][event]      = nbEvents
        TtotGeneCounts  = {} # format: TtotGeneCounts[event][gnId]   = nbEvents  (over all chr)
        TtotEventCounts = {} # format: TtotEventCounts[event]        = nbEvents  (over all chr)
        # filtered data based
        FgeneCounts     = {} # format: FgeneCounts[chr][event][gnId] = nbEvents
        FeventCounts    = {} # format: FeventCounts[chr][event]      = nbEvents
        FtotGeneCounts  = {} # format: FtotGeneCounts[event][gnId]   = nbEvents  (over all chr)
        FtotEventCounts = {} # format: FtotEventCounts[event]        = nbEvents  (over all chr)
        # canonical data based
        CgeneCounts     = {} # format: CgeneCounts[chr][event][gnId] = nbEvents
        CeventCounts    = {} # format: CeventCounts[chr][event]      = nbEvents
        CtotGeneCounts  = {} # format: CtotGeneCounts[event][gnId]   = nbEvents  (over all chr)
        CtotEventCounts = {} # format: CtotEventCounts[event]        = nbEvents  (over all chr)

        # summarize unfiltered data
        for i in xrange(len(subDirs)):

            chr = subDirs[i].split('_',1)[1]

            if not geneCounts.has_key(chr):
                geneCounts[chr]   = {}
                eventCounts[chr]  = {}

            infiles = [ f for f in os.listdir(options.inDir + '/' + subDirs[i]) if f.endswith('_events') ]

            for infile in infiles:
                event = infile.split('_',1)[0]
                if not totEventCounts.has_key(event):
                    totEventCounts[event]  = 0
                    totGeneCounts[event]   = {}
                if not eventCounts[chr].has_key(event):
                    eventCounts[chr][event]  = 0
                    geneCounts[chr][event]   = {}

                fh = open(options.inDir + '/' + subDirs[i] + '/' + infile, 'r')
                for line in fh:
                    if line.startswith('#'):
                        continue
                    else:
                        gnId = line.split('\t',1)[0]

                        if geneCounts[chr][event].has_key(gnId):
                            geneCounts[chr][event][gnId] += 1
                        else:
                            geneCounts[chr][event][gnId]  = 1

                        if totGeneCounts[event].has_key(gnId):
                            totGeneCounts[event][gnId] += 1
                        else:
                            totGeneCounts[event][gnId]  = 1

                        eventCounts[chr][event] += 1
                        totEventCounts[event]   += 1


        # summarize tweaked data
        for i in xrange(len(subDirsTweaked)):

            chr = subDirsTweaked[i].split('_',1)[1]

            if not TgeneCounts.has_key(chr):
                TgeneCounts[chr]  = {}
                TeventCounts[chr] = {}

            infiles = [ f for f in os.listdir(options.inDir + '/' + subDirsTweaked[i]) if f.endswith('_events') ]

            for infile in infiles:
                event = infile.split('_',1)[0]
                if not TtotEventCounts.has_key(event):
                    TtotEventCounts[event] = 0
                    TtotGeneCounts[event]  = {}
                if not TeventCounts[chr].has_key(event):
                    TeventCounts[chr][event] = 0
                    TgeneCounts[chr][event]  = {}

                fh = open(options.inDir + '/' + subDirsTweaked[i] + '/' + infile, 'r')
                for line in fh:
                    if line.startswith('#'):
                        continue
                    else:
                        gnId = line.split('\t',1)[0]

                        if TgeneCounts[chr][event].has_key(gnId):
                            TgeneCounts[chr][event][gnId] += 1
                        else:
                            TgeneCounts[chr][event][gnId]  = 1

                        if TtotGeneCounts[event].has_key(gnId):
                            TtotGeneCounts[event][gnId] += 1
                        else:
                            TtotGeneCounts[event][gnId]  = 1

                        TeventCounts[chr][event] += 1
                        TtotEventCounts[event]   += 1


        # summarize filtered data
        for i in xrange(len(subDirsFiltered)):

            chr = subDirsFiltered[i].split('_',1)[1]

            if not FgeneCounts.has_key(chr):
                FgeneCounts[chr]  = {}
                FeventCounts[chr] = {}

            infiles = [ f for f in os.listdir(options.inDir + '/' + subDirsFiltered[i]) if f.endswith('_events') ]

            for infile in infiles:
                event = infile.split('_',1)[0]
                if not FtotEventCounts.has_key(event):
                    FtotEventCounts[event] = 0
                    FtotGeneCounts[event]  = {}
                if not FeventCounts[chr].has_key(event):
                    FeventCounts[chr][event] = 0
                    FgeneCounts[chr][event]  = {}

                fh = open(options.inDir + '/' + subDirsFiltered[i] + '/' + infile, 'r')
                for line in fh:
                    if line.startswith('#'):
                        continue
                    else:
                        gnId = line.split('\t',1)[0]

                        if FgeneCounts[chr][event].has_key(gnId):
                            FgeneCounts[chr][event][gnId] += 1
                        else:
                            FgeneCounts[chr][event][gnId]  = 1

                        if FtotGeneCounts[event].has_key(gnId):
                            FtotGeneCounts[event][gnId] += 1
                        else:
                            FtotGeneCounts[event][gnId]  = 1

                        FeventCounts[chr][event] += 1
                        FtotEventCounts[event]      += 1


        # summarize canonical data
        for i in xrange(len(subDirsCanonical)):

            chr = subDirsCanonical[i].split('_',1)[1]

            if not CgeneCounts.has_key(chr):
                CgeneCounts[chr]  = {}
                CeventCounts[chr] = {}

            infiles = [ f for f in os.listdir(options.inDir + '/' + subDirsCanonical[i]) if f.endswith('_events') ]

            for infile in infiles:
                event = infile.split('_',1)[0]
                if not CtotEventCounts.has_key(event):
                    CtotEventCounts[event] = 0
                    CtotGeneCounts[event]  = {}
                if not CeventCounts[chr].has_key(event):
                    CeventCounts[chr][event] = 0
                    CgeneCounts[chr][event]  = {}

                fh = open(options.inDir + '/' + subDirsCanonical[i] + '/' + infile, 'r')
                for line in fh:
                    if line.startswith('#'):
                        continue
                    else:
                        gnId = line.split('\t',1)[0]

                        if CgeneCounts[chr][event].has_key(gnId):
                            CgeneCounts[chr][event][gnId] += 1
                        else:
                            CgeneCounts[chr][event][gnId]  = 1

                        if CtotGeneCounts[event].has_key(gnId):
                            CtotGeneCounts[event][gnId] += 1
                        else:
                            CtotGeneCounts[event][gnId]  = 1

                        CeventCounts[chr][event] += 1
                        CtotEventCounts[event]      += 1

        # output summary
        eventKeys = totEventCounts.keys()
        eventKeys.sort()
        for event in eventKeys:
            chrKeys = eventCounts.keys()
            chrKeys.sort()
            for chr in chrKeys:
                outFile.write('%s\t%s\t%i\t%i\t%i\t%i\t%i\t%i\t%i\t%i\n' % \
                              (chr, event, \
                               (eventCounts.has_key(chr) and eventCounts[chr].has_key(event)) and eventCounts[chr][event] or 0, \
                               (TeventCounts.has_key(chr) and TeventCounts[chr].has_key(event)) and TeventCounts[chr][event] or 0, \
                               (FeventCounts.has_key(chr) and FeventCounts[chr].has_key(event)) and FeventCounts[chr][event] or 0, \
                               (CeventCounts.has_key(chr) and CeventCounts[chr].has_key(event)) and CeventCounts[chr][event] or 0, \
                               (geneCounts.has_key(chr) and geneCounts[chr].has_key(event)) and len(geneCounts[chr][event]) or 0,
                               (TgeneCounts.has_key(chr) and TgeneCounts[chr].has_key(event)) and len(TgeneCounts[chr][event]) or 0,
                               (FgeneCounts.has_key(chr) and FgeneCounts[chr].has_key(event)) and len(FgeneCounts[chr][event]) or 0,
                               (CgeneCounts.has_key(chr) and CgeneCounts[chr].has_key(event)) and len(CgeneCounts[chr][event]) or 0,
                               ))
            outFile.write('#%s\t%s\t%i\t%i\t%i\t%i\t%i\t%i\t%i\t%i\n' % \
                          ('total', event, \
                           totEventCounts.has_key(event) and totEventCounts[event] or 0, \
                           TtotEventCounts.has_key(event) and TtotEventCounts[event] or 0, \
                           FtotEventCounts.has_key(event) and FtotEventCounts[event] or 0, \
                           CtotEventCounts.has_key(event) and CtotEventCounts[event] or 0, \
                           totGeneCounts.has_key(event) and len(totGeneCounts[event]) or 0, \
                           TtotGeneCounts.has_key(event) and len(TtotGeneCounts[event]) or 0, \
                           FtotGeneCounts.has_key(event) and len(FtotGeneCounts[event]) or 0, \
                           CtotGeneCounts.has_key(event) and len(CtotGeneCounts[event]) or 0, \
                           ))

        outFile.close()
