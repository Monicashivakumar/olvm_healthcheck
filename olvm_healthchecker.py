import os
from operator import itemgetter
from itertools import groupby
from datetime import datetime
import re

class result_storage:
    """
    A class used as a storage of generated results.
    
    Attributes
    ----------
        command_storage : dict
            The dictionary to store all results.
            The keys are are unique item names, values are the generated text results.
        command_table : list
            The list of all item names of command_storage.
        command_list_msg : list
            All messages that will be printed as an usage.
            
    Methods
    -------
        add(self,command,text)
            Add an item to the dictionary command_storage.
        append(self,command,text)
            Add text to the end of the corresponding result in the dictionary.
        get(self,command)
            Get the result of the given item name.
        print_command(self)
            Print the usage message.
        print_all(self)
            Print all results in the command_storage.
    
    """
    command_storage = {}
    command_table = []
    command_list_msg = []
    def __init__(self): pass

    def add(self,command,text):
        """
        Add an item to the dictionary "command_storage".
    
        Parameters
        ----------
            command : str
                Unique item name that is used to identify different results.
            text : str
                The result that is stored with unique item name.
                
        Returns
        -------
        None
        
        """
        self.command_table.append(command)
        self.command_storage[command] = text
        self.command_list_msg.append(str(len(self.command_storage)-1) + ": " + command)
    
    def append(self,command,text):
        """
        Add text to the end of the corresponding result in the dictionary.
    
        Parameters
        ----------
            command : str
                The item name that indicates which item in the dictionary is going to be updated.
            text : str
                The additional part that is going to be added to the result.
                
        Returns
        -------
        None
        
        """
        self.command_storage[command] = self.command_storage[command] + text
    def get(self,command):
        """
        Get the result of the given item name.
    
        Parameters
        ----------
            command : str
                The item name that indicates which item is going to be accessed.
                
        Returns
        -------
        None
        
        """
        return self.command_storage[command]
    def print_command(self):
        """
        Print the usage message.
        """
        self.command_list_msg.append(str(len(self.command_storage)) + ": Print all information")
        self.command_list_msg.append(str(len(self.command_storage)+1) + ": Exit")
        
        max_width = len(max(self.command_list_msg, key = len))
        msg = "+" + "-"*max_width + "+\n"
        for command in self.command_list_msg:
            msg += "|" + command + " "*(max_width-len(command)) + "|\n"
        msg += "+" + "-"*max_width + "+\n"
        while(True):
            try:
                num = int(raw_input(msg + "Please provide the number to get the corresponding information: "))
                if num < 0 or num > len(self.command_storage)+1:
                    print("Please provide the number in the list.")
                elif num == len(self.command_storage):
                    print(self.print_all())
                elif num == len(self.command_storage)+1:
                    exit()
                else:                                                                                                           
                    print(self.command_storage.get(self.command_table[num]))
            except KeyboardInterrupt:
                print("\n")
                exit()
            except ValueError:
                print("Invalid input type, please try again.\n")
                continue
    def print_all(self):
        """
        Print all results in the command_storage.
    
        Parameters
        ----------
        None
        
        Returns
        -------
            output_txt : str
                The text of all values in command_storage.
        
        """
        output_txt = ""
        for key in self.command_table:
            if '-' not in key:
                output_txt += self.command_storage.get(key) + "\n\n\n"
        
        return output_txt
            
        

class path_collection:
    """
    A class used as a collection of useful directory or path.
    
    Attributes
    ----------
        sosreport_date : list
            The date sosreport created, e.g. ["2021","06","16"].
        sosreport_filename : str
            The name of the sosreport.
        sosreport : str
            The path of sosreport in log-collector-data folder.
        sosreport_engine : str
            The path of engine sosreport.
        log_collector_data : str
            The path of log-collector-data folder.
        sql_file : str
            The path of restore.sql.
        output_dir : str
            The directory of the output folder.
        output_path : str
            The path of the output folder.
        output_txt : str
            The path of the text folder in the output folder.
    Methods
    -------
    None
    
    
    """
    sosreport_date = []
    sosreport_filename = ""
    sosreport = ""
    sosreport_engine = ""
    log_collector_data = ""
    sql_file = ""
    output_dir = ""
    output_path = ""
    output_txt = ""
    
    def __init__(self,sosreport_path,output_dir,dt_string):
        """
        Constructs a collection of useful path for the given directory.

        Parameters
        ----------
            sosreport_path : str
                The path of the sosreport with a log-collector-data and an engine sosreport inside.
            output_dir : str
                The path of the output folder.
            dt_string : str
                The current local date and time.
                
        """
      #  if str(os.path.basename(sosreport_path)).endswith(".tar.xz"):
       #     os.system("cd "+ os.path.dirname(sosreport_path) + "; tar -xf " + os.path.basename(sosreport_path))
        #    sosreport_path = sosreport_path[:str(sosreport_path).find(".tar.xz")]
        
        self.sosreport_filename = os.path.basename(sosreport_path)
        date_str = str(self.sosreport_filename).partition("-LogCollector-")[2]
        self.sosreport_date.append(date_str[:4])
        self.sosreport_date.append(date_str[4:6])
        self.sosreport_date.append(date_str[6:8])
        self.output_dir = output_dir
        
        # log_collector_data and sosreport_engine
        # parent_folder = os.path.join(os.getcwd(), sosreport)
        for file_name in os.listdir(sosreport_path):
            if file_name == 'log-collector-data':
                if self.log_collector_data != "":
                    print("There are more than one log-collector-data.")
                else:
                    self.log_collector_data = os.path.join(sosreport_path, "log-collector-data")
            elif str(file_name).startswith("sosreport-"):
                if self.sosreport_engine != "":
                    print("There are more than one engine-sosreport.")
                else:
                    self.sosreport_engine = os.path.join(sosreport_path, file_name)
        
        if self.log_collector_data == "":
            print("There is no log-collector-data.")
        if self.sosreport_engine == "":
            print("There is no engine-sosreport.")
        
        
        # Output folder
        self.output_path = os.path.join(self.output_dir, "olvm_healthchecker_output_" + date_str)
        if os.path.basename(self.output_path) not in os.listdir(self.output_dir):
            os.mkdir(os.path.join(self.output_dir, "olvm_healthchecker_output_" + date_str))
        
        
        # Untar sosreport in log-collector-data
        untar(self.log_collector_data, 'sosreport', 'tar.xz')
        files_with_date = list(filter(lambda x: x.find(self.sosreport_date[0]+"-"+self.sosreport_date[1]+"-"+self.sosreport_date[2]) != -1, os.listdir(self.log_collector_data)))
        if len(files_with_date) == 0:
            print("No sosreport in the log-collector-data folder.")
        else:
            for file_name in files_with_date:
                if not str(file_name).endswith(".tar.xz") and not str(file_name).endswith(".md5"):
                    self.sosreport = os.path.join(self.log_collector_data,file_name)
        if self.sosreport == "":
            print("sosreport in log-collector-data was not untarred successfully.")
        
        # Untar pgdump-scl-rh-postgresql10 in postgresql
        untar(os.path.join(self.sosreport,"sos_commands","postgresql"), 'pgdump', 'tar')
        
        # restore.sql:
        sosreport_log = list(filter(lambda x: x.startswith('sosreport-'), os.listdir(self.log_collector_data)))
        if len(sosreport_log) != 1:
            print("Correct start path not given. Please input again.")
        else:
            # restore_sql = open(os.path.join(self.log_collector_data, sosreport_log[0], "sos_commands", "postgresql", "pgdump-scl-rh-postgresql10", "restore.sql"))
            restore_sql = open(os.path.join(self.log_collector_data, sosreport_log[0], "sos_commands", "postgresql", "restore.sql"))
            self.sql_file = restore_sql.read()
            restore_sql.close()
            # return sql_file
        
        # Output - txt:
        self.output_txt = open(os.path.join(self.output_path, "olvm_healthchecker_" + dt_string + ".txt"), 'w')


