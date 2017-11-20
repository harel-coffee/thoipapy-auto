#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author:         BO ZENG
Created:        Monday December 12 12:33:08 2016
Operation system required: Linux (currently not available for windows)
Dependencies:   Python 3.5
                numpy
                Bio
                freecontact (currently only availble in linux)
                pandas
Purpose:        Self-interacting single-pass membrane protein interface residues prediction
Credits:        All sections by Bo Zeng.
Further Details:

"""

import argparse
import os
import thoipapy
from thoipapy import common
import csv

# read the command line arguments
parser = argparse.ArgumentParser()
# add only a single argument, the path to the settings file.
parser.add_argument("-s",  # "-settingsfile",
                    help=r'Full path to your excel settings file.'
                         r'E.g. "\Path\to\your\settingsfile.xlsx"')
parser.add_argument("-i",  # "-setting input fasta file location",
                    help=r'Full path to your input file.'
                         r'E.g. "\Path\to\your\input.fasta"')
parser.add_argument("-tmd",  # "-setting input fasta file location",
                    help=r'Full path to your input file contain the tmd sequence.'
                         r'E.g. "\Path\to\your\P01908_tmd.txt"')
parser.add_argument("-ts",  # "-setting tm start",
                    help=r'integere tm start value'
                         r'E.g. "219"')
parser.add_argument("-te",  # "-setting tm end ",
                    help=r'integer tm end value.'
                         r'E.g. "231"')
parser.add_argument("-of",  # "-setting output file path",
                    help=r'Full path to your prediction output file.'
                         r'E.g. "\Path\to\your output_file\"')
parser.add_argument("-email_to",  # "-setting output file location",
                    help=r'user email given on web server'
                         r'E.g. "***REMOVED***"')
if __name__ == "__main__":

    print('\nRun thoipapy as follows:')
    print(r'python \Path\to\run.py -s \Path\to\your\settingsfile.xlsx -i \Path\to\your\input.fasta -tmd \Path\to\your\input_tmd.txt '
          r'-ts tm_start_position -te tm_end_position -of C:\Path\to\your output_file\ -email_to email_address')

    # get the command-line arguments
    args = parser.parse_args()
    # args.s is the excel_settings_file input by the user
    set_=common.create_settingdict(args.s)
    if args.of:
        output_file_loc=os.path.join(args.of,"output.csv")
        output_parse_file=os.path.join(args.of,"output_parse.csv")
        output_png_loc=os.path.join(args.of,"outp.png")
    tm_protein_name=set_["tm_protein_name"]
    Data_type=set_["Datatype"]

    logging=common.setup_keyboard_interrupt_and_error_logging(set_,tm_protein_name)

    tmp_lists=thoipapy.proteins.get_tmp_lists.extract_tmps_from_input_file(set_)
    test_tmp_lists=thoipapy.proteins.get_tmp_lists.extract_test_tmps_from_input_file(set_)
    set_["tm_protein_name"]='input'
    set_["input_fasta_file"]=args.i
    set_["input_tmd_file"]=args.tmd
    set_["tm_start"]=args.ts
    set_["tm_end"]=args.te
    set_["email_to"]=args.email_to
    set_["tm_len"]=thoipapy.common.calculate_fasta_file_length(set_)

    if args.tmd is not None:
       set_["tm_start"],set_["tm_end"] = common.tmd_positions_match_fasta(set_)

    if not set_["multiple_tmp_simultaneous"]:
        query_protein_tmd_file = os.path.join(set_["Protein_folder"], "Query_Protein_Tmd.csv")
        query_protein_tmd_file_handle=open(query_protein_tmd_file,"w")
        writer = csv.writer(query_protein_tmd_file_handle, delimiter=',', quoting = csv.QUOTE_NONE,lineterminator='\n')
        writer.writerow(["Protein","TMD_Length","TMD_Start","TMD_End"])
        writer.writerow([set_["tm_protein_name"],set_["tm_len"],set_["tm_start"],set_["tm_end"]])
        query_protein_tmd_file_handle.close()
        set_["list_of_tmd_start_end"]=query_protein_tmd_file

    thoipapy.common.create_TMD_surround20_fasta_file(set_)

    ###################################################################################################
    #                                                                                                 #
    #                   homologous download with hhblits                                              #
    #                                                                                                 #
    ###################################################################################################


    if set_["run_retrieve_homologous_with_hhblits"]:
        #thoipapy.hhblits.download.download_homologous_with_hhblits(set_, logging)

        thoipapy.hhblits.download.parse_a3m_alignment( set_, logging)

        ###################################################################################################
        #                                                                                                 #
        #                   homologous download from NCBI                                                 #
        #                                                                                                 #
        ###################################################################################################


    if set_["run_retrieve_NCBI_homologous_with_blastp"]:
        thoipapy.NCBI_BLAST.download.download.download_homologous_from_ncbi(set_, logging)


        ###################################################################################################
        #                                                                                                 #
        #                   convert homologous xml file to csv                                            #
        #                                                                                                 #
        ###################################################################################################


    if set_["run_parse_homologous_xml_into_csv"]:
        thoipapy.NCBI_BLAST.parse.parser.parse_NCBI_xml_to_csv(set_,logging)

    if set_["parse_csv_homologous_to_alignment"]:
        thoipapy.NCBI_BLAST.parse.parser.extract_filtered_csv_homologous_to_alignments(set_,logging)


        ###################################################################################################
        #                                                                                                 #
        #                   Random Forest feature calculation                                             #
        #                                                                                                 #
        ###################################################################################################


    if set_["RandomForest_feature_calculation"]:

        #thoipapy.RF_features.feature_calculate.mem_a3m_homologous_filter(set_, logging)

        if set_["pssm_feature_calculation"]:
            thoipapy.RF_features.feature_calculate.pssm_calculation(set_,logging)

        if set_["entropy_feature_calculation"]:
            thoipapy.RF_features.feature_calculate.entropy_calculation(set_, logging)

        if set_["cumulative_coevolution_feature_calculation"]:
            #thoipapy.RF_features.feature_calculate.coevoluton_calculation_with_freecontact(set_, logging)
            thoipapy.RF_features.feature_calculate.cumulative_co_evolutionary_strength_parser(tmp_lists, tm_protein_name,thoipapy ,set_, logging)


        if set_["lips_score_feature_calculation"]:
            thoipapy.RF_features.feature_calculate.Lips_score_calculation(tmp_lists,tm_protein_name, thoipapy, set_, logging)
            thoipapy.RF_features.feature_calculate.Lips_score_parsing( set_, logging)

        #thoipapy.RF_features.feature_calculate.convert_bind_data_to_csv(set_, logging)

        if set_["combine_feature_into_train_data"]:
            #thoipapy.RF_features.feature_calculate.features_combine_to_traindata( set_, logging)
            #thoipapy.RF_features.feature_calculate.adding_physical_parameters_to_train_data( set_, logging)
            #thoipapy.RF_features.feature_calculate.features_combine_to_testdata( set_, logging)
            #thoipapy.RF_features.feature_calculate.adding_physical_parameters_to_test_data(set_, logging)
            thoipapy.RF_features.feature_calculate.combine_all_train_data_for_random_forest(set_,logging)

    if set_["run_random_forest"]:
        #thoipapy.RF_features.RF_Train_Test.RF_10flod_cross_validation(tmp_lists,thoipapy,set_,logging)
        thoipapy.RF_features.RF_Train_Test.run_Rscipt_random_forest(tmp_lists, thoipapy, set_, output_file_loc,logging)

    if set_["parse_prediciton_output"]:
        thoipapy.RF_features.Output_Parse.parse_Predicted_Output(thoipapy,set_,output_file_loc,output_parse_file,logging)

    if set_["Send_sine_curve_to_email"]:
        print('begining to run run sine curve fitting')
        thoipapy.Sine_Curve.SineCurveFit.Save_Sine_Curve_Result(set_,output_file_loc,output_png_loc)
        logging.info('the fitting of sine curve is done')

            ###################################################################################################
            #                                                                                                 #
            #                  Bind residues calculation for train data                                       #
            #                                                                                                 #
            ###################################################################################################


    if set_["Atom_Close_Dist"]:
        infor=thoipapy.Atom_Dist.Residu_Closest_Dist.homodimer_residue_closedist_calculate_from_complex(thoipapy, set_, logging)
        print(infor)

    if set_["Send_email_finished"]:
        thoipapy.Send_Email.Send_Email_Smtp.send_email_when_finished(set_, thoipapy,output_parse_file,output_png_loc)
