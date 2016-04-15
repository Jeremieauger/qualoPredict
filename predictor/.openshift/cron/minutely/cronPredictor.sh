#!/bin/bash

if [ ! -f $OPENSHIFT_DATA_DIR/last_run ]; then
	touch $OPENSHIFT_DATA_DIR/last_run
fi

if [[ $(find $OPENSHIFT_DATA_DIR/last_run -mmin +29) ]]; then #run every 30 mins
	rm -f $OPENSHIFT_DATA_DIR/last_run
	touch $OPENSHIFT_DATA_DIR/last_run
	python $OPENSHIFT_REPO_DIR/python/predictor.py > $OPENSHIFT_DATA_DIR/predictor.log 2>&1
	python $OPENSHIFT_REPO_DIR/python/rainAndTemp.py > $OPENSHIFT_DATA_DIR/rainAndTemp.log 2>&1
	python $OPENSHIFT_REPO_DIR/python/flowAndLevel.py >> $OPENSHIFT_DATA_DIR/flowAndLevel.log 2>&1
	echo $(date) >> $OPENSHIFT_DATA_DIR/timeOfRuns.log
fi