class Html_builder:
    """
    A class used to build a HTML file with elements.
    
    Attributes
    ----------
        tabs : list
            List of the HTML class attributes for all tabs.
        element_html : list
            List for element in HTML file, including:
                - table with information fetched from restore.sql.
                - div with information fetched from specific directory for different hosts.
        table_counter : int
            Number of tables that is used to assign different id for each table.
        style : str
            Style sheet to HTML file.
        script : str
            Functions written by JavaScript code.
        
    Methods
    -------
        add_table(self,class_att,name_info,name_table,header,rows,show_col)
            Add a table element to the Html_builder object.
        add_collapsible(self,class_att_button,class_att_content,text)
            Add a collapsible button to the Html_builder object.
        add_div(self,class_att,text)
            Add a <div> section to the Html_builder object.
        generate_file(self)
            Generate an HTML file with all elements.
    
    """
    tabs = []
    element_html = []
    table_counter = 0
    styles = "<style>\
                /* Hide scrollbar for Chrome, Safari and Opera */\
                    .tabcontent::-webkit-scrollbar {\
                    display: none;\
                }\
                /* Hide scrollbar for IE, Edge and Firefox */\
                .tabcontent {\
                    -ms-overflow-style: none;  /* IE and Edge */\
                    scrollbar-width: none;  /* Firefox */\
                }\
                table {\
                    font-family: arial, sans-serif;\
                    border-collapse: collapse;\
                    width: 100%;\
                    overflow:scroll;\
                }\
                /* Style the table */\
                td,th {\
                    border: 1px solid #dddddd;\
                    text-align: left;\
                    padding: 8px;\
                }\
                tr:nth-child(even){\
                    background-color: #dddddd;\
                }\
                /* Style the tab */\
                .tab {\
                    overflow: hidden;\
                    border: 1px solid #ccc;\
                    background-color: #f1f1f1;\
                }\
                /* Style the buttons inside the tab */\
                .tab button {\
                    background-color: inherit;\
                    float: left;\
                    border: none;\
                    outline: none;\
                    cursor: pointer;\
                    padding: 14px 16px;\
                    transition: 0.3s;\
                    font-size: 17px;\
                }\
                /* Change background color of buttons on hover */\
                .tab button:hover {\
                    background-color: #ddd;\
                }\
                /* Change background color of active tab button */\
                .tab button.active_tab {\
                    background-color: #ccc;\
                }\
                /* Style the tab content */\
                .tabcontent {\
                    display: none;\
                    padding: 6px 12px;\
                    border: 1px solid #ccc;\
                    border-top: none;\
                    overflow:scroll;\
                }\
                /* Style the collapsible button */\
                .collapsible {\
                    background-color: #777;\
                    color: white;\
                    cursor: pointer;\
                    padding: 18px;\
                    width: 100%;\
                    border: none;\
                    text-align: left;\
                    outline: none;\
                    font-size: 15px;\
                }\
                /* Change the color when hover on the collapsible button */\
                .collapsible:hover {\
                    background-color: #555;\
                }\
            </style>"
    
    script = "<script>\
            function show_hide_column(id_of_table,col_no, do_show) {\
                var stl;\
                if (do_show) stl = '';\
                else stl = 'none';\
                var tbl  = document.getElementById(id_of_table);\
                var rows = tbl.getElementsByTagName('tr');\
                for (var row=1; row<rows.length;row++) {\
                  var cels = rows[row].getElementsByTagName('td');\
                  cels[col_no].style.display=stl;\
                }\
                var head = tbl.getElementsByTagName('th');\
                head[col_no].style.display=stl;\
            }\
            function openTab(evt, class_att) {\
                var i, tabcontent, tablinks;\
                tabcontent_all = document.getElementsByClassName(\"tabcontent\");\
                for (i = 0; i < tabcontent_all.length; i++) {\
                  tabcontent_all[i].style.display = \"none\";\
                }\
                tablinks = document.getElementsByClassName(\"tablinks\");\
                for (i = 0; i < tablinks.length; i++) {\
                  tablinks[i].className = tablinks[i].className.replace(\" active_tab\", \"\");\
                }\
                tabcontent_show = document.getElementsByClassName(class_att);\
                for (i = 0; i < tabcontent_show.length; i++) {\
                  tabcontent_show[i].style.display = \"block\";\
                }\
                evt.currentTarget.className += \" active_tab\";\
            }\
            function openCollapsible(class_att_button,class_att_content) {\
                var coll = document.getElementsByClassName(class_att_button+\"_\"+class_att_content);\
                var i;\
                for (i = 0; i < coll.length; i++) {\
                    if (coll[i].style.display === \"block\") {\
                      coll[i].style.display = \"none\";\
                    } else {\
                      coll[i].style.display = \"block\";\
                    }\
                }\
            }\
            </script>"
            
            
    def __init__(self,tabs):
        """
        Constructs all the necessary attributes for the Html_builder object.

        Parameters
        ----------
            tabs : list
                List of the HTML class attributes for all tabs.
        """
        self.tabs = tabs
    
    def add_table(self,class_att,name_info,name_table,header,rows,show_col):
        """
        Add a table element to the Html_builder object.

        Parameters
        ----------
            class_att : str
                HTML class attribute for this table, it is used to categorize tables for tabs and collapsible buttons.
                There are two kinds of attribute: <Tab name> or <Tab name>_<Database | Hosts | Hosted_Engine>, the former will be shown when tab clicked, the latter will be shown when the collapsible button clicked
            name_info : str
                Table name that indicates the information or purpose of the table, e.g. 'KVM Hosts'
            name_table: str
                Table name in restore.sql, e.g. 'public.vds_static'
            header : list
                List of column names of the table.
            rows : list
                List of all row entries of the table.
            show_col : list
                List of the column indexes that need to be shown when the HTML file is created
                
        Returns
        -------
        None
        
        """
        
        self.table_counter += 1
        table_str = "<div class=\"tabcontent "+class_att+"\"><h3>"+name_info+"</h3><h5>(This table is fetched from "+name_table+" table in restore.sql)</h5>"
        
        # Filter button
        table_str += '<form><label>Column filter:</label><select name=filter_col_no>'
        for idx,col in enumerate(header):
            table_str += '<option value=\''+str(idx)+'\'>' + col + '</option>'
        table_str += '</select>'
        table_str += "<input type='button' onClick=\"javascript:show_hide_column('table_id_"+str(self.table_counter)+"',filter_col_no.value,  true);\" value='show'>\
                  <input type='button' onClick=\"javascript:show_hide_column('table_id_"+str(self.table_counter)+"',filter_col_no.value, false);\" value='hide'></form>"
        
        # Header
        table_str += '<table id=\'table_id_'+str(self.table_counter)+'\'><tr>'
        for idx,col in enumerate(header):
            if idx in show_col:
                table_str += '<th>' + col + '</th>'
            else:
                table_str += "<th style=\"display: none;\">" + col + "</th>"
        table_str += '</tr>'
        
        # Rows
        for row in rows:
            table_str += '<tr>'
            for idx,grid in enumerate(row):
                if idx in show_col:
                    if str(grid) == "Not a match":
                        table_str += '<td style=\"color: Red;\">' + grid + '</td>'
                    elif str(grid) == "Match":
                        table_str += '<td style=\"color: Green;\">' + grid + '</td>'
                    else:
                        if re.search("<*>",grid) != None:
                            table_str += '<td>' + str(grid).replace("<", "&lt;").replace(">", "&gt;") + '</td>'
                        else:
                            table_str += '<td>' + grid + '</td>'
                else:
                    if str(grid) == "Not a match":
                        table_str += "<td style=\"display: none, color: Red;\">" + grid + "</td>"
                    elif str(grid) == "Match":
                        table_str += "<td style=\"display: none, color: Green;\">" + grid + "</td>"
                    else:
                        if re.search("<*>",grid) != None:
                            table_str += "<td style=\"display: none;\">" + str(grid).replace("<", "&lt;").replace(">", "&gt;") + "</td>"
                        else:
                            table_str += "<td style=\"display: none;\">" + grid + "</td>"
            table_str += '</tr>'
        
        table_str += '</table></div>'
        self.element_html.append(table_str)
    
    def add_collapsible(self,class_att_button,class_att_content,text):
        """
        Add a collapsible button to the Html_builder object.

        Parameters
        ----------
            class_att_button : str
                HTML class attribute for this collapsible button.
            class_att_content : str
                HTML class attribute for elements in this collapsible section.
            text : str
                The contents of the collapsible section.
                
        Returns
        -------
        None
        
        """
        
        self.element_html.append("<button type=\"button\" class=\"tabcontent collapsible "+class_att_button+"\" onClick=\"javascript:openCollapsible('"+class_att_button+"','"+class_att_content+"');\">"+text+"</button>")
    
    def add_div(self,class_att,text):
        """
        Add a <div> section to the Html_builder object.

        Parameters
        ----------
            class_att : str
                HTML class attribute for this <div> section.
            text: str
                The contents of this <div> section.
                
        Returns
        -------
        None
        
        """
        
        self.element_html.append("<div class=\"tabcontent "+class_att+"\" style=\"white-space: pre-wrap;\">"+text+"</div>")
    
    def generate_file(self,dt_string):
        """
        Generate an HTML file with all elements.
        
        Parameters
        ----------
            dt_string : str
                    The current local date and time.
                    
        """
        html = open(os.path.join(path.output_path, "olvm_healthchecker_"+dt_string+".html"), 'w')
        html.write('<html><head>' + self.styles + self.script+'</head><body><h1>OLVM Report</h1>')
        tab_div = "<div class=\"tab\">"
        
        for tab in self.tabs:
            tab_div += "<button class=\"tablinks\" onclick=\"openTab(event, '"+tab.replace(" ","")+"')\">"+tab+"</button>"
        tab_div += "</div>"
                    
        html.write(tab_div)
        for ele in self.element_html:
            html.write(ele)
        
        html.write('</body></html>')
    
