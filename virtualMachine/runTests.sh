#!/bin/bash

for testcase in *_UT.py
do
	python $testcase
done