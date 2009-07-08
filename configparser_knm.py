import ConfigParser             # knm config
import xml.dom.minidom
import os
import dbus                     # maybe reduce deps and postprocess dbus.Byte?

class ConfigParserKNM:
    "Parse ~/.kde/share/config/knetworkmanagerrc"

    def __init__(self):
        p = ConfigParser.RawConfigParser()
        ok = p.read(os.getenv("HOME") + "/.kde/share/config/knetworkmanagerrc")

        self.conmaps_d = {}
        for s in p.sections():
            path = s.split("_")
            #print "##", path
            if path[0] in ["ConnectionSetting", "ConnectionSecrets"]:
                cid = path[1]
                self.conmaps_d.setdefault(cid, {})
                part = path[2]

                values = {}
                for (n, v) in p.items(s):
                    # WTF, Value_ is transformed to value_
                    if n[:6]  == "value_":
                        n = n[6:]
                        v = self.ParseValue(v)
                        #print "# %s:%s" % (n, v)
                        # do not overwrite ConnectionSecrets
                        # with empty ConnectionSettings field
                        try:
                            vv = self.conmaps_d[cid][part][n]
                        except KeyError:
                            vv = ""
                        if vv == "":
                            values[n] = v
                if len(values) != 0: # empty 802-1x confuses NM!?
                    self.conmaps_d[cid].setdefault(part, {})
                    self.conmaps_d[cid][part].update(**values)
                #print "PARSED", cid, part, values

    def ConMaps(self):
        return self.conmaps_d.values()

    def ParseValue(self, v):
        v = eval('"%s"' % v)    # unescape backslashes
        dom = xml.dom.minidom.parseString(v)
        return self.ParseNode(dom.documentElement)

    def ParseNode(self, n):
        t = n.localName
        if t != "list":
            v = self.NodeText(n)

        if t == "string":
            return v
        elif t == "byte":
            return dbus.Byte(int(v))
        elif t == "bool":
            return v == "true"
        elif t == "int32" or t == "uint32":
            return int(v)
        elif t == "list":
            v = []
            c = n.firstChild
            while c != None:
                if c.localName != None: # whitespace
                    v.append(self.ParseNode(c))
                c = c.nextSibling
            return v

    def NodeText(self, n):
        if n.hasChildNodes():
            return n.firstChild.wholeText
        else:
            return ""