def untar(path,head,tail):
    """
    Extract the archive with specific pattern and locate in given directory.
    
    Parameters
    ----------
        path : str
            Location of the file.
        head : str
            The prefix of the file extracted.
        tail : str
            The last part of the tar file name that indicates compression, e.g. '.tar.xz' or 'tar'
            
    Returns
    -------
    None

    """
    
    zipped_files = []
    unzipped = False
    for file_name in os.listdir(path):
        if str(file_name).endswith(tail):
            zipped_files.append(file_name)
        elif str(file_name).startswith(head) and not str(file_name).startswith(tail):
            unzipped = True
    if unzipped is False:
        if len(zipped_files) > 1:
            print("There should be exactly one tar file to be untarred.")
        elif len(zipped_files) == 1:
            os.system("cd "+path+"; tar -xf " + zipped_files[0]) #  + " > /dev/null"
            # if str(tail).endswith("xz"):
            #     os.system("cd "+path+"; tar -zxvf " + zipped_files[0] + " > /dev/null")
            #     # tar_file = lzma.open(os.path.join(path,zipped_files[0]))
            # else:
            #     tar_file = tarfile.open(os.path.join(path,zipped_files[0]))
            #     tar_file.extractall()
            #     tar_file.close()


def format_table(dat_dict,show_column):
    """
    Print as a table formatting.

    Parameters
    ----------
        dat_dict : dict
            Relevant info in dat. file.
            Structure of an item in dat_dict: "<name_table>": ['<name_dat>',['<col_names>'],[<bigest length of rows in each column>],[[<row1>],[<row2>],[<row3>]]]
            e.g. 'public.network': ['7459.dat',  ['id', 'name', 'mtu'], [2,9,4], [['0', 'Storage', '9000'], ['1', 'ovirtmgmt', '9000'],...]]
        show_col : list
            List of the column indexes that need to be printed.
            
    Returns
    -------
        return_txt : str
            String of the generated formatting table.
    
    """
    
    max_width = 80
    header = dat_dict[1]
    col_space = dat_dict[2]
    rows = dat_dict[3]
    divider_row = "" 
    divider_header = ""
    return_txt = ""
    
    # Adjust the column width
    for idx,width in enumerate(col_space):
        if idx in show_column or show_column[0] == 'filter_disable':
            if width > max_width:
                col_space[idx] = max_width
            if col_space[idx] <= len(header[idx]):
                col_space[idx] = len(header[idx])  
            divider_row += "+"+"-"*col_space[idx]
            divider_header += "+"+"="*col_space[idx]
    divider_row += "+\n"
    divider_header += "+\n"
    
    # Print out the header
    return_txt += divider_row
    for idx,width in enumerate(col_space):
        if idx in show_column:
            return_txt += "|" + header[idx] + " "*(width-len(header[idx]))
    return_txt += "|\n"+divider_header
    
    # Print out all rows
    for row in rows:
        rest = row[:]
        need_next_line = len(col_space)
        while need_next_line > 0:
            need_next_line = len(col_space)
            for idx,width in enumerate(col_space):      
                if idx in show_column:
                    cur_line = ""
                    if rest[idx] != "":
                        if len(rest[idx]) > max_width:
                            cur_line = rest[idx][:max_width]
                            rest[idx] = rest[idx][max_width:]
                        else:
                            cur_line = rest[idx]
                            rest[idx] = ""
                            need_next_line -= 1
                    else:
                        need_next_line -= 1
                    return_txt += "|" + cur_line + " "*(width-len(cur_line))
                else:
                    need_next_line -= 1
            return_txt += "|\n"
        return_txt += divider_row
    return return_txt
