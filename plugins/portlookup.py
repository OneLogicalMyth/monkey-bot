import csv
import json
import os


class portlookup(object):

    def start(self, command, rootpath):
        message = 'Sorry I do not understand what port number you are requesting.'
        attachment = False

        self.port_list = []
        with open(rootpath + '/resources/portlookup/service-names-port-numbers.csv', mode='r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                row_out = {"short": True, "title": "{}/{}".format(row[1], row[2]).upper(), "value": "{} - {}".format(row[0], row[3])}
                self.port_list.append(row_out)

        if command.startswith('port'):
            if ' ' in command:  # check for space
                if not command.split(' ')[1].isdigit():
                    return "That's a funny looking port number :thinking_face:", attachment
                PortNo = "{}/".format(command.split(' ')[1])  # add the slash so it matches correctly
                if PortNo:
                    PortDetail = [d for d in self.port_list if d['title'].startswith(PortNo)]
                    attachment = True
                    if PortDetail:
                        port_file = rootpath + '/resources/portlookup/' + str(PortNo)[:-1] + '.json'
                        file_exists = os.path.isfile(port_file)
                        if file_exists:
                            with open(port_file, 'r') as port_file_json:
                                port_info = json.load(port_file_json)
                                if "Notes" in port_info:
                                    PortDetail.append({"short": False, "title": "Notes", "value": "{}".format('\n'.join(port_info["Notes"]))})
                                if "URLs" in port_info:
                                    PortDetail.append({"short": False, "title": "URLs", "value": "{}".format('\n'.join(port_info["URLs"]))})
                        message = [
                            {
                                "fallback": "blah",
                                "pretext": "The following port details were found:",
                                "fields": PortDetail
                            }
                        ]
                    else:
                        message = [
                            {
                                "fallback": "blah",
                                "pretext": "No port details found, was it a private port?\n\n System Ports (0-1023)\nUser Ports (1024-49151)\nDynamic and/or Private Ports (49152-65535)\n\n<https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml|Manually lookup on iana>"
                            }
                        ]

        return message, attachment
