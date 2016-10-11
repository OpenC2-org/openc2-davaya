"""
Cyber Observable Expression 2.1 definitions

Selected CybOX 2.1 objects used by OpenC2.  Abstract syntax information extracted from XSD source documents.
"""

__version__ = "0.1"
__meta__ = {
    "namespace": "http://cybox.mitre.org/common-2",
}

from codec import Attribute, Choice, Enumerated, Map, Record, Boolean, Integer, String

class Layer3ProtocolType(Enumerated):      # Network_Connection_Object.xsd
    ns = "cybox"
    vals = ["IPv4", "IPv6", "ICMP", "IGMP", "IGRP", "CLNP",
            "EGP", "EIGRP", "IPSec", "IPX", "Routed-SMLT", "SCCP"]

class Layer4ProtocolType(Enumerated):       # Cybox_common.xsd
    ns = "cybox"
    vals = ["TCP", "UDP", "AH", "ESP", "GRE", "IL", "SCTP", "Sinec_H1", "SPX", "DCCP"]

class AddressObject(Record):
    ns = "AddressObj"
    vals = [
        ("Address_Value", String, ["?"], ""),
        ("VLAN_Name", String, ["?"], ""),
        ("VLAN_Num", Integer, ["?"], "")]

class DeviceObject(Map):
    ns = "DeviceObj"
    vals = [
        ("Description", String, ["?"], ""),
        ("Device_Type", String, ["?"], ""),
        ("Manufacturer", String, ["?"], ""),
        ("Model", String, ["?"], ""),
        ("Serial_Number", String, ["?"], ""),
        ("Firmware_Version", String, ["?"], ""),
        ("System_Details", String, ["?"], "")]

class DiskObject(Record):
    ns = "DiskObj"
    vals = []                          # TODO: fill in

class DiskPartitionObject(Record):
    ns = "DiskPartitionObj"
    vals = []                          # TODO: fill in

class DomainNameTypeEnum(Enumerated):
    ns = "DomainNameObj"
    vals = ["FQDN", "TLD"]

class DomainNameObject(Record):
    ns = "DomainNameObj"
    vals = [
        ("type", DomainNameTypeEnum, [], ""),
        ("Value", String, [], "")]

class EmailMessageObject(Record):
    ns = "EmailMessageObj"
    vals = []                          # TODO: fill in

class FileObject(Record):
    ns = "FileObj"
    vals = []                          # TODO: fill in

class HostnameObject(Record):      # Hostname_Object.xsd - unspecified string object - FQDN?
    ns = "HostnameObj"
    vals = [
        ("Hostname_Value", String, [], ""),    # Optional in cybox, required in OpenC2
        ("Naming_System", String, ["?"], "")]

class MemoryObject(Record):
    ns = "MemoryObj"
    vals = []                          # TODO: fill in

class NetworkFlowObject(Record):
    ns = "NetworkFlowObj"
    vals = []                          # TODO: fill in

class NetworkPacketObject(Record):
    ns = "NetworkPacketObj"
    vals = []                          # TODO: fill in

class NetworkSubnetObject(Record):
    ns = "NetworkSubnetObj"
    vals = []                          # TODO: fill in

class PortObject(Record):
    ns = "PortObj"
    vals = [
        ("Port_Value", Integer, ["?","[1:]"], ""),
        ("Layer4_Protocol", Layer4ProtocolType, ["?"], "")]

class ProcessObject(Record):
    ns = "ProcessObj"
    vals = []                          # TODO: fill in

class ProductObject(Record):
    ns = "ProductObj"
    vals = []                          # TODO: fill in

class SocketAddressChoice(Choice):
    ns = "SocketAddressObj"
    vals = [
        ("IP_Address", AddressObject, [], ""),
        ("Hostname", HostnameObject, [], "")]

class SocketAddressObject(Record):
    ns = "SocketAddressObj"
    vals = [
        ("*", SocketAddressChoice, [], ""),
        ("Port", PortObject, ["?"], "")]