def format_group(dat_dict,order,show_col):
    """
    Print as a group formatting by following the specific order.

    Parameters
    ----------
        dat_dict : dict
            Relevant info in dat. file.
            Structure of an item in dat_dict: "<name_table>": ['<name_dat>',['<col_names>'],[<bigest length of rows in each column>],[[<row1>],[<row2>],[<row3>]]]
            e.g. 'public.network': ['7459.dat',  ['id', 'name', 'mtu'], [2,9,4], [['0', 'Storage', '9000'], ['1', 'ovirtmgmt', '9000'],...]]
        order : list
            List of the column indexes in the order of the hierarchy.
        show_col : list
            List of the column indexes that need to be printed.
            
    Returns
    -------
        result_trim : str
            String of the generated formatting table.
    
    """
    
    header = dat_dict[1]
    rows = dat_dict[3]
    indent_size = 4
    indent_unit = " " * indent_size
    divider_entry_size = 40
    divider_entry = "-" * divider_entry_size + "\n"
    # Sort by the order 
    rows.sort(key=itemgetter(*order))
    
    # Group by the order
    current_hierarchy = {} # Same values shared with all rows in the current hierarchy e.output_file_txt.{col_idx: col value}
    global printout_str
    printout_str = "" # Initialization (In case something left by other calling)
    def group_print(counter):
        '''Print all entries in current order.'''
        global printout_str
        def rows_print(row,identical_values):
            """
            Print the entries at the bottom of the hierarchy with list format.
            
            Parameters
            ----------
                row : list
                    The row entry.
                identical_values : list
                    The list of columns that don't need to be printed since these are identical far all entries in this hierarchy.
                    
            Returns
            -------
            None
            
            """
            global printout_str
            printout_str += str(indent_unit * len(identical_values)) + divider_entry
            for col_idx, col_name in enumerate(header):
                if col_idx not in identical_values and col_idx in show_col:
                    printout_str += str(indent_unit * len(identical_values)) + col_name + ": " + row[col_idx] + "\n"
            printout_str += str(indent_unit * len(identical_values)) + divider_entry
            
            
        for elt, items in groupby(rows, itemgetter(order[counter])):
            current_hierarchy[order[counter]] = elt
            
            # Print the name of current hierarchy
            printout_str += " "*indent_size*counter + header[order[counter]] + ": " + elt + "\n"
            if counter == len(order)-1:
                # Check if the row is belong to this bottom hierarchy
                for i in items:
                    check_pass = True 
                    for key in current_hierarchy:
                        if i[key] != current_hierarchy.get(key): check_pass = False
                    if check_pass == True: 
                        rows_print(i,current_hierarchy.keys())
            else:
                group_print(counter+1)
    
    group_print(0)
    # Modify the result string by deleting unnecessary lines
    result_trim = ""
    printout_string_lines = printout_str.split("\n")
    if len(printout_string_lines) != 1: # Only one line
        for line_idx,line in enumerate(printout_string_lines[:-1]):
            space_size = len(line) - len(line.lstrip())
            if line_idx != 0:
                line_last = printout_string_lines[line_idx-1]
                space_size_last = len(line_last) - len(line_last.lstrip())
            if line_idx != range(len(printout_str.split("\n"))-1):
                line_next = printout_string_lines[line_idx+1]
                space_size_next = len(line_next) - len(line_next.lstrip())
            
            if line_idx == 0:
                # The first line
                if space_size != space_size_next:
                    result_trim += line + "\n"
            elif line_idx != range(len(printout_string_lines)-1): #################
                # The line in the middle
                if line.lstrip().startswith("-----"):  #################
                    if line_last.lstrip().startswith("-----"):
                        continue
                    else:
                        result_trim += line + "\n"
                elif space_size_next > space_size or (space_size_last == space_size and space_size_next == space_size):
                    key_pre = line_last[:line_last.find(": ")]
                    key_cur = line[:line.find(": ")]
                    key_next = line_next[:line_next.find(": ")]
                    if not (key_pre == key_cur and key_cur == key_next):
                        result_trim += line + "\n"
            else:
                # Last line
                if space_size == space_size_last and space_size != 0:
                    result_trim += line + "\n"
                    
    return result_trim

    
'''                                
==================================================================--Network Information from Database--==================================================================
'''

def dat_info(class_att,name_info,name_table,format_info,filter_info,sort_info,result_storage_key,result_storage):
    """
    Get information in given table from restore.sql, print out with given format after filtering and sorting. 
    
    Parameters
    ----------
        class_att : str
            HTML class attribute that is used when add a table in HTML file, indicates which tabs or collapsible buttons it locates.
            There are two kinds of attribute: <Tab name> or <Tab name>_<Collipsible button name>, the former will be shown when tab clicked, the latter will be shown when the collapsible button is clicked.
        name_info : str
            Table name that indicates the information or purpose of the table, e.g. 'KVM Hosts'.
        name_table : str
            Table name in restore.sql, e.g. 'public.vds_static'.
        format_info : list
            Format related information. There are two kinds of format_info: ['table'] and ['group',[<hierachy order>]].
        filter_info : dict
            Dictionary with two filter related items. 
            <filter type> can be 'filter_in', 'filter_out', or 'filter_disable'.
            'col_value' is to filter a specific column for given values and 'col_index' is to filter given column by index. 
            e.g. filter_info = {
                'col_value':[<filter type>,<column index>,[<filter value>]],
                'col_index':[<filter type>,[<column index>]]
                }
        sort_info : list
            Index list of the column to be sorted.
        result_storage_key : str
            The unique name that will be used as a key while storing result in the dictionary result_storage.
        result_storage : dict
            The dictionary that stores all generated results. 
            
    Returns
    -------
        dat_dict : dict
            Dictionary of all information from dat. files.
            structure of an item: "<name_table>": ['<name_dat>',['<col_names>'],[<bigest length of rows in each column>],[[<row1>],[<row2>],[<row3>]]]
            e.g. output_file_txt. {'public.network': ['7459.dat',  ['id', 'name', 'mtu'], [2,9,4], [['0', 'Storage', '9000'], ['1', 'ovirtmgmt', '9000'],...]]
        
    """
    
    
    dat_dict = {}
    def dat_to_dict(info_dict):
        """Store information in dat. file to the dictionary."""
        # parent_path = os.path.join(path.log_collector_data, path.sosreport, "sos_commands", "postgresql","pgdump-scl-rh-postgresql10") ######################################3
        parent_path = os.path.join(path.sosreport, "sos_commands", "postgresql") #path.log_collector_data, 
        dat = open(os.path.join(parent_path, info_dict[0]))
        col_num = len(info_dict[1]) # Number of the column
        col_space = [0]*col_num # The largest string size in each column
        info_dict.append([])
        info_dict.append([]) # Append an empty row for col_space and rows in dat. file
        
        filter_type = filter_info.get('col_value')[0]
        filter_col = filter_info.get('col_value')[1] if filter_type != 'filter_disable' else []
        filter_values = filter_info.get('col_value')[2] if filter_type != 'filter_disable' else []
        for line in dat:
            # Separate the line for different column
            line.replace(" ","").replace("\n","").replace("\t",",").strip()
            grid = line.split("\t")
        
            if len(grid) == col_num:
                if (filter_type == 'filter_out' and any(x not in grid[filter_col] for x in filter_values)) or (filter_type == 'filter_in' and any(x in grid[filter_col] for x in filter_values)) or filter_type == 'filter_disable':
                    grid[len(grid)-1] = grid[len(grid)-1][:-1] # Remove \n in the end of every line
                    info_dict[3].append(grid) # Append the new row
                    for i in range(len(grid)):
                        if len(grid[i]) > col_space[i]:
                            col_space[i] = len(grid[i]) 
        info_dict[2] = col_space
        dat.close()
    
    # Look into the .sql file
    sql_commands = [x.strip() for x in path.sql_file.split(';')]
    for command in sql_commands:
        start_from = command.find('COPY '+name_table + " ")
        dat_end = command.find('.dat')
    
        if start_from != -1 and dat_end != -1:
            # Find column names
            col_left = command.find('(',start_from)
            col_right = command.find(')',start_from)
            col_names = [x.strip() for x in command[col_left+1:col_right].split(',')]
            # Find .dat file name
            dat_start = dat_end
            while command[dat_start] != '/':
                dat_start -= 1
            dat_name = command[dat_start+1:dat_end+4]
    
            dat_dict[command[start_from+5:col_left-1]] = [dat_name,col_names]
    # Look into the .dat files
    txt_tmp = ""
    for info_key,info_values in dat_dict.items():
        txt_tmp += "\n\n" + name_info + "\n"
        txt_tmp += "(This table is fetched from " + info_key + " table in restore.sql)\n"
        dat_to_dict(info_values)
        
        # Sort
        if sort_info[0] != 'sort_disable':
            info_values[3] = sorted(info_values[3], key=lambda x: x[sort_info[0]])
        # Filter
        if filter_info.get('col_index')[0] == 'filter_disable':
            show_column = [idx for idx in range(len(info_values[1]))]
        elif filter_info.get('col_index')[0] == 'filter_out':
            show_column = [idx for idx in range(len(info_values[1])) if idx not in filter_info.get('col_index')[1]]
        else:
            show_column = filter_info.get('col_index')[1]
        
        html_builder.add_table(class_att,name_info,info_key,info_values[1],info_values[3],show_column) 
        if format_info[0] == 'table':
            txt_tmp += format_table(info_values,show_column)
        elif format_info[0] == 'group':
            txt_tmp += format_group(info_values,format_info[1],show_column)
    
    result_storage.append(result_storage_key,txt_tmp)
    return dat_dict

