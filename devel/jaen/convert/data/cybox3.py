"""
Cyber Observable Expression v3.0 (cybox) definitions used by OpenC2
"""

__version__ = "0.1"
__meta__ = {
    "namespace": "http://openc2.org/observables",
    "title": "Cyber Observable Expression v3 definitions",
    "description": "OpenC2 Cyber Observable datatypes based on objects defined in STIX v2 Part 4."
}

from devel.jaen.convert.pycodec import Choice, Enumerated, Map, Record, Boolean, Integer, String

# Core vocabularies

class HashAlgorithmType(Enumerated):    # Cybox 3.0 does not define a TypeName
    ns = 'cybox3'                       # Open vocabulary, Type string is 'hash-algo-ov'
    vals = [            # ElementID:
        'md5',              #  1
        'md6',              #  2
        'ripemd-160',       #  3
        'sha-1',            #  4
        'sha-224',          #  5
        'sha-256',          #  6
        'sha-384',          #  7
        'sha-512',          #  8
        'sha3-224',         #  9
        'sha3-256',         # 10
        'sha3-384',         # 11
        'sha3-512',         # 12
        'ssdeep',           # 13
        'whirlpool'         # 14
    ]

class EncryptionAlgorithmType(Enumerated):
    ns = 'cybox3'                       # Open vocabulary, Type string is 'encryption-algo-ov'
    vals = [                # ElementID:
        'aes128-ecb',           #  1
        'aes128-cbc',           #  2
        'aes128-cfb',           #  3
        'aes128-cofb',          #  4
        'aes128-ctr',           #  5
        'aes128-xts',           #  6
        'aes128-gcm',           #  7
        'salsa20',              #  8
        'salsa8',               #  9
        'chacha20-poly1305',    # 10
        'chacha20',             # 11
        'des-cbc',              # 12
        '3des-cbc',             # 13
        'des-ebc',              # 14
        '3des-ebc',             # 15
        'cast128-cbc',          # 16
        'cast256-cbc'           # 17
    ]

# Host Objects

class FileExtensions(Map):
    ns = 'cybox3'
    vals = []

class Hashes(Map):
    ns = 'cybox3'
    vals = []

class CyboxObjectRefs(Map):
    ns = 'cybox3'
    vals = []

class ArtifactObjectRef(Map):
    ns = 'cybox3'
    vals = []

class ObjectRef(Map):
    ns = 'cybox3'
    vals = []

class ObjectRefs(Map):
    ns = 'cybox3'
    vals = []

class WindowsRegistryValueTypes(Map):
    ns = 'cybox3'
    vals = []

class CyboxObjects(Map):
    ns = 'cybox3'
    vals = []

class CyboxActions(Map):
    ns = 'cybox3'
    vals = []


class FileObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', String, [], ''),      # Must be 'file-object'
        ('description', String, ['?'], ''),
        ('extended_properties', FileExtensions, ['?'], ''),
        ('hashes', Hashes, ['?'], ''),    # Dictionary of hashes
        ('size', Integer, ['?'], ''),
        ('file_name', String, ['?'], ''),
        ('file_name_enc', String, ['?'], ''),
        ('file_name_hex', String, ['?'], ''),    # hex
        ('magic_number', String, ['?'], ''),     # hex
        ('mime_type', String, ['?'], ''),
        ('created', String, ['?'], ''),          # timestamp
        ('modified', String, ['?'], ''),         # timestamp
        ('accessed', String, ['?'], ''),         # timestamp
        ('parent_directory_ref', String, ['?'], ''), # object-ref to directory-object
        ('is_encrypted', Boolean, ['?'], ''),
        ('encryption_algorithm', EncryptionAlgorithmType, ['?'], ''),     # is_encrypted MUST be True
        ('decryption_key', String, ['?'], ''),   # is_encrypted MUST be True
        ('contains_refs', CyboxObjectRefs, ['?'], ''),    # list of object-ref
        ('file_content_ref', ArtifactObjectRef, ['?'], '')    # artifact-object
    ]

class DirectoryObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', String, [], ''),      # Must be 'directory-object'
        ('description', String, ['?'], ''),
        ('extended_properties', FileExtensions, ['?'], ''),
        ('path', String, [], ''),
        ('path_enc', String, ['?'], ''),
        ('path_hex', String, ['?'], ''),         # hex
        ('created', String, ['?'], ''),  # timestamp
        ('modified', String, ['?'], ''),  # timestamp
        ('accessed', String, ['?'], ''),  # timestamp
        ('contains_refs', ObjectRefs, ['?'], ''),  # list of object-ref to file-object or directory-object
    ]

class WindowsRegistryKeyObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', String, [], ''),      # Must be 'windows-registry-key-object'
        ('description', String, ['?'], ''),
        ('extended_properties', FileExtensions, ['?'], ''),
        ('key', String, [], ''),
        ('values', WindowsRegistryValueTypes, ['?'], ''),
        ('modified', String, ['?'], ''),         # timestamp
        ('creator_ref', ObjectRef, ['?'], ''),    # object-ref to user-account-object
        ('number_of_subkeys', Integer, ['?'], '')
    ]

class MutexObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', String, [], ''),      # Must be 'mutex-object'
        ('description', String, ['?'], ''),
        ('extended_properties', FileExtensions, ['?'], ''),
        ('name', String, [], '')
    ]

#  x509-certificate-object
#  software-object
#  artifact-object
#  process-object
#  user-account-object

# Network Objects

class IPv4AddressObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', String, [], ''),                      # Must be 'ipv4-address-object'
        ('description', String, ['?'], ''),
        ('extended_properties', FileExtensions, ['?'], ''),
        ('value', String, [], ''),                     # CIDR format
        ('resolves_to_refs', ObjectRefs, ['?'], ''),      # list of object-ref to mac-address-object
        ('belongs_to_refs', ObjectRefs, ['?'], '')        # list of object ref to as-object
    ]

class IPv6AddressObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', String, [], ''),                      # Must be 'ipv6-address-object'
        ('description', String, ['?'], ''),
        ('extended_properties', FileExtensions, ['?'], ''),
        ('value', String, [], ''),                     # CIDR format
        ('resolves_to_refs', ObjectRefs, ['?'], ''),      # list of object-ref to mac-address-object
        ('belongs_to_refs', ObjectRefs, ['?'], '')        # list of object ref to as-object
    ]

class MACAddressObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', String, [], ''),              # Must be 'mac-address-object'
        ('description', String, ['?'], ''),
        ('extended_properties', FileExtensions, ['?'], ''),
        ('value', String, [], ''),             # colon-delimited MAC-48 address
    ]

class EmailAddressObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', String, [], ''),              # Must be 'email-address-object'
        ('description', String, ['?'], ''),
        ('extended_properties', FileExtensions, ['?'], ''),
        ('value', String, [], ''),             # RFC 5322 addr-spec
        ('display_name', String, ['?'], '')      # RFC 5322 display-name
    ]

class URLObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', String, [], ''),              # Must be 'url-object'
        ('description', String, ['?'], ''),
        ('extended_properties', FileExtensions, ['?'], ''),
        ('value', String, [], '')
    ]

class DomainNameObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', String, [], ''),              # Must be 'domain-name-object'
        ('description', String, ['?'], ''),
        ('extended_properties', FileExtensions, ['?'], ''),
        ('value', String, [], ''),
        ('resolves_to_refs', ObjectRefs, ['?'], ''),  # list of object-ref to ipv4-address-object, ipv6-address-object, domain-name-object
    ]                                           #  Typo - called resolves-to as of 8/30

class ASObject(Map):
    ns = 'cybox3'
    vals = [
        ('type', String, [], ''),      # Must be 'as-object'
        ('description', String, ['?'], ''),
        ('extended_properties', FileExtensions, ['?'], ''),
        ('number', Integer, [], ''),
        ('name', String, ['?'], ''),
        ('regional_internet_Registry', String, ['?'], '')
    ]

#  Network Connection Object
#  Email Message Object

# Common Types

class CyboxObject(Choice):
    ns = 'cybox3'
    vals = []

class CyboxBaseObject(Record):              # Base type for all CybOX 3 objects
    ns = 'cybox3'                           # TODO: combine vals instead of replacing in derived class
    vals = [
        ('type', CyboxObjects, [], ''),
        ('description', String, ['?'], ''),
        ('extended_properties', Map, ['?'], '')
    ]

class CyboxContainer(Record):           # Collection of related CybOX 3 objects and actions
    ns = 'cybox3'
    vals = [
        ('type', String, [], ''),          # 'cybox-container'
        ('spec_version', String, [], ''),  #  e.g., '3.0'
        ('objects', CyboxObjects, ['?'], ''), # Cybox 3.0 says 'dictionary' with list index properties, allow real list
        ('actions', CyboxActions, ['?'], '')  # RESERVED
    ]
