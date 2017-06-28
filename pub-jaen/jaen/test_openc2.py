import json
import os
import unittest

from jaen.codec.codec import Codec
from jaen.codec.jaen import jaen_load
from jaen.codec.codec_utils import flatten, fluff, dlist


class OpenC2(unittest.TestCase):

    def _write_examples(self, name, cmds):
        """
        Create example JSON files as a side effect of running unit tests
        """

        if True:        # Set to False to not write example files
            for n, encoding in enumerate(["", "_flat", "_concise", "_min"]):
                if cmds[n] is not None:
                    with open(os.path.join("examples", name + encoding + ".json"), "w") as f:
                        f.write(json.dumps(cmds[n]))

    def setUp(self):
        jaen = jaen_load(os.path.join("schema", "openc2.jaen"))
        self.tc = Codec(jaen)

    def test01_mitigate_domain(self):
        cmd_api = {
            "action": "mitigate",
            "target": {
                "domain_name": {"value": "cdn.badco.org"}}}
        cmd_flat = {
            "action": "mitigate",
            "target.domain_name.value": "cdn.badco.org"
        }
        cmd_noname = {"1": 32, "2": {"7": {"1": "cdn.badco.org"}}}
        cmd_concise = ["mitigate",{"domain_name": ["cdn.badco.org"]}]
        cmd_min = [32, {"7": ["cdn.badco.org"]}]

                                            # Minified (list/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_min)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_min), cmd_api)
        self.tc.set_mode(False, True)       # Concise (list/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_concise)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_concise), cmd_api)
        self.tc.set_mode(True, False)       # unused (dict/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_noname)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_noname), cmd_api)
        self.tc.set_mode(True, True)        # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(flatten(cmd_api), cmd_flat)
        self.assertEqual(fluff(cmd_flat), cmd_api)
        self._write_examples("t01_mitigate_domain", [cmd_api, cmd_flat, cmd_concise, cmd_min])

    def test02_query_openc2(self):
        cmd_api = {"action": "query", "target": {"openc2": {"schema":""}}}
        cmd_flat = {"action": "query", "target.openc2.schema": ""}
        cmd_noname = {"1":3, "2":{"2":{"2":""}}}
        cmd_concise = ["query", {"openc2": {"schema":""}}]
        cmd_min = [3,{"2":{"2":""}}]

                                            # Minified (list/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_min)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_min), cmd_api)
        self.tc.set_mode(False, True)       # Concise (list/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_concise)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_concise), cmd_api)
        self.tc.set_mode(True, False)       # unused (dict/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_noname)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_noname), cmd_api)
        self.tc.set_mode(True, True)        # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(flatten(cmd_api), cmd_flat)
        self.assertEqual(fluff(cmd_flat), cmd_api)
        self._write_examples("t02_query_openC2", [cmd_api, cmd_flat, cmd_concise, cmd_min])

    def test03_contain_user(self):
        cmd_api = {
            "action": "contain",
            "target": {
                "user_account":{
                    "user_id": "21942",
                    "account_login": "jsmith",
                    "is_disabled": True,
                    "account_last_login": "2017-03-16T07:38:12-04:00"}}}

        cmd_flat = {
            "action": "contain",
            "target.user_account.user_id": "21942",
            "target.user_account.account_login": "jsmith",
            "target.user_account.is_disabled": True,
            "target.user_account.account_last_login": "2017-03-16T07:38:12-04:00"
        }

        cmd_noname = {
            "1":7,
            "2":{
                "19":{
                    "1": "21942",
                    "2": "jsmith",
                    "8": True,
                    "13": "2017-03-16T07:38:12-04:00"}}}

        cmd_concise = [
            "contain",{
                "user_account":{
                    "user_id": "21942",
                    "account_login": "jsmith",
                    "is_disabled": True,
                    "account_last_login": "2017-03-16T07:38:12-04:00"}}]

        cmd_min = [7,{"19":{"1":"21942","2":"jsmith","8": True,"13":"2017-03-16T07:38:12-04:00"}}]

                                            # Minified (list/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_min)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_min), cmd_api)
        self.tc.set_mode(False, True)       # Concise (list/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_concise)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_concise), cmd_api)
        self.tc.set_mode(True, False)       # unused (dict/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_noname)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_noname), cmd_api)
        self.tc.set_mode(True, True)        # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(flatten(cmd_api), cmd_flat)
        self.assertEqual(fluff(cmd_flat), cmd_api)
        self._write_examples("t03_contain_user", [cmd_api, cmd_flat, cmd_concise, cmd_min])

    def test04_deny_ip(self):
        cmd_api = {
            "action": "deny",
            "target": {
                "ip_connection": {
                    "src_addr": {"name": {"value": "www.badco.com"}},
                    "src_port": {"protocol": "https"},
                    "dst_addr": {"ipv4": {"value": "192.168.1.1"}},
                    "layer4_protocol": "TCP"
                }},
            "actuator": {
                "network_firewall": {"asset_id": "30"}},
            "modifiers": {
                "command_id": "pf17_8675309",
                "context": "91",
                "start_time": "2016-11-25T08:10:31-04:00",
                "duration": "PT2M30S"}}

        cmd_flat = {
            "action": "deny",
            "target.ip_connection.src_addr.name.value": "www.badco.com",
            "target.ip_connection.src_port.protocol": "https",
            "target.ip_connection.dst_addr.ipv4.value": "192.168.1.1",
            "target.ip_connection.layer4_protocol": "TCP",
            "actuator.network_firewall.asset_id": "30",
            "modifiers.command_id": "pf17_8675309",
            "modifiers.context": "91",
            "modifiers.start_time": "2016-11-25T08:10:31-04:00",
            "modifiers.duration": "PT2M30S"
        }

        cmd_noname = {
            "1": 6,
            "2": {"15": {
                "1": {"3": {"1": "www.badco.com"}},
                "2": {"2": 443},
                "3": {"1": {"1": "192.168.1.1"}},
                "5": 6}},
            "3": {"14": {"2": "30"}},
            "4": {
                "1": "91",
                "2": "2016-11-25T08:10:31-04:00",
                "4": "PT2M30S",
                "6": "pf17_8675309"}}

        cmd_concise = [
            "deny",
            {"ip_connection": [
                {"name": ["www.badco.com"]},
                {"protocol": "https"},
                {"ipv4": ["192.168.1.1"]},
                None,
                "TCP"]},
            {"network_firewall": [None, "30"]},
            {"context": "91",
            "start_time": "2016-11-25T08:10:31-04:00",
            "duration": "PT2M30S",
            "command_id": "pf17_8675309"}]

        cmd_min = [6,
            {"15": [
                {"3": ["www.badco.com"]},
                {"2": 443},
                {"1": ["192.168.1.1"]},
                None,
                6]},
            {"14": [None, "30"]},
            {"1": "91",
             "2": "2016-11-25T08:10:31-04:00",
             "4": "PT2M30S",
             "6": "pf17_8675309"}]

                                            # Minified (list/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_min)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_min), cmd_api)
        self.tc.set_mode(False, True)       # Concise (list/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_concise)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_concise), cmd_api)
        self.tc.set_mode(True, False)       # unused (dict/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_noname)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_noname), cmd_api)
        self.tc.set_mode(True, True)        # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(flatten(cmd_api), cmd_flat)
        self.assertEqual(fluff(cmd_flat), cmd_api)
        self._write_examples("t04_deny_ip", [cmd_api, cmd_flat, cmd_concise, cmd_min])

    def test05_scan_domain(self):
        cmd_api = {           # API / Verbose (dict/name)
            "action": "scan",
            "target": {
                "domain_name": {
                    "value": "www.example.com",
                    "resolves_to": [
                        {"ipv4": {"value": "198.51.100.2"}},
                        {"name": {"value": "ms34.example.com"}}]}}}

        cmd_flat = {
            "action": "scan",
            "target.domain_name.value": "www.example.com",
            "target.domain_name.resolves_to.0.ipv4.value": "198.51.100.2",
            "target.domain_name.resolves_to.1.name.value": "ms34.example.com"
        }

        cmd_noname = {         # unused (dict/tag)
            "1": 1,
            "2": {
                "7": {
                    "1": "www.example.com",
                    "2": [
                        {"1":{"1": "198.51.100.2"}},
                        {"3":{"1": "ms34.example.com"}}]}}}

        cmd_concise = [        # Concise (list/name)
            "scan", {
                "domain_name": [
                    "www.example.com", [
                        {"ipv4": ["198.51.100.2"]},
                        {"name": ["ms34.example.com"]}]]}]

        cmd_min = [1,{"7":["www.example.com",[{"1":["198.51.100.2"]},{"3":["ms34.example.com"]}]]}]

                                            # Minified (list/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_min)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_min), cmd_api)
        self.tc.set_mode(False, True)       # Concise (list/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_concise)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_concise), cmd_api)
        self.tc.set_mode(True, False)       # unused (dict/tag)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_noname)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_noname), cmd_api)
        self.tc.set_mode(True, True)        # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(flatten(cmd_api), cmd_flat)
        self.assertEqual(dlist(fluff(cmd_flat)), cmd_api)       # Convert numeric dict to list
        self._write_examples("t05_scan_domain", [cmd_api, cmd_flat, cmd_concise, cmd_min])

    def test06_update_software(self):
        cmd_api = {         # API / Verbose (dict/name)
            "action": "update",
            "target": {
                "software": {
                    "name": "VirusBeGone",
                    "vendor": "McAfmantec"}},
            "actuator": {
                "process_remediation_service": {
                    "actuator_id": "dns://host03274.example.org"}},
            "modifiers": {
                "command_id": "474074afb389",
                "command_src": "dns://orch.example.org",
                "response": "ack",
                "source": "https://updates.example.org/win7_x64/patch_201704_0137.cab"}}

        cmd_flat = {
            "action": "update",
            "target.software.vendor": "McAfmantec",
            "target.software.name": "VirusBeGone",
            "actuator.process_remediation_service.actuator_id": "dns://host03274.example.org",
            "modifiers.command_id": "474074afb389",
            "modifiers.command_src": "dns://orch.example.org",
            "modifiers.response": "ack",
            "modifiers.source": "https://updates.example.org/win7_x64/patch_201704_0137.cab"}

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(flatten(cmd_api), cmd_flat)
        self.assertEqual(dlist(fluff(cmd_flat)), cmd_api)  # Convert numeric dict to list
        self._write_examples("t06_update_software", [cmd_api, cmd_flat, None, None])

        # -- Response

        rsp_api = {
            "status": "Processing",
            "statusText": "Updating McAfmantec VirusBeGone ...",
            "response_src": "dns://orch.example.org",
            "command_ref": "474074afb389"}

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Response", rsp_api), rsp_api)
        self.assertEqual(self.tc.decode("OpenC2Response", rsp_api), rsp_api)
        self._write_examples("t06_update_software_rsp", [rsp_api, None, None, None])

    def test07_update_file(self):
        cmd_api = {
            "action": "update",
            "target": {
                "file": {
                    "parent_directory": {
                        "path":"\\\\someshared-drive\\somedirectory\\configurations"},
                    "name": "firewallconfiguration.txt"
                }
            },
            "actuator": {
                "network_firewall": {"actuator_id": "dns://host03274.example.org"}}
        }
        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t07_update_file", [cmd_api, None, None, None])

    def test08_negotiation(self):
        cmd_api = {
            "action": "query",
            "target": {
                "openc2": {"comm_supported":""}
            },
            "actuator": {
                "any": {"actuator_id": "https://router7319.example.org"}}
        }
        rsp_api = {
            "status": "OK",
            "results": {
                "comms": {
                    "serialization": ["JSON", "JSON-min", "XML", "Protobuf"],
                    "connection": [{"DXL": {"channel": "c2-channel"}}]
                }
            }
        }
        cmd2_api = {
            "action": "set",
            "target": {
                "openc2": {
                    "comm_selected":{
                        "serialization": "Protobuf",
                        "connection": {
                            "REST": {
                                "port": {"protocol":"https"}}}}}},
            "actuator": {
                "any": {"actuator_id": "https://router7319.example.org"}}
        }
        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.encode("OpenC2Response", rsp_api), rsp_api)
        self.assertEqual(self.tc.decode("OpenC2Response", rsp_api), rsp_api)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd2_api), cmd2_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd2_api), cmd2_api)
        self._write_examples("t08_negotiation1", [cmd_api, None, None, None])
        self._write_examples("t08_negotiation2", [rsp_api, None, None, None])
        self._write_examples("t08_negotiation3", [cmd2_api, None, None, None])

    def test09_cancel_command(self):
        cmd_api = {
            "action": "cancel",
            "target": {
                "openc2": {"command": "b33cd1d4-aeb4-43a3-bfe9-806f4a84ef79"}}}

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t09_cancel_command", [cmd_api, None, None, None])

    def test10_delete_email(self):
        cmd_api = {
            "action": "delete",
            "target": {
                "email_message": {
                    "date": "2017-06-07T14:30:31-04:00",
                    "from": {"value": "ginsu@spamco.org"},
                    "subject": "Special Offer!"
                }}}

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t10_delete_email", [cmd_api, None, None, None])

    def test11_stop_process(self):
        cmd_api = {
            "action": "delete",
            "target": {
                "process": {
                    "pid": 17325,
                    "name": "rm -rf /*.*"
                }},
            "actuator": {
                "endpoint": {"actuator_id": "dns://i3494.hosts.example.com"}
            },
            "modifiers": {
                "method": {"stop": "graceful"}
            }
        }

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t11_stop_process", [cmd_api, None, None, None])

    def test12_locate_ipaddr(self):
        cmd_api = {
            "action": "locate",
            "target": {
                "ipv4_addr": {
                    "value": "209.59.128.0/18",
                    "belongs_to": [{"number": 32244}, {"number": 25820}]
                }}
        }

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t12_locate_ipaddr", [cmd_api, None, None, None])

    def test13_redirect_url(self):
        cmd_api = {
            "action": "redirect",
            "target": {
                "url": "https://www.shezuly.com/qqmusic.exe" }
        }

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t13_redirect_url", [cmd_api, None, None, None])

    def test14_stop_user_session(self):
        cmd_api = {
            "action": "stop",
            "target": {
                "user_session": {
                    "effective-user": "John Q. Public",
                    "effective-user-id": "17239",
                    "login-time": "2017-07-03T15:27:14-07:00"}}
        }

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t14_stop_user_session", [cmd_api, None, None, None])

    def test15_report_artifact(self):
        cmd_api = {
            "action": "report",
            "target": {
                "artifact": {

                }}
        }

        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        self.assertEqual(self.tc.encode("OpenC2Command", cmd_api), cmd_api)
        self.assertEqual(self.tc.decode("OpenC2Command", cmd_api), cmd_api)
        self._write_examples("t15_report_artifact", [cmd_api, None, None, None])

    def testb1_foo(self):       # Unknown action
        cmd_api = {
            "action": "foo",
            "target": {"device": {"model": "bar"}}}
        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        with self.assertRaises(ValueError):
            self.tc.encode("OpenC2Command", cmd_api)
        with self.assertRaises(ValueError):
            self.tc.decode("OpenC2Command", cmd_api)

    def testb2_scan(self):      # Unknown target device property
        cmd_api = {
            "action": "scan",
            "target": {
                "device": {"dummy": "bar"}
                }}
        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        with self.assertRaises(ValueError):
            self.tc.encode("OpenC2Command", cmd_api)
        with self.assertRaises(ValueError):
            self.tc.decode("OpenC2Command", cmd_api)


    def testb3_scan(self):      # Extra targets
        cmd_api = {
            "action": "scan",
            "target": {
                "device": {"model": "bar"},
                "author": "Charles Dickens",
                "title": "A Tale of Two Cities",
                "quote": "We had everything before us, we had nothing before us, we were all going direct to Heaven, "
                    "we were all going direct the other way— in short, the period was so far like the present period, "
                    "that some of its noisiest authorities insisted on its being received, for good or for evil, in the "
                    "superlative degree of comparison only."
                }}
        self.tc.set_mode(True, True)    # API / Verbose (dict/name)
        with self.assertRaises(ValueError):
            self.tc.encode("OpenC2Command", cmd_api)
        with self.assertRaises(ValueError):
            self.tc.decode("OpenC2Command", cmd_api)

if __name__ == "__main__":
    unittest.main()