def search_dat_by_col(column_key):
    """
    Print all table names with the given column
    
    Parameters
    ----------
        column_key : str
            Column name that is used to find all tables with this in restore.sql, e.g. 'public.network'.
             
    Returns
    -------
    None
    
    """
    
    dat_dict = {}
    # Look into the .sql file
    sql_commands = [x.strip() for x in sql_file.split(';')]
    for command in sql_commands:
        start_from = command.find('COPY ')
        dat_end = command.find('.dat')
    
        if start_from != -1 and dat_end != -1:
            # Find column names
            col_left = command.find('(',start_from)
            col_right = command.find(')',start_from)
            col_names = [x.strip() for x in command[col_left+1:col_right].split(',')]
            if column_key in col_names:
                # Find .dat file name
                dat_start = dat_end
                while command[dat_start] != '/':
                    dat_start -= 1
                dat_name = command[dat_start+1:dat_end+4]
        
                # Put into the dictionary
                dat_dict[command[start_from+5:col_left-1]] = [dat_name,col_names]
    # Print a list of all relevant dat. files
    print('\n\nAll dat. files with the column, ' + column_key + ', included:\n')
    
    for dat_file in dat_dict.keys():
        print(dat_file + '\n') 
   

'''                                
==================================================================--Network Information from Hosts--==================================================================
'''
def info_from_engine(info_files):
    """
    Look into engine sosreport to fetch information.
    
    Parameters
    ----------
        info_files : dict
            Dictionary of all information that will be fetched for the engine.
            structure of an item in info_files: '<name_info>':[<directory of the file>,<filter_info>]
            e.g. "Version" : ["installed-rpms",['line',['ovirt-engine'],' ']]
            The filter information in this example means the file is read line by line, if the given string 'ovirt-engine' in this line, fetch the string before ' '.
    Returns
    -------
        info_str : str
            Information fetched from the given file.
    
    """
    info_str = ""
    for info in info_files.keys():
        info_str += "\n" + info + ":\n"
        if os.path.isfile(os.path.join(path.sosreport_engine,info_files.get(info)[0])):
            z = open(os.path.join(path.sosreport_engine,info_files.get(info)[0]))
            for i in z.readlines():
                if info_files.get(info)[1][0] == 'filter_disable': 
                    info_str += i
                elif info_files.get(info)[1][0] == 'line':
                    for grep in info_files.get(info)[1][1]:
                        if grep in i:
                            if len(info_files.get(info)[1]) > 2:
                                info_str += i[:i.find(info_files.get(info)[1][2])] + "\n"
                            else:
                                info_str += i + "\n"
        else: 
            print("The file '" + os.path.join(path.sosreport_engine,info_files.get(info)[0]) + "' is not exist.")
    return info_str

def info_from_host(host,info_files):
    """
    Look into host sosreport to fetch information.
    
    Parameters
    ----------
        host : str
            Host name.
        info_files : dict
            Dictionary of all information that will be fetched for the host.
            structure of an item in info_files: '<name_info>':[<directory of the file>,<filter_info>]
            e.g. "IP" : [os.path.join("sos_commands","networking","ip_-o_addr"),['line',['vdsm-4'],' ']]
            The filter information in this example means the file is read line by line, if the given string 'vdsm-4' in this line, fetch the string before ' '.
    Returns
    -------
        info_str : str
            Information fetched from the given file.
    
    """
    info_str = "\n================================Host: " + host + "================================\n"
    
    for info in info_files.keys():
        info_str += "\n" + info + ":\n"
        for file in os.listdir(os.path.join(path.log_collector_data,host)):
            host_name = host[:str(host).find(".")]
            if str(file).startswith("sosreport-" + host_name) and not str(file).endswith(".tar.xz"):
                info_file = str(os.path.join(path.log_collector_data, str(host), file, info_files.get(info)[0]))
                if os.path.isfile(info_file):
                    z = open(str(os.path.join(path.log_collector_data, str(host), file, info_files.get(info)[0])))
                    for i in z.readlines():
                        if info_files.get(info)[1][0] == 'filter_disable': 
                            info_str += i
                        elif info_files.get(info)[1][0] == 'line':
                            for grep in info_files.get(info)[1][1]:
                                if grep in i:
                                    if len(info_files.get(info)[1]) > 2:
                                        info_str += i[:i.find(info_files.get(info)[1][2])] + "\n"
                                    else:
                                        info_str += i + "\n"
    return info_str

