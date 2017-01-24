//-
// ==========================================================================
// Copyright 2015 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk
// license agreement provided at the time of installation or download,
// or which otherwise accompanies this software in either electronic
// or hard copy form.
// ==========================================================================
//+

//
//  This example plugin demonstrates how to implement a Maya File Translator.
//  In this example, the user can create one or more nurbsSpheres, nurbsCylinders or nurbsCones.
//  The user can translate them around.
//
//  The LEP files can be referenced by Maya files.
//  
//  It is to be noted that this example was made to be simple.  Hence, there are limitations.
//  For example, every geometry saved will have its values reset to default,
//  except their translation if the option "Show Position" has been turned on.  To find what 
//  geometries we can export, we search by name, hence, if a polygon cube contains in its 
//  named the string "nurbsSphere", it will be written out as a nurbs sphere.

#include <maya/MStatus.h>
#include <maya/MObject.h>
#include <maya/MFnPlugin.h>
#include <maya/MString.h>
#include <maya/MVector.h>
#include <maya/MStringArray.h>
#include <maya/MPxFileTranslator.h>
#include <maya/MGlobal.h>
#include <maya/MItDag.h>
#include <maya/MObject.h>
#include <maya/MPlug.h>
#include <maya/MItSelectionList.h>
#include <maya/MSelectionList.h>
#include <maya/MIOStream.h>
#include <maya/MFStream.h>
#include <maya/MFileIO.h>
#include <maya/MFnTransform.h>
#include <maya/MNamespace.h>
#include <string.h>


//This is the backbone for creating a MPxFileTranslator
class OffTranslator : public MPxFileTranslator {
public:

	//Constructor
	OffTranslator() {};
	//Destructor
	virtual            ~OffTranslator() {};

	//This tells maya that the translator can read files.
	//Basically, you can import or load with your translator.
	bool haveReadMethod() const { return true; }

	//This tells maya that the translator can write files.
	//Basically, you can export or save with your translator.
	bool haveWriteMethod() const { return false; }

	//If this method returns true, and the lep file is referenced in a scene, the write method will be
	//called when a write operation is performed on the parent file.  This use is for users who wish
	//to implement a custom file referencing system.
	//For this example, we will return false as we will use Maya's file referencing system.
	bool haveReferenceMethod() const { return false; }

	//If this method returns true, it means we support namespaces.
	bool haveNamespaceSupport()    const { return true; }

	//This method is used by Maya to create instances of the translator.
	static void* creator();

	//This returns the default extension ".lep" in this case.
	MString defaultExtension() const;

	//If this method returns true it means that the translator can handle opening files 
	//as well as importing them.
	//If the method returns false then only imports are handled. The difference between 
	//an open and an import is that the scene is cleared(e.g. 'file -new') prior to an 
	//open, which may affect the behaviour of the translator.
	bool canBeOpened() const { return true; }

	//Maya will call this method to determine if our translator
	//is capable of handling this file.
	MFileKind identifyFile(const MFileObject& fileName,
		const char* buffer,
		short size) const;

	//This function is called by maya when import or open is called.
	MStatus reader(const MFileObject& file,
		const MString& optionsString,
		MPxFileTranslator::FileAccessMode mode);

	//This function is called by maya when export or save is called.
	/*MStatus writer(const MFileObject& file,
	const MString& optionsString,
	MPxFileTranslator::FileAccessMode mode);*/

private:
	//The magic string to verify it's a LEP file
	//simply "<LEP>"
	static MString const magic;
};

//Creates one instance of the LepTranslator
void* OffTranslator::creator()
{
	return new OffTranslator();
}

// Initialize our magic string
MString const OffTranslator::magic("OFF");





