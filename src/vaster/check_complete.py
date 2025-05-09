#!/usr/bin/env python
"""
Copyright (C) Swinburne 2024
"""
from vaster.vtools import measure_running_time 
from vaster.structure import DataBasic

import glob
import time
import os
import sys
import argparse

import logging
logger = logging.getLogger(__name__)

__author__ = "Yuanming Wang <yuanmingwang@swin.edu.au>"


def _main():
    start_time = time.time()

    parser = argparse.ArgumentParser(
        prog='VOevent', 
        description='VO Event trigger', 
        epilog='Example usage: python ~/scripts/notebooks/notes/template.py -h', 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, 
        )
    parser.add_argument('-s', '--sbids', type=int, nargs='+', default=None, 
                        help='input sbid for prepare scripts, number only, emplty for all sbids in this folder')
    parser.add_argument('--dir', type=str, default='.', help='output directory')
    # parser.add_argument('--dry-run', action='store_true', help='Perform a dry run')
    parser.add_argument('-v', '--verbose', action='store_true',help='make it verbose')
    args = parser.parse_args()

    make_verbose(args)
    logger.info(args)

    if args.sbids is None:
        folderlist = glob.glob(os.path.join(args.dir, "SB*"))
        logger.info(folderlist)
        sbidlist = [ int(folder.split('SB')[-1]) for folder in folderlist]
        sbidlist.sort()
        logger.info('Found %s SBIDs: %s', len(folderlist), sbidlist)
        args.sbids = sbidlist


    for i, sbid in enumerate(args.sbids):
        logger.debug("Processing observation SB%s (%s/%s)", sbid, i+1, len(args.sbids))
        databasic = DataBasic(sbid, args.dir)
        paths = databasic.paths
        nbeam = databasic.nbeam

        sbid_complete, num_peak, num_chisq = check_sbid_compelte(args, sbid, paths, nbeam)
        num_cand = measure_final_candidates(args, sbid, paths)
        # num_short_images = check_num_short_images(args, sbid, paths)
        text = f" peak_beams = {num_peak:<5} chisq_beams = {num_chisq:<5} final_cands = {num_cand}"
        if sbid_complete and num_peak == nbeam and num_chisq==nbeam:
            logger.info('   SB%s complete   TRUE: %s', sbid, text)
        elif sbid_complete and (num_peak > nbeam or num_chisq>nbeam):
            logger.warning(' * SB%s complete UNSURE: %s', sbid, text)
        else:
            logger.warning('** SB%s complete  FALSE: %s', sbid, text)


    end_time = time.time()
    measure_running_time(start_time, end_time)



def make_verbose(args):
    if args.verbose:
        logging.basicConfig(
            format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
            level=logging.DEBUG,
            datefmt='%Y-%m-%d %H:%M:%S')
        logger.warning("verbose mode")
    else:
        logging.basicConfig(
            format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S')
        


def check_sbid_compelte(args, sbid, paths, nbeam):
    peak_cand = glob.glob( os.path.join(paths['path_cand'], "*peak*cand.csv" ))
    logger.debug(peak_cand)
    chisq_cand = glob.glob( os.path.join(paths['path_cand'], "*chisquare*cand.csv" ))
    logger.debug(chisq_cand)

    if len(peak_cand) % nbeam != 0:
        status = False
    elif len(chisq_cand) % nbeam != 0:
        status = False
    else:
        status = True

    return status, len(peak_cand), len(chisq_cand)


def check_num_short_images(args, sbid, paths):
    short_images = glob.glob( os.path.join(paths['path_images'], "*beam00*image.fits") )
    return len(short_images)
    

def measure_final_candidates(args, sbid, paths):
    num_cand = len(glob.glob( os.path.join(paths['path_cand'], "*lightcurve*.png") ))
    return num_cand


if __name__ == '__main__':
    _main()