def healthchecker(default_values,result_storage):
    """
    Compare provided default values to the actual values.
    
    Parameters
    ----------
        default_values : dict
            All default values.
        result_storage : dict
            The dictionary that stores all generated results.
            
    Returns
    -------
    None
    """
    config_dict = {}
    config_ele = []
    check_table_header = ["Name","Actual Value","Default Value","Check Result"]
    check_table_col_space = [0]*len(check_table_header)
    check_table_rows = []
    
    # Get all engine_config
    engine_config = open(os.path.join(path.sosreport_engine,"sos_commands","ovirt","engine-config_--all"))
    engine_config_split = engine_config.read().split("version: ")
    for idx,config in enumerate(engine_config_split):
        if idx == 0:
            config_ele.append(str(config[:str(config).find(": ")]).strip("\n"))
            config_ele.append(str(config).lstrip()[str(config).find(": ")+2:])
        else:
            config_ele.append(str(config).lstrip()[:str(config).find("\n")])
            if idx != len(engine_config_split)-1:
                config_ele.append(str(config[str(config).find("\n"):str(config).find(": ")]).strip("\n"))
                config_ele.append(str(config).strip()[str(config).find(": ")+2:])
    
    count = 0           
    for idx,ele in enumerate(config_ele[::3]):
        count += 1
        config_dict.setdefault(ele, []).append([config_ele[3*idx+1],config_ele[3*idx+2]])
    
    
    # Health check
    for key,value_list in default_values.items():
        if key not in config_dict.keys():
            print("The engine config doesn't have the entry: ",key)
        else:
            value_actual = ""
            value_default = value_list[0]
            if len(value_list) == 1:
            # No need to check for different versions now so get the first element #################version and <>
                value_actual = config_dict.get(key)[0][0]
            else:
                for ele in config_dict.get(key):
                    if ele[1] == value_list[1]:
                        value_actual = ele[0]
                if value_actual == "":
                    print("There is no value with this version.")
            if re.search("<*>",value_default) == None:
                match = 'Match' if value_default == value_actual else 'Not a match'
            else:
                match = 'Match' if value_default[value_default.find(":"):] == value_actual[value_actual.find(":"):] else 'Not a match'
                
            check_table_rows.append([key,value_actual,value_default,match])
            for row in check_table_rows:
                for idx in range(len(row)):
                    if len(row[idx]) > check_table_col_space[idx]:
                        check_table_col_space[idx] = len(row[idx]) 
                        
            
    
    show_column = [idx for idx in range(len(check_table_header))]
    txt_tmp = format_table(["Health Check",check_table_header,check_table_col_space,check_table_rows],show_column)
    html_builder.add_table("HealthCheck","Health Check","",check_table_header,check_table_rows,show_column)
    result_storage.append('Health Check',txt_tmp)
        
    
'''
========================================================================================================================================================================================
---------------------------------------------------------------------------------------All Output---------------------------------------------------------------------------------------
========================================================================================================================================================================================
'''
# Setup
# usage_text = ""
# print(usage_text)
# sosreport_path = os.path.realpath(raw_input("Enter the path of sosreport: "))
# output_dir = os.path.realpath(raw_input("Enter the directory of the output: "))
dt_string = datetime.now().strftime("%m%d%Y-%H%M%S")
try:
    
    #sosreport_path = os.path.realpath(raw_input("Enter the path of sosreport: "))
    sosreport_path = os.getcwd()
#    if '.tar' in sosreport_path:
#        while not os.path.isfile(sosreport_path):
#            sosreport_path = os.path.realpath(raw_input("There is no such file, please try again.\nEnter the path of sosreport: "))
#    else:
#        while not os.path.isdir(sosreport_path):
#           sosreport_path = os.path.realpath(raw_input("There is no such file, please try again.\nEnter the path of sosreport: "))
    
    #output_dir = os.path.realpath(raw_input("Enter the directory of the output: "))
    output_dir = os.getcwd()
#   while not os.path.isdir(output_dir):
#        output_dir = os.path.realpath(raw_input("There is no such directory, please try again.\nEnter the directory of the output: "))
        
except KeyboardInterrupt:
    print("\n")
    exit()
path = path_collection(sosreport_path,output_dir,dt_string)
usage = result_storage()
hosts = []
VMs_up = [] 
sql_file = path.sql_file
printout_str = ""
output_file_txt = path.output_txt
html_builder = Html_builder(["KVM Hosts","Virtual Machines","Versions","Network Topology","Storage Topology","Health Check","Error Events","Other"])

txt_kvmhosts = "\
============================================================================================================================\n\
---------------------------------------------------------KVM Hosts----------------------------------------------------------\n\
============================================================================================================================\n\
"
usage.add('KVM Hosts', txt_kvmhosts)
filter_info_vds_static = {
    'col_value':['filter_disable'],
    'col_index':['filter_in',[0,1,2,3,5]]
    }
KVMHosts_dic = dat_info('KVMHosts','KVM hosts','public.vds_static',['table'],filter_info_vds_static,['sort_disable'],'KVM Hosts',usage)
hosts = [i[3] for i in KVMHosts_dic.get('public.vds_static')[3]]
usage.append('KVM Hosts', "\nNumber of KVM hosts: " + str(len(hosts)) + "\n" + "\n")
usage.append('KVM Hosts', "Names of KVM hosts: "+ "\n")
for host in hosts: 
    usage.append('KVM Hosts', host+"\n")
    # Untar sosreport for hosts
#    untar(os.path.join(path.log_collector_data,host), 'sosreport', 'tar.xz')

txt_virtualmachines = "\
============================================================================================================================\n\
------------------------------------------------------Virtual Machines------------------------------------------------------\n\
============================================================================================================================\n\
"
usage.add('Virtual Machines', txt_virtualmachines)
usage.add('Virtual Machines - Database', "")
usage.add('Virtual Machines - Hosts', "")

usage.append('Virtual Machines - Database', "\nVirtual Machines Information for Database:\n")
html_builder.add_collapsible('VirtualMachines', 'Database', 'Virtual Machines Information for database')
    
filter_info_vm_dynamic = {
    'col_value':['filter_disable'],
    'col_index':['filter_in',[0,1,53]]
    }
VM_dic = dat_info('VirtualMachines_Database','Virtual Machines','public.vm_dynamic',['table'],filter_info_vm_dynamic,['sort_disable'],'Virtual Machines - Database',usage)
VMs_up = [i[53] for i in VM_dic.get('public.vm_dynamic')[3] if i[1] == '1']
usage.append('Virtual Machines - Database', "\n"+"Number of Virtual Machines that are Up: " + str(len(VMs_up)) + "\n" + "\n") #writing this info to report file
usage.append('Virtual Machines - Database', "Names of Virtual Machines that are Up: "+ "\n")
for i in VMs_up:
    usage.append('Virtual Machines - Database', i+"\n")

usage.append('Virtual Machines - Hosts', "\nVirtual Machines Information for Hosts:\n")
vm_hosts_info = ""
# vm_hosts_info += "This information is fetched by the commands:\n\
# $ cat sos_commands/virsh/virsh_-r_list_--all\n\
# $ cat sos_commands/vdsm/vdsm-client_Host_getAllVmStats |grep -B1 '\"status\":'\n"

html_builder.add_collapsible('VirtualMachines', 'Hosts', 'Virtual Machines Information for hosts')
vm_hosts_info_files = {"VM State" : [os.path.join("sos_commands", "virsh", "virsh_-r_list_--all"),['filter_disable']], 
                       "All VM stats" : [os.path.join("sos_commands", "vdsm", "vdsm-client_Host_getAllVmStats"),['line',['\"status\"','\"vmName\"'],',']]}

for host in hosts:
    vm_hosts_info += info_from_host(host,vm_hosts_info_files)