// An LEP file is an ascii whose first line contains the string <LEP>.
// The read does not support comments, and assumes that the each
// subsequent line of the file contains a valid MEL command that can
// be executed via the "executeCommand" method of the MGlobal class.
//
MStatus OffTranslator::reader(const MFileObject& file,
	const MString& options,
	MPxFileTranslator::FileAccessMode mode)
{

	cout << "INSIDE READER" << endl;
	const MString fname = file.fullName();

	MStatus rval(MS::kSuccess);
	const int maxLineSize = 1024;
	char buf[maxLineSize];

	ifstream inputfile(fname.asChar(), ios::in);
	if (!inputfile) {
		// open failed
		cout << fname << ": could not be opened for reading\n" << endl;
		return MS::kFailure;
	}

	if (!inputfile.getline(buf, maxLineSize)) {
		cerr << "file " << fname << " contained no lines ... aborting\n";
		return MS::kFailure;
	}

	if (0 != strncmp(buf, magic.asChar(), magic.length())) {
		cerr << "first line of file " << fname;
		cerr << " did not contain " << magic.asChar() << " ... aborting\n";
		return MS::kFailure;
	}


	char buf2[maxLineSize];

	//Traitement de la première ligne
	inputfile.getline(buf2, maxLineSize);
	MString line = buf2; 
	MStringArray tokensGen; 
	line.split(' ', tokensGen); 

	const int nb_vertices = tokensGen[0].asInt();

	const int nb_facettes = tokensGen[1].asInt();

	//Parcourir tous les vertices du file
	float vertices[100000] ;
	
	for (int i = 0; i < nb_vertices; i++) {
		inputfile.getline(buf2, maxLineSize);
		MString line = buf2;
		MStringArray tokens;
		line.split(' ', tokens);
		
		vertices[3 * i] = tokens[0].asFloat(); 
		vertices[3 * i+1] = tokens[1].asFloat();
		vertices[3 * i+2] = tokens[2].asFloat();
	}

	for (int j = 0; j < nb_facettes; j++) {
		//MString string = "polyCreateFacet -p 0.0 0.0 0.0 -p 10.0 0.0 0.0 -p 10.0 10.0 0.0;";
		inputfile.getline(buf2, maxLineSize);
		MString line = buf2;
		MStringArray tokens;
		line.split(' ', tokens);

		MString cmdString = "polyCreateFacet -p "; 
		cmdString += vertices[3*tokens[1].asInt()]; 
		cmdString += " "; 
		cmdString += vertices[3*tokens[1].asInt()+1];
		cmdString += " ";
		cmdString += vertices[3*tokens[1].asInt()+2];
		cmdString += " ";
		cmdString += "-p ";
		cmdString += vertices[3*tokens[2].asInt() +0];
		cmdString += " ";
		cmdString += vertices[3*tokens[2].asInt()+1];
		cmdString += " ";
		cmdString += vertices[3*tokens[2].asInt() +2];
		cmdString += " ";
		cmdString += "-p ";
		cmdString += vertices[3*tokens[3].asInt() +0];
		cmdString += " ";
		cmdString += vertices[3*tokens[3].asInt() +1];
		cmdString += " ";
		cmdString += vertices[3*tokens[3].asInt() +2 ];
		cmdString += " ";



		if (!MGlobal::executeCommand(cmdString))
			rval = MS::kFailure;
	}
	inputfile.close();

	return rval;
}

// Whenever Maya needs to know the preferred extension of this file format,
// it calls this method. For example, if the user tries to save a file called
// "test" using the Save As dialog, Maya will call this method and actually
// save it as "test.lep". Note that the period should *not* be included in
// the extension.
MString OffTranslator::defaultExtension() const
{
	return "off";
}


//This method is pretty simple, maya will call this function
//to make sure it is really a file from our translator.
//To make sure, we have a little magic number and we verify against it.
MPxFileTranslator::MFileKind OffTranslator::identifyFile(
	const MFileObject& fileName,
	const char* buffer,
	short size) const
{
	// Check the buffer for the "LEP" magic number, the
	// string "<LEP>\n"

	MFileKind rval = kNotMyFileType;

	if ((size >= (short)magic.length()) &&
		(0 == strncmp(buffer, magic.asChar(), magic.length())))
	{
		rval = kIsMyFileType;
	}
	return rval;
}

MStatus initializePlugin(MObject obj)
{
	MStatus   status;
	MFnPlugin plugin(obj, PLUGIN_COMPANY, "3.0", "Any");

	// Register the translator with the system
	// The last boolean in this method is very important.
	// It should be set to true if the reader method in the derived class
	// intends to issue MEL commands via the MGlobal::executeCommand 
	// method.  Setting this to true will slow down the creation of
	// new objects, but allows MEL commands other than those that are
	// part of the Maya Ascii file format to function correctly.
	status = plugin.registerFileTranslator("Off",
		"",
		OffTranslator::creator,
		"",
		"showPositions=1",
		true);
	if (!status)
	{
		status.perror("registerFileTranslator");
		return status;
	}

	return status;
}

MStatus uninitializePlugin(MObject obj)
{
	MStatus   status;
	MFnPlugin plugin(obj);

	status = plugin.deregisterFileTranslator("Off");
	if (!status)
	{
		status.perror("deregisterFileTranslator");
		return status;
	}

	return status;
}
