#! /usr/bin/env python
#
# png2djvu - A software to merge multiple png images to a single djvu file
#       
# Copyright (c) 2013
#	 Balasankar C <c.balasankar@gmail.com>
#
#       
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#       
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import pygtk
import gtk
import sys
import os


class Base:
	#Exit Button
	def destroy(self,widget,data=None):					
		if os.path.isdir("tmp"):
                  os.removedirs("tmp");
		sys.exit()			
	
	#Select output file
	def outputselect(self,widget):
	        dialog1=gtk.FileChooserDialog("Name Output File",None,gtk.FILE_CHOOSER_ACTION_SAVE,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
	        dialog1.set_default_response(gtk.RESPONSE_OK)
	        filter = gtk.FileFilter()
               	filter.set_name("djvu Files")										
               	filter.add_pattern("*.djvu")
        	dialog1.add_filter(filter)
		response = dialog1.run()
		self.outputfilename=dialog1.get_filename()
		dialog1.destroy()
		
	#Selecting input files	
	def selectfile(self,widget):
	        dialog=gtk.FileChooserDialog("Select Input Files",None,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
	        dialog.set_default_response(gtk.RESPONSE_OK)
	        dialog.set_select_multiple(True)
        	filter = gtk.FileFilter()
        	filter.set_name("png Files")									
        	filter.add_pattern("*.png")
        	dialog.add_filter(filter)
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			self.filelist = dialog.get_filenames()		
		dialog.destroy()	
	
        #Converting png files to individual pdf files		
	def convert(self,widget):										
		flag=1
		if not os.path.isdir("tmp"):
		  print"creating tmp folder"
		  os.makedirs("tmp");
		j=100
		for p in self.filelist:		
			print p
			cmnd = "convert \""+p+"\" tmp/"+str(j)+"_temp.pdf "
			flag=os.system(cmnd)
			j=j+1
		md1= gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE, "Error while creating pdf")
		if flag!=0:
			md1.run()
			md1.destroy()
			return
                #Merging pdf files to a single pdf files
                md1= gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE, "Error while merging pdf")
		cmnd2="pdftk tmp/*.pdf cat output tmp/file_merged.pdf"		
		flag=os.system(cmnd2)
		if flag!=0:
			md1.run()
			md1.destroy()
			return
                #Converting pdf file to djvu file
                md1= gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE, "Error while creating djvu")			
		cmnd3="pdf2djvu -o "+self.outputfilename+".djvu tmp/file_merged.pdf"		
		flag=os.system(cmnd3)
		if flag!=0:
			md1.run()
			md1.destroy()
			return
		j=100
		for p in self.filelist:
                        #Removing unwanted individual pdf files
                        md1= gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE, "Error while removing pdfs")
			cmnd4="rm tmp/"+str(j)+"_temp.pdf"						
			flag=os.system(cmnd4)
			j=j+1
		if flag!=0:
			md1.run()
			md1.destroy()
			return
		cmnd5="rm tmp/file_merged.pdf"									
		#Removing  unwanted merged pdf file
		flag=os.system(cmnd5)
		#Removing temp directory
		cmnd6 = "rmdir tmp"		
		if os.path.isdir("tmp"):
		  flag=os.system(cmnd6)
		if flag!=0:
			md1.run()
			md1.destroy()
			return
		md = gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,gtk.BUTTONS_CLOSE, "Successfully Converted")
		md.run()		
		#Displaying successful message
		md.destroy()
		
	def __init__(self):
	        #Main function
		self.flag=0
		self.window = gtk.Window()
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.windowx,self.windowy = self.window.get_position()
		self.windowheight,self.windowwidth = self.window.get_size()		
		self.window.show()
		self.fixed = gtk.Fixed()
		self.window.connect("destroy",self.destroy)
		self.button4=gtk.Button("Exit")
		self.button1 = gtk.Button("Open")
		self.button3 = gtk.Button("Convert")
		self.button2 = gtk.Button("Choose Output File")
		self.button3.connect("clicked",self.convert)		
		self.button4.connect("clicked",self.destroy)		
		self.button1.connect("clicked",self.selectfile)
		self.button2.connect("clicked",self.outputselect)
		self.button3.set_size_request(150,50)				
		self.button1.set_size_request(150,50)	
		self.button2.set_size_request(150,50)	
		self.button4.set_size_request(150,50)	
		self.fixed.put(self.button1,30,30)
		self.fixed.put(self.button2,30,100)
		self.fixed.put(self.button4,30,240)		
		self.fixed.put(self.button3,30,170)
		self.filelist=""
		self.window.add(self.fixed)
		self.window.show_all()
	def main(self):
		gtk.main()
	
if __name__ == "__main__":
	base= Base()
	base.main()

