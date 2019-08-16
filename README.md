Multiword-Expression aware Neural Machine Translation
=====================================================

This repository contains preprocessing scripts and datasets relative to my MSc project.
The purpose is to facilitate reproduction and extension studies of our experiments
on MWE aware Neural Machine Translation.

DATASETS
--------

The train directory contains 5 subdirectories, one for each method:
	MWE_dictionary > training data for experiment 1 (sample, for copyright limitations); 
	MWE_backtrans > training data for experiment 2 (sample, for copyright limitations); 
	MWE_wordwithspaces > training data for experiment 3 (complete); 
	MWE_iob_small > training data for experiment 4 (complete); 
	MWE_iob_big > training data for experiment 5 (sample for size limitations, available upon request).

The test directory contains:
	test_ted, test_mwe, test_joint (en/it);
	test_100 (annotated), test_ted_annotated (annotated by Monti et al.).

MWE_LISTS
---------

Contains the list of MWEs extracted from the train_big dataset with the annotate_mwe.py method in the 
mwetoolkit, with frequency information (first column), 
MWE surface form (second column), length of MWE (thirds column).

SCRIPTS
-------

Contains
	process_data.py > preprocessing and postprocessing scripts for data cleaning;
	process_testset.py > scripts for preprocessing and analysis of testsets;
	process_xml.py > script for crawling and parsing the dictionaries in xml format;
	score_mwe.py > implementation of the Score_mwe metrics.