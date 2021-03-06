#!/usr/bin/env python
import Bio
from accessoryFunctions.accessoryFunctions import GenObject, printtime, get_version
import sys
import os
from spadespipeline.bowtie import Bowtie2CommandLine

__author__ = 'adamkoziol'


class Versions(object):
    def versions(self):
        for sample in self.metadata:
            # Initialise the attribute
            sample.software = GenObject()
            # Populate the versions of the software used
            ss = sample.software
            ss.python = self.python
            ss.arch = self.arch
            ss.blast = self.blast
            ss.bowtie2 = self.bowversion
            ss.samtools = self.samversion
            ss.qualimap = self.qualimap
            ss.mash = self.mash
            ss.prodigal = self.prodigal
            ss.pipeline = self.commit
            ss.spades = self.spades
            ss.bbmap = self.bbmap
            ss.fastqc = self.fastqc
            ss.blc2fastq = self.bcl2fastq
            ss.perl = self.perl
            ss.biopython = self.biopython
            ss.java = self.java
            # ss.docker = self.docker

    def __init__(self, inputobject):
        self.metadata = inputobject.runmetadata.samples
        self.start = inputobject.starttime
        self.commit = inputobject.commit
        # Determine the versions of the software used
        printtime('Populating metadata', self.start)
        self.python = sys.version.replace('\n', '')
        self.arch = ", ".join(os.uname())
        self.blast = get_version(['blastn', '-version']).decode('utf-8').split('\n')[0].split()[1]
        self.spades = get_version(['spades.py', '-v']).decode('utf-8').split('\n')[0].split()[1]
        self.bowversion = Bowtie2CommandLine(version=True)()[0].split('\n')[0].split()[-1]
        self.samversion = get_version(['samtools', '--version']).decode('utf-8').split('\n')[0].split()[1]
        # Qualimap seems to have an Java warning message that doesn't necessarily show up on every system
        # Only capture the line that starts with 'Qualimap'
        qualimaplist = get_version(['qualimap', '--help']).decode('utf-8').split('\n')
        for line in qualimaplist:
            if 'QualiMap' in line:
                self.qualimap = line.split()[1]
        self.mash = get_version(['mash']).decode('utf-8').split('\n')[1].split()[2]
        self.prodigal = get_version(['prodigal', '-v']).decode('utf-8').split('\n')[1].split()[1]
        self.bbmap = get_version(['bbversion.sh']).decode('utf-8')
        self.fastqc = get_version(['fastqc', '--version']).decode('utf-8').split('\n')[0].split()[1]
        # Uncomment this once you figure ou where this file is stored.
        self.bcl2fastq = "2"
        self.perl = get_version(['perl', '-v']).decode('utf-8').split('\n')[1].split('This is ')[1]
        self.biopython = Bio.__version__
        self.java = get_version(['java', '-showversion']).decode('utf-8').split('\n')[0].split()[2].replace('"', '')
        # self.docker = get_version(['docker', 'version']).split('\n')[1].split()[1]
        self.versions()
