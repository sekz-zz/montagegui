#!/usr/bin/env python

/* montagegui.py -- a simple gui for Imagemagick montage command line tool.

   Copyright 2012 Seksan Poltree <seksan.poltree@gmail.com>.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

import pygtk
pygtk.require('2.0')
import gtk

import shlex, subprocess

class MontageGUI:


	def generate(self, widget, data=None):
		filenames = ""
		for item in self.chooser.get_filenames(): filenames = filenames + ' "' + item + '"'

		command_line = "/usr/bin/montage -mode concatenate -quality " + self.quality.get_text() + " -tile " + self.tile.get_text() + "x " + filenames +" -frame 1 -resize "+ str( ( int(self.maxwidth.get_text()) / int(self.tile.get_text()) ) )+ " -title \"" + self.title.get_text()+"\" out.jpg"
		print command_line
		args = shlex.split(command_line)
		p = subprocess.Popen(args)

	def choose(self, widget, data=None):
		self.chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		self.chooser.set_current_folder(".")
		self.chooser.set_select_multiple(True)
		self.chooser.set_default_response(gtk.RESPONSE_OK)

		filter = gtk.FileFilter()
		filter.set_name("Images")
		filter.add_mime_type("image/png")
		filter.add_mime_type("image/jpeg")
		filter.add_mime_type("image/gif")
		filter.add_pattern("*.png")
		filter.add_pattern("*.jpg")
		filter.add_pattern("*.gif")
		self.chooser.add_filter(filter)

		response = self.chooser.run()
		if response == gtk.RESPONSE_OK:
			filenames = self.chooser.get_filenames()
			names = ""
			for f in filenames:
				names = names + f + '\n'
			self.selected_files.set_text(names)
		elif response == gtk.RESPONSE_CANCEL:
			print 'Closed, no files selected'

		self.chooser.hide()

	def delete_event(self, widget, event, data=None):
		return False

	def destroy(self, widget, data=None):
		gtk.main_quit()

	def __init__(self):
		# create a new window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title("Imagemagick Montage GUI")
		self.window.set_border_width(10)
		self.window.set_default_size(500, 350)

		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)

		vbox = gtk.VBox(False, 5)
		self.window.add(vbox)

		top_hbox = gtk.HBox(False,5)
		top_vbox = gtk.VBox(True,3)

		hbox1 = gtk.HBox(False, 0)
		self.maxwidth = gtk.Entry()
		self.maxwidth.set_text("900")
		hbox1.add(gtk.Label("Max Output Width (px) : "))
		hbox1.add(self.maxwidth)

		hbox2 = gtk.HBox(False, 0)
		self.tile = gtk.Entry()
		self.tile.set_text("2")
		hbox2.add(gtk.Label("Tile Column (x) : "))
		hbox2.add(self.tile)

		hbox3 = gtk.HBox(False, 0)
		self.quality = gtk.Entry()
		self.quality.set_text("85")
		hbox3.add(gtk.Label("Output quality (%) : "))
		hbox3.add(self.quality)


		frame = gtk.Frame("Selected File")
		frame.set_size_request(350, 300)
		self.selected_files = gtk.Label("")
		self.selected_files.set_justify(gtk.JUSTIFY_LEFT)
		scroller = gtk.ScrolledWindow()
		scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		scroller.add_with_viewport(self.selected_files)
		frame.add(scroller)


		self.gen_button = gtk.Button("Generate")
		self.gen_button.set_size_request(70, 30)
		self.gen_button.connect("clicked", self.generate, None)
		valign1 = gtk.Alignment(1, 0, 0, 0)
		valign1.add(self.gen_button)

		self.choose_button = gtk.Button("Browse")
		self.choose_button.set_size_request(70, 30)
		self.choose_button.connect("clicked", self.choose, None)
		valign2 = gtk.Alignment(1, 0, 0, 0)
		valign2.add(self.choose_button)

		frame_hbox = gtk.HBox(False, 0)
		frame_hbox.add(frame)
		frame_hbox.add(valign2)

		hbox5 = gtk.HBox(False, 0)
		self.title = gtk.Entry()
		self.title.set_text("")
		hbox5.add(gtk.Label("Title of Image : "))
		hbox5.add(self.title)


		# This packs the button into the window (a GTK container).
		
		top_vbox.add(hbox5)
		top_vbox.add(hbox1)
		top_vbox.add(hbox2)
		top_vbox.add(hbox3)

		top_hbox.add(top_vbox)
		top_hbox.add(valign1)

		
		vbox.add(top_hbox)
		vbox.add(frame_hbox)

		# and the window
		self.window.show_all()

	def main(self):
		gtk.main()

if __name__ == "__main__":
	gui = MontageGUI()
	gui.main()