usage.append('Virtual Machines - Hosts', vm_hosts_info)
html_builder.add_div('VirtualMachines_Hosts', vm_hosts_info)

usage.append('Virtual Machines',usage.get('Virtual Machines - Database'))
usage.append('Virtual Machines',usage.get('Virtual Machines - Hosts'))

txt_versions = "\
============================================================================================================================\n\
----------------------------------------------------------Versions----------------------------------------------------------\n\
============================================================================================================================\n\
"
usage.add('Versions', txt_versions)
usage.add('Versions - Engine', "")
usage.add('Versions - Hosts', "")

usage.append('Versions - Engine', "\nVersions for Engine:\n")
versions_engine_info = ""
# versions_engine_info += "This information is fetched by the commands:\n\
# $ cat installed-rpms |grep ovirt-engine\n"

html_builder.add_collapsible('Versions', 'Engine', 'Versions for engine')
versions_engine_info_files = {"Version" : ["installed-rpms",['line',['ovirt-engine']]]}
versions_engine_info += info_from_engine(versions_engine_info_files)
usage.append('Versions - Engine', versions_engine_info)
html_builder.add_div('Versions_Engine', versions_engine_info)

usage.append('Versions - Hosts', "\nVersions for Hosts:\n")
versions_hosts_info = ""
# versions_hosts_info += "This information is fetched by the commands:\n\
# $ cat installed-rpms |grep vdsm-4\n\
# $ cat installed-rpms |grep libvirt-5\n\
# $ cat installed-rpms |grep qemu-system-x86\n"
html_builder.add_collapsible('Versions', 'Hosts', 'Versions for hosts')
versions_hosts_info_files = {"vdsm" : [os.path.join("sos_commands", "rpm", "sh_-c_rpm_--nodigest_-qa_--qf_NAME_-_VERSION_-_RELEASE_._ARCH_INSTALLTIME_date_awk_-F_printf_-59s_s_n_1_2_sort_-V"),['line',['vdsm-4']]], 
                             "libvirt" : [os.path.join("sos_commands", "rpm", "sh_-c_rpm_--nodigest_-qa_--qf_NAME_-_VERSION_-_RELEASE_._ARCH_INSTALLTIME_date_awk_-F_printf_-59s_s_n_1_2_sort_-V"),['line',['libvirt-5']]], 
                             "qemu" : [os.path.join("sos_commands", "rpm", "sh_-c_rpm_--nodigest_-qa_--qf_NAME_-_VERSION_-_RELEASE_._ARCH_INSTALLTIME_date_awk_-F_printf_-59s_s_n_1_2_sort_-V"),['line',['qemu-system-x86']]]}
for host in hosts:
    versions_hosts_info += info_from_host(host,versions_hosts_info_files)
usage.append('Versions - Hosts', versions_hosts_info)
html_builder.add_div('Versions_Hosts', versions_hosts_info)

usage.append('Versions', usage.get('Versions - Engine'))
usage.append('Versions', usage.get('Versions - Hosts'))


txt_networktopology = "\
============================================================================================================================\n\
------------------------------------------------------Network Topology------------------------------------------------------\n\
============================================================================================================================\n\
"
usage.add('Network Topology', txt_networktopology)
usage.add('Network Topology - Database', "")
usage.add('Network Topology - Hosts', "")

usage.append('Network Topology - Database', "\nNetwork Information for Database:\n")
html_builder.add_collapsible('NetworkTopology', 'Database', 'Network Topology for database')

filter_info_network = {
    'col_value':['filter_disable'],
    'col_index':['filter_in',[1,2,4,7,9,10,11]]
    }
dat_info('NetworkTopology_Database','Network','public.network',['table'],filter_info_network,['sort_disable'],'Network Topology - Database',usage) # ['group',[1],[]]

filter_info_network_cluster = {
    'col_value':['filter_disable'],
    'col_index':['filter_in',[1,2,3,4,8,9,10]]
    }
dat_info('NetworkTopology_Database','Network Attachments','public.network_attachments',['table'],filter_info_network_cluster,['sort_disable'],'Network Topology - Database',usage)

filter_info_network_cluster = {
    'col_value':['filter_disable'],
    'col_index':['filter_disable']
    }
dat_info('NetworkTopology_Database','Network Cluster','public.network_cluster',['table'],filter_info_network_cluster,['sort_disable'],'Network Topology - Database',usage)

filter_info_network_filter = {
    'col_value':['filter_disable'],
    'col_index':['filter_disable']
    }
dat_info('NetworkTopology_Database','Network Filter','public.network_filter',['table'],filter_info_network_filter,['sort_disable'],'Network Topology - Database',usage)

usage.append('Network Topology - Database', "\nNetwork Information for Hosts:\n")
network_hosts_hosts = ""
# network_hosts_hosts += "This information is fetched by the commands:\n\
# $ cat sos_commands/networking/ip_-o_addr\n\
# $ cat sos_commands/networking/route_-n\n\
# $ cat sos_commands/networking/bridge_-d_vlan_show\n\
# $ cat sos_commands/networking/ip_-s_-d_link\n"
html_builder.add_collapsible('NetworkTopology', 'Hosts', 'Network Topology for hosts')
network_hosts_info_files = {"IP" : [os.path.join("sos_commands","networking","ip_-o_addr"),['filter_disable']],
                            "Route" : [os.path.join("sos_commands","networking","route_-n"),['filter_disable']],
                            "Vlan" : [os.path.join("sos_commands","networking","bridge_-d_vlan_show"),['filter_disable']],
                            "TAP Device" : [os.path.join("sos_commands","networking","ip_-s_-d_link"),['filter_disable']]}
for host in hosts:
    network_hosts_hosts += info_from_host(host,network_hosts_info_files)
usage.append('Network Topology - Database',network_hosts_hosts)
html_builder.add_div('NetworkTopology_Hosts', network_hosts_hosts)

usage.append('Network Topology', usage.get('Network Topology - Database'))
usage.append('Network Topology', usage.get('Network Topology - Hosts'))

txt_storagetopology = "\
============================================================================================================================\n\
------------------------------------------------------Storage Topology------------------------------------------------------\n\
============================================================================================================================\n\
"
usage.add('Storage Topology', txt_storagetopology)
usage.add('Storage Topology - Database', "")
usage.add('Storage Topology - Hosts', "")

usage.append('Storage Topology - Database', "\nStorage Information for Database:\n")
html_builder.add_collapsible('StorageTopology', 'Database', 'Storage Topology for database')
filter_info_gluster_volumes = {
    'col_value':['filter_disable'],
    'col_index':['filter_in',[2,3,4,10]]
    }
dat_info('StorageTopology_Database','Volumes','public.gluster_volumes',['table'],filter_info_gluster_volumes,['sort_disable'],'Storage Topology - Database',usage) 
filter_info_storage_pool = {
    'col_value':['filter_disable'],
    'col_index':['filter_in',[1,2,3,5,8]]
    }
dat_info('StorageTopology_Database','Data Centers','public.storage_pool',['table'],filter_info_storage_pool,['sort_disable'],'Storage Topology - Database',usage) 
filter_info_base_disks = {
    'col_value':['filter_disable'],
    'col_index':['filter_in',[0,3,4,5,7,8,9,10]]
    }