class NetworkConnectionObject(Record):      # Network_Connection_Object.xsd
    ns = "NetworkConnectionObj"
    vals = [                                 # TODO: fill in all fields of xsd.
        ("Layer3Protocol", Layer3ProtocolType, ["?"], ""),
        ("Layer4Protocol", Layer4ProtocolType, ["?"], ""),
        ("SourceSocketAddress", SocketAddressObject, ["?"], ""),
        ("DestinationSocketAddress", SocketAddressObject, ["?"], "")]

class SystemObject(Record):
    ns = "SystemObj"
    vals = []                          # TODO: fill in

class URITypeEnum(Enumerated):
    ns = "cybox"
    vals = ["URL", "General URN", "Domain Name"]

class URIObject(Record):
    ns = "URIObj"
    vals = [
        ("type", URITypeEnum, [], ""),
        ("Value", String, [], "")]        # cyboxCommon:AnyURIObjectPropertyType

class UserAccountObject(Record):
    ns = "UserAccountObj"
    vals = []                          # TODO: fill in

class UserSessionObject(Record):
    ns = "UserSessionObj"
    vals = [
        ("Effective_Group", String, ["?"], ""),
        ("Effective_Group_ID", String, ["?"], ""),
        ("Effective_User", String, ["?"], ""),
        ("Effective_User_ID", String, ["?"], ""),
        ("Login_Time", String, ["?"], ""),       # cyboxCommon:DateTimeObjectPropertyType
        ("Logout_Time", String, ["?"], "")]      # cyboxCommon:DateTimeObjectPropertyType

class VolumeObject(Record):
    ns = "VolumeObj"
    vals = []                          # TODO: fill in

class WindowsRegistryKeyObject(Record):
    ns = "WindowsRegistryKeyObj"
    vals = []                          # TODO: fill in

class WindowsServiceObject(Record):
    ns = "WindowsServiceObj"
    vals = []                          # TODO: fill in

class X509CertificateObject(Enumerated):
    ns = "cybox"
    vals = ["Certificate", "RawCertificate", "CertificateSignature"]

class CyboxObject(Attribute):
    ns = "cybox"
    vals = [
        ("Address", AddressObject, [], ""),                         #  1
        ("Device", DeviceObject, [], ""),                           #  2
        ("Disk", DiskObject, [], ""),                               #  3
        ("Disk_Partition", DiskPartitionObject, [], ""),            #  4
        ("Domain_Name", DomainNameObject, [], ""),                  #  5
        ("Email_Message", EmailMessageObject, [], ""),              #  6
        ("File", FileObject, [], ""),                               #  7
        ("Hostname", HostnameObject, [], ""),                       #  8
        ("Memory", MemoryObject, [], ""),                           #  9
        ("Network_Connection", NetworkConnectionObject, [], ""),    # 10
        ("Network_Flow", NetworkFlowObject, [], ""),                # 11
        ("Network_Packet", NetworkPacketObject, [], ""),            # 12
        ("Network_Subnet", NetworkSubnetObject, [], ""),            # 13
        ("Port", PortObject, [], ""),                               # 14
        ("Process", ProcessObject, [], ""),                         # 15
        ("Product", ProductObject, [], ""),                         # 16
        ("Socket_Address", SocketAddressObject, [], ""),            # 17
        ("System", SystemObject, [], ""),                           # 18
        ("URI", URIObject, [], ""),                                 # 19
        ("User_Account", UserAccountObject, [], ""),                # 20
        ("User_Session", UserSessionObject, [], ""),                # 21
        ("Volume", VolumeObject, [], ""),                           # 22
        ("Windows_Registry_Key", WindowsRegistryKeyObject, [], ""), # 23
        ("Windows_Service", WindowsServiceObject, [], ""),          # 24
        ("X509_Certificate", X509CertificateObject, [], "")]        # 25