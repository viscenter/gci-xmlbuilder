from Tkinter import *                   #import library that enables the creation of the GUI
#from ttk import *
from tkFileDialog import *              #import library to be able to ask file name by dialog box
import tkMessageBox                     #import library that facilitates the creation of dialop pop-up boxes
import csv                              #import library that faciliates reading and writting csv files
import xml.etree.cElementTree as ET     #import library that facilitates writting xml files
from xml.dom import minidom             
import os
import os.path
import re

tree_columns = ("country", "capital", "currency")

class App:

    def __init__(self, master):
        
        self.RootWindow = master
        
        (self.RootWindow).configure(borderwidth=20)
        
        self.answer = StringVar()
        
        self.itemList = []
        self.indexList = []
        self.subitemList = []
        
        self.leindex = IntVar()
        self.olditemID = StringVar()
        
        self.openxmlfile = StringVar(self.RootWindow)
        (self.openxmlfile).set("Untitled")
        Label(self.RootWindow, textvariable=self.openxmlfile).grid(row=0, column=1, sticky=N+E+W+S)
        
        self.openxmlfile_path = StringVar(self.RootWindow)
        
        self.listbox = Listbox(self.RootWindow, width=125, height=35, selectmode=MULTIPLE)
        (self.listbox).grid(row=1, column=0, columnspan=3, sticky=N+E+W+S)
        
        #container = Frame()
        #container.grid(row=1, column=0, columnspan=3, sticky=N+E+W+S)
        #
        ## XXX Sounds like a good support class would be one for constructing
        ##     a treeview with scrollbars.
        #self.tree = Treeview(columns=tree_columns, show="headings")
        #vsb = Scrollbar(orient="vertical", command=self.tree.yview)
        #hsb = Scrollbar(orient="horizontal", command=self.tree.xview)
        #self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        #self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        #vsb.grid(column=1, row=0, sticky='ns', in_=container)
        #hsb.grid(column=0, row=1, sticky='ew', in_=container)
        #
        #container.grid_columnconfigure(0, weight=1)
        #container.grid_rowconfigure(0, weight=1)
        
        
        #left corner buttons
        
        self.item_frame = Frame(self.RootWindow)
        (self.item_frame).grid(row=2, column=0, sticky=W)

        self.add_el = Button(self.item_frame, text="+", command=lambda: self.addElmClick("add"))
        (self.add_el).focus_force()
        (self.add_el).grid(row=0, column=0, sticky=W)
        
        self.delete_el = Button(self.item_frame, text="-", command=self.deleteElmClick)
        (self.delete_el).grid(row=0, column=1, sticky=W)
        
        self.edit_info = Button(self.item_frame, text="Edit", command=lambda: self.addElmClick("edit"))
        (self.edit_info).grid(row=0, column=2, sticky=W)
        
        self.import_info = Button(self.item_frame, text="Import", command=lambda: self.openInfoClick("import"))
        (self.import_info).grid(row=0, column=3, sticky=W)
        
        #middle buttons
        
        self.duplicate_frame = Frame(self.RootWindow)
        self.duplicate_frame.grid(row=2, column=1, sticky=E)
        
        #self.replace will store the value of the radio button selection, or 0 if user decides to do nothing when a duplicate on import appears. 0 means "do nothing", 1 means "replace one", and 2 means "replace all"
        self.replace = IntVar()
        (self.replace).set(1)
        Radiobutton(self.duplicate_frame, text="replace one at a time", variable=self.replace, value=0).grid(row=0, column=0, sticky=E)
        Radiobutton(self.duplicate_frame, text="replace all", variable=self.replace, value=1).grid(row=0, column=1, sticky=E)
        
        #right corner buttons

        self.save_frame = Frame(self.RootWindow)
        (self.save_frame).grid(row=2, column=2, sticky=E)
        
        self.open_info = Button(self.save_frame, text="New", command= self.newClick)
        (self.open_info).grid(row=0, column=0, sticky=W)
        
        self.open_info = Button(self.save_frame, text="Open", command=lambda: self.openInfoClick("open"))
        (self.open_info).grid(row=0, column=1, sticky=W)
        
        self.save_info = Button(self.save_frame, text="Save", command=lambda: self.saveClick("overwrite"))
        (self.save_info).grid(row=0, column=2, sticky=W)
        
        self.save_as_info = Button(self.save_frame, text="Save As...", command=lambda: self.saveClick("write")) #export information to xml file
        (self.save_as_info).grid(row=0, column=3, sticky=W)


    def newClick(self):
        
        if len(self.itemList) > 0:
        
            #self.newwin = Toplevel()
            #(self.newwin).title('WARNING')
            #(self.newwin).configure(borderwidth=20)
            #(self.newwin).resizable(width=FALSE, height=FALSE)
            #
            #message = "This operation will delete all the existing items. Are you sure you want to continue?"
            #Label(self.newwin, text=message).grid(row=0, rowspan=3, column=1, columnspan=2, sticky=W)
            #Button(self.newwin, text='Yes', command= self.newContinued).grid(row=3, column=1, sticky=E)
            #Button(self.newwin, text='No', command=lambda: (self.newwin).destroy()).grid(row=3, column=2, sticky=W)
            #
            #(self.newwin).mainloop()
            ##(self.newwin).destroy
            
            result = tkMessageBox.askquestion("warning", "This operation will delete all the existing items. Are you sure you want to continue?", icon='warning')
            
            if result == 'yes':
                
                self.itemList = []
                self.subitemList = []
                (self.listbox).delete(0, END)
                
                (self.openxmlfile_path).set("")
                (self.openxmlfile).set("Untitled")
            
        else:
            
            (self.openxmlfile_path).set("")
            (self.openxmlfile).set("Untitled")

    
    def getFilePath(self):
        
        if (self.item_type.get()) == "collection":
            filename = askdirectory(title='please select a directory')              
        else:
            filename = askopenfilename(title='please select a file')          
        
        (self.item_file).delete(0, END)
        (self.item_file).insert(END, filename)      
        
        
    def onTypeChange(self, *args):
        
        #reset google path and transcript labels to be black
        
        (self.item_googlePath_label).configure(foreground = "black")
        (self.item_transcript_label).configure(foreground = "black")
        
        letype = self.item_type.get()
        
        if letype == "video":
            
            #change file path label to "youtube id"
            
            (self.filepathlabel).set("Youtube ID #:")
            
            #disable google cs path entry 
            
            (self.item_googlePath).configure(state='disabled')
            
            #set google path label to be grey
            
            (self.item_googlePath_label).configure(foreground = "grey")
            
        elif letype == "collection":
            
            #change file path label to "collection path"
            
            (self.filepathlabel).set("Collection Path:")
            
            #disable transcript entry 
            
            (self.item_transcript).configure(state='disabled')
            
            #set transcript label to be grey
            
            (self.item_transcript_label).configure(foreground = "grey")
        
        
    def addElmClick(self, order):
        
        if order == "edit":
        
            selected = (self.listbox).curselection()
            
            if len(selected) != 1:
                
                return
        
        self.AddItemWindow = Tk()
        
        (self.AddItemWindow).title("Add Item...")
        
        #(self.AddItemWindow).configure(background='grey')
        
        (self.AddItemWindow).configure(borderwidth=20)
        
        (self.AddItemWindow).resizable(width=FALSE, height=FALSE)
        
        ###
        #left side
        ###
        
        #create left container
        
        self.left_frame = Frame(self.AddItemWindow)
        self.left_frame.grid(row=0, column=0, sticky=W)
        
        #keep a count of rows
        
        lerow = 0
        
        #create item type label
        
        item_type_label = Label(self.left_frame, text = "Type:", justify=LEFT)
        item_type_label.grid(row=lerow, column=0, sticky=W)

        #create item 'file' label
        
        self.filepathlabel = StringVar(self.left_frame)
        (self.filepathlabel).set("File Path:")
        item_file_label = Label(self.left_frame, textvariable = self.filepathlabel, justify=LEFT)
        item_file_label.grid(row=lerow, column=1, sticky=W)
        
        lerow += 1
        
        #create item type option menu
        
        self.item_type = StringVar(self.left_frame)
        (self.item_type).set("image") # default value
        
        self.option_menu = OptionMenu(self.left_frame, self.item_type, "image", "collection", "video")
        self.option_menu.grid(row=lerow, column=0, sticky=W)
        
        #self.option_menu.bind("<<MenuSelect>>", self.onTypeChange)
        
        (self.item_type).trace("w", self.onTypeChange)
        
        #create item file entry widget
        
        self.item_file = Entry(self.left_frame, width=20)
        self.item_file.grid(row=lerow, column=1, columnspan=2, sticky=W)
        
        #create item file browse button
        
        filebutton = Button(self.left_frame, text='Browse', command=self.getFilePath)
        filebutton.grid(row=lerow, column=1, columnspan=2, sticky=E)
        
        lerow += 1
        
        #create google CS path label
        
        self.item_googlePath_label = Label(self.left_frame, text = "Google CS Path:", justify=LEFT)
        self.item_googlePath_label.grid(row=lerow, column=0, columnspan=2, sticky=W)
        
        lerow += 1
        
        #create google CS path entry widget
        
        self.item_googlePath = Entry(self.left_frame, width=60)
        self.item_googlePath.grid(row=lerow, column=0, columnspan=2, sticky=W)
        
        lerow += 1
        
        #create item title label
        
        item_title_label = Label(self.left_frame, text = "Title:", justify=LEFT)
        item_title_label.grid(row=lerow, column=0, columnspan=2, sticky=W)
        
        lerow += 1
        
        #create title entry widget
        
        self.item_title = Entry(self.left_frame, width=60)
        self.item_title.grid(row=lerow, column=0, columnspan=2, sticky=W)
        
        lerow += 1
        
        #create item description label
        
        item_description_label = Label(self.left_frame, text = "Description:", justify=LEFT)
        item_description_label.grid(row=lerow, column=0, columnspan=2, sticky=W)
        
        lerow += 1
        
        #create item description entry widget
        
        self.item_description = Text(self.left_frame, wrap=WORD, width=69, height=5, borderwidth=2, relief=SUNKEN)
        self.item_description.grid(row=lerow, rowspan=2, columnspan=2, sticky=W)
        
        lerow += 2
          
        self.YesNo = IntVar()  
        self.checkBox = Checkbutton(self.left_frame, text="Auto-generate folio description for subitems?", variable=self.YesNo, onvalue=1, offvalue=0)
        self.checkBox.grid(row=lerow, column=0, columnspan=2, sticky=W)

        lerow += 1
        
        #create item transcript label
        
        self.item_transcript_label = Label(self.left_frame, text = "Transcript:", justify=LEFT)
        self.item_transcript_label.grid(row=lerow, column=0, columnspan=2, sticky=W)
        
        lerow += 1
        
        #create item transcript entry widget
        
        self.item_transcript = Text(self.left_frame, wrap=WORD, width=69, height=5, borderwidth=2, relief=SUNKEN)
        self.item_transcript.grid(row=lerow, rowspan=2, column=0, columnspan=2, sticky=W)
        
        lerow +=2
        
        #create item disclaimer label
        
        item_disclamer_label = Label(self.left_frame, text = "Disclaimer:", justify=LEFT)
        item_disclamer_label.grid(row=lerow, column=0, columnspan=2, sticky=W)
        
        lerow += 1
        
        #create item disclamer entry widget
        
        self.item_disclaimer = Text(self.left_frame, wrap=WORD, width=69, height=5, borderwidth=2, relief=SUNKEN)
        self.item_disclaimer.grid(row=lerow, rowspan=2, column=0, columnspan=2, sticky=W)
        
        lerow +=2
        
        #create item 'Original Source' label
        
        item_originalSource_label = Label(self.left_frame, text = "Original Source:", justify=LEFT)
        item_originalSource_label.grid(row=lerow, column=0, sticky=W)
        
        #create item 'original source URL' label
        
        item_oriURL_label = Label(self.left_frame, text = "URL:", justify=LEFT)
        item_oriURL_label.grid(row=lerow, column=1, sticky=W)
        
        lerow += 1
        
        #create item original source entry widget
        
        self.item_originalSource = Entry(self.left_frame, width=30)
        self.item_originalSource.grid(row=lerow, column=0, sticky=W)
     
        #create item URL entry widget
        
        self.item_oriURL = Entry(self.left_frame, width=30)
        self.item_oriURL.grid(row=lerow, column=1, sticky=W)
        
        lerow += 1
        
        #create item 'license' label
        
        item_license_label = Label(self.left_frame, text = "License:", justify=LEFT)
        item_license_label.grid(row=lerow, column=0, sticky=W)
        
        #create item 'license URL' label
        
        item_liURL_label = Label(self.left_frame, text = "URL:", justify=LEFT)
        item_liURL_label.grid(row=lerow, column=1, sticky=W)
        
        lerow += 1
        
        #create item license entry widget
        
        self.item_license = Entry(self.left_frame, width=30)
        self.item_license.grid(row=lerow, column=0, sticky=W)
        
        #create item URL entry widget
        
        self.item_liURL = Entry(self.left_frame, width=30)
        self.item_liURL.grid(row=lerow, column=1, sticky=W)
        
        lerow += 1
        
        #create item 'copyright' label
        
        item_copyright_label = Label(self.left_frame, text = "Copyright:", justify=LEFT)
        item_copyright_label.grid(row=lerow, column=0, sticky=W)
        
        #create item permission label
        
        item_permission_label = Label(self.left_frame, text = "Permission/Usage:", justify=LEFT)
        item_permission_label.grid(row=lerow, column=1, sticky=W)
        
        lerow += 1
        
        #create item copyright entry widget
        
        self.item_copyright = Entry(self.left_frame, width=30)
        self.item_copyright.grid(row=lerow, column=0, sticky=W)
        
        #create item permission entry widget
        
        self.item_permission = Entry(self.left_frame, width=30)
        self.item_permission.grid(row=lerow, column=1, sticky=W)
        
        lerow += 1

        #create empty labels for spacing
        
        #empty_label1 = Label(self.left_frame, text = "")
        #empty_label1.grid(row=lerow, column=0, columnspan=2, sticky=W)
        
        #lerow += 1
        
        #empty_label2 = Label(self.left_frame, text = "")
        #empty_label2.grid(row=lerow, column=0, columnspan=2, sticky=W)
        
        #lerow += 1
        
        #create import button
        
        self.import_csv= Button(self.left_frame, text="Import CSV", command=self.importCSVClick)
        self.import_csv.grid(row=lerow, column=0, sticky=W)
        
        ###
        #right side
        ###
        
        #create right container
        
        self.right_frame = Frame(self.AddItemWindow)
        self.right_frame.grid(row=0, column=1, sticky=W)
        
        lerow = 0
        
        #create google id label
        
        item_googleID_label = Label(self.right_frame, text = "Google Item ID:", justify=LEFT)
        item_googleID_label.grid(row=lerow, column=0, sticky=W)
        
        lerow += 1
        
        #create google id entry widget
        
        self.item_googleID = Entry(self.right_frame, width=60)
        self.item_googleID.grid(row=lerow, column=0, sticky=W)
        
        lerow += 1
        
        #type, language, format frame
        
        self.TLF_frame = Frame(self.right_frame)
        self.TLF_frame.grid(row=lerow, column=0, sticky=W)
        
        #create file type label
        
        item_fileType_label = Label(self.TLF_frame, text = "Type:", justify=LEFT)
        item_fileType_label.grid(row=0, column=0, sticky=W)
        
        #create file type entry widget
        
        self.item_fileType = Entry(self.TLF_frame, width=20)
        self.item_fileType.grid(row=1, column=0, sticky=W)
        
        #empty space between filetype and language
        
        empty_label1 = Label(self.TLF_frame, text = "        ")
        empty_label1.grid(row=0, column=1, sticky=W)
    
        empty_label1 = Label(self.TLF_frame, text = "        ")
        empty_label1.grid(row=1, column=1, sticky=W)
        
        #create language label
        
        item_language_label = Label(self.TLF_frame, text = "Language:", justify=LEFT)
        item_language_label.grid(row=0, column=2, sticky=N+S+W+E)
        
        #create language option menu widget
        
        self.item_language = StringVar(self.TLF_frame)
        (self.item_language).set("en") # default value
        
        self.option_menu2 = OptionMenu(self.TLF_frame, self.item_language, "en", "la", "af", "sq", "ar", "az", "eu", "bn", "be", "bg", "ca", "zh-CN", "zh-TW", "hr", "cs", "da", "nl", "eo", "et", "tl", "fi", "fr", "gl", "ka", "de", "el", "gu", "ht", "iw", "hi", "hu", "is", "id", "ga", "it", "ja", "kn", "ko", "lv", "lt", "mk", "ms", "mt", "no", "fa", "pl", "pt", "ro", "ru", "sr", "sk", "sl", "es", "sw", "sv", "ta", "te", "th", "tr", "uk", "ur", "vi", "cy", "yi")
        (self.option_menu2).config(width=1) #not resizing
        self.option_menu2.grid(row=1, column=2, sticky=N+S+W+E)
        
        #empty space between language and format
        
        empty_label1 = Label(self.TLF_frame, text = "       ")
        empty_label1.grid(row=0, column=3, sticky=W)
        
        empty_label1 = Label(self.TLF_frame, text = "       ")
        empty_label1.grid(row=1, column=3, sticky=W)
        
        #create format label
        
        item_format_label = Label(self.TLF_frame, text = "Format:", justify=LEFT)
        item_format_label.grid(row=0, column=4, sticky=W)
        
        #create format entry widget
        
        self.item_format = Entry(self.TLF_frame, width=20)
        self.item_format.grid(row=1, column=4, sticky=W)
        
        lerow += 1
        
        #provenance, subject, creator frame
        
        self.PSC_frame = Frame(self.right_frame)
        self.PSC_frame.grid(row=lerow, column=0, sticky=W)
        
        #create provenance label
        
        item_provenance_label = Label(self.PSC_frame, text = "Provenance:", justify=LEFT)
        item_provenance_label.grid(row=0, column=0, sticky=W)
        
        #create provenance entry widget
        
        self.item_provenance = Entry(self.PSC_frame, width=19)
        self.item_provenance.grid(row=1, column=0, sticky=W)
        
        #create subject label
        
        item_subject_label = Label(self.PSC_frame, text = "Subject:", justify=LEFT)
        item_subject_label.grid(row=0, column=1, sticky=W)
        
        #create subject entry widget
        
        self.item_subject = Entry(self.PSC_frame, width=19)
        self.item_subject.grid(row=1, column=1, sticky=W)
        
        #create creator label
        
        item_creator_label = Label(self.PSC_frame, text = "Creator:", justify=LEFT)
        item_creator_label.grid(row=0, column=2, sticky=W)
        
        #create creator entry widget
        
        self.item_creator = Entry(self.PSC_frame, width=19)
        self.item_creator.grid(row=1, column=2, sticky=W)
        
        lerow += 1
        
        #contributor, publisher frame
        
        self.CP_frame = Frame(self.right_frame)
        self.CP_frame.grid(row=lerow, column=0, sticky=W)
        
        #create contributor label
        
        item_contributor_label = Label(self.CP_frame, text = "Contributor:", justify=LEFT)
        item_contributor_label.grid(row=0, column=0, sticky=W)
        
        #create contributor entry widget
        
        self.item_contributor = Entry(self.CP_frame, width=27)
        self.item_contributor.grid(row=1, column=0, sticky=W)
        
        #empty space between contributor and publisher
        
        empty_label1 = Label(self.CP_frame, text = "       ")
        empty_label1.grid(row=0, column=1, sticky=W)
        
        empty_label1 = Label(self.CP_frame, text = "       ")
        empty_label1.grid(row=1, column=1, sticky=W)
        
        #create publisher label
        
        item_publisher_label = Label(self.CP_frame, text = "Publisher:", justify=LEFT)
        item_publisher_label.grid(row=0, column=2, sticky=W)
        
        #create publisher entry widget
        
        self.item_publisher = Entry(self.CP_frame, width=27)
        self.item_publisher.grid(row=1, column=2, sticky=W)
        
        lerow += 1
        
        #create identifier label
        
        item_identifier_label = Label(self.right_frame, text = "Archival Identifier:", justify=LEFT)
        item_identifier_label.grid(row=lerow, column=0, sticky=W)
        
        lerow += 1
        
        #create identifier entry widget
        
        self.item_identifier = Entry(self.right_frame, width=60)
        self.item_identifier.grid(row=lerow, column=0, sticky=W)
        
        lerow += 1
        
        #create "primary location and date" label
        
        item_primary_label = Label(self.right_frame, text = "Primary Location and Date:", justify=LEFT)
        item_primary_label.grid(row=lerow, column=0, sticky=W)
        
        lerow += 1
        
        #primary location frame
        
        self.PriLoc_frame = Frame(self.right_frame)
        self.PriLoc_frame.grid(row=lerow, column=0, sticky=W)     
        
        #create longitude label
        
        item_primaryLongitude_label = Label(self.PriLoc_frame, text = "Longitude:", justify=LEFT)
        item_primaryLongitude_label.grid(row=0, column=0, sticky=W)
        
        #create longitude entry widget
        
        self.item_primaryLongitude = Entry(self.PriLoc_frame, width=14)
        self.item_primaryLongitude.grid(row=1, column=0, sticky=W)
        
        #empty space between longitude and latitude
        
        empty_label1 = Label(self.PriLoc_frame, text = "   ")
        empty_label1.grid(row=0, column=1, sticky=W)
        
        empty_label1 = Label(self.PriLoc_frame, text = "   ")
        empty_label1.grid(row=1, column=1, sticky=W)
        
        #create latitude label
        
        item_primaryLatitude_label = Label(self.PriLoc_frame, text = "Latitude:", justify=LEFT)
        item_primaryLatitude_label.grid(row=0, column=2, sticky=W)
        
        #create latitude entry widget
        
        self.item_primaryLatitude = Entry(self.PriLoc_frame, width=14)
        self.item_primaryLatitude.grid(row=1, column=2, sticky=W)
        
        #empty space between latitude and place
        
        empty_label1 = Label(self.PriLoc_frame, text = "  ")
        empty_label1.grid(row=0, column=3, sticky=W)
        
        empty_label1 = Label(self.PriLoc_frame, text = "  ")
        empty_label1.grid(row=1, column=3, sticky=W)
        
        #create place label 
        
        item_primaryPlace_label = Label(self.PriLoc_frame, text = "Place:", justify=LEFT)
        item_primaryPlace_label.grid(row=0, column=4, sticky=W)
        
        #create place entry widget
        
        self.item_primaryPlace = Entry(self.PriLoc_frame, width=25)
        self.item_primaryPlace.grid(row=1, column=4, sticky=W)
        
        ##########
        
        lerow += 1
        
        #primary date frame
        
        self.PriDate_frame = Frame(self.right_frame)
        self.PriDate_frame.grid(row=lerow, column=0, sticky=W)   
        
        #create start date label 
        
        item_primStartDate_label = Label(self.PriDate_frame, text = "Start Date:", justify=LEFT)
        item_primStartDate_label.grid(row=0, column=0, sticky=W)
        
        #empty space between start label and start day
        
        empty_label1 = Label(self.PriDate_frame, text = "  ")
        empty_label1.grid(row=0, column=1, sticky=W)
        
        #create start date day entry widget
        
        self.item_primStartDay = Entry(self.PriDate_frame, width=3)
        self.item_primStartDay.grid(row=0, column=2, sticky=W)
        
        #empty space between start day and start month
        
        empty_label1 = Label(self.PriDate_frame, text = "  ")
        empty_label1.grid(row=0, column=3, sticky=W)
        
        #create start date month entry widget
        
        self.item_primStartMonth = Entry(self.PriDate_frame, width=3)
        self.item_primStartMonth.grid(row=0, column=4, sticky=W)
        
        #empty space between start month and start year
        
        empty_label1 = Label(self.PriDate_frame, text = "  ")
        empty_label1.grid(row=0, column=5, sticky=W)
        
        #create start date year entry widget 
        
        self.item_primStartYear = Entry(self.PriDate_frame, width=5)
        self.item_primStartYear.grid(row=0, column=6, sticky=W)
        
        #empty space between start year and end label
        
        empty_label1 = Label(self.PriDate_frame, text = "  ")
        empty_label1.grid(row=0, column=7, sticky=W)
        
        #create end date label 
        
        item_primEndDate_label = Label(self.PriDate_frame, text = "End Date:", justify=LEFT)
        item_primEndDate_label.grid(row=0, column=8, sticky=W)
        
        #empty space between end label and end day
        
        empty_label1 = Label(self.PriDate_frame, text = "  ")
        empty_label1.grid(row=0, column=9, sticky=W)
        
        #create end date day entry widget
        
        self.item_primEndDay = Entry(self.PriDate_frame, width=3)
        self.item_primEndDay.grid(row=0, column=10, sticky=W)
        
        #empty space between end day and end month
        
        empty_label1 = Label(self.PriDate_frame, text = "  ")
        empty_label1.grid(row=0, column=11, sticky=W)
        
        #create end date month entry widget
        
        self.item_primEndMonth = Entry(self.PriDate_frame, width=3)
        self.item_primEndMonth.grid(row=0, column=12, sticky=W)
        
        #empty space between end month and end year
        
        empty_label1 = Label(self.PriDate_frame, text = "  ")
        empty_label1.grid(row=0, column=13, sticky=W)
        
        #create end date year entry widget 
        
        self.item_primEndYear = Entry(self.PriDate_frame, width=5)
        self.item_primEndYear.grid(row=0, column=14, sticky=W)
        
        ###
        #add dd, mm and yyyy labels
        ###  
        
        #start dd label
        
        dd_label = Label(self.PriDate_frame, text = "dd", foreground = "grey", justify=LEFT)
        dd_label.grid(row=1, column=2, sticky=W)
        
        #start mm label
        
        mm_label = Label(self.PriDate_frame, text = "mm", foreground = "grey", justify=LEFT)
        mm_label.grid(row=1, column=4, sticky=W)
        
        #start yyyy label
        
        yyyy_label = Label(self.PriDate_frame, text = "yyyy", foreground = "grey", justify=LEFT)
        yyyy_label.grid(row=1, column=6, sticky=W)
        
        #end dd label
        
        dd_label = Label(self.PriDate_frame, text = "dd", foreground = "grey", justify=LEFT)
        dd_label.grid(row=1, column=10, sticky=W)
        
        #end mm label
        
        mm_label = Label(self.PriDate_frame, text = "mm", foreground = "grey", justify=LEFT)
        mm_label.grid(row=1, column=12, sticky=W)
        
        #end yyyy label
        
        yyyy_label = Label(self.PriDate_frame, text = "yyyy", foreground = "grey", justify=LEFT)
        yyyy_label.grid(row=1, column=14, sticky=W)
        
        
        lerow += 1
        
        #create "created location and date" label
        
        item_created_label = Label(self.right_frame, text = "Location and Date Created:", justify=LEFT)
        item_created_label.grid(row=lerow, column=0, sticky=W)
        
        lerow += 1
        
        #created location frame
        
        self.CreLoc_frame = Frame(self.right_frame)
        self.CreLoc_frame.grid(row=lerow, column=0, sticky=W)     
        
        #create longitude label
        
        item_createdLongitude_label = Label(self.CreLoc_frame, text = "Longitude:", justify=LEFT)
        item_createdLongitude_label.grid(row=0, column=0, sticky=W)
        
        #create longitude entry widget
        
        self.item_createdLongitude = Entry(self.CreLoc_frame, width=14)
        self.item_createdLongitude.grid(row=1, column=0, sticky=W)
        
        #empty space between longitude and latitude
        
        empty_label1 = Label(self.CreLoc_frame, text = "   ")
        empty_label1.grid(row=0, column=1, sticky=W)
        
        empty_label1 = Label(self.CreLoc_frame, text = "   ")
        empty_label1.grid(row=1, column=1, sticky=W)
        
        #create latitude label
        
        item_createdLatitude_label = Label(self.CreLoc_frame, text = "Latitude:", justify=LEFT)
        item_createdLatitude_label.grid(row=0, column=2, sticky=W)
        
        #create latitude entry widget
        
        self.item_createdLatitude = Entry(self.CreLoc_frame, width=14)
        self.item_createdLatitude.grid(row=1, column=2, sticky=W)
        
        #empty space between latitude and place
        
        empty_label1 = Label(self.CreLoc_frame, text = "  ")
        empty_label1.grid(row=0, column=3, sticky=W)
        
        empty_label1 = Label(self.CreLoc_frame, text = "  ")
        empty_label1.grid(row=1, column=3, sticky=W)
        
        #create place label 
        
        item_createdPlace_label = Label(self.CreLoc_frame, text = "Place:", justify=LEFT)
        item_createdPlace_label.grid(row=0, column=4, sticky=W)
        
        #create place entry widget
        
        self.item_createdPlace = Entry(self.CreLoc_frame, width=25)
        self.item_createdPlace.grid(row=1, column=4, sticky=W)
        
        ##########
        
        lerow += 1
        
        #created date frame
        
        self.CreDate_frame = Frame(self.right_frame)
        self.CreDate_frame.grid(row=lerow, column=0, sticky=W)   
        
        #create start date label 
        
        item_creStartDate_label = Label(self.CreDate_frame, text = "Start Date:", justify=LEFT)
        item_creStartDate_label.grid(row=0, column=0, sticky=W)
        
        #empty space between start label and start day
        
        empty_label1 = Label(self.CreDate_frame, text = "  ")
        empty_label1.grid(row=0, column=1, sticky=W)
        
        #create start date day entry widget
        
        self.item_creStartDay = Entry(self.CreDate_frame, width=3)
        self.item_creStartDay.grid(row=0, column=2, sticky=W)
        
        #empty space between start day and start month
        
        empty_label1 = Label(self.CreDate_frame, text = "  ")
        empty_label1.grid(row=0, column=3, sticky=W)
        
        #create start date month entry widget
        
        self.item_creStartMonth = Entry(self.CreDate_frame, width=3)
        self.item_creStartMonth.grid(row=0, column=4, sticky=W)
        
        #empty space between start month and start year
        
        empty_label1 = Label(self.CreDate_frame, text = "  ")
        empty_label1.grid(row=0, column=5, sticky=W)
        
        #create start date year entry widget 
        
        self.item_creStartYear = Entry(self.CreDate_frame, width=5)
        self.item_creStartYear.grid(row=0, column=6, sticky=W)
        
        #empty space between start year and end label
        
        empty_label1 = Label(self.CreDate_frame, text = "  ")
        empty_label1.grid(row=0, column=7, sticky=W)
        
        #create end date label 
        
        item_creEndDate_label = Label(self.CreDate_frame, text = "End Date:", justify=LEFT)
        item_creEndDate_label.grid(row=0, column=8, sticky=W)
        
        #empty space between end label and end day
        
        empty_label1 = Label(self.CreDate_frame, text = "  ")
        empty_label1.grid(row=0, column=9, sticky=W)
        
        #create end date day entry widget
        
        self.item_creEndDay = Entry(self.CreDate_frame, width=3)
        self.item_creEndDay.grid(row=0, column=10, sticky=W)
        
        #empty space between end day and end month
        
        empty_label1 = Label(self.CreDate_frame, text = "  ")
        empty_label1.grid(row=0, column=11, sticky=W)
        
        #create end date month entry widget
        
        self.item_creEndMonth = Entry(self.CreDate_frame, width=3)
        self.item_creEndMonth.grid(row=0, column=12, sticky=W)
        
        #empty space between end month and end year
        
        empty_label1 = Label(self.CreDate_frame, text = "  ")
        empty_label1.grid(row=0, column=13, sticky=W)
        
        #create end date year entry widget 
        
        self.item_creEndYear = Entry(self.CreDate_frame, width=5)
        self.item_creEndYear.grid(row=0, column=14, sticky=W)
        
        ###
        #add dd, mm and yyyy labels
        ###  
        
        #start dd label
        
        dd_label = Label(self.CreDate_frame, text = "dd", foreground = "grey", justify=LEFT)
        dd_label.grid(row=1, column=2, sticky=W)
        
        #start mm label
        
        mm_label = Label(self.CreDate_frame, text = "mm", foreground = "grey", justify=LEFT)
        mm_label.grid(row=1, column=4, sticky=W)
        
        #start yyyy label
        
        yyyy_label = Label(self.CreDate_frame, text = "yyyy", foreground = "grey", justify=LEFT)
        yyyy_label.grid(row=1, column=6, sticky=W)
        
        #end dd label
        
        dd_label = Label(self.CreDate_frame, text = "dd", foreground = "grey", justify=LEFT)
        dd_label.grid(row=1, column=10, sticky=W)
        
        #end mm label
        
        mm_label = Label(self.CreDate_frame, text = "mm", foreground = "grey", justify=LEFT)
        mm_label.grid(row=1, column=12, sticky=W)
        
        #end yyyy label
        
        yyyy_label = Label(self.CreDate_frame, text = "yyyy", foreground = "grey", justify=LEFT)
        yyyy_label.grid(row=1, column=14, sticky=W)
        
        lerow += 1
        
        #published "published location and date" label
        
        item_published_label = Label(self.right_frame, text = "Location and Date Published:", justify=LEFT)
        item_published_label.grid(row=lerow, column=0, sticky=W)
        
        lerow += 1
        
        #published location frame
        
        self.PubLoc_frame = Frame(self.right_frame)
        self.PubLoc_frame.grid(row=lerow, column=0, sticky=W)     
        
        #published longitude label
        
        item_publishedLongitude_label = Label(self.PubLoc_frame, text = "Longitude:", justify=LEFT)
        item_publishedLongitude_label.grid(row=0, column=0, sticky=W)
        
        #published longitude entry widget
        
        self.item_publishedLongitude = Entry(self.PubLoc_frame, width=14)
        self.item_publishedLongitude.grid(row=1, column=0, sticky=W)
        
        #empty space between longitude and latitude
        
        empty_label1 = Label(self.PubLoc_frame, text = "   ")
        empty_label1.grid(row=0, column=1, sticky=W)
        
        empty_label1 = Label(self.PubLoc_frame, text = "   ")
        empty_label1.grid(row=1, column=1, sticky=W)
        
        #published latitude label
        
        item_publishedLatitude_label = Label(self.PubLoc_frame, text = "Latitude:", justify=LEFT)
        item_publishedLatitude_label.grid(row=0, column=2, sticky=W)
        
        #published latitude entry widget
        
        self.item_publishedLatitude = Entry(self.PubLoc_frame, width=14)
        self.item_publishedLatitude.grid(row=1, column=2, sticky=W)
        
        #empty space between latitude and place
        
        empty_label1 = Label(self.PubLoc_frame, text = "  ")
        empty_label1.grid(row=0, column=3, sticky=W)
        
        empty_label1 = Label(self.PubLoc_frame, text = "  ")
        empty_label1.grid(row=1, column=3, sticky=W)
        
        #published place label 
        
        item_publishedPlace_label = Label(self.PubLoc_frame, text = "Place:", justify=LEFT)
        item_publishedPlace_label.grid(row=0, column=4, sticky=W)
        
        #published place entry widget
        
        self.item_publishedPlace = Entry(self.PubLoc_frame, width=25)
        self.item_publishedPlace.grid(row=1, column=4, sticky=W)
        
        ##########
        
        lerow += 1
        
        #published date frame
        
        self.PubDate_frame = Frame(self.right_frame)
        self.PubDate_frame.grid(row=lerow, column=0, sticky=W)   
        
        #published start date label 
        
        item_pubStartDate_label = Label(self.PubDate_frame, text = "Start Date:", justify=LEFT)
        item_pubStartDate_label.grid(row=0, column=0, sticky=W)
        
        #empty space between start label and start day
        
        empty_label1 = Label(self.PubDate_frame, text = "  ")
        empty_label1.grid(row=0, column=1, sticky=W)
        
        #published start date day entry widget
        
        self.item_pubStartDay = Entry(self.PubDate_frame, width=3)
        self.item_pubStartDay.grid(row=0, column=2, sticky=W)
        
        #empty space between start day and start month
        
        empty_label1 = Label(self.PubDate_frame, text = "  ")
        empty_label1.grid(row=0, column=3, sticky=W)
        
        #published start date month entry widget
        
        self.item_pubStartMonth = Entry(self.PubDate_frame, width=3)
        self.item_pubStartMonth.grid(row=0, column=4, sticky=W)
        
        #empty space between start month and start year
        
        empty_label1 = Label(self.PubDate_frame, text = "  ")
        empty_label1.grid(row=0, column=5, sticky=W)
        
        #published start date year entry widget 
        
        self.item_pubStartYear = Entry(self.PubDate_frame, width=5)
        self.item_pubStartYear.grid(row=0, column=6, sticky=W)
        
        #empty space between start year and end label
        
        empty_label1 = Label(self.PubDate_frame, text = "  ")
        empty_label1.grid(row=0, column=7, sticky=W)
        
        #published end date label 
        
        item_pubEndDate_label = Label(self.PubDate_frame, text = "End Date:", justify=LEFT)
        item_pubEndDate_label.grid(row=0, column=8, sticky=W)
        
        #empty space between end label and end day
        
        empty_label1 = Label(self.PubDate_frame, text = "  ")
        empty_label1.grid(row=0, column=9, sticky=W)
        
        #published end date day entry widget
        
        self.item_pubEndDay = Entry(self.PubDate_frame, width=3)
        self.item_pubEndDay.grid(row=0, column=10, sticky=W)
        
        #empty space between end day and end month
        
        empty_label1 = Label(self.PubDate_frame, text = "  ")
        empty_label1.grid(row=0, column=11, sticky=W)
        
        #published end date month entry widget
        
        self.item_pubEndMonth = Entry(self.PubDate_frame, width=3)
        self.item_pubEndMonth.grid(row=0, column=12, sticky=W)
        
        #empty space between end month and end year
        
        empty_label1 = Label(self.PubDate_frame, text = "  ")
        empty_label1.grid(row=0, column=13, sticky=W)
        
        #published end date year entry widget 
        
        self.item_pubEndYear = Entry(self.PubDate_frame, width=5)
        self.item_pubEndYear.grid(row=0, column=14, sticky=W)
        
        ###
        #add dd, mm and yyyy labels
        ###  
        
        #start dd label
        
        dd_label = Label(self.PubDate_frame, text = "dd", foreground = "grey", justify=LEFT)
        dd_label.grid(row=1, column=2, sticky=W)
        
        #start mm label
        
        mm_label = Label(self.PubDate_frame, text = "mm", foreground = "grey", justify=LEFT)
        mm_label.grid(row=1, column=4, sticky=W)
        
        #start yyyy label
        
        yyyy_label = Label(self.PubDate_frame, text = "yyyy", foreground = "grey", justify=LEFT)
        yyyy_label.grid(row=1, column=6, sticky=W)
        
        #end dd label
        
        dd_label = Label(self.PubDate_frame, text = "dd", foreground = "grey", justify=LEFT)
        dd_label.grid(row=1, column=10, sticky=W)
        
        #end mm label
        
        mm_label = Label(self.PubDate_frame, text = "mm", foreground = "grey", justify=LEFT)
        mm_label.grid(row=1, column=12, sticky=W)
        
        #end yyyy label
        
        yyyy_label = Label(self.PubDate_frame, text = "yyyy", foreground = "grey", justify=LEFT)
        yyyy_label.grid(row=1, column=14, sticky=W)

        lerow += 1

        #add/cancel buttons frame
        
        self.AC_frame = Frame(self.right_frame)
        self.AC_frame.grid(row=lerow, column=0, sticky=E)

        #create Add button
        
        textV = StringVar(self.AC_frame)
        
        if order == "edit":
        
            self.editEntryInfo() #function call ... leindex = ...
            additem = Button(self.AC_frame, text="Update", command=lambda: self.checkForErrors(order))  
            
        else:
            
            additem = Button(self.AC_frame, text="Add", command=lambda: self.checkForErrors(order))  
                  
        additem.grid(row=0, column=0, sticky=W)
        
        #create Cancel button
        
        cancelitem = Button(self.AC_frame, text='Cancel', command=lambda: (self.AddItemWindow).destroy())
        cancelitem.grid(row=0, column=1, sticky=W)
        
        (self.AddItemWindow).mainloop() 
        #(self.AddItemWindow).destroy() causes problem when user clicks on x button but window won't close without this when 'cancel' is clicked
    
    
    def deleteElmClick(self):
        
        selected = (self.listbox).curselection()
        
        while len(selected) != 0:
            
            if "*" not in (self.openxmlfile).get():
        
                xmlname = (self.openxmlfile).get()
                xmlname = xmlname + "*"
                (self.openxmlfile).set(xmlname)
            
            index = int(selected[0])                 #get index from 'selected' as an integer
            (self.listbox).delete(index)             #delete first selected item
            
            itemIndex = self.indexList[index]       #get index of element to remove of item list, from the index list
            del self.itemList[itemIndex]            #remove corresponding element from item list
            
            #del self.indexList[index]               #remove corresponding element from index list ... program doesn't work with this line?
            
            selected = (self.listbox).curselection() #have to recalculate list because it got shorter since we deleted an item 
        
        
    def editEntryInfo(self):
        
        ###
        #get index of selected item
        ###
        
        selected = (self.listbox).curselection()
        
        self.leindex = int(selected[0]) #only one item selected
        
        elemIndex = self.leindex
        
        #store old item ID
        
        self.olditemID = self.itemList[elemIndex][10]
        
        ###
        #get info from itemList and write it on the entry widgets
        ###
        
        #item type
        (self.item_type).set(self.itemList[elemIndex][0])
        
        #item title
        (self.item_title).delete(0, END)
        (self.item_title).insert(END, self.itemList[elemIndex][1]) 
        
        #item description
        #(self.item_description).delete(0, END)
        (self.item_description).insert(END, self.itemList[elemIndex][2]) 
        
        #item transcript
        #(self.item_transcript).delete(0, END)
        (self.item_transcript).insert(END, self.itemList[elemIndex][3])         
        
        #item originalSource
        (self.item_originalSource).delete(0, END)
        (self.item_originalSource).insert(END, self.itemList[elemIndex][4]) 

        #item license
        (self.item_license).delete(0, END)
        (self.item_license).insert(END, self.itemList[elemIndex][5])
        
        #item copyright
        (self.item_copyright).delete(0, END)
        (self.item_copyright).insert(END, self.itemList[elemIndex][6])
        
        #item permission
        (self.item_permission).delete(0, END)
        (self.item_permission).insert(END, self.itemList[elemIndex][7])
        
        #item file
        (self.item_file).delete(0, END)
        (self.item_file).insert(END, self.itemList[elemIndex][8])
        
        #item googlePath
        (self.item_googlePath).delete(0, END)
        (self.item_googlePath).insert(END, self.itemList[elemIndex][9])
        
        #item googleID
        (self.item_googleID).delete(0, END)
        (self.item_googleID).insert(END, self.itemList[elemIndex][10])
        
        #item fileType
        (self.item_fileType).delete(0, END)
        (self.item_fileType).insert(END, self.itemList[elemIndex][11])
        
        #item language
        (self.item_language).set(self.itemList[elemIndex][12])

        #item format
        (self.item_format).delete(0, END)
        (self.item_format).insert(END, self.itemList[elemIndex][13]) 

        #item provenance
        (self.item_provenance).delete(0, END)
        (self.item_provenance).insert(END, self.itemList[elemIndex][14])
        
        #item subject
        (self.item_subject).delete(0, END)
        (self.item_subject).insert(END, self.itemList[elemIndex][15])
        
        #item creator
        (self.item_creator).delete(0, END)
        (self.item_creator).insert(END, self.itemList[elemIndex][16]) 

        #item contributor
        (self.item_contributor).delete(0, END)
        (self.item_contributor).insert(END, self.itemList[elemIndex][17]) 

        #item publisher
        (self.item_publisher).delete(0, END)
        (self.item_publisher).insert(END, self.itemList[elemIndex][18]) 

        #item primary place
        (self.item_primaryPlace).delete(0, END)
        (self.item_primaryPlace).insert(END, self.itemList[elemIndex][19])
        
        #item primaryLatitude
        (self.item_primaryLatitude).delete(0, END)
        (self.item_primaryLatitude).insert(END, self.itemList[elemIndex][20]) 

        #item primaryLongitude
        (self.item_primaryLongitude).delete(0, END)
        (self.item_primaryLongitude).insert(END, self.itemList[elemIndex][21])
        
        #item primStartDay
        (self.item_primStartDay).delete(0, END)
        (self.item_primStartDay).insert(END, self.itemList[elemIndex][22])

        #item primStartMonth
        (self.item_primStartMonth).delete(0, END)
        (self.item_primStartMonth).insert(END, self.itemList[elemIndex][23])
        
        #item primStartYear
        (self.item_primStartYear).delete(0, END)
        (self.item_primStartYear).insert(END, self.itemList[elemIndex][24])

        #item primEndDay
        (self.item_primEndDay).delete(0, END)
        (self.item_primEndDay).insert(END, self.itemList[elemIndex][25])
        
        #item primEndMonth
        (self.item_primEndMonth).delete(0, END)
        (self.item_primEndMonth).insert(END, self.itemList[elemIndex][26])
        
        #item primEndYear
        (self.item_primEndYear).delete(0, END)
        (self.item_primEndYear).insert(END, self.itemList[elemIndex][27])
        
        #item createdPlace
        (self.item_createdPlace).delete(0, END)
        (self.item_createdPlace).insert(END, self.itemList[elemIndex][28])
        
        #item createdLatitude
        (self.item_createdLatitude).delete(0, END)
        (self.item_createdLatitude).insert(END, self.itemList[elemIndex][29])
            
        #item createdLongitude
        (self.item_createdLongitude).delete(0, END)
        (self.item_createdLongitude).insert(END, self.itemList[elemIndex][30])
        
        #item creStartDay
        (self.item_creStartDay).delete(0, END)
        (self.item_creStartDay).insert(END, self.itemList[elemIndex][31])
        
        #item creStartMonth
        (self.item_creStartMonth).delete(0, END)
        (self.item_creStartMonth).insert(END, self.itemList[elemIndex][32])
        
        #item creStartYear
        (self.item_creStartYear).delete(0, END)
        (self.item_creStartYear).insert(END, self.itemList[elemIndex][33])
        
        #item creEndDay
        (self.item_creEndDay).delete(0, END)
        (self.item_creEndDay).insert(END, self.itemList[elemIndex][34])
        
        #item creEndMonth
        (self.item_creEndMonth).delete(0, END)
        (self.item_creEndMonth).insert(END, self.itemList[elemIndex][35])
        
        #item creEndYear
        (self.item_creEndYear).delete(0, END)
        (self.item_creEndYear).insert(END, self.itemList[elemIndex][36])
        
        #item publishedPlace
        (self.item_publishedPlace).delete(0, END)
        (self.item_publishedPlace).insert(END, self.itemList[elemIndex][37])
        
        #item publishedLatitude
        (self.item_publishedLatitude).delete(0, END)
        (self.item_publishedLatitude).insert(END, self.itemList[elemIndex][38])
        
        #item publishedLongitude
        (self.item_publishedLongitude).delete(0, END)
        (self.item_publishedLongitude).insert(END, self.itemList[elemIndex][39])
        
        #item pubStartDay
        (self.item_pubStartDay).delete(0, END)
        (self.item_pubStartDay).insert(END, self.itemList[elemIndex][40])
        
        #item pubStartMonth
        (self.item_pubStartMonth).delete(0, END)
        (self.item_pubStartMonth).insert(END, self.itemList[elemIndex][41])
        
        #item pubStartYear
        (self.item_pubStartYear).delete(0, END)
        (self.item_pubStartYear).insert(END, self.itemList[elemIndex][42])
        
        #item pubEndDay
        (self.item_pubEndDay).delete(0, END)
        (self.item_pubEndDay).insert(END, self.itemList[elemIndex][43])
        
        #item pubEndMonth
        (self.item_pubEndMonth).delete(0, END)
        (self.item_pubEndMonth).insert(END, self.itemList[elemIndex][44])

        #item pubEndYear
        (self.item_pubEndYear).delete(0, END)
        (self.item_pubEndYear).insert(END, self.itemList[elemIndex][45])

        #item identifier
        (self.item_identifier).delete(0, END)
        (self.item_identifier).insert(END, self.itemList[elemIndex][46])
        
        #originalSource URL
        (self.item_oriURL).delete(0, END)
        (self.item_oriURL).insert(END, self.itemList[elemIndex][47])
        
        #license URL
        (self.item_liURL).delete(0, END)
        (self.item_liURL).insert(END, self.itemList[elemIndex][48])
        
        #item disclaimer
        #(self.item_disclaimer).delete(0, END)
        (self.item_disclaimer).insert(END, self.itemList[elemIndex][49])
        
        #yes/no to autogenerated description for subitems
        (self.YesNo).set(self.itemList[elemIndex][50])
        
        #print (self.YesNo).get()
        
        if (self.YesNo).get() == 1:
            
            checkBox.select()
        
     
    def overwriteClick(self, index, order):
        
        #store original value of self.index
        original = self.leindex
        
        # have index of item that will be overwritten
        self.leindex = index
        
        # use code of edit function to overwrite with written info on window
        self.editListInfo(True)
        
        if order == "edit":
            
            #delete item you were editing from list
            (self.listbox).delete(original)
            
            #delete information of item from item list
            del self.itemList[original]
            
            #remove index from index list ***NOT SURE ABOUT THIS
            del self.indexList[original]
        
        
        #close add window
        (self.AddItemWindow).destroy()

        #create pop up window
        
        message = "item with id " + self.itemList[self.leindex][10] + " was overwritten" #********can't access that index anymore...
        
        tkMessageBox.showerror("done!", message, icon='info')
        
        #put self.index back to original value
        self.leindex = original
        
        
        
     
    def editListInfo(self, overwrite):
        
        if "*" not in (self.openxmlfile).get():
        
            xmlname = (self.openxmlfile).get()
            xmlname = xmlname + "*"
            (self.openxmlfile).set(xmlname)
        
        
        elemIndex = self.leindex
        
        #item type
        self.itemList[elemIndex][0] = (self.item_type).get()
        
        #item title
        self.itemList[elemIndex][1] = (self.item_title).get()
        
        #item description
        self.itemList[elemIndex][2] = (self.item_description).get("1.0", END) 
        
        #item transcript
        self.itemList[elemIndex][3] = (self.item_transcript).get("1.0", END)          
        
        #item originalSource
        self.itemList[elemIndex][4] = (self.item_originalSource).get()

        #item license
        self.itemList[elemIndex][5] = (self.item_license).get()
        
        #item copyright
        self.itemList[elemIndex][6] = (self.item_copyright).get()
        
        #item permission
        self.itemList[elemIndex][7] = (self.item_permission).get()
        
        #item file
        self.itemList[elemIndex][8] = (self.item_file).get()
        
        #item googlePath
        self.itemList[elemIndex][9] = (self.item_googlePath).get()
        
        #item googleID
        self.itemList[elemIndex][10] = (self.item_googleID).get()
        
        #item fileType
        self.itemList[elemIndex][11] = (self.item_fileType).get()
        
        #item language
        self.itemList[elemIndex][12] = (self.item_language).get()

        #item format
        self.itemList[elemIndex][13] = (self.item_format).get() 

        #item provenance
        self.itemList[elemIndex][14] = (self.item_provenance).get()
        
        #item subject
        self.itemList[elemIndex][15] = (self.item_subject).get()
        
        #item creator
        self.itemList[elemIndex][16] = (self.item_creator).get()

        #item contributor
        self.itemList[elemIndex][17] = (self.item_contributor).get()

        #item publisher
        self.itemList[elemIndex][18] = (self.item_publisher).get()

        #item primary place
        self.itemList[elemIndex][19] = (self.item_primaryPlace).get()
        
        #item primaryLatitude
        self.itemList[elemIndex][20] = (self.item_primaryLatitude).get() 

        #item primaryLongitude
        self.itemList[elemIndex][21] = (self.item_primaryLongitude).get()
        
        #item primStartDay
        self.itemList[elemIndex][22] = (self.item_primStartDay).get()

        #item primStartMonth
        self.itemList[elemIndex][23] = (self.item_primStartMonth).get()
        
        #item primStartYear
        self.itemList[elemIndex][24] = (self.item_primStartYear).get()

        #item primEndDay
        self.itemList[elemIndex][25] = (self.item_primEndDay).get()
        
        #item primEndMonth
        self.itemList[elemIndex][26] = (self.item_primEndMonth).get()
        
        #item primEndYear
        self.itemList[elemIndex][27] = (self.item_primEndYear).get()
        
        #item createdPlace
        self.itemList[elemIndex][28] = (self.item_createdPlace).get()
        
        #item createdLatitude
        self.itemList[elemIndex][29] = (self.item_createdLatitude).get()
            
        #item createdLongitude
        self.itemList[elemIndex][30] = (self.item_createdLongitude).get()
        
        #item creStartDay
        self.itemList[elemIndex][31] = (self.item_creStartDay).get()
        
        #item creStartMonth
        self.itemList[elemIndex][32] = (self.item_creStartMonth).get()
        
        #item creStartYear
        self.itemList[elemIndex][33] = (self.item_creStartYear).get()
        
        #item creEndDay
        self.itemList[elemIndex][34] = (self.item_creEndDay).get()
        
        #item creEndMonth
        self.itemList[elemIndex][35] = (self.item_creEndMonth).get()
        
        #item creEndYear
        self.itemList[elemIndex][36] = (self.item_creEndYear).get()
        
        #item publishedPlace
        self.itemList[elemIndex][37] = (self.item_publishedPlace).get()
        
        #item publishedLatitude
        self.itemList[elemIndex][38] = (self.item_publishedLatitude).get()
        
        #item publishedLongitude
        self.itemList[elemIndex][39] = (self.item_publishedLongitude).get()
        
        #item pubStartDay
        self.itemList[elemIndex][40] = (self.item_pubStartDay).get()
        
        #item pubStartMonth
        self.itemList[elemIndex][41] = (self.item_pubStartMonth).get()
        
        #item pubStartYear
        self.itemList[elemIndex][42] = (self.item_pubStartYear).get()
        
        #item pubEndDay
        self.itemList[elemIndex][43] = (self.item_pubEndDay).get()
        
        #item pubEndMonth
        self.itemList[elemIndex][44] = (self.item_pubEndMonth).get()

        #item pubEndYear
        self.itemList[elemIndex][45] = (self.item_pubEndYear).get()

        #item identifier
        self.itemList[elemIndex][46] = (self.item_identifier).get()
        
        #originalSource URL
        self.itemList[elemIndex][47] = (self.item_oriURL).get()
        
        #license URL
        self.itemList[elemIndex][48] = (self.item_liURL).get()
        
        #disclaimer
        self.itemList[elemIndex][49] = (self.item_disclaimer).get("1.0",END)
    
        #yes/no to autogenerate
        
        self.itemList[elemIndex][50] = (self.YesNo).get()
    
        #if item ID had been changed, then change the old item ID stored in (some of) the subitems to the new ID
    
        if (not overwrite):
            
            if ((self.itemList[elemIndex][10]) != (self.olditemID)):
    
                index = 0
                
                while index < len(self.subitemList): 
                    
                    if (self.subitemList[index][0]) == (self.olditemID): #this is working
                        
                        self.subitemList[index][0] = self.itemList[elemIndex][10]
                        
                    index = index + 1
        
            ###
            #edit info from visible list
            ###
            
            #delete corresponding item from list
            
            (self.listbox).delete(self.leindex)
            
            #re-add item to list
        
            string = str((self.itemList[self.leindex][0]) + (self.itemList[self.leindex][1]))
            
            (self.listbox).insert(self.leindex, string)
            
            #add index to index list
            
            self.indexList[self.leindex] = self.leindex
                
            #close window
            (self.AddItemWindow).destroy()
        
  
    def importCSVClick(self): #NEEDS A CHANGIN'
        
        csvFileName = askopenfilename()
        
        try:
            
            fin = open(csvFileName, 'r')
            
        except IOError as e:
            
            print("\n\n({})".format(e))  #report error given by python
            return #leave function
            
            
        inter = csv.reader(fin) #read file
        csvData = [] #initialize list that will contain the csv data
        for row in inter: #go through each line/row in the read csv file
           csvData.append(row) #add each line/row from the csv file into the list csvData[]
     
        ###
        #Check column names of csv file. If there are any issues, report them and exit the function. GOTTA MAKE IT SO THAT THIS ISN'T NECESSARY
        ###
        testData = ['title', 'description', 'type', 'format', 'location:placename', 'location:lat', 'location:lon', 'date:start', 'date:end', 'language', 'provenance', 'subject', 'datecreated:start', 'datecreated:end', 'originalsource:text', 'originalsource:url', 'customtext:copyright', 'customtext:permission', 'customtext:license', 'customlink:licenseurl:text']
        i = 0 
        while i < len(csvData[0]): #check that the first row that was read from the csv file contains the names of each column and that those names are the same as the ones in testData[]
           if(csvData[0][i] != testData[i]): #if a value within the first row of the read csv does not correspond with the parallel value of testData[]...
              #msg = "Wrong first row, Stopping." + "["+str(csvData[0][i]) + "] is not the same as [" + str(testData[i])+"]"
              return #leave the function 
           i = i + 1 
        
        ###   
        #add the csv information into the entry widgets.
        ###
        
        #title
        (self.item_title).delete(0, END)
        (self.item_title).insert(END, csvData[1][0]) 
        
        #description
        #(self.item_description).delete(0, END) #...doesn't work, gives error
        (self.item_description).insert(END, csvData[1][1])
        
        #type
        (self.item_fileType).delete(0, END)
        (self.item_fileType).insert(END, csvData[1][2])
        
        #format
        (self.item_format).delete(0, END)
        (self.item_format).insert(END, csvData[1][3])
        
        #primary place
        (self.item_primaryPlace).delete(0, END)
        (self.item_primaryPlace).insert(END, csvData[1][4])
        
        #primary latitude
        (self.item_primaryLatitude).delete(0, END)
        (self.item_primaryLatitude).insert(END, csvData[1][5])
        
        #primary longitude
        (self.item_primaryLongitude).delete(0, END)
        (self.item_primaryLongitude).insert(END, csvData[1][6])
        
        #primary start date csvData[1][7]
    
        #primary end date csvData[1][8]
        
        #language
        (self.item_language).set(csvData[1][9])
        
        #provenance
        (self.item_provenance).delete(0, END)
        (self.item_provenance).insert(END, csvData[1][10])
        
        #subject
        (self.item_subject).delete(0, END)
        (self.item_subject).insert(END, csvData[1][11])
        
        #start date csvData[1][12]
        
        startDate = csvData[1][12]
        
        if startDate.find('-') == -1: #no hyphens in date string
            
            (self.item_primStartYear).delete(0, END)
            (self.item_primStartYear).insert(END, startDate)
        
        else:
            
            dividedDate = startDate.split("-")
            
            if len(dividedDate) == 2: # MM-YYYY
                
                (self.item_primStartMonth).delete(0, END)
                (self.item_primStartMonth).insert(END, dividedDate[0])                
                
                (self.item_primStartYear).delete(0, END)
                (self.item_primStartYear).insert(END, dividedDate[1])
                
            elif len(dividedDate) == 3: # DD-MM-YYYY
                
                (self.item_primStartDay).delete(0, END)
                (self.item_primStartDay).insert(END, dividedDate[0])
                
                (self.item_primStartMonth).delete(0, END)
                (self.item_primStartMonth).insert(END, dividedDate[1])                
                
                (self.item_primStartYear).delete(0, END)
                (self.item_primStartYear).insert(END, dividedDate[2])
        
        #end date 
        
        endDate = csvData[1][13]
        
        if endDate.find('-') == -1: #no hiphens in date string
            
            (self.item_primEndYear).delete(0, END)
            (self.item_primEndYear).insert(END, endDate)
        
        else:
            
            dividedDate = endDate.split("-")
            
            if len(dividedDate) == 2: # MM-YYYY
                
                (self.item_primEndMonth).delete(0, END)
                (self.item_primEndMonth).insert(END, dividedDate[0])                
                
                (self.item_primEndYear).delete(0, END)
                (self.item_primEndYear).insert(END, dividedDate[1])
                
            elif len(dividedDate) == 3: # DD-MM-YYYY
                
                (self.item_primEndDay).delete(0, END)
                (self.item_primEndDay).insert(END, dividedDate[0])
                
                (self.item_primEndMonth).delete(0, END)
                (self.item_primEndMonth).insert(END, dividedDate[1])                
                
                (self.item_primEndYear).delete(0, END)
                (self.item_primEndYear).insert(END, dividedDate[2])

        #original source text
        (self.item_originalSource).delete(0, END)
        (self.item_originalSource).insert(END, csvData[1][14])
        
        #original source url
        (self.item_oriURL).delete(0, END)
        (self.item_oriURL).insert(END, csvData[1][15])
        
        #copyright
        (self.item_copyright).delete(0, END)
        (self.item_copyright).insert(END, csvData[1][16])
        
        #permission
        (self.item_permission).delete(0, END)
        (self.item_permission).insert(END, csvData[1][17])
        
        #license text
        (self.item_license).delete(0, END)
        (self.item_license).insert(END, csvData[1][18])
        
        #license url
        (self.item_liURL).delete(0, END)
        (self.item_liURL).insert(END, csvData[1][19])     
        
    
    def checkForErrors(self, order):
        
        #make entry widgets have no highlight first
        
        #(self.item_type).configure(highlightbackground="black")
        (self.item_title).configure(highlightbackground="white")
        (self.item_description).configure(highlightbackground="white")
        (self.item_file).configure(highlightbackground="white")
        (self.item_googlePath).configure(highlightbackground="white")
        (self.item_googleID).configure(highlightbackground="white")
        (self.item_primStartDay).configure(highlightbackground="white")
        (self.item_primStartMonth).configure(highlightbackground="white")
        (self.item_primStartYear).configure(highlightbackground="white")
        (self.item_primEndDay).configure(highlightbackground="white")
        (self.item_primEndMonth).configure(highlightbackground="white")
        (self.item_primEndYear).configure(highlightbackground="white")
        (self.item_creStartDay).configure(highlightbackground="white")
        (self.item_creStartMonth).configure(highlightbackground="white")
        (self.item_creStartYear).configure(highlightbackground="white")
        (self.item_creEndDay).configure(highlightbackground="white")
        (self.item_creEndMonth).configure(highlightbackground="white")
        (self.item_creEndYear).configure(highlightbackground="white")
        (self.item_pubStartDay).configure(highlightbackground="white")
        (self.item_pubStartMonth).configure(highlightbackground="white")
        (self.item_pubStartYear).configure(highlightbackground="white")
        (self.item_pubEndDay).configure(highlightbackground="white")
        (self.item_pubEndMonth).configure(highlightbackground="white")
        (self.item_pubEndYear).configure(highlightbackground="white")
        
        
        #now check for errors in input
        
        error = False
        
        #if (self.item_type).get() == "":
            
            #error = True
            
            #(self.item_type).configure(highlightbackground="red")
            
        if (self.item_title).get() == "":
            
            error = True
            
            (self.item_title).configure(highlightbackground="red")
            
        #if (self.item_description).get("1.0",END) == "\n":
            
        #    error = True
            
        #    (self.item_description).configure(highlightbackground="red")
        
        if (order == "add") and ((self.item_file).get() == ""):
            
            error = True
            
            (self.item_file).configure(highlightbackground="red")
            
        #if (self.item_googlePath).get() == "": ***can be empty, so no more of this, but may do other type of validation later
        #     
        #    error = True
        #    
        #    (self.item_googlePath).configure(highlightbackground="red")
            
        if (self.item_googleID).get() == "":
            
            error = True
            
            (self.item_googleID).configure(highlightbackground="red")

          
        ####  
        #primary date
        ###
            
        if (((self.item_primStartDay.get()) != "") & ((self.item_primStartYear.get()) != "")) & ((self.item_primStartMonth.get()) == ""):
            
            error = True
            
            (self.item_primStartMonth).configure(highlightbackground="red")
            
        if ((self.item_primStartDay.get()) != "") & ((self.item_primStartYear.get()) == "") & ((self.item_primStartMonth.get()) == ""):
            
            error = True
            
            (self.item_primStartMonth).configure(highlightbackground="red")
            (self.item_primStartYear).configure(highlightbackground="red")
            
        primStartDay = self.item_primStartDay.get()    
            
        if (primStartDay != ""):
            
            if (not (primStartDay).isdigit()) or (int(primStartDay) > 31):
            
                error = True
            
                (self.item_primStartDay).configure(highlightbackground="red")
            
            
        primStartMonth = self.item_primStartMonth.get()    
            
        if (primStartMonth != ""):
        
            if (not (primStartMonth).isdigit()) or (int(primStartMonth) > 12):
            
                error = True
            
                (self.item_primStartMonth).configure(highlightbackground="red")
        
        
        primStartYear = self.item_primStartYear.get()
        
        if (primStartYear != ""):
            
            if (not (primStartYear).isdigit()) or (len(primStartYear) > 4):
            
                error = True
            
                (self.item_primStartYear).configure(highlightbackground="red")

        
        if (((self.item_primEndDay.get()) != "") & ((self.item_primEndYear.get()) != "")) & ((self.item_primEndMonth.get()) == ""):
            
            error = True
            
            (self.item_primEndMonth).configure(highlightbackground="red")
            
        if ((self.item_primEndDay.get()) != "") & ((self.item_primEndYear.get()) == "") & ((self.item_primEndMonth.get()) == ""):
            
            error = True
            
            (self.item_primEndMonth).configure(highlightbackground="red")
            (self.item_primEndYear).configure(highlightbackground="red")
            
            
        primEndDay = self.item_primEndDay.get()    
            
        if (primEndDay != ""):
            
            if (not (primEndDay).isdigit()) or (int(primEndDay) > 31):
            
                error = True
            
                (self.item_primEndDay).configure(highlightbackground="red")
            
            
        primEndMonth = self.item_primEndMonth.get()    
            
        if (primEndMonth != ""):
            
            if (not (primEndMonth).isdigit()) or (int(primEndMonth) > 12):
            
                error = True
            
                (self.item_primEndMonth).configure(highlightbackground="red")
        
        
        primEndYear = self.item_primEndYear.get()
        
        if (primEndYear != ""):
            
            if (not (primEndYear).isdigit()) & (len(primEndYear) > 4):
            
                error = True
            
                (self.item_primEndYear).configure(highlightbackground="red")

        ####  
        #created date
        ###
            
        if (((self.item_creStartDay.get()) != "") & ((self.item_creStartYear.get()) != "")) & ((self.item_creStartMonth.get()) == ""):
            
            error = True
            
            (self.item_creStartMonth).configure(highlightbackground="red")
            
        if ((self.item_creStartDay.get()) != "") & ((self.item_creStartYear.get()) == "") & ((self.item_creStartMonth.get()) == ""):
            
            error = True
            
            (self.item_creStartMonth).configure(highlightbackground="red")
            (self.item_creStartYear).configure(highlightbackground="red")
            
        creStartDay = self.item_creStartDay.get()    
            
        if (creStartDay != ""):
            
            if (not (creStartDay).isdigit()) or (int(creStartDay) > 31):
            
                error = True
            
                (self.item_creStartDay).configure(highlightbackground="red")
            
            
        creStartMonth = self.item_creStartMonth.get()    
            
        if (creStartMonth != ""):
        
            if (not (creStartMonth).isdigit()) or (int(creStartMonth) > 12):
            
                error = True
            
                (self.item_creStartMonth).configure(highlightbackground="red")
        
        
        creStartYear = self.item_creStartYear.get()
        
        if (creStartYear != ""):
            
            if (not (creStartYear).isdigit()) or (len(creStartYear) > 4):
            
                error = True
            
                (self.item_creStartYear).configure(highlightbackground="red")

        
        if (((self.item_creEndDay.get()) != "") & ((self.item_creEndYear.get()) != "")) & ((self.item_creEndMonth.get()) == ""):
            
            error = True
            
            (self.item_creEndMonth).configure(highlightbackground="red")
            
        if ((self.item_creEndDay.get()) != "") & ((self.item_creEndYear.get()) == "") & ((self.item_creEndMonth.get()) == ""):
            
            error = True
            
            (self.item_creEndMonth).configure(highlightbackground="red")
            (self.item_creEndYear).configure(highlightbackground="red")
            
            
        creEndDay = self.item_creEndDay.get()    
            
        if (creEndDay != ""):
            
            if (not (creEndDay).isdigit()) or (int(creEndDay) > 31):
            
                error = True
            
                (self.item_creEndDay).configure(highlightbackground="red")
            
            
        creEndMonth = self.item_creEndMonth.get()    
            
        if (creEndMonth != ""):
            
            if (not (creEndMonth).isdigit()) or (int(creEndMonth) > 12):
            
                error = True
            
                (self.item_creEndMonth).configure(highlightbackground="red")
        
        
        creEndYear = self.item_creEndYear.get()
        
        if (creEndYear != ""):
            
            if (not (creEndYear).isdigit()) & (len(creEndYear) > 4):
            
                error = True
            
                (self.item_creEndYear).configure(highlightbackground="red")

        ####  
        #published date
        ###
            
        if (((self.item_pubStartDay.get()) != "") & ((self.item_pubStartYear.get()) != "")) & ((self.item_pubStartMonth.get()) == ""):
            
            error = True
            
            (self.item_pubStartMonth).configure(highlightbackground="red")
            
        if ((self.item_pubStartDay.get()) != "") & ((self.item_pubStartYear.get()) == "") & ((self.item_pubStartMonth.get()) == ""):
            
            error = True
            
            (self.item_pubStartMonth).configure(highlightbackground="red")
            (self.item_pubStartYear).configure(highlightbackground="red")
            
        pubStartDay = self.item_pubStartDay.get()    
            
        if (pubStartDay != ""):
            
            if (not (pubStartDay).isdigit()) or (int(pubStartDay) > 31):
            
                error = True
            
                (self.item_pubStartDay).configure(highlightbackground="red")
            
            
        pubStartMonth = self.item_pubStartMonth.get()    
            
        if (pubStartMonth != ""):
        
            if (not (pubStartMonth).isdigit()) or (int(pubStartMonth) > 12):
            
                error = True
            
                (self.item_pubStartMonth).configure(highlightbackground="red")
        
        
        pubStartYear = self.item_pubStartYear.get()
        
        if (pubStartYear != ""):
            
            if (not (pubStartYear).isdigit()) or (len(pubStartYear) > 4):
            
                error = True
            
                (self.item_pubStartYear).configure(highlightbackground="red")

        
        if (((self.item_pubEndDay.get()) != "") & ((self.item_pubEndYear.get()) != "")) & ((self.item_pubEndMonth.get()) == ""):
            
            error = True
            
            (self.item_pubEndMonth).configure(highlightbackground="red")
            
        if ((self.item_pubEndDay.get()) != "") & ((self.item_pubEndYear.get()) == "") & ((self.item_pubEndMonth.get()) == ""):
            
            error = True
            
            (self.item_pubEndMonth).configure(highlightbackground="red")
            (self.item_pubEndYear).configure(highlightbackground="red")
            
            
        pubEndDay = self.item_pubEndDay.get()    
            
        if (pubEndDay != ""):
            
            if (not (pubEndDay).isdigit()) or (int(pubEndDay) > 31):
            
                error = True
            
                (self.item_pubEndDay).configure(highlightbackground="red")
            
            
        pubEndMonth = self.item_pubEndMonth.get()    
            
        if (pubEndMonth != ""):
            
            if (not (pubEndMonth).isdigit()) or (int(pubEndMonth) > 12):
            
                error = True
            
                (self.item_pubEndMonth).configure(highlightbackground="red")
        
        
        pubEndYear = self.item_pubEndYear.get()
        
        if (pubEndYear != ""):
            
            if (not (pubEndYear).isdigit()) & (len(pubEndYear) > 4):
            
                error = True
            
                (self.item_pubEndYear).configure(highlightbackground="red")
                
                #check that item IDs do not repeat among items
        
        if not error: #no error, error = False
        
            if order == "edit":
                
                if (self.olditemID) != (self.item_googleID).get():
                
                    i = 0
                    
                    while i < len(self.itemList):
                        
                        if (self.item_googleID).get() == (self.itemList[i][10]):
                            
                            error = True
                            
                            (self.item_googleID).configure(highlightbackground="red")
                            
                            #print "google IDs can not repeat among items!"
                            
                            #self.duplicateWin = Toplevel()
                            #(self.duplicateWin).title('WARNING')
                            #(self.duplicateWin).configure(borderwidth=20)
                            #(self.duplicateWin).resizable(width=FALSE, height=FALSE)
                            #
                            #message = "The specified google ID already exists for another item. \nDo you want to override the item?"
                            #Label(self.duplicateWin, text=message).grid(row=0, rowspan=3, column=1, columnspan=2, sticky=W)
                            #Button(self.duplicateWin, text='Yes', command=lambda: self.overwriteClick(i,order)).grid(row=3, column=1, sticky=E) #, command=win.destroy)
                            #Button(self.duplicateWin, text='No', command=(self.duplicateWin).destroy).grid(row=3, column=2, sticky=W)
                            #
                            #(self.duplicateWin).mainloop()
                            
                            result = tkMessageBox.askquestion("duplicate item", "The specified google ID already exists for another item. \nDo you want to override the item?", icon='warning')
                            
                            if result == 'yes':
                                self.overwriteClick(i,order)
                            
                            i = len(self.itemList) 
                            
                        i += 1
        
            else:
                
                i = 0
                
                while i < len(self.itemList):
                    
                    if (self.item_googleID).get() == (self.itemList[i][10]):
                        
                        error = True
                        
                        (self.item_googleID).configure(highlightbackground="red")
                        
                        #print "google IDs can not repeat among items!"
                        
                        #self.duplicateWin = Toplevel()
                        #(self.duplicateWin).title('WARNING')
                        #(self.duplicateWin).configure(borderwidth=20)
                        #(self.duplicateWin).resizable(width=FALSE, height=FALSE)
                        #
                        #message = "The specified google ID already exists for another item. \nDo you want to override the item?"
                        #Label(self.duplicateWin, text=message).grid(row=0, rowspan=3, column=1, columnspan=2, sticky=W)
                        #Button(self.duplicateWin, text='Yes', command=lambda: self.overwriteClick(i,order)).grid(row=3, column=1, sticky=E) #, command=win.destroy)
                        #Button(self.duplicateWin, text='No', command=(self.duplicateWin).destroy).grid(row=3, column=2, sticky=W)
                        #
                        #(self.duplicateWin).mainloop()
                        
                        result = tkMessageBox.askquestion("duplicate item", "The specified google ID already exists for another item. \nDo you want to override the item?", icon='warning')
                            
                        if result == 'yes':
                            self.overwriteClick(i,order)
                        
                        i = len(self.itemList) 
                        
                    i += 1
        
            if not error:
                    
                if order == "add":
                    
                    self.addItemClick()
                    
                else:
                    
                    self.editListInfo(False)
    
        
    def addItemClick(self):
        
        if "*" not in (self.openxmlfile).get():
        
            xmlname = (self.openxmlfile).get()
            xmlname = xmlname + "*"
            (self.openxmlfile).set(xmlname)

            
        tempList = []
            
        tempList.append((self.item_type).get())
        tempList.append((self.item_title).get())
        tempList.append((self.item_description).get("1.0",END))
        tempList.append((self.item_transcript).get("1.0",END))
        tempList.append((self.item_originalSource).get())
        tempList.append((self.item_license).get())
        tempList.append((self.item_copyright).get())
        tempList.append((self.item_permission).get())
        
        tempList.append((self.item_file).get())
        
        tempList.append((self.item_googlePath).get())
        tempList.append((self.item_googleID).get())
        tempList.append((self.item_fileType).get())
        tempList.append((self.item_language).get())
        tempList.append((self.item_format).get())
        tempList.append((self.item_provenance).get())
        tempList.append((self.item_subject).get())
        tempList.append((self.item_creator).get())
        tempList.append((self.item_contributor).get())
        tempList.append((self.item_publisher).get())
        
        #primary 
        tempList.append((self.item_primaryPlace).get())
        tempList.append((self.item_primaryLatitude).get())
        tempList.append((self.item_primaryLongitude).get())
        tempList.append((self.item_primStartDay).get())
        tempList.append((self.item_primStartMonth).get())
        tempList.append((self.item_primStartYear).get())
        tempList.append((self.item_primEndDay).get())
        tempList.append((self.item_primEndMonth).get())
        tempList.append((self.item_primEndYear).get())
        
        #created
        tempList.append((self.item_createdPlace).get())
        tempList.append((self.item_createdLatitude).get())
        tempList.append((self.item_createdLongitude).get())
        tempList.append((self.item_creStartDay).get())
        tempList.append((self.item_creStartMonth).get())
        tempList.append((self.item_creStartYear).get())
        tempList.append((self.item_creEndDay).get())
        tempList.append((self.item_creEndMonth).get())
        tempList.append((self.item_creEndYear).get())
        
        #published
        tempList.append((self.item_publishedPlace).get())
        tempList.append((self.item_publishedLatitude).get())
        tempList.append((self.item_publishedLongitude).get())
        tempList.append((self.item_pubStartDay).get())
        tempList.append((self.item_pubStartMonth).get())
        tempList.append((self.item_pubStartYear).get())
        tempList.append((self.item_pubEndDay).get())
        tempList.append((self.item_pubEndMonth).get())
        tempList.append((self.item_pubEndYear).get())
        
        tempList.append((self.item_identifier).get())

        #URLs
        
        tempList.append((self.item_oriURL).get())
        tempList.append((self.item_liURL).get())
        
        #disclaimer
        tempList.append((self.item_disclaimer).get("1.0",END))
        
        #yes/no to autogenerated data
        tempList.append((self.YesNo).get())
        
            
        (self.itemList).append(tempList)
            
        (self.indexList).append(len(self.itemList) - 1) #index of last added item
        
        
        self.item_id = self.item_googleID
        
        if (self.item_type.get()) == "collection": #if the item is a collection, add subitems into subitem list
            
            #get names of files/pages
            
            namesOfFiles = os.listdir((self.item_file).get()) 
 
            for i in namesOfFiles: 
               separated = i.split('.')
               extension = separated[len(separated) - 1]
               if extension != 'jpg': #if a file in the directory does not have the extension .jpg (so it's not a image), then remove its name from the namesOfFiles list.
                  #print("\n\nignoring file named "+i)
                  namesOfFiles.remove(i)
         
            EnglishTranscript = "None for now..."
            LatinTranscript = "None for now..."
         
            tempList = [] #reuse tempList to store information of one subitem at a time
            
            counter = 0
        
            while counter < len(namesOfFiles):
                ###
                #create list that corresponds to one subitem
                ###
                
                filename = namesOfFiles[counter]
        
                tempList.append((self.item_id).get())   #add item id to be able to later identify to which item does this subitem belong to
                
                #get page number from file name so to create the id, title and descripton of the subitem
                NoExtList = filename.split(".")
                NoExtFile = NoExtList[0]              #filename without extension
                DividedName= NoExtFile.split("-")     #filename divided by '-'
                sizeNoExt = len(DividedName)      
                pageNumber = DividedName[sizeNoExt - 1]
                pageNumber = int(pageNumber) #last part of file name, the page number
                
                #add id of subitem
                tempList.append((self.item_id).get() + "-" + str(pageNumber))
                
                #add title of subitem
                tempList.append("Page "+str(pageNumber))             
                
                if (self.YesNo).get() == 1: #if user selected to autogenerate folio descriptions, add folio description of subitem
                
                    LePage = ""
                    folioNum = str((pageNumber+1)//2)
                    
                    if (folioNum[len(folioNum)-1] == '1') & (folioNum != '11'):
                        LePage = "st"
                    else:
                        if (folioNum[len(folioNum)-1] == '2') & (folioNum != '12'):
                            LePage = "nd"
                        else:
                            if (folioNum[len(folioNum)-1] == '3') & (folioNum != '13'):
                                LePage = "rd"
                            else:
                                LePage = "th"
                        
                    folioInfo = "The " + folioNum + LePage + " folio." #note, // is for integer division, it truncates the result.
                        
                    tempList.append(folioInfo)
                    
                else: #description tag will not exist
                    
                    tempList.append("")
                
                #add image path
                pathOfImage = (self.item_googlePath).get() + filename #result: googlePath/ChadGospels-page.jpg
                tempList.append(pathOfImage)
                
                #add english and latin transcripts
                tempList.append(EnglishTranscript)                   
                tempList.append(LatinTranscript)                     
                
                #add the list with the subitem information into the list that will contain the info of ALL the subitems
                (self.subitemList).append(tempList)                          
                
                counter += 1  #increment counter by 1
                
                tempList = [] #reinitialize tempList            
        
        #add info to visible list        
        string = str((self.itemList[len(self.itemList) - 1][0]) + (self.itemList[len(self.itemList) - 1][1]))
        (self.listbox).insert(END, string)
        
        #add index to index list
        
        (self.indexList).append(len(self.itemList) - 1)
            
        #close window
        (self.AddItemWindow).destroy()
        
      
      
    ###
    #Function that parses an existing xml file and calls the getIndex function with a tag as the parameter, so to know in what position of the tempList list to save the tag info
    ###
    
    def openInfoClick(self, order): #**** HAVING BIG PROBLEM WITH WARNING WINDOWS
        
        #set up boolean variables
         
        isduplicate = False 
         
        lefound = False
         
        #define itemindex 
         
        itemindex = 0
         
        #define item type 
         
        item_type = ""
        
        #get xml file name
        
        filename = askopenfilename(title='please select the xml file you wish to open')
        
        #have loop that keeps asking user for file name if the filename given is not .xml
        
        wrong = True
        
        while wrong:
         
            if filename == "":
               
               return
           
            elif (not filename.endswith('.xml')):
               
                filename = askopenfilename(title='please try again. select an XML file this time.')
                
            else:
               
                wrong = False
        
        #if "open" was clicked, change displayed file name on window and erase contents from itemList and subitemList, as well as contents from visible list
        
        if order == "open":
            
            (self.openxmlfile_path).set(filename)
            
            shortname = filename.split("/")
            shortlength = len(shortname)
            xmlname = shortname[shortlength - 1]
            
            (self.openxmlfile).set(xmlname)
        
            self.itemList = []
            
            self.subitemList = []
            
            (self.listbox).delete(0, END)
            
        else: #if order == "import"
            
            if "*" not in (self.openxmlfile).get():
        
                xmlname = (self.openxmlfile).get()
                xmlname = xmlname + "*"
                (self.openxmlfile).set(xmlname)

        #initialize list to have 50 elements
        
        tempList = []
        subList = []
        
        i = 0
        
        while i < 51:
            
            tempList.append("")
            
            i = i + 1
        
        #parse xml file
    
        lDocument = ET.ElementTree()
        lDocument.parse(filename)
        lRoot = lDocument.getroot()
        
        root = lRoot.getchildren()
        
        #initialize integer variable
        
        leindex = 0
        
        ###
        #get item ID
        ###
        for child in root:
            
            #empty tempList and subList so to reuse them
        
            tempList = []
            subList = []
            
            i = 0
        
            #make temoList into a list with 50 elements
        
            while i < 51:
            
                tempList.append("")
                
                i = i + 1
            
            #look for tag that is item
            
            if (child.tag == "item"):
                
                #if the identifier tag exists and the contents of it are not empty...
                
                if (child.attrib['identifier'] != None) and (child.attrib['identifier'] != ""):
                
                    #if doing import ... check for duplicate item
                
                    if order == "import":
                    
                        i = 0
                    
                        #go through all of the items in itemList while no duplicates have been found
                    
                        while (i < len(self.itemList)) and (not lefound): 
                
                            if child.attrib['identifier'] == (self.itemList[i][10]):
                                
                                #duplicate id found
                                
                                itemindex = i
                                
                                #if replaceAll == False: #if replaceAll isn't true, pop up window that says there's a duplicate item
                                
                                if (self.replace).get() == 1: #replace one item at a time
                                
                                    #pop up window to ask user what to do about duplicate ID
                                
                                    msg = "A duplicate item has been encountered, with id " + (self.itemList[i][10]) + ". You have choosen the option of replacing one item at a time. Do you want to do this?"
                                
                                    result = tkMessageBox.askquestion("warning", msg, icon='warning')
                                    
                                    if result == 'no':
                                      
                                        (self.replace).set(0)
                                        
                                elif (self.replace).get() == 2: #replace al duplicate item at one
                                    
                                    #pop up window to ask user what to do about duplicate ID
                                
                                    msg = "Are you sure that you want to replace all duplicates?"
                                
                                    result = tkMessageBox.askquestion("warning", msg, icon='warning')
                                    
                                    if result == 'no':
                                      
                                        (self.replace).set(0)

                                isduplicate = True

                                lefound = True #set lefound to true because a duplicate item was found
                                
                            i += 1
                            
                        lefound = False
                        
                    #store id in temp list    
                    leindex = self.getIndex("theid")
                    tempList[leindex] = child.attrib['identifier']
                    itemID = child.attrib['identifier']
                
            root_tags = child #contains tags within the "item" tag
            
            #go through all the tags within an item
            
            for Rchild in root_tags: 
                
                leindex2 = 0
                
                if (Rchild.tag == "customlink") or (Rchild.tag == "originalSource"):
            
                    if (Rchild.tag == "customlink"):
                        
                        leindex = self.getIndex(Rchild.attrib['name']) #the tag
                        leindex2 = self.getIndex((Rchild.attrib['name']) + "_URL") 
                        
                    else:
                        
                        leindex = self.getIndex(Rchild.tag)
                        leindex2 = self.getIndex((Rchild.tag) + "_URL")
                    
                    if (Rchild[0].text != None) and (Rchild[0].text != ""):
                    
                        tempList[leindex] = Rchild[0].text   #text
                
                    if (Rchild[0].attrib['href'] != None) and (Rchild[0].attrib['href'] != ""):
                
                        tempList[leindex2] = Rchild[0].attrib['href'] #url   
                
                elif (Rchild.tag == "customtext"):
                    
                    if (Rchild[0].text != None) and (Rchild[0].text != ""):
                    
                        leindex = self.getIndex(Rchild.attrib['name'])
                        
                        tempList[leindex] = Rchild[0].text
               
                elif (Rchild.tag == "locationCreated") or (Rchild.tag == "locationPublished") or (Rchild.tag == "location"):
                    
                    leindex = self.getIndex(Rchild.tag)
                    
                    location = Rchild.getchildren()
                    
                    for Lchild in location:
                    
                        if (Lchild.text != None) and (Lchild.text != ""):
                    
                            if Lchild.tag == "placename":
                            
                                tempList[leindex] = Lchild.text
        
                            elif Lchild.tag == "latitude":
                            
                                tempList[leindex + 1] = Lchild.text
                                
                            elif Lchild.tag == "longitude":
                            
                                tempList[leindex + 2] = Lchild.text
                        
                elif ((Rchild.tag == "dateCreated") or (Rchild.tag == "datePublished") or (Rchild.tag == "date")):
                    
                    if (Rchild[0].text != None) and (Rchild[0].text != ""):
                    
                        leindex = self.getIndex(Rchild.tag)
                        
                        start = True
                        end = True
                        
                        wholeDate = Rchild[0].text
                        
                        if wholeDate.find('/') == -1:
                            
                            startDate = wholeDate
                            end = False
                        
                        else:
                            
                            wholeDiv = wholeDate.split("/")
                            
                            startDate = wholeDiv[0]
                            
                            endDate = wholeDiv[1]
                        
                        if start:
                            
                            dividedStart = startDate.split("-")
                            
                            if startDate.find('-') == -1: #no hyphens in date string
                                
                                tempList[leindex + 2] = startDate #start year
                            
                            else:
                                
                                if len(dividedStart) == 2: # MM-YYYY
                                    
                                    tempList[leindex + 1] = dividedStart[1] #month    
                                    
                                    tempList[leindex + 2] = dividedStart[0] #year
                                    
                                elif len(dividedStart) == 3: # DD-MM-YYYY
                                    
                                    tempList[leindex] = dividedStart[2]     #day    
                                    
                                    tempList[leindex + 1] = dividedStart[1] #month           
                                    
                                    tempList[leindex + 2] = dividedStart[0] #year
                           
                        if end:
                            
                            dividedEnd = endDate.split("-")
                            
                            if endDate.find('-') == -1: #no hyphens in date string
                                
                                tempList[leindex + 5] = endDate
                            
                            else:
                                
                                if len(dividedEnd) == 2: # MM-YYYY
                                    
                                    tempList[leindex + 4] = dividedEnd[1]  #month      
                                    
                                    tempList[leindex + 5] = dividedEnd[0]  #year
                                    
                                elif len(dividedEnd) == 3: # DD-MM-YYYY
                                    
                                    tempList[leindex + 3] = dividedEnd[2]  #day
                                    
                                    tempList[leindex + 4] = dividedEnd[1]  #month        
                                    
                                    tempList[leindex + 5] = dividedEnd[0]  #year
                    
                elif (Rchild.tag == "image"):
                
                    if (Rchild.attrib['filename'] != None) and (Rchild.attrib['filename'] != ""):
                
                        item_type = "image"
                    
                        leindex = self.getIndex(Rchild.tag) #index to store file path. leindex + 1 is position to store google path.
                        
                        divPath = (Rchild.attrib['filename']).split("/")    
                        
                        tempList[leindex] = divPath[len(divPath) - 1]
                        
                        if len(divPath) > 1:
                            
                            gooPath = divPath[0] + "/"
                            
                            i = 1
                            while i < (len(divPath) - 1):
                                
                                gooPath = gooPath + divPath[i] + "/"
                                i = i + 1
                        
                            tempList[leindex + 1] = gooPath
                    
                elif (Rchild.tag == "video"):
                
                    if (Rchild.attrib['youtubeid'] != None) and (Rchild.attrib['youtubeid'] != ""):
                    
                        item_type = "video"
                    
                        leindex = self.getIndex(Rchild.tag) #index to store file path. 
                        
                        tempList[leindex] = Rchild.attrib['youtubeid']
                    
                elif (Rchild.tag != "sequence"):       
                
                    if (Rchild[0].text != None) and (Rchild[0].text != ""):
                
                        leindex = self.getIndex(Rchild.tag)
                        
                        tempList[leindex] = Rchild[0].text
                    
                elif Rchild.tag == "sequence":
                
                    item_type = "collection"

                    #i = 0
                    
                    #while i < len(Rchild):

                    lechildren = Rchild.getchildren()
            
                    for Schild in lechildren:
                        
                        subList = []
                    
                        subList.append(itemID)
                    
                        if Schild.tag == "subitem":
                                
                            subList.append(Schild.attrib['identifier'])
                
                        sequence_tags = Schild #Rchild[i]
                        
                        for SSchild in sequence_tags:
                            
                            #print Schild.tag
                            
                            if SSchild.tag != "image":
                                
                                info = SSchild[0].text
                                
                            else:
                                
                                info = SSchild.attrib['filename']
                                
                            subList.append(info)
                            
                    #i = i + 1
                    
                        (self.subitemList).append(subList)
                        
                
            tempList[0] = item_type
            
            tempList[50] = 0 #NO to autogenerated subitem description
            
            #if user said to replace one or to replace all, and the current item is a duplicate, then...
            
            if (((self.replace).get() == 1) or ((self.replace).get() == 2)) and isduplicate:
                
                self.itemList[itemindex] = tempList
                
                ###
                #edit info from visible list
                ###
                
                #delete corresponding item from list
                
                (self.listbox).delete(itemindex)
                
                #re-add item to list
            
                string = str((self.itemList[itemindex][0]) + (self.itemList[itemindex][1]))
                
                (self.listbox).insert(itemindex, string)
                
                #add index to index list
                
                self.indexList[itemindex] = itemindex
            
            elif not isduplicate:
                
                print "no repetition"
                
                #no replacements
                
                (self.itemList).append(tempList)
    
                #add info to visible list        
                string = str((self.itemList[len(self.itemList) - 1][0]) + (self.itemList[len(self.itemList) - 1][1]))
                (self.listbox).insert(END, string)
                
                #add index to index list
                
                (self.indexList).append(len(self.itemList) - 1)
                
            
            if (self.replace).get() == 1:
            
                #pop up that says item was replaced
                
                msg = "Item with id " + (self.itemList[itemindex][10]) + " has been replaced."
                
                tkMessageBox.showinfo("done!", msg, icon='info')        
                

            #restart isduplicate to False
            
            isduplicate = False

                
        #pop up that says all repeated items were replaced
        
        if (self.replace).get() == 2:
            
            msg = "All duplicate items have been replaced."
                
            tkMessageBox.showinfo("done!", msg, icon='info')   
        
    
    
    ###
    #Function that returns index where info of tag should be saved into tempList array
    ###
    
    def getIndex(self, tag):
        
        if tag == "title":
            #item title
            return 1
        
        elif tag == "description":
            #item description
            return 2
        
        elif tag == "transcript":
            #item transcript
            return 3          
        
        elif tag == "originalSource":
            #item originalSource
            return 4
    
        elif tag == "license":
            #item license
            return 5
        
        elif tag == "copyright":
            #item copyright
            return 6
        
        elif tag == "permission":
            #item permission
            return 7
        
        elif (tag == "image") or (tag == "video") or (tag == "file"):
            
            return 8
        
        elif tag == "theid":
            #item googleID
            return 10
        
        elif tag == "type":
            #item fileType
            return 11
        
        elif tag == "language":
            #item language
            return 12
    
        elif tag == "format":
            #item format
            return 13
    
        elif tag == "provenance":
            #item provenance
            return 14
        
        elif tag == "subject":
            #item subject
            return 15
        
        elif tag == "creator":
            #item creator
            return 16
    
        elif tag == "contributor":
            #item contributor
            return 17
    
        elif tag == "publisher":
            #item publisher
            return 18
    
        elif tag == "location":
            #item primary place
            return 19
        
        elif tag == "date":
            #item primStartDay
            return 22
        
        elif tag == "locationCreated":
            #item createdPlace
            return 28
    
        elif tag == "dateCreated":
            #item creStartDay
            return 31
    
        elif tag == "locationPublished":
            #item publishedPlace
            return 37
        
        elif tag == "datePublished":
            #item pubStartDay
            return 40
    
        elif tag == "identifier":
            #item identifier
            return 46
        
        elif tag == "originalSource_URL":
            
            return 47
        
        elif tag == "license_URL":
            
            return 48
        
        elif tag == "disclaimer":
            #disclaimer
            return 49
 



    def saveClick(self, order):
        
        if ( ((self.openxmlfile).get() == "Untitled") or ((((self.openxmlfile).get() == "Untitled*"))) and (order == "overwrite")) or (order == "write"):
            
            xmlFileName = asksaveasfilename(title="select a folder to save the xml file and write the new file name for the file")
        
            wrong = True
        
            while wrong:
             
                if xmlFileName == "":
                   
                   return
               
                elif (not xmlFileName.endswith('.xml')):
                   
                    xmlFileName = asksaveasfilename(title='please try again. the file must have \".xml\" as the extension.')
                    
                else:
                   
                    wrong = False
        else:
            
            xmlFileName = (self.openxmlfile_path).get()
        
        #export as xml
        
        Itemset = ET.Element("itemset") #root of xml file
        
        i = 0
        
        while i < len(self.itemList): #for each item
        
            #for dates
            
            start = ""
            end = ""
        
            #write the item tag with the google ID
            
            if self.itemList[i][10] != "":
            
                Item = ET.SubElement(Itemset, "item")     #'item' is a child of 'itemset'
                itemID = self.itemList[i][10]         #get ID information from item list
                Item.set("identifier", itemID)   #write the identifier of the item
            
            #write the title tag
            
            if self.itemList[i][1] != "":
            
                Title = ET.SubElement(Item, "title")  #'title' is a child of 'item'
                Text = ET.SubElement(Title, "text")   #'text' is a child of 'title'
                Text.set("lang", "en")                # creates the tag: <text lang="en">
                Text.text = self.itemList[i][1]            #second value of item i, gives the title
             
            #write the description tag
            
            if self.itemList[i][2].rstrip() != "":
            
                Description = ET.SubElement(Item, "description") #'description' is a child of 'item'
                Text = ET.SubElement(Description, "text")        #'text' is a child of 'description'
                Text.set("lang", "en")                           # creates the tag: <text lang="en">
                Text.text = (self.itemList[i][2]).rstrip()       #remove newline at end with rstrip()
              
            #write the transcript tag 
            
            if (self.itemList[i][3]).rstrip() != "":
                
                Transcript = ET.SubElement(Item, "transcript") 
                Text = ET.SubElement(Transcript, "text")       
                Text.set("lang", "en")                         
                Text.text = self.itemList[i][3].rstrip()       #remove new line at end with rstrip()
                
            #write the disclaimer tag
            
            if (self.itemList[i][49]).rstrip() != "":
                
                CustomText1 = ET.SubElement(Item, "customtext") 
                CustomText1.set("name", "disclaimer")
                Text = ET.SubElement(CustomText1, "text")   #text tag     
                Text.text = self.itemList[i][49]
                
                
            #write the type tag
            
            if self.itemList[i][11] != "":
            
                Type = ET.SubElement(Item, "type")       
                Text = ET.SubElement(Type, "text")  #text tag      
                Text.text = self.itemList[i][11]
                
            #write the format tag
            
            if self.itemList[i][13] != "":
            
                Format = ET.SubElement(Item, "format")      
                Text = ET.SubElement(Format, "text")  #text tag        
                Text.text = self.itemList[i][13]  
                
            #write the primary location tag
            
            if (self.itemList[i][19] != "") or (self.itemList[i][20] != "") or (self.itemList[i][21] != ""):
            
                Location = ET.SubElement(Item, "location")
                
                if self.itemList[i][20] != "":
                    
                    Latitude = ET.SubElement(Location, "latitude")   #latitude tag     
                    Latitude.text = self.itemList[i][20]
                
                if self.itemList[i][21] != "":
                
                    Longitude = ET.SubElement(Location, "longitude") #longitude tag       
                    Longitude.text = self.itemList[i][21]
                
                if self.itemList[i][19] != "":
                
                    Placename = ET.SubElement(Location, "placename") #placename tag
                    Placename.set("lang", "en")                           
                    Placename.text = self.itemList[i][19]
                
            #write the primary date tag
            
            if (self.itemList[i][24] != "") or (self.itemList[i][27] != ""):
                
                Date = ET.SubElement(Item, "date")     
                DateValue = ET.SubElement(Date, "dateValue")   #dateValue tag
                
                if self.itemList[i][24] != "":
                
                    if self.itemList[i][22] == "" and self.itemList[i][23] != "": #day is empty, month isn't
                       
                        start = self.itemList[i][24] + "-" + self.itemList[i][23]
                        
                    elif self.itemList[i][23] == "": #month is empty
                        
                        start = self.itemList[i][24]
                        
                    else: #none are empty
                        
                        start = self.itemList[i][24] + "-" + self.itemList[i][23] + "-" + self.itemList[i][22]
                
                
                if self.itemList[i][27] != "":
                    
                    if self.itemList[i][25] == "" and self.itemList[i][23] != "": #day is empty, month isn't
                        
                        end = self.itemList[i][27] + "-" + self.itemList[i][26]
                     
                    elif self.itemList[i][26] == "": #month is empty
                        
                        end = self.itemList[i][27]
                        
                    else: #none are empty
                        
                        end = self.itemList[i][27] + "-" + self.itemList[i][26] + "-" + self.itemList[i][25] 

                if start == end: #if the start date and end date are the same, only write the start date (start and end are interchangeable)
                    DateValue.text = start
                elif start == "":
                    DateValue.text = end
                elif end == "":
                    DateValue.text = start
                else:
                    DateValue.text = start + "/" + end              #interval of year has to be written as: start/end
                
            #write the created location tag
            
            if (self.itemList[i][28] != "") or (self.itemList[i][29] != "") or (self.itemList[i][30] != ""):
            
                creLocation = ET.SubElement(Item, "locationCreated")
                
                if self.itemList[i][29] != "":
                    creLatitude = ET.SubElement(creLocation, "latitude")   #latitude tag     
                    creLatitude.text = self.itemList[i][29]
               
                if self.itemList[i][30] != "":    
                    creLongitude = ET.SubElement(creLocation, "longitude") #longitude tag       
                    creLongitude.text = self.itemList[i][30]
                    
                if self.itemList[i][28] != "":        
                    crePlacename = ET.SubElement(creLocation, "placename") #placename tag
                    crePlacename.set("lang", "en")                           
                    crePlacename.text = self.itemList[i][28]
                
            #write the dateCreated tag
            
            if (self.itemList[i][33] != "") or (self.itemList[i][36] != ""): #31: startday, 32: startmonth, 33: startyear, 34: endday, 35: endmonth, 36: endyear
                
                DateCreated = ET.SubElement(Item, "dateCreated")     
                DateValue = ET.SubElement(DateCreated, "dateValue")   #dateValue tag
                
                if self.itemList[i][33] != "":
                
                    if self.itemList[i][31] == "" and self.itemList[i][32] != "": #day is empty, month isn't
                       
                        start = self.itemList[i][33] + "-" + self.itemList[i][32]
                        
                    elif self.itemList[i][32] == "": #month is empty
                        
                        start = self.itemList[i][33]
                        
                    else: #none are empty
                        
                        start = self.itemList[i][33] + "-" + self.itemList[i][32] + "-" + self.itemList[i][31]
                
                
                if self.itemList[i][36] != "":
                    
                    if self.itemList[i][34] == "" and self.itemList[i][32] != "": #day is empty, month isn't
                        
                        end = self.itemList[i][36] + "-" + self.itemList[i][35]
                     
                    elif self.itemList[i][35] == "": #month is empty
                        
                        end = self.itemList[i][36]
                        
                    else: #none are empty
                        
                        end = self.itemList[i][36] + "-" + self.itemList[i][35] + "-" + self.itemList[i][34]
                                   
                if start == end: #if the start date and end date are the same, only write the start date (start and end are interchangeable)
                    DateValue.text = start
                elif start == "":
                    DateValue.text = end
                elif end == "":
                    DateValue.text = start
                else:
                    DateValue.text = start + "/" + end              #interval of year has to be written as: start/end         
                
            
            #write the published location tag
            
            if (self.itemList[i][37] != "") or (self.itemList[i][38] != "") or (self.itemList[i][39] != ""):
                
                pubLocation = ET.SubElement(Item, "locationPublished")
                
                if self.itemList[i][38] != "":
                    pubLatitude = ET.SubElement(pubLocation, "latitude")   #latitude tag     
                    pubLatitude.text = self.itemList[i][38]
                    
                if self.itemList[i][39] != "":
                    pubLongitude = ET.SubElement(pubLocation, "longitude") #longitude tag       
                    pubLongitude.text = self.itemList[i][39]
                
                if self.itemList[i][37] != "":    
                    pubPlacename = ET.SubElement(pubLocation, "placename") #placename tag
                    pubPlacename.set("lang", "en")                           
                    pubPlacename.text = self.itemList[i][37]
                
            #write the published date tag
            
            if (self.itemList[i][42] != "") or (self.itemList[i][45] != ""): #40: startday, 41: startmonth, 42: startyear, 43: endday, 44: endmonth, 45: endyear
                
                DatePublished = ET.SubElement(Item, "datePublished")     
                DateValue = ET.SubElement(DatePublished, "dateValue")   #dateValue tag
                
                if self.itemList[i][42] != "":
                
                    if self.itemList[i][40] == "" and self.itemList[i][41] != "": #day is empty, month isn't
                       
                        start = self.itemList[i][42] + "-" + self.itemList[i][41]
                        
                    elif self.itemList[i][41] == "": #month is empty
                        
                        start = self.itemList[i][42]
                        
                    else: #none are empty
                        
                        start = self.itemList[i][42] + "-" + self.itemList[i][41] + "-" + self.itemList[i][40]
                
                
                if self.itemList[i][45] != "":
                    
                    if self.itemList[i][43] == "" and self.itemList[i][41] != "": #day is empty, month isn't
                        
                        end = self.itemList[i][45] + "-" + self.itemList[i][44]
                     
                    elif self.itemList[i][44] == "": #month is empty
                        
                        end = self.itemList[i][45]
                        
                    else: #none are empty
                        
                        end = self.itemList[i][45] + "-" + self.itemList[i][44] + "-" + self.itemList[i][43]
                                   
                if start == end: #if the start date and end date are the same, only write the start date (start and end are interchangeable)
                    DateValue.text = start
                elif start == "":
                    DateValue.text = end
                elif end == "":
                    DateValue.text = start
                else:
                    DateValue.text = start + "/" + end              #interval of year has to be written as: start/end                           
            
                
            #write the language tag
            
            if self.itemList[i][12] != "":
                
                Language = ET.SubElement(Item, "language")     
                Text = ET.SubElement(Language, "text")   #text tag     
                Text.text = self.itemList[i][12]
                
            #write the provenance tag
            
            if self.itemList[i][14] != "":
            
                Provenance = ET.SubElement(Item, "provenance")     
                Text = ET.SubElement(Provenance, "text")   #text tag     
                Text.text = self.itemList[i][14]
                
            #write the subject tag
            
            if self.itemList[i][15] != "":
            
                Subject = ET.SubElement(Item, "subject")     
                Text = ET.SubElement(Subject, "text")   #text tag     
                Text.text = self.itemList[i][15]                
                
            #******    
                
            #write the originalSource tag
            
            if (self.itemList[i][4] != "") and (self.itemList[i][47] != ""):
            
                OriginalSource = ET.SubElement(Item, "originalSource") 
                Url = ET.SubElement(OriginalSource, "url")  #url tag
                TheLink = self.itemList[i][47]  #original source url
                Url.set("href", TheLink)               
                Url.text = self.itemList[i][4] #original source text
                
            #write the copyright tag
            
            if self.itemList[i][6] != "":
            
                CustomText1 = ET.SubElement(Item, "customtext") 
                CustomText1.set("name", "copyright")
                Text = ET.SubElement(CustomText1, "text")   #text tag     
                Text.text = self.itemList[i][6]
                
            #write the permission tag
            
            if self.itemList[i][7] != "":
                
                CustomText2 = ET.SubElement(Item, "customtext") 
                CustomText2.set("name", "permission")
                Text = ET.SubElement(CustomText2, "text")   #text tag     
                Text.text = self.itemList[i][7]
                
            #write the license tag
            
            if (self.itemList[i][5] != "") and (self.itemList[i][48] != ""):
                
                CustomLink = ET.SubElement(Item, "customlink") 
                CustomLink.set("name", "license")
                Url = ET.SubElement(CustomLink, "url")  #url tag
                TheLink = self.itemList[i][48]  #license url
                Url.set("href", TheLink)               
                Url.text = self.itemList[i][5] #license text
            
            #extra tags coming up!
            
            #write the creator tag
            
            if self.itemList[i][16] != "":
                
                Creator = ET.SubElement(Item, "creator")     
                Text = ET.SubElement(Creator, "text")   #text tag     
                Text.text = self.itemList[i][16]                
                
            #write the contributor tag
            
            if self.itemList[i][17] != "":
                
                Subject = ET.SubElement(Item, "contributor")     
                Text = ET.SubElement(Subject, "text")   #text tag     
                Text.text = self.itemList[i][17]
                
            #write the publisher tag
            
            if self.itemList[i][18] != "":
                
                Subject = ET.SubElement(Item, "publisher")     
                Text = ET.SubElement(Subject, "text")   #text tag     
                Text.text = self.itemList[i][18]      
            
            #write the identifier tag
            
            if self.itemList[i][46] != "":
                
                Identifier = ET.SubElement(Item, "identifier") #'description' is a child of 'item'
                IdentifierValue = ET.SubElement(Identifier, "identifierValue")        #'text' is a child of 'description'
                IdentifierValue.text = self.itemList[i][46]
            
            if (self.itemList[i][0]) == "image":
                
                #write the image tag
                Image = ET.SubElement(Item, "image") 
                lepath = self.itemList[i][8].split("/")
                TheFilePath = self.itemList[i][9] + lepath[len(lepath) - 1]
                Image.set("filename", TheFilePath)
                
            elif (self.itemList[i][0]) == "video":
                
                #write the image tag
                Image = ET.SubElement(Item, "video") 
                TheFilePath = self.itemList[i][8]
                Image.set("youtubeid", TheFilePath)

            elif (self.itemList[i][0]) == "collection":
                    
                    #look for index of subitem where the item id is the same as the current item id
                    
                    index = 0
                    j = 0
                    found = False
                    
                    while (index < len(self.subitemList)) and (not found): 
                        
                        if (self.subitemList[index][0]) == (self.itemList[i][10]): #this is working
                            
                            j = index
                            found = True
                            
                        index = index + 1
            
                    ###
                    #Create a sequence that will contain subitems (pages of the manuscript)
                    ###
                    Sequence = ET.SubElement(Item, "sequence") 
                    
                    ###
                    #Have a loop that will go through all the subitems and will add their information into the xml file
                    ###
                    
                    while (j < len(self.subitemList) - 1) and (self.subitemList[j][0] == self.itemList[i][10]): #for each subitem
                            
                            #write the subitem tag
                            Subitem = ET.SubElement(Sequence, "subitem") #'subitem' is a child of 'sequence'
                            TheIdentifier = self.subitemList[j][1]             #get this information from subitem list
                            Subitem.set("identifier", TheIdentifier)      #write the identifier of the subitem
                            
                            #write the title tag
                            Title = ET.SubElement(Subitem, "title")  #this time it's a child of 'subitem'
                            Text = ET.SubElement(Title, "text")                
                            Text.text = self.subitemList[j][2]
                            
                            #write the description tag
                            
                            if self.subitemList[j][3] != "":
                                
                                Description = ET.SubElement(Subitem, "description")
                                Text = ET.SubElement(Description, "text")                                
                                Text.text = self.subitemList[j][3]
                            
                            #write the image tag
                            Image = ET.SubElement(Subitem, "image") 
                            TheFilePath = self.subitemList[j][4]
                            Image.set("filename", TheFilePath)     
                            
                            ###commented out because it was causing errors in upload to google cultural institute. also, we did not have it working yet.
                            #write the transcript tag
                            #Transcript = ET.SubElement(Subitem, "transcript") 
                            #Text1 = ET.SubElement(Transcript, "text")  
                            #Text1.set("lang", "en")            #text in english        
                            #Text1.text = self.subitemList[j][5]     #english transcript                  
                            #Text2 = ET.SubElement(Transcript, "text")  
                            #Text2.set("lang", "la")            #text in latin       
                            #Text2.text = self.subitemList[j][6]     #latin transcript
                            
                            j = j + 1 #increment counter of the subitem loop by 1
                            
            i = i + 1 #increment counter of the item while loop by 1
        
        ###
        #Write all the information  we've stored so far into an xml file
        ###
        
        xmlFile = open(xmlFileName, 'w') 
        
        reparsed = minidom.parseString(ET.tostring(Itemset)) 
        
        thetext = reparsed.toprettyxml(indent='  ')
        
        #reference for the following 2 lines of code: http://stackoverflow.com/questions/749796/pretty-printing-xml-in-python
        text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)    
        prettyXml = text_re.sub('>\g<1></', thetext)
        
        xmlFile.write(prettyXml.encode("ascii","ignore"))
        
        xmlFile.close()                  
        
        #save path of xml file and change file name displayed in first window
        
        (self.openxmlfile_path).set(xmlFileName)
        
        shortname = xmlFileName.split("/")
        shortlength = len(shortname)
        xmlname = shortname[shortlength - 1]
        
        (self.openxmlfile).set(xmlname)
        
        
        
root = Tk()
(root).title("XML Builder")

app = App(root)

root.mainloop()        
        
        
        
        
        
        
        
        