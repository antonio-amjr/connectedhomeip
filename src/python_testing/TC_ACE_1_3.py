#
#    Copyright (c) 2022 Project CHIP Authors
#    All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

# See https://github.com/project-chip/connectedhomeip/blob/master/docs/testing/python.md#defining-the-ci-test-arguments
# for details about the block below.
#
# === BEGIN CI TEST ARGUMENTS ===
# test-runner-runs: run1
# test-runner-run/run1/app: ${ALL_CLUSTERS_APP}
# test-runner-run/run1/factoryreset: True
# test-runner-run/run1/quiet: True
# test-runner-run/run1/app-args: --discriminator 1234 --KVS kvs1 --trace-to json:${TRACE_APP}.json
# test-runner-run/run1/script-args: --storage-path admin_storage.json --commissioning-method on-network --discriminator 1234 --passcode 20202021 --trace-to json:${TRACE_TEST_JSON}.json --trace-to perfetto:${TRACE_TEST_PERFETTO}.perfetto
# === END CI TEST ARGUMENTS ===

import logging

import chip.clusters as Clusters
from chip.interaction_model import Status
from matter_testing_support import MatterBaseTest, TestStep, async_test_body, default_matter_test_main
from mobly import asserts


def acl_subject(cat: int) -> int:
    return 0xFFFFFFFD00000000 | cat


