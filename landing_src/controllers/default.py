#!/usr/bin/env python

import os
import json

def index():
	if IsDebugMode():
		return GenerateDebugResponse()
	else:
		return GenerateNormalResponse()

def IsJsonFormat():
	return 'format' in request.vars and 'json' == request.vars['format'].lower()

def IsDebugMode():
	return 'debug' in request.vars

def GetDatasets():
	FOLDER_EXCLUSIONS = frozenset( [ 'admin', 'examples', 'welcome', 'termite' ] )
	applications_parent = request.env['applications_parent']
	applications_path = '{}/applications'.format( applications_parent )
	folders = []
	for folder in os.listdir( applications_path ):
		applications_subpath = '{}/{}'.format( applications_path, folder )
		if os.path.isdir( applications_subpath ):
			if folder not in FOLDER_EXCLUSIONS:
				folders.append( folder )
	folders = sorted( folders )
	return folders

def GenerateNormalResponse():
	data = {
		'server_type' : 'topic_models',
		'dataset_identifiers' : GetDatasets()
	}
	if IsJsonFormat():
		return json.dumps( data, encoding = 'utf-8', indent = 2, sort_keys = True )
	else:
		return data

def GenerateDebugResponse():
	def GetEnv( env ):
		data = {}
		for key in env:
			value = env[key]
			if isinstance( value, dict ) or \
			   isinstance( value, list ) or isinstance( value, tuple ) or \
			   isinstance( value, str ) or isinstance( value, unicode ) or \
			   isinstance( value, int ) or isinstance( value, long ) or isinstance( value, float ) or \
			   value is None or value is True or value is False:
				data[ key ] = value
			else:
				data[ key ] = 'N/A'
		return data

	info = {
		'env' : GetEnv( request.env ),
		'cookies' : request.cookies,
		'vars' : request.vars,
		'get_vars' : request.get_vars,
		'post_vars' : request.post_vars,
		'folder' : request.folder,
		'application' : request.application,
		'function' : request.function,
		'args' : request.args,
		'extension' : request.extension,
		'now' : str( request.now )
	}
	return json.dumps( info, encoding = 'utf-8', indent = 2, sort_keys = True )