dat_info('StorageTopology_Database','Storage Disks','public.base_disks',['table'],filter_info_base_disks,['sort_disable'],'Storage Topology - Database',usage) 
filter_info_storage_domain_static = {
    'col_value':['filter_disable'],
    'col_index':['filter_in',[2,3,4,5]]
    }
dat_info('StorageTopology_Database','Storage Domains','public.storage_domain_static',['table'],filter_info_storage_domain_static,['sort_disable'],'Storage Topology - Database',usage) 

usage.append('Storage Topology - Hosts',"\nStorage Information for Hosts:\n")
storage_hosts_info = ""
# storage_hosts_info += "This information is fetched by the commands:\n\
# $ cat sos_commands/vdsm/vdsm-client_Host_getConnectedStoragePools\n\
# $ cat sos_commands/vdsm/vdsm-client_Host_getStorageDomains\n"
html_builder.add_collapsible('StorageTopology', 'Hosts', 'Storage Topology for hosts')
storage_hosts_info_files = {"Connected Storage Pools" : [os.path.join("sos_commands","vdsm","vdsm-client_Host_getConnectedStoragePools"),['filter_disable']], 
                            "Storage Domains" : [os.path.join("sos_commands","vdsm","vdsm-client_Host_getStorageDomains"),['filter_disable']]}
for host in hosts:
    storage_hosts_info += info_from_host(host,storage_hosts_info_files)
usage.append('Storage Topology - Hosts',storage_hosts_info)
html_builder.add_div('StorageTopology_Hosts', storage_hosts_info)

usage.append('Storage Topology',usage.get('Storage Topology - Database'))
usage.append('Storage Topology',usage.get('Storage Topology - Hosts'))

txt_healthcheck = "\
============================================================================================================================\n\
--------------------------------------------------------Health Check---------------------------------------------------------\n\
============================================================================================================================\n\
"
usage.add('Health Check', txt_healthcheck)

txt_healthcheck += "\nHealth Check:\n"
default_values = {
    'vdsTimeout':['180'],
    'vdsConnectionTimeout':['20'],
    'VdsRefreshRate':['3'],
    'TimeoutToResetVdsInSeconds':['60'],
    'StoragePoolRefreshTimeInSeconds':['10'],
    'SpmVCpuConsumption':['1'],
    'SpmCommandFailOverRetries':['3'],
    'SPMFailOverAttempts':['3'],
    'DelayResetForSpmInSeconds':['20'],
    'StorageDomainFailureTimeoutInMinutes':['5'],
    'MaxStorageVdsTimeoutCheckSec':['30'],
    'MaxStorageVdsDelayCheckSec':['5'],
    'ImageProxyAddress': ['<OLVM FQDN>:54323', 'general'],
    'ImageTransferClientTicketValidityInSeconds':['36000'],
    'LogMaxNetworkUsedThresholdInPercentage':['95'],
    'MaxVdsMemOverCommit': ['200'],
    'MaxVdsMemOverCommitForServers': ['150'] ,
    'UserSessionTimeOutInterval': ['30']
    }
healthchecker(default_values,usage)


txt_errorevents = "\
============================================================================================================================\n\
--------------------------------------------------------Error Events--------------------------------------------------------\n\
============================================================================================================================\n\
"
usage.add('Error Events',txt_errorevents)
filter_info_audit_log = {
    'col_value':['filter_in',13,['error','Error','failed','Failed','except','Except']],
    'col_index':['filter_in',[9,13]]
    }
dat_info('ErrorEvents','Error Events','public.audit_log',['table'],filter_info_audit_log,[9],'Error Events',usage)


txt_other = "\
============================================================================================================================\n\
-----------------------------------------------------------Other------------------------------------------------------------\n\
============================================================================================================================\n\
"
usage.add('Other', txt_other)
usage.add('Other - Datacenter Tree for hosts', "")
usage.add('Other - Hosted Engine for hosts', "")

usage.append('Other - Datacenter Tree for hosts',"\nDatacenter Tree for Hosts:\n")
html_builder.add_collapsible('Other', 'Datacenter_Tree', 'Datacenter Tree for hosts')
datacenter_tree_hosts_info = ""
# datacenter_tree_hosts_info += "This information is fetched by the commands:\n\
# $ cat sos_commands/vdsm/su_vdsm_-s_.bin.sh_-c_tree_-l_.rhev.data-center\n"
datacenter_tree_hosts_info_files = {"Datacenter Tree" : [os.path.join("sos_commands","vdsm","su_vdsm_-s_.bin.sh_-c_tree_-l_.rhev.data-center"),['filter_disable']]}
for host in hosts:
    datacenter_tree_hosts_info += info_from_host(host,datacenter_tree_hosts_info_files)
usage.append('Other - Datacenter Tree for hosts',datacenter_tree_hosts_info)
html_builder.add_div('Other_Datacenter_Tree', datacenter_tree_hosts_info)


usage.append('Other - Hosted Engine for hosts', "\nHosted Engine for Hosts:\n")
html_builder.add_collapsible('Other', 'Hosted_Engine', 'Hosted Engine for hosts')
hosted_engine_hosts_info = ""
# hosted_engine_hosts_info += "This information is fetched by the commands:\n\
# $ cat etc/ovirt-hosted-engine/hosted-engine.conf  | egrep 'disk|sdUUID|spUUID|vmid'\n\
# $ cat sos_commands/ovirt_hosted_engine/hosted-engine_--vm-status\n\
# $ cat sos_commands/ovirt_hosted_engine/hosted-engine_--check-liveliness\n"
hosted_engine_hosts_info_files = {"Datacenter Tree" : [os.path.join("etc","ovirt-hosted-engine","hosted-engine.conf"),['line',['disk','sdUUID','spUUID','vmid']]],
                                  "Liveliness":[os.path.join("sos_commands","ovirt_hosted_engine","hosted-engine_--check-liveliness"),['filder_disable']]}
for host in hosts:
    hosted_engine_hosts_info += info_from_host(host,hosted_engine_hosts_info_files)
usage.append('Other - Hosted Engine for hosts', hosted_engine_hosts_info)
html_builder.add_div('Other_Hosted_Engine', hosted_engine_hosts_info)

usage.append('Other', usage.get('Other - Datacenter Tree for hosts'))
usage.append('Other', usage.get('Other - Hosted Engine for hosts'))

html_builder.generate_file(dt_string)
output_file_txt.write(usage.print_all())

'''
Print a message block after all files generated successfully.
'''
generated_msg = []
generated_msg.append("Files are generated successfully!")
generated_msg.append("")
generated_msg.append("Source sosreport:")
generated_msg.append(sosreport_path)
generated_msg.append("Directory of the output files:")
generated_msg.append(path.output_path)
generated_msg.append("Generated files:")
generated_msg.append("olvm_healthchecker_" + dt_string + ".txt")
generated_msg.append("olvm_healthchecker_" + dt_string + ".html")
max_width = len(max(generated_msg, key = len))
msg = "+" + "="*max_width + "+\n"
for idx,command in enumerate(generated_msg):
    if idx == 1:
        msg += "+" + "-"*max_width + "+\n"
    else:
        msg += "|" + command + " "*(max_width-len(command)) + "|\n"
msg += "+" + "="*max_width + "+\n"
print(msg)
usage.print_command()