class TC_ACE_1_3(MatterBaseTest):

    async def write_acl(self, acl):
        # This returns an attribute status
        result = await self.default_controller.WriteAttribute(self.dut_node_id, [(0, Clusters.AccessControl.Attributes.Acl(acl))])
        asserts.assert_equal(result[0].Status, Status.Success, "ACL write failed")
        print(result)

    async def read_descriptor_expect_success(self, th, endpoint: int):
        cluster = Clusters.Objects.Descriptor
        attribute = Clusters.Descriptor.Attributes.DeviceTypeList
        await self.read_single_attribute_check_success(dev_ctrl=th, endpoint=endpoint, cluster=cluster, attribute=attribute)

    async def read_descriptor_expect_unsupported_access(self, th, endpoint: int):
        cluster = Clusters.Objects.Descriptor
        attribute = Clusters.Descriptor.Attributes.DeviceTypeList
        await self.read_single_attribute_expect_error(
            dev_ctrl=th, endpoint=endpoint, cluster=cluster, attribute=attribute, error=Status.UnsupportedAccess)

    def desc_TC_ACE_1_3(self) -> str:
        return "[TC-ACE-1.3] Subjects"

    def steps_TC_ACE_1_3(self) -> list[TestStep]:
        steps = [
            TestStep(1, "Commissioning, already done", is_commissioning=True),
            TestStep(2, "TH0 writes ACL all view on PIXIT.ACE.TESTENDPOINT"),
            TestStep(3, "TH1 reads EP0 descriptor - expect SUCCESS"),
            TestStep(4, "TH2 reads EP0 descriptor - expect SUCCESS"),
            TestStep(5, "TH3 reads EP0 descriptor - expect SUCCESS"),
            TestStep(6, "TH0 writes ACL TH1 view on EP0"),
            TestStep(7, "TH1 reads EP0 descriptor - expect SUCCESS"),
            TestStep(8, "TH2 reads EP0 descriptor - expect UNSUPPORTED_ACCESS"),
            TestStep(9, "TH3 reads EP0 descriptor - expect UNSUPPORTED_ACCESS"),
            TestStep(10, "TH0 writes ACL TH2 view on EP0"),
            TestStep(11, "TH1 reads EP0 descriptor - expect UNSUPPORTED_ACCESS"),
            TestStep(12, "TH2 reads EP0 descriptor - expect SUCCESS"),
            TestStep(13, "TH3 reads EP0 descriptor - expect UNSUPPORTED_ACCESS"),
            TestStep(14, "TH0 writes ACL TH3 view on EP0"),
            TestStep(15, "TH1 reads EP0 descriptor - expect UNSUPPORTED_ACCESS"),
            TestStep(16, "TH2 reads EP0 descriptor - expect UNSUPPORTED_ACCESS"),
            TestStep(17, "TH3 reads EP0 descriptor - expect SUCCESS"),
            TestStep(18, "TH0 writes ACL TH1 TH2 view on EP0"),
            TestStep(19, "TH1 reads EP0 descriptor - expect SUCCESS"),
            TestStep(20, "TH2 reads EP0 descriptor - expect SUCCESS"),
            TestStep(21, "TH3 reads EP0 descriptor - expect UNSUPPORTED_ACCESS"),
            TestStep(22, "TH0 writes ACL TH1 TH3 view on EP0"),
            TestStep(23, "TH1 reads EP0 descriptor - expect SUCCESS"),
            TestStep(24, "TH2 reads EP0 descriptor - expect UNSUPPORTED_ACCESS"),
            TestStep(25, "TH3 reads EP0 descriptor - expect SUCCESS"),
            TestStep(26, "TH0 writes ACL TH2 TH3 view on EP0"),
            TestStep(27, "TH1 reads EP0 descriptor - expect UNSUPPORTED_ACCESS"),
            TestStep(28, "TH2 reads EP0 descriptor - expect SUCCESS"),
            TestStep(29, "TH3 reads EP0 descriptor - expect SUCCESS"),
            TestStep(30, "TH0 writes ACL TH1 TH2 TH3 view on EP0"),
            TestStep(31, "TH1 reads EP0 descriptor - expect SUCCESS"),
            TestStep(32, "TH2 reads EP0 descriptor - expect SUCCESS"),
            TestStep(33, "TH3 reads EP0 descriptor - expect SUCCESS"),
            TestStep(34, "TH0 writes ACL cat1v1 view on EP0"),
            TestStep(35, "TH1 reads EP0 descriptor - expect SUCCESS"),
            TestStep(36, "TH2 reads EP0 descriptor - expect SUCCESS"),
            TestStep(37, "TH3 reads EP0 descriptor - expect SUCCESS"),
            TestStep(38, "TH0 writes ACL cat1v2 view on EP0"),
            TestStep(39, "TH1 reads EP0 descriptor - expect SUCCESS"),
            TestStep(40, "TH2 reads EP0 descriptor - expect SUCCESS"),
            TestStep(41, "TH3 reads EP0 descriptor - expect UNSUPPORTED_ACCESS"),
            TestStep(42, "TH0 writes ACL cat1v3 view on EP0"),
            TestStep(43, "TH1 reads EP0 descriptor - expect SUCCESS"),
            TestStep(44, "TH2 reads EP0 descriptor - expect UNSUPPORTED_ACCESS"),
            TestStep(45, "TH3 reads EP0 descriptor - expect UNSUPPORTED_ACCESS"),
            TestStep(46, "TH0 writes ACL cat2v1 view on EP0"),
            TestStep(47, "TH1 reads EP0 descriptor - expect UNSUPPORTED_ACCESS"),
            TestStep(48, "TH2 reads EP0 descriptor - expect SUCCESS"),
            TestStep(49, "TH3 reads EP0 descriptor - expect SUCCESS"),
            TestStep(50, "TH0 writes ACL cat2v2 view on EP0"),
            TestStep(51, "TH1 reads EP0 descriptor - expect UNSUPPORTED_ACCESS"),
            TestStep(52, "TH2 reads EP0 descriptor - expect UNSUPPORTED_ACCESS"),
            TestStep(53, "TH3 reads EP0 descriptor - expect SUCCESS"),
            TestStep(54, "TH0 writes ACL cat2v3 view on EP0"),
            TestStep(55, "TH1 reads EP0 descriptor - expect UNSUPPORTED_ACCESS"),
            TestStep(56, "TH2 reads EP0 descriptor - expect UNSUPPORTED_ACCESS"),
            TestStep(57, "TH3 reads EP0 descriptor - expect UNSUPPORTED_ACCESS"),
            TestStep(58, "TH0 writes ACL back to default")
        ]
        return steps

    @async_test_body
    async def test_TC_ACE_1_3(self):
        cat1_id = 0x11110000
        cat2_id = 0x22220000

        cat1v1 = cat1_id | 0x0001
        cat1v2 = cat1_id | 0x0002
        cat1v3 = cat1_id | 0x0003
        cat2v1 = cat2_id | 0x0001
        cat2v2 = cat2_id | 0x0002
        cat2v3 = cat2_id | 0x0003
        logging.info('cat1v1 0x%x', cat1v1)

        endpoint = 0

        self.step(1)

        fabric_admin = self.certificate_authority_manager.activeCaList[0].adminList[0]

        TH0_nodeid = self.matter_test_config.controller_node_id
        TH1_nodeid = self.matter_test_config.controller_node_id + 1
        TH2_nodeid = self.matter_test_config.controller_node_id + 2
        TH3_nodeid = self.matter_test_config.controller_node_id + 3

        TH1 = fabric_admin.NewController(nodeId=TH1_nodeid,
                                         paaTrustStorePath=str(self.matter_test_config.paa_trust_store_path),
                                         catTags=[cat1v3])
        TH2 = fabric_admin.NewController(nodeId=TH2_nodeid,
                                         paaTrustStorePath=str(self.matter_test_config.paa_trust_store_path),
                                         catTags=[cat1v2, cat2v1])
        TH3 = fabric_admin.NewController(nodeId=TH3_nodeid,
                                         paaTrustStorePath=str(self.matter_test_config.paa_trust_store_path),
                                         catTags=[cat1v1, cat2v2])

        self.step(2, endpoint)
        TH0_admin_acl = Clusters.AccessControl.Structs.AccessControlEntryStruct(
            privilege=Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum.kAdminister,
            authMode=Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum.kCase,
            subjects=[TH0_nodeid],
            targets=[Clusters.AccessControl.Structs.AccessControlTargetStruct(endpoint=endpoint, cluster=0x001f)])
        all_view = Clusters.AccessControl.Structs.AccessControlEntryStruct(
            privilege=Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum.kView,
            authMode=Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum.kCase,
            subjects=[],
            targets=[Clusters.AccessControl.Structs.AccessControlTargetStruct(endpoint=endpoint)])
        acl = [TH0_admin_acl, all_view]
        await self.write_acl(acl)

        self.step(3, endpoint)
        await self.read_descriptor_expect_success(TH1, endpoint)

        self.step(4, endpoint)
        await self.read_descriptor_expect_success(TH2, endpoint)

        self.step(5, endpoint)
        await self.read_descriptor_expect_success(TH3, endpoint)

        self.step(6, endpoint)
        th1_view = Clusters.AccessControl.Structs.AccessControlEntryStruct(
            privilege=Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum.kView,
            authMode=Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum.kCase,
            subjects=[TH1_nodeid],
            targets=[Clusters.AccessControl.Structs.AccessControlTargetStruct(endpoint=endpoint)])
        acl = [TH0_admin_acl, th1_view]
        await self.write_acl(acl)
        self.step(7, endpoint)
        await self.read_descriptor_expect_success(TH1, endpoint)

        self.step(8, endpoint)
        await self.read_descriptor_expect_unsupported_access(TH2, endpoint)

        self.step(9, endpoint)
        await self.read_descriptor_expect_unsupported_access(TH3, endpoint)

        self.step(10, endpoint)
        th2_view = Clusters.AccessControl.Structs.AccessControlEntryStruct(
            privilege=Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum.kView,
            authMode=Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum.kCase,
            subjects=[TH2_nodeid],
            targets=[Clusters.AccessControl.Structs.AccessControlTargetStruct(endpoint=endpoint)])

        acl = [TH0_admin_acl, th2_view]
        await self.write_acl(acl)
        self.step(11, endpoint)
        await self.read_descriptor_expect_unsupported_access(TH1, endpoint)

        self.step(12, endpoint)
        await self.read_descriptor_expect_success(TH2, endpoint)

        self.step(13, endpoint)
        await self.read_descriptor_expect_unsupported_access(TH3, endpoint)

        self.step(14, endpoint)
        th3_view = Clusters.AccessControl.Structs.AccessControlEntryStruct(
            privilege=Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum.kView,
            authMode=Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum.kCase,
            subjects=[TH3_nodeid],
            targets=[Clusters.AccessControl.Structs.AccessControlTargetStruct(endpoint=endpoint)])

        acl = [TH0_admin_acl, th3_view]
        await self.write_acl(acl)
        self.step(15, endpoint)
        await self.read_descriptor_expect_unsupported_access(TH1, endpoint)

        self.step(16, endpoint)
        await self.read_descriptor_expect_unsupported_access(TH2, endpoint)

        self.step(17, endpoint)
        await self.read_descriptor_expect_success(TH3, endpoint)

        self.step(18, endpoint)
        th12_view = Clusters.AccessControl.Structs.AccessControlEntryStruct(
            privilege=Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum.kView,
            authMode=Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum.kCase,
            subjects=[TH1_nodeid, TH2_nodeid],
            targets=[Clusters.AccessControl.Structs.AccessControlTargetStruct(endpoint=endpoint)])

        acl = [TH0_admin_acl, th12_view]
        await self.write_acl(acl)
        self.step(19, endpoint)
        await self.read_descriptor_expect_success(TH1, endpoint)

        self.step(20, endpoint)
        await self.read_descriptor_expect_success(TH2, endpoint)

        self.step(21, endpoint)
        await self.read_descriptor_expect_unsupported_access(TH3, endpoint)

        self.step(22, endpoint)
        th13_view = Clusters.AccessControl.Structs.AccessControlEntryStruct(
            privilege=Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum.kView,
            authMode=Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum.kCase,
            subjects=[TH1_nodeid, TH3_nodeid],
            targets=[Clusters.AccessControl.Structs.AccessControlTargetStruct(endpoint=endpoint)])

        acl = [TH0_admin_acl, th13_view]
        await self.write_acl(acl)
        self.step(23, endpoint)
        await self.read_descriptor_expect_success(TH1, endpoint)

        self.step(24, endpoint)
        await self.read_descriptor_expect_unsupported_access(TH2, endpoint)

        self.step(25, endpoint)
        await self.read_descriptor_expect_success(TH3, endpoint)

        self.step(26, endpoint)
        th23_view = Clusters.AccessControl.Structs.AccessControlEntryStruct(
            privilege=Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum.kView,
            authMode=Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum.kCase,
            subjects=[TH2_nodeid, TH3_nodeid],
            targets=[Clusters.AccessControl.Structs.AccessControlTargetStruct(endpoint=endpoint)])

        acl = [TH0_admin_acl, th23_view]
        await self.write_acl(acl)
        self.step(27, endpoint)
        await self.read_descriptor_expect_unsupported_access(TH1, endpoint)

        self.step(28, endpoint)
        await self.read_descriptor_expect_success(TH2, endpoint)

        self.step(29, endpoint)
        await self.read_descriptor_expect_success(TH3, endpoint)

        self.step(30, endpoint)
        th123_view = Clusters.AccessControl.Structs.AccessControlEntryStruct(
            privilege=Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum.kView,
            authMode=Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum.kCase,
            subjects=[TH1_nodeid, TH2_nodeid, TH3_nodeid],
            targets=[Clusters.AccessControl.Structs.AccessControlTargetStruct(endpoint=endpoint)])

        acl = [TH0_admin_acl, th123_view]
        await self.write_acl(acl)
        self.step(31, endpoint)
        await self.read_descriptor_expect_success(TH1, endpoint)

        self.step(32, endpoint)
        await self.read_descriptor_expect_success(TH2, endpoint)

        self.step(33, endpoint)
        await self.read_descriptor_expect_success(TH3, endpoint)

        self.step(34, endpoint)
        cat1v1_view = Clusters.AccessControl.Structs.AccessControlEntryStruct(
            privilege=Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum.kView,
            authMode=Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum.kCase,
            subjects=[acl_subject(cat1v1)],
            targets=[Clusters.AccessControl.Structs.AccessControlTargetStruct(endpoint=endpoint)])
        acl = [TH0_admin_acl, cat1v1_view]
        await self.write_acl(acl)

        self.step(35, endpoint)
        await self.read_descriptor_expect_success(TH1, endpoint)

        self.step(36, endpoint)
        await self.read_descriptor_expect_success(TH2, endpoint)

        self.step(37, endpoint)
        await self.read_descriptor_expect_success(TH3, endpoint)

        self.step(38, endpoint)
        cat1v2_view = Clusters.AccessControl.Structs.AccessControlEntryStruct(
            privilege=Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum.kView,
            authMode=Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum.kCase,
            subjects=[acl_subject(cat1v2)],
            targets=[Clusters.AccessControl.Structs.AccessControlTargetStruct(endpoint=endpoint)])

        acl = [TH0_admin_acl, cat1v2_view]
        await self.write_acl(acl)

        self.step(39, endpoint)
        await self.read_descriptor_expect_success(TH1, endpoint)

        self.step(40, endpoint)
        await self.read_descriptor_expect_success(TH2, endpoint)

        self.step(41, endpoint)
        await self.read_descriptor_expect_unsupported_access(TH3, endpoint)

        self.step(42, endpoint)
        cat1v3_view = Clusters.AccessControl.Structs.AccessControlEntryStruct(
            privilege=Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum.kView,
            authMode=Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum.kCase,
            subjects=[acl_subject(cat1v3)],
            targets=[Clusters.AccessControl.Structs.AccessControlTargetStruct(endpoint=endpoint)])

        acl = [TH0_admin_acl, cat1v3_view]
        await self.write_acl(acl)

        self.step(43, endpoint)
        await self.read_descriptor_expect_success(TH1, endpoint)

        self.step(44, endpoint)
        await self.read_descriptor_expect_unsupported_access(TH2, endpoint)

        self.step(45, endpoint)
        await self.read_descriptor_expect_unsupported_access(TH3, endpoint)

        self.step(46, endpoint)
        cat2v1_view = Clusters.AccessControl.Structs.AccessControlEntryStruct(
            privilege=Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum.kView,
            authMode=Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum.kCase,
            subjects=[acl_subject(cat2v1)],
            targets=[Clusters.AccessControl.Structs.AccessControlTargetStruct(endpoint=endpoint)])

        acl = [TH0_admin_acl, cat2v1_view]
        await self.write_acl(acl)

        self.step(47, endpoint)
        await self.read_descriptor_expect_unsupported_access(TH1, endpoint)

        self.step(48, endpoint)
        await self.read_descriptor_expect_success(TH2, endpoint)

        self.step(49, endpoint)
        await self.read_descriptor_expect_success(TH3, endpoint)

        self.step(50, endpoint)
        cat2v2_view = Clusters.AccessControl.Structs.AccessControlEntryStruct(
            privilege=Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum.kView,
            authMode=Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum.kCase,
            subjects=[acl_subject(cat2v2)],
            targets=[Clusters.AccessControl.Structs.AccessControlTargetStruct(endpoint=endpoint)])

        acl = [TH0_admin_acl, cat2v2_view]
        await self.write_acl(acl)

        self.step(51, endpoint)
        await self.read_descriptor_expect_unsupported_access(TH1, endpoint)

        self.step(52, endpoint)
        await self.read_descriptor_expect_unsupported_access(TH2, endpoint)

        self.step(53, endpoint)
        await self.read_descriptor_expect_success(TH3, endpoint)

        self.step(54, endpoint)
        cat2v3_view = Clusters.AccessControl.Structs.AccessControlEntryStruct(
            privilege=Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum.kView,
            authMode=Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum.kCase,
            subjects=[acl_subject(cat2v3)],
            targets=[Clusters.AccessControl.Structs.AccessControlTargetStruct(endpoint=endpoint)])

        acl = [TH0_admin_acl, cat2v3_view]
        await self.write_acl(acl)

        self.step(55, endpoint)
        await self.read_descriptor_expect_unsupported_access(TH1, endpoint)

        self.step(56, endpoint)
        await self.read_descriptor_expect_unsupported_access(TH2, endpoint)

        self.step(57, endpoint)
        await self.read_descriptor_expect_unsupported_access(TH3, endpoint)

        self.step(58)

        full_acl = Clusters.AccessControl.Structs.AccessControlEntryStruct(
            privilege=Clusters.AccessControl.Enums.AccessControlEntryPrivilegeEnum.kAdminister,
            authMode=Clusters.AccessControl.Enums.AccessControlEntryAuthModeEnum.kCase,
            subjects=[TH0_nodeid],
            targets=[])

        acl = [full_acl]
        await self.write_acl(acl)


if __name__ == "__main__":
    default_matter_test_main()
